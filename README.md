# EasyGif
 A quick gif sending discord bot written in python

## Invite Link
https://bit.ly/invite-easygif

> Or simply type `.gifinvite` if you already have it in your discord server.

### Authorization/Permission
The bot doesn't have any administrator permissions (because it's pretty weird for a gif sending bot to have such permissions) and thus won't be able to access every channel of your server (if the channel is restricted to a certain role for example).

> Feel free to adjust EasyGif role access to enjoy the bot everywhere you want it to be!

## What is EasyGif?
EasyGif is a simple bot which helps you send GIFs as quick as possible on Discord.
> Simply type `.gif <search term>` replacing `<search term>` with the theme of the gif you want to send.

But it has also cool features!
- Write `.gifrandom` to send a random GIF to the channel
- Write `.gifstats` to display your statistics on EasyGif
- Write `.gifchange` to change the last gif you sent with EasyGif *(yea if you didn't like it)*
- Write `.gifdelete` to delete the last gif you sent with EasyGif *(if you made an oopsie)*

### Provider
EasyGif uses currently two providers: Giphy and Tenor GIF.

Each gif provider has 50% of chance of being the one chosen for your gif.

GIFs from your search term are chosen using the search API endpoint for each provider and chosing randomly between the first 10 GIFs results *(to give it more diversity)*

## Development

**You won't find any key in the source code of EasyGif** 

EasyGif is in constant development and fixes are made on a regular basis (but I also try to add some new features ehe)

If you want to help us and join me here is a quick guide.

#### Dependencies
EasyGif won't live long without the help of its dependencies and awesome modules that others made, which includes:
- Requests *(To make HTTP requests to the different API EasyGif uses)*
> Can be installed using `PIP` (the python package manager) through the command: `pip install requests`
- Discord.py *(basically what makes the bot running and communicating with discord)*
> Can be installed using `PIP` through the command: `pip install discord.py`
- Firebase Admin SDK *(to manage the database)*
> Can be installed using `PIP` through the command: `pip install firebase-admin`

> You could install psutil through `pip install psutil` but you won't be able to test it because the `.easygif_masterlogs` is restricted to me. 

#### Firebase
EasyGif records every GIF request made *(including with `.gifchange`)* in a Firebase Real-Time Database for statistical purposes (when you type `.gifstats`) but for nothing else (not even for my stats).

All of your data can be cleared from the database using `.gifstats_clear`

#### Servers
- The bot is hosted with Heroku *(the free plan lol)*

> Therefore, **you won't find any key in the source code of EasyGif** (every key is stored with config variables directly on Heroku) (even the firebase authentificating file name).

- Assets used frequently *(such as the Giphy logo and the Tenor logo, used in every GIF requests for legal reasons)* are stored in a website made for EasyGif assets only.

