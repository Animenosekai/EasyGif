#####                           EasyGif discord bot
#####
##### © Anime no Sekai - 2020
##### for Python 3
#####

# IMPORTS

### INSTALLED WITH PIP
from discord.ext import commands # to get discord commands
import discord # to communicate with discord
import psutil # to get system details
import requests # to make http requests
# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

### NATIVE TO PYTHON
import json
import random
import os
import datetime
import asyncio
from collections import Counter
import platform

if not os.path.exists(os.environ['firebase-auth-json']):
    download = requests.get(os.environ['firebase-auth-json-from-assets'])
    open(os.environ['firebase-auth-json'], 'wb').write(download.content)

# INITIALIZING FIREBASE
os.system('ls')
cred = credentials.Certificate(os.environ['firebase-auth-json'])
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['databaseURL']
})

# VARIABLES DEFINING
### FIREBASE VARIABLES
firebase = db.reference('users')

### REACTION EMOJI WHILE MESSAGE RECEIVED (FROM MY DISCORD SERVER)
roger_reaction = '<:easygif_roger:712005159676411914>'

### DEFINING CLIENT/BOT AND ITS PREFIX 
client = commands.Bot(command_prefix='.')

### CLEAR AFTER EVERYTHING IS INITIALIZED
os.system('cls' if os.name == 'nt' else 'clear')


# WHEN THE BOT IS UP
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.gifhelp')) # GAME ACTIVITY
    print('EasyGif is ready.') # LOG THAT THE BOT IS READY

# MAIN COMMAND: .gif <SEARCH>
@client.command(pass_context=True)
async def gif(context, *, search):
    await context.message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    print('')
    print("→ '.gif " + search + f"' came from the server: {context.guild}  (user: {context.author})") # LOG

    embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gif {}`'.format(search), colour=discord.Colour.blue()) # CREATE AN MESSAGE EMBED INSTANCE

    provider = random.randint(0,1) # CHOOSE THE PROVIDER RANDOMLY

    if provider == 0: #GIPHY
        search.replace(' ', '+') # MAKE SURE THAT SPACES ARE URL-ENCODED
        response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + os.environ['giphy-api-key'] + '&limit=10') # MAKE A SEARCH WITH THE GIPHY API
        data = json.loads(response.text) # GET THE RESPONSE AS A DICT

        gif_choice = random.randint(0, 9) # CHOOSE RANDOMLY FROM THE FIRST 10 ANSWERS
        result_gif = data['data'][gif_choice]['images']['original']['url'] # GETTING THE GIF (result)

        embed.set_image(url=result_gif) # SET THE IMAGE IN THE EMBED AS THE GIF
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy") # SET THE FOOTER WITH THE PROVIDER NAME FOR LEGAL REASONS
        
        await context.send(embed=embed) # SEND THIS NEW MESSAGE
        await context.message.delete() # DELETE THE ORIGINAL MESSAGE (to make it clean)

        print("← '.gif " + search + "' response: " + result_gif) # LOG
        
        # FIREBASE (recording that the user has made a request)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": search,
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "giphy",
            "item_number": gif_choice
        }
        
        ### UPDATING THE DATABASE
        user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
        user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE

    elif provider == 1: #TENOR GIF
        search.replace(' ', '+')
        response = requests.get('https://api.tenor.com/v1/search?q=' + search + '&key=' + os.environ['tenor-api-key'] + '&limit=10')
        data = json.loads(response.text)

        gif_choice = random.randint(0, 9)
        result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

        await context.send(embed=embed)
        await context.message.delete()

        print("← '.gif " + search + "' response: " + result_gif)


        # FIREBASE (recording that the user has made a request)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": search,
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "tenor",
            "item_number": gif_choice
        }
        
        ### UPDATING THE DATABASE
        user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
        user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE
            

# RANDOM GIF: .gifrandom
@client.command(pass_context=True)
async def gifrandom(context):
    await context.message.add_reaction(roger_reaction)

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    print('')
    print(f"→ '.gifrandom' came from the server: {context.guild}  (user: {context.author})")
    embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gifrandom`', colour=discord.Colour.blue())
    provider = random.randint(0,1)
    if provider == 0: #GIPHY RANDOM
        response = requests.get('https://api.giphy.com/v1/gifs/random?api_key=' + os.environ['giphy-api-key'])
        data = json.loads(response.text)
        result_gif = data['data']['images']['original']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")
        await context.send(embed=embed)
        await context.message.delete()
        print("← '.gifrandom' response: " + result_gif)

        # FIREBASE (recording that the user has made a request)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": "random",
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "giphy",
            "item_number": "random"
        }
        
        ### UPDATING THE DATABASE
        user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
        user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE

    elif provider == 1: # TENOR GIF (RANDOM ANIME GIF)
        response = requests.get('https://api.tenor.com/v1/search?q=anime&key=' + os.environ['tenor-api-key'] + '&limit=10')
        data = json.loads(response.text)
        gif_choice = random.randint(0, 9)
        result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

        await context.send(embed=embed)
        await context.message.delete()

        print("← '.gifrandom' response: " + result_gif)


        # FIREBASE (recording that the user has made a request)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": "random",
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "tenor",
            "item_number": gif_choice
        }
        
        ### UPDATING THE DATABASE
        user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
        user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE



