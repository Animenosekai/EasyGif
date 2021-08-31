"""
EasyGif

© Anime no Sekai, 2021
"""

# IMPORTS

### NATIVE TO PYTHON
import asyncio
import random
from datetime import datetime
from traceback import print_exc

import discord  # to communicate with discord
from discord.ext import commands  # to get discord commands
from discord.utils import escape_markdown

from config import (COMMAND_PREFIX, DEBUG_MODE, EASYGIF_VERSION, GIPHY_RANDOM_ENDPOINT,
                    GIPHY_SEARCH_ENDPOINT, RANDOM_DICTIONARY, ROGER_REACTION, SFW_GIPHY_RANDOM_ENDPOINT, SFW_GIPHY_SEARCH_ENDPOINT, SFW_TENOR_RANDOM_ENDPOINT, SFW_TENOR_SEARCH_ENDPOINT,
                    TENOR_RANDOM_ENDPOINT, TENOR_SEARCH_ENDPOINT)
from models.embed import Embed
from models.provider import Giphy, Tenor
from models.results import Results
from templates.botstats import BOTSTATS_TEMPLATE, POWERED_BY
from templates.help import HELP_TEMPLATE
from templates.stats import STATS_TEMPLATE
from utils import exceptions
from utils.exceptions import EasyGifException
from utils.log import LogLevels, log
from utils.mongo import mongo_users
from utils.request import Request
from utils.sanitize import url_encode
from utils.short import create_short_url

### DEFINING CLIENT/BOT AND ITS PREFIX 
client = commands.Bot(command_prefix=COMMAND_PREFIX, case_insensitive=True)

# WHEN THE BOT IS UP
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.gifhelp')) # GAME ACTIVITY
    log("EasyGif is ready", level=LogLevels.INFO)

async def error_handler(context, error):
    if DEBUG_MODE:
        print_exc()
    if isinstance(error, EasyGifException):
        await context.send(error.SAFE_MESSAGE.format(mention=context.author.mention))
    else:
        log("An unknown error occured: {name} {error}".format(name=error.__class__.__name__, error=str(error)), level=LogLevels.ERROR)
        await context.send(exceptions.EasyGifException.SAFE_MESSAGE.format(mention=context.author.mention))