@client.command(pass_context=True)
async def gifdelete(context):
    await context.message.add_reaction(roger_reaction)
    print('')
    print(f"→ Delete request came from the server: {context.guild}  (user: {context.author})")
    status = await context.send('Searching your last gif...')
    found = False
    messages = await context.channel.history(limit=None).flatten()
    try:
        for message in messages:
            if message.author == client.user:
                if len(message.embeds) != 0:
                    if message.embeds[0].title == f'From {context.author}':
                        await status.edit(content='Deleting it...')
                        found = True
                        await message.delete()
                        print(f"← {context.author}'s GIF deleted on {context.guild}")
                        await status.edit(content='Last gif deleted! ✨')
                        await asyncio.sleep(3)
                        await status.delete()
                        await context.message.delete()
            if found == True:
                break
        if found == False:
            await status.edit(content='❌ An error occured while searching your last gif!')
            await asyncio.sleep(3)
            await status.delete()
            await context.message.delete()
    except:
        await status.edit(content='❌ An error occured while deleting your last gif!')
        await asyncio.sleep(3)
        await status.delete()
        await context.message.delete()



@client.command(pass_context=True)
async def gifchange(context):
    await context.message.add_reaction(roger_reaction)

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    status = await context.send('Searching your last gif...')
    found = False
    messages = await context.channel.history(limit=None).flatten()
    for message in messages:
        if message.author == client.user:
            if len(message.embeds) != 0:

                if message.embeds[0].title == f'From {context.author}':
                    found = True
                    embed_desc = message.embeds[0].description
                    search_term = embed_desc[15:]
                    search_term = search_term[:-1]
                    if search_term == 'ando' or search_term == 'andom' or search_term == 'random':
                        print('')
                        print(f"→ '.gifchange random' came from the server: {context.guild}  (user: {context.author})")
                        embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gifrandom`', colour=discord.Colour.blue())
                        provider = random.randint(0,1)
                        if provider == 0: #GIPHY RANDOM
                            response = requests.get('https://api.giphy.com/v1/gifs/random?api_key=' + os.environ['giphy-api-key'])
                            data = json.loads(response.text)
                            result_gif = data['data']['images']['original']['url']

                            embed.set_image(url=result_gif)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()

                            print("← '.gifchange random' response: " + result_gif)

                            # FIREBASE (recording that the user has made a request)
        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": "random",
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": result_gif,
                                "provider": "giphy",
                                "item_number": "random"
                            }
                            
                            ### UPDATING THE DATABASE
                            user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
                            user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE

                        elif provider == 1: # TENOR GIF (RANDOM ANIME GIF)
                            response = requests.get('https://api.tenor.com/v1/search?q=anime&key=' + os.environ['tenor-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

                            embed.set_image(url=result_gif)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()
                            
                            print("← '.gifchange random' response: " + result_gif)

                            # FIREBASE (recording that the user has made a request)
        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": "random",
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": result_gif,
                                "provider": "tenor",
                                "item_number": gif_choice
                            }
                            
                            ### UPDATING THE DATABASE
                            user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
                            user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE

                    else:
                        print('')
                        print("→ '.gifchange " + search_term + f"' came from the server: {context.guild}  (user: {context.author})")
                        await status.edit(content='Searching a new gif...')

                        embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gif {}`'.format(search_term), colour=discord.Colour.blue())
                        provider_from_url = message.embeds[0].image.url
                        provider_from_url = provider_from_url[:19]
                        provider_from_url = provider_from_url[14:]

                        if provider_from_url in "tenor":
                            provider = 0
                        else:
                            provider = 1

                        if provider == 0: #GIPHY
                            search_term.replace(' ', '+')
                            response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search_term + '&api_key=' + os.environ['giphy-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            new_image = data['data'][gif_choice]['images']['original']['url']

                            embed.set_image(url=new_image)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()
                            print("← '.gifchange " + search_term + "' response: " + new_image)
                            
                            # FIREBASE (recording that the user has made a request)
        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": search_term,
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": new_image,
                                "provider": "giphy",
                                "item_number": gif_choice
                            }
                            
                            ### UPDATING THE DATABASE
                            user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
                            user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE

                        elif provider == 1: #TENOR GIF
                            search_term.replace(' ', '+')
                            response = requests.get('https://api.tenor.com/v1/search?q=' + search_term + '&key=' + os.environ['tenor-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            new_image = data['results'][gif_choice]['media'][0]['gif']['url']

                            embed.set_image(url=new_image)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()

                            print("← '.gifchange " + search_term + "' response: " + new_image)

                            # FIREBASE (recording that the user has made a request)
        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": search_term,
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": new_image,
                                "provider": "tenor",
                                "item_number": gif_choice
                            }
                            
                            ### UPDATING THE DATABASE
                            user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
                            user_node.push().set(data) # SENDING THE DATA AS A NEW NODE IN THE DATABASE
        if found == True:
            break


@client.command(pass_context=True)
async def gifdeletes(context):
    await gifdelete(context)

@client.command(pass_context=True)
async def gifchanges(context):
    await gifchange(context)


@client.command(pass_context=True)
async def gifstats(context):
    await context.message.add_reaction(roger_reaction)
    status = await context.send('Retrieving your informations...')
    print('')
    print(f"→ Stats request came from the server: {context.guild}  (user: {context.author})")

    try:    
        user_node = firebase.child('requests/' + str(context.author.id))
        user_data = user_node.get()
    except:
        await status.edit(content='❌ An error occured while retrieving your infos!')
        await asyncio.sleep(2)
        user_data = "There is an error"

    if user_data != None:
        total_number_of_gifs = len(user_data)
        servers = []
        commands = []
        providers = []
        gifs = []
        for gif in user_data:
            servers.append(user_data[gif]['server'])
            commands.append(user_data[gif]['search_term'])
            providers.append(user_data[gif]['provider'])
            gifs.append(user_data[gif]['response'])
        
        most_used_server = max(set(servers), key=servers.count)
        most_used_search_term = max(set(commands), key=commands.count)
        most_used_provider = max(set(providers), key=providers.count)
        most_used_gif = max(set(gifs), key=gifs.count)
        
        try:
            linkRequest = {"destination": f"{most_used_gif}", "title": "EasyGif - Redirecting you to the orginal GIF"}
            requestHeaders = {"Content-type": "application/json", "apikey": os.environ['rebrandly-api-key']}

            shorten_link_request = requests.post("https://api.rebrandly.com/v1/links", data = json.dumps(linkRequest), headers=requestHeaders)

            shorten_link_information = json.loads(shorten_link_request.text)
            shorten_link = 'https://' + shorten_link_information['shortUrl']
        except:
            print('An error occured while shortening the link')
            shorten_link = most_used_gif
        embed = discord.Embed(title='EasyGif Stats', colour=discord.Colour.blue())
        embed.add_field(name=f'Stats for {context.author.name}', value=f"Total Number of GIFs: **{str(total_number_of_gifs)}**\nMost active server: **{most_used_server}**\nMost searched term: **{most_used_search_term}**\nMost sent GIF: **{shorten_link}**\nMost used GIF provider: **{most_used_provider}**")
        embed.set_footer(text='©Anime no Sekai - 2020')
        await status.edit(content='', embed=embed)
        await context.message.delete()
    elif user_data == "There is an error":
        print(f'Error while retrieving infos for {context.author}')
    else:
        await status.edit(content="You haven't sent any gif with me yet!")
    print(f"← Stats sent on {context.guild} to {context.author}")

@client.command(pass_context=True)
async def gifstat(context):
    await gifstats(context)

@client.command(pass_context=True)
async def gifstats_clear(context):
    await context.message.add_reaction(roger_reaction)
    status = await context.send('Deleting your data...')
    print('')
    print(f"→ User Stats clear request came from the server: {context.guild}  (user: {context.author})")
    await asyncio.sleep(1)
    ### UPDATING THE DATABASE
    user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
    if user_node.get() != None:
        try:
            user_node.delete()
            await status.edit(content='Done! ✨')
            print(f"← Data cleared for {context.author}")
            await asyncio.sleep(2)
            await status.delete()
            await context.message.delete()
        except:
            print('Error while deleting the data')
            await status.edit(content='❌ An error occured while deleting your data!')
            await asyncio.sleep(2)
    else:
        print(f"← No data to clear for {context.author}")
        await status.edit(content="You haven't sent any gif with me yet!")
        await asyncio.sleep(2)

@client.command(pass_context=True)
async def gif_statsclear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstatsclear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstat_clear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstatclear(context):
    await gifstats_clear(context)


@client.command(pass_context=True)
async def gifhelp(context):
    await context.message.add_reaction(roger_reaction)
    print('')
    print(f"→ Help request came from the server: {context.guild}  (user: {context.author})")
    embed = discord.Embed(title='EasyGif Help Center', colour=discord.Colour.blue())
    embed.add_field(name='Available Commands', value="`.gif <search term>`: Searches a GIF on Giphy or Tenor (50% of chance for each) with the term you provided and sends it.\n`.gifrandom`: Sends a random GIF.\n`.gifchange`: Changes your last sent GIF.\n`.gifdelete`: Deletes the last sent GIF.\n`.gifstats`: Gives you your EasyGif's stats.\n`.gifstats_clear`: Clears your data from my database\n`.gifinvite`: Gives you a link to invite EasyGif on any discord server.\n`.easygifstats`: Gives EasyGif bot stats\n`.easygif_dev`: Gives you a link to easygif github repo.\n`.gifhelp`: Sends the message you are currently reading.")
    embed.set_author(name=f"Requested by {context.author}")
    embed.set_footer(text="EasyGif by Anime no Sekai - 2020")
    await context.send(embed=embed)
    print(f"← Help Center sent on {context.guild} to {context.author}")
    await context.message.delete()

@client.command(pass_context=True)
async def gifhelps(context):
    await gifhelp(context)

@client.command(pass_context=True)
async def easygifstats(context):
    await context.message.add_reaction(emoji=roger_reaction)
    print('')
    print(f"→ EasyGif Bot Stats request came from the server: {context.guild}  (user: {context.author})")
    number_of_servers_easygif_is_in = str(len(client.guilds))
    latency = round(client.latency * 1000,2)
    users = str(len(client.users))
    embed = discord.Embed(title='EasyGif Bot Stats', colour=discord.Colour.blue())
    embed.add_field(name='Stats', value=f"Version: **EasyGif v.1.5**\nPing/Latency: **{latency}ms**\nNumber of servers: **{number_of_servers_easygif_is_in}**\nNumber of users: **{users}**\nDeveloper: **Anime no Sekai**\nProgramming Language: **Python**")
    embed.add_field(name='Powered by', value="Giphy\nTenor GIF\nHeroku\nGoogle Firebase\nRequests Python Library\ndiscord.py Python Library\nRebrand.ly\nNetlify\nGitHub\nDiscord")
    await context.send(embed=embed)
    print(f"← EasyGif Bot Stats sent on {context.guild} to {context.author}")
    await context.message.delete()

@client.command(pass_context=True)
async def easygif_stats(context):
    await easygifstats(context)

@client.command(pass_context=True)
async def easygif_stat(context):
    await easygifstats

@client.command(pass_context=True)
async def easygifstat(context):
    await easygifstats

@client.command(pass_context=True)
async def gifinvite(context):
    print('')
    print(f"→ Invite link request came from the server: {context.guild}  (user: {context.author})")
    await context.message.add_reaction(emoji=roger_reaction)
    await context.send(content="I'm glad that you wanna share me with your friends!")
    await asyncio.sleep(2)
    await context.send(content="Here is the link: **https://bit.ly/invite-easygif**")
    print(f"← Invite link sent on {context.guild} to {context.author}")
    
@client.command(pass_context=True)
async def gifinvites(context):
    await gifinvite(context)

@client.command(pass_context=True)
async def gifdonate(context):
    print(f"→ Donation request came from the server: {context.guild}  (user: {context.author})")
    await context.message.add_reaction(emoji=roger_reaction)
    await context.send(content="Thank's for having interest in the development of EasyGif!")
    await asyncio.sleep(random.uniform(1.5, 2.3))
    await context.send(content="The fact that you're using this bot is already amazing")
    await asyncio.sleep(random.uniform(0.8, 1.5))
    await context.send(content="But I won't lie, keeping the database and the server alive will cost me money someday")
    await asyncio.sleep(random.uniform(0.8, 1.5))
    donatelink_embed = discord.Embed(title='Donation Links', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**PayPal**', value="https://paypal.me/animenosekai")
    donatelink_embed.add_field(name='**uTip** (if you want to help me without spending anything)', value="https://utip.io/animenosekai")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using EasyGif!")
    await context.send(embed=donatelink_embed)
    print(f"← Donation links sent on {context.guild} to {context.author}")

@client.command(pass_context=True)
async def gifdonates(context):
    await gifdonate(context)

@client.command(pass_context=True)
async def easygif_donate(context):
    await gifdonate(context)
    

@client.command(pass_context=True)
async def easygif_development(context):
    print(f"→ Development links request came from the server: {context.guild}  (user: {context.author})")
    await context.message.add_reaction(emoji=roger_reaction)
    await context.send(content="Thank's for having interest in the development of EasyGif!")
    await asyncio.sleep(random.uniform(0.8, 1.3))
    donatelink_embed = discord.Embed(title='GitHub Repository', colour=discord.Colour.blue())
    donatelink_embed.add_field(name='**GitHub**', value="https://github.com/Animenosekai/EasyGif")
    donatelink_embed.set_footer(text="©Anime no Sekai - Thank you for using EasyGif!")
    await context.send(embed=donatelink_embed)
    print(f"← Development links sent on {context.guild} to {context.author}")
  
@client.command(pass_context=True)
async def gifdevelopment(context):
    await easygif_development(context)

@client.command(pass_context=True)
async def gifdev(context):
    await easygif_development(context)
    
@client.command(pass_context=True)
async def dev_easygif(context):
    await easygif_development(context)
    
@client.command(pass_context=True)
async def development_easygif(context):
    await easygif_development(context)
    
    
@client.command(pass_context=True)
async def easygif_dev(context):
    await easygif_development(context)
    
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@client.command(pass_context=True)
async def easygif_masterlogs(context):
    print('')
    print(f"→ Logs request came from the server: {context.guild}  (user: {context.author})") #LOG
    if context.author.id == int(os.environ['anise-discord-uid']): #IF ME
        # STATUS AND LOG
        status = await context.send(content='Preparing your logs, master!')
        print(f" -- Successfully authenticated as EasyGif dev -- ")
        
        # CREATING THE EMBEDS
        embed_systeminfo_system = discord.Embed(title='Master Logs - System Infos', colour=discord.Colour.blue())
        embed_systeminfo_cpu = discord.Embed(title='Master Logs - CPU Infos', colour=discord.Colour.blue())
        embed_systeminfo_ram = discord.Embed(title='Master Logs - Memory Infos', colour=discord.Colour.blue())
        embed_systeminfo_disk = discord.Embed(title='Master Logs - Disk Infos', colour=discord.Colour.blue())
        embed_systeminfo_network = discord.Embed(title='Master Logs - Network Infos', colour=discord.Colour.blue())
        embed_apikeys = discord.Embed(title='Master Logs - API Keys', colour=discord.Colour.blue())

        # API KEYS FIELD
        embed_apikeys.add_field(name="API Keys", value="**You can now access all of those infos from the Heroku App Dashboard**")
        
        # VARIABLES DECLARATION
        uname = platform.uname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
        boottime = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        cpufreq = psutil.cpu_freq()
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        # PER CORE CPU DETAILS
        cpu_usage_per_core = {}
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            cpu_usage_per_core[str(i)] = str(percentage)
        cpu_usage_per_core_string = ''
        for core in cpu_usage_per_core:
            cpu_usage_per_core_string = cpu_usage_per_core_string + "\nCore " + str(core) + ': ' + str(cpu_usage_per_core[str(core)]) + '%'

        # DISK PARTITIONS DETAILS
        informations_per_partition = {}

        partitions = psutil.disk_partitions()
        for partition in partitions:
            informations_per_partition[partition.device] = f"\nMountpoint: **{partition.mountpoint}**\nFile System type: **{partition.fstype}**\n"
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            informations_per_partition[partition.device] = informations_per_partition[partition.device] + f'Total Size: **{get_size(partition_usage.total)}**\nUsed: **{get_size(partition_usage.total)}**\nFree: **{get_size(partition_usage.free)}**\nPercentage: **{partition_usage.percent}%**\n'

        partitions_informations_string = ''

        for partition in informations_per_partition:
            partitions_informations_string = partitions_informations_string + f'\n== Partition: **{partition}** =={informations_per_partition[partition]}'


        # TO MAKE SURE IT DOES NOT EXCEED 1024 CHARACTERS
        try:
            partitions_informations_string = partitions_informations_string[:915]
        except:
            pass

        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        try:
            total_read_disk = disk_io.read_bytes()
        except:
            total_read_disk = 0
            await status.edit(content='❌ An error occured while looking for disk total read informations!')
        
        try:
            total_write_disk = disk_io.write_bytes()
        except:
            total_write_disk = 0
            await status.edit(content='❌ An error occured while looking for disk total write informations!')
        

        # NETWORK INTERFACES DETAILS
        network_interfaces = {}

        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_interfaces[interface_name] = f"IP Address: **{address.address}**\nNetmask: **{address.netmask}**\nBrodcast IP: **{address.broadcast}**\n"
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    network_interfaces[interface_name] = f"MAC Address: **{address.address}**\nNetmask: **{address.netmask}**\nBrodcast MAC: **{address.broadcast}**\n"

        network_interfaces_string = ''
        for interface in network_interfaces:
            network_interfaces_string = network_interfaces_string + f" == Interface: {interface} ==\n{network_interfaces[interface]}"

        # TO MAKE SURE IT DOES NOT EXCEED 1024 CHARACTERS
        try:
            network_interfaces_string = network_interfaces_string[:905]
        except:
            pass
    
        # MAKING FIELDS
        try:
            embed_systeminfo_system.add_field(name='System Infos', value=f"System: **{uname.system}**\nNode Name: **{uname.node}**\nRelease: **{uname.release}**\nVersion: **{uname.machine}**\nProcessor: **{uname.processor}**\n\n\nBoot Time: **{boottime}**")
        except:
            await status.edit(content='❌ An error occured while looking for system informations!')
        try:
            embed_systeminfo_cpu.add_field(name='CPU Infos', value=f"Physical cores: **{psutil.cpu_count(logical=False)}**\nTotal cores: **{psutil.cpu_count(logical=True)}**\nMax Frequency: **{cpufreq.max:.2f}Mhz**\nMin Frequency: **{cpufreq.min:.2f}Mhz**\nCurrent Frequency: **{cpufreq.current:.2f}Mhz**\nCPU Usage Per Core: **{cpu_usage_per_core_string}\n**Total CPU Usage: **{psutil.cpu_percent()}%**")
        except:
            await status.edit(content='❌ An error occured while looking for CPU informations!')
        try:
            embed_systeminfo_ram.add_field(name='RAM Infos', value=f"Total: **{get_size(svmem.total)}**\nAvailable: **{get_size(svmem.available)}**\nUsed: **{get_size(svmem.used)}**\nPercentage: **{svmem.percent}%**\n=== SWAP ===\nTotal: **{get_size(swap.total)}**\nFree: **{get_size(swap.free)}**\nUsed: **{get_size(swap.used)}**\nPercentage: **{swap.percent}%**")
        except:
            await status.edit(content='❌ An error occured while looking for RAM informations!')
        try:
            embed_systeminfo_disk.add_field(name='Disk Infos', value=f"**=== Partitions Information ===**\n{partitions_informations_string}\n**=== IO Information ===**\nTotal read: **{get_size(total_read_disk)}**\nTotal write: **{get_size(total_write_disk)}**")
        except:
            await status.edit(content='❌ An error occured while looking for disk informations!')
        try:
            embed_systeminfo_network.add_field(name='Network Infos', value=f"**=== Interfaces Information ===**\n{network_interfaces_string}\n**=== IO Information ===\n**Total Bytes Sent: **{get_size(net_io.bytes_sent)}**\nTotal Bytes Received: **{get_size(net_io.bytes_recv)}**")
        except:
            await status.edit(content='❌ An error occured while looking for network interfaces informations!')
        # SEND EVERYTHING
        master = client.get_user(int(os.environ['anise-discord-uid']))
        await master.send(content='Here are your logs, master!')
        await master.send(embed=embed_apikeys)
        await master.send(embed=embed_systeminfo_system)
        await master.send(embed=embed_systeminfo_cpu)
        await master.send(embed=embed_systeminfo_ram)
        await master.send(embed=embed_systeminfo_disk)
        await master.send(embed=embed_systeminfo_network)
        await status.edit(content='Your logs have been sent in your dm!')
        await context.message.delete()
        print(f"← Master logs sent to {context.author}") #LOG
    else: #NOT ME
        await context.send(content="Sorry but you do not seem like my creator.")

client.run(os.environ['easygif-discordbot-token'])