# MAIN COMMAND: .gif <SEARCH>
@client.command(pass_context=True)
async def gif(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            content = escape_markdown(context.message.clean_content)[len(COMMAND_PREFIX) + 4:] # removing .gif and cleaning up the content
            _search = str(content)
            search = url_encode(_search)

            now = datetime.utcnow().timestamp()

            log("→ '.gif {query}' came from the server {server} (user: {user})".format(query=_search, server=context.guild, user=context.author))

            results = None
            channel_is_nsfw = context.channel.is_nsfw()
            for _ in range(3): # try 3 times
                if random.randint(0, 1) == 0: # GIPHY
                    provider = Giphy()
                    if not channel_is_nsfw:
                        req = Request(SFW_GIPHY_SEARCH_ENDPOINT.format(query=search))
                    else:
                        req = Request(GIPHY_SEARCH_ENDPOINT.format(query=search))
                else: # TENOR
                    provider = Tenor()
                    if not channel_is_nsfw:
                        req = Request(SFW_TENOR_SEARCH_ENDPOINT.format(query=search))
                    else:
                        req = Request(TENOR_SEARCH_ENDPOINT.format(query=search))
                results = Results(query=_search, results=req.json, provider=provider)

                if len(results.results) < 1:
                    results = None
                else:
                    break

            if results is None:
                raise exceptions.NoResult("We couldn't find any result")

            result = results.random
            embed = Embed(author=context.author, command=".gif {query}".format(query=_search), image=result, provider=provider)
            message = await context.send(embed=embed.dump())
            log("← '.gif {query}'; Response: {result}".format(query=_search, result=result))

            ### UPDATING THE DATABASE
            mongo_users.update_one({"_id": context.author.id}, {"$push": {"responses": {
                "searchTerm": _search,
                "server": context.guild.id,
                "timestamp": now,
                "response": result,
                "responseId": message.id,
                "provider": provider.provider
            }}}, upsert=True)
        
    except Exception as err:
        await error_handler(context=context, error=err)

# RANDOM GIF: .gifrandom
@client.command(pass_context=True)
async def gifrandom(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            now = datetime.utcnow().timestamp()

            log("→ '.gifrandom' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            results = None
            channel_is_nsfw = context.channel.is_nsfw()
            for _ in range(5): # try 5 times
                if random.randint(0, 1) == 0: # GIPHY
                    provider = Giphy()
                    if not channel_is_nsfw:
                        req = Request(SFW_GIPHY_RANDOM_ENDPOINT, cache=False)
                    else:
                        req = Request(GIPHY_RANDOM_ENDPOINT, cache=False)
                else: # TENOR
                    provider = Tenor()
                    if not channel_is_nsfw:
                        req = Request(SFW_TENOR_RANDOM_ENDPOINT.format(query=random.choice(RANDOM_DICTIONARY)))
                    else:
                        req = Request(TENOR_RANDOM_ENDPOINT.format(query=random.choice(RANDOM_DICTIONARY)))
                results = Results(query=None, results=req.json, provider=provider, random=True)

                if len(results.results) < 1:
                    results = None
                else:
                    break

            if results is None:
                raise exceptions.NoResult("We couldn't find any result")

            result = results.random
            embed = Embed(author=context.author, command=".gifrandom", image=result, provider=provider)
            message = await context.send(embed=embed.dump())
            log("← '.gifrandom'; Response: {result}".format(result=result))

            ### UPDATING THE DATABASE
            mongo_users.update_one({"_id": context.author.id}, {"$push": {"responses": {
                "searchTerm": None,
                "server": context.guild.id,
                "timestamp": now,
                "response": result,
                "responseId": message.id,
                "provider": provider.provider
            }}}, upsert=True)
            
    except Exception as err:
        await error_handler(context=context, error=err)


def get_last_message(context):
    user_data = mongo_users.find_one({"_id": context.author.id}, projection={"responses": {"$slice": -1}})
    if user_data is None:
        return None
    else:
        return user_data["responses"][0]

@client.command(pass_context=True, aliases=["gifdeletes"])
async def gifdelete(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            status = await context.send('{mention} Searching your last GIF...'.format(mention=context.author.mention))

            log("→ '.gifdelete' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            data = get_last_message(context)
            if data is None:
                await context.send("{mention} It seems like you have no GIF sent by you".format(mention=context.author.mention))
                return

            try:
                message = await context.fetch_message(data["responseId"])
            except Exception:
                raise exceptions.MessageNotFound("We couldn't find the message {id}".format(id=data["responseId"]))

            await message.delete()
            await status.edit(content='{mention} Last GIF deleted! ✨'.format(mention=context.author.mention))

            log("← '.gifdelete' for {user}".format(user=context.author))

            ### UPDATING THE DATABASE
            mongo_users.update_one({"_id": context.author.id}, {"$pull": {"responses": data}}, upsert=True)
            
    except Exception as err:
        await error_handler(context=context, error=err)


@client.command(pass_context=True, aliases=["gifchanges"])
async def gifchange(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            status = await context.send('{mention} Changing your last GIF...'.format(mention=context.author.mention))

            now = datetime.utcnow().timestamp()

            log("→ '.gifchange' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            data = get_last_message(context)
            if data is None:
                await context.send("{mention} It seems like you have no GIF sent by you".format(mention=context.author.mention))
                return

            try:
                message = await context.fetch_message(data["responseId"])
            except Exception:
                raise exceptions.MessageNotFound("We couldn't find the message {id}".format(id=data["responseId"]))


            update_data = {"timestamp": now}
            channel_is_nsfw = context.channel.is_nsfw()

            if data["searchTerm"] is None:
                results = None
                for _ in range(5): # try 5 times
                    if random.randint(0, 1) == 0: # GIPHY
                        provider = Giphy()
                        if not channel_is_nsfw:
                            req = Request(SFW_GIPHY_RANDOM_ENDPOINT, cache=False)
                        else:
                            req = Request(GIPHY_RANDOM_ENDPOINT, cache=False)
                    else: # TENOR
                        provider = Tenor()
                        if not channel_is_nsfw:
                            req = Request(SFW_TENOR_RANDOM_ENDPOINT.format(query=random.choice(RANDOM_DICTIONARY)))
                        else:
                            req = Request(TENOR_RANDOM_ENDPOINT.format(query=random.choice(RANDOM_DICTIONARY)))
                    update_data["provider"] = provider.provider
                    results = Results(query=None, results=req.json, provider=provider, random=True)

                    if len(results.results) < 1:
                        results = None
                    else:
                        break

                if results is None:
                    raise exceptions.NoResult("We couldn't find any result")

                result = results.random
                embed = Embed(author=context.author, command=".gifrandom", image=result, provider=provider)
                update_data["response"] = result
            else:
                search = url_encode(data["searchTerm"])

                results = None
                for _ in range(3): # try 3 times
                    if random.randint(0, 1) == 0: # GIPHY
                        provider = Giphy()
                        if not channel_is_nsfw:
                            req = Request(SFW_GIPHY_SEARCH_ENDPOINT.format(query=search))
                        else:
                            req = Request(GIPHY_SEARCH_ENDPOINT.format(query=search))
                    else: # TENOR
                        provider = Tenor()
                        if not channel_is_nsfw:
                            req = Request(SFW_TENOR_SEARCH_ENDPOINT.format(query=search))
                        else:
                            req = Request(TENOR_SEARCH_ENDPOINT.format(query=search))
                    update_data["provider"] = provider.provider
                    results = Results(query=data["searchTerm"], results=req.json, provider=provider)

                    if len(results.results) < 1:
                        results = None
                    else:
                        break

                if results is None:
                    raise exceptions.NoResult("We couldn't find any result")

                result = results.random
                embed = Embed(author=context.author, command=".gif {query}".format(query=data["searchTerm"]), image=result, provider=provider)
                update_data["response"] = result
            data = dict(data)
            new_data = data.copy()
            new_data.update(update_data)

            await message.edit(embed=embed.dump())
            await status.edit(content='{mention} Last gif changed! ✨'.format(mention=context.author.mention))
            await asyncio.sleep(3)
            await status.delete()

            log("← '.gifchange' for {user}".format(user=context.author))

            ### UPDATING THE DATABASE
            mongo_users.update_one({"_id": context.author.id}, {"$pull": {"responses": data}}, upsert=True)
            mongo_users.update_one({"_id": context.author.id}, {"$push": {"responses": new_data}}, upsert=True)
            
    except Exception as err:
        await error_handler(context=context, error=err)

@client.command(pass_context=True, aliases=["gifstat"])
async def gifstats(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            log("→ '.gifstats' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            data = mongo_users.find_one({"_id": context.author.id})
            if data is None:
                await context.send("{mention} It seems like you have no GIF sent by you".format(mention=context.author.mention))
                return

            responses = data["responses"]
            servers = []
            searches = []
            providers = []
            results = []
            for GIF in responses:
                servers.append(GIF["server"])
                searches.append(GIF["searchTerm"])
                providers.append(GIF["provider"])
                results.append(GIF["response"])

            GUILD = await client.fetch_guild(max(set(servers), key=servers.count))

            SEARCH = max(set(searches), key=searches.count)
            if SEARCH is None:
                SEARCH = ".gifrandom"
            SEARCH = str(SEARCH)

            PROVIDER = str(max(set(providers), key=providers.count)).title()
            RESULT = str(max(set(results), key=results.count)).title()
            try:
                RESULT = create_short_url(RESULT)
            except Exception:
                pass

            embed = discord.Embed(title='EasyGif Stats', colour=discord.Colour.blue())
            embed.add_field(name=f'Stats for {context.author.name}', value=STATS_TEMPLATE.format(
                gif_number=len(responses),
                server=str(GUILD),
                search=SEARCH,
                gif=RESULT,
                provider=PROVIDER
            ))
            embed.set_footer(text='© Anime no Sekai - 2021')
            await context.send(embed=embed)

            log("← '.gifstats' for {user}".format(user=context.author))
            
    except Exception as err:
        await error_handler(context=context, error=err)

@client.command(pass_context=True, aliases=["gifclears"])
async def gifclear(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            status = await context.send('{mention} Clearing your data...'.format(mention=context.author.mention))

            log("→ '.gifclear' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            mongo_users.delete_one({"_id": context.author.id})

            await status.edit(content='{mention} We successfully cleared your data! ✨'.format(mention=context.author.mention))

            log("← '.gifclear' for {user}".format(user=context.author))

    except Exception as err:
        await error_handler(context=context, error=err)

@client.command(pass_context=True, aliases=["gifhelps"])
async def gifhelp(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            log("→ '.gifhelp' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            embed = discord.Embed(title='EasyGif Help Center', colour=discord.Colour.blue())
            embed.add_field(name='Available Commands', value=HELP_TEMPLATE)
            embed.set_author(name=f"Requested by {context.author}")
            embed.set_footer(text="© Anime no Sekai — 2021")
            await context.send(embed=embed)

            log("← '.gifhelp' for {user}".format(user=context.author))

    except Exception as err:
        await error_handler(context=context, error=err)


@client.command(pass_context=True, aliases=["easygifstat"])
async def easygifstats(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            log("→ '.easygifstats' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            embed = discord.Embed(title='EasyGif Bot Stats', colour=discord.Colour.blue())
            embed.add_field(name='Stats', value=BOTSTATS_TEMPLATE.format(
                version=EASYGIF_VERSION,
                latency=round(client.latency * 1000, 2),
                servers=len(client.guilds),
                users=mongo_users.count_documents({})
            ))
            embed.add_field(name='Powered by', value=POWERED_BY)

            await context.send(embed=embed)

            log("← '.easygifstats' for {user}".format(user=context.author))

    except Exception as err:
        await error_handler(context=context, error=err)

@client.command(pass_context=True, aliases=["gifinvites"])
async def gifinvite(context):
    try:
        async with context.typing():
            await context.message.add_reaction(ROGER_REACTION) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

            log("→ '.gifinvite' came from the server {server} (user: {user})".format(server=context.guild, user=context.author))

            await context.send(content="I'm glad that you wanna share me with your friends!")
            await context.send(content="Here is the link: **https://bit.ly/invite-easygif**")

            log("← '.gifinvite' for {user}".format(user=context.author))

    except Exception as err:
        await error_handler(context=context, error=err)
