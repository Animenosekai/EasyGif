# EasyGif

[![EasyGif Logo](https://easygif-assets.netlify.app/assets/public/logos/easygif/easygif_logo.jpg)](https://bit.ly/invite-easygif)

### **A quick gif sending discord bot written in python**

## Invite Link

**<https://bit.ly/invite-easygif>**

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

More commands could be found using `.gifhelp` in a discord server where the bot already got invited.

### Provider

EasyGif uses currently two providers: Giphy and Tenor GIF.

Each gif provider has 50% of chance of being the one chosen for your gif.

GIFs from your search term are chosen using the search API endpoint for each provider and chosing randomly between the  results *(to give it more diversity)*

Using `.gifrandom` you have a 50% percent of chance of having a random gif from the `RANDOM_DICTIONARY` ([config.py](config.py)).

## Development

**You won't find any key in the source code of EasyGif**

EasyGif is in constant development and fixes are made on a regular basis (but I also try to add some new features ehe)

**If you have any issues, questions, development problem: feel free to ask in the issues section**

#### Dependencies

EasyGif won't live long without the help of its dependencies and awesome modules that others made, which includes:

- Requests *(To make HTTP requests to the different API EasyGif uses)*

> Can be installed using `PIP` (the python package manager) through the command: `pip install requests`

- Discord.py *(basically what makes the bot running and communicating with discord)*

> Can be installed using `PIP` through the command: `pip install discord.py`

- PyMongo *(to communicate with the database)*

> Can be installed using `PIP` through the command: `pip install pymongo`

### APIs and Documentations

Service | Documentations
------------ | -------------
MongoDB | [**MongoDB Manual**](https://docs.mongodb.com/manual/)
Heroku | [**Heroku Documentations**](https://devcenter.heroku.com/categories/reference)
discord.py | [**discord.py Documentations**](https://discordpy.readthedocs.io/en/latest/index.html#)
Discord (API) | [**Discord Developper Portal**](https://discord.com/developers/docs/intro)
Giphy | [**Giphy API Documentations**](https://developers.giphy.com/docs/api#quick-start-guide)
Tenor | [**Tenor GIF API Documentations**](https://tenor.com/gifapi/documentation)
Rebrand.ly | [**Rebrand.ly API Documentations**](https://developers.rebrandly.com/docs)
Requests | [**Requests Library Docs**](https://requests.readthedocs.io/en/master/)
Python 3 | [**Python 3.8.3 Docs**](https://docs.python.org/3/)

- MongoDB is the database used
- Heroku is used to host the bot (for the bot to run 24/24)
- discord.py is used to communicate with Discord's servers and contains multiple discord related functions
- Discord is used to... well is used by you primarily but also by us to configure the bot
- Giphy API is used to search and provide gifs
- Tenor API is used to search and provide gifs
- Rebrand.ly API is used to make gif link for `.gifstats` much shorter
- Requests Python Library is used to make HTTP requests
- Python is the programming language used to make the bot
- Netlify is used to host the assets
- GitHub is used to host assets and code

### Versions

Here are the versions used for EasyGif's development.

Service | Version
------------ | -------------
PyMongo | **Version 3.11.3**
discord.py | **Version 1.7.1**
Requests | **Version 2.23.0**
Python 3 | **Version 3.9.6**

The bot is currently on version: **`v2.0`**

#### Commands

Common commands mistypes are handled with functions written with mistypes that redirects to the main function.

#### MongoDB

EasyGif records every GIF request made *(including with `.gifchange`)* in a MongoDB Database for statistical purposes (when you type `.gifstats`).

All of your data can be cleared from the database using `.gifclear`

#### Servers

- The bot is hosted with Heroku *(the free plan)*

- Assets used frequently *(such as the Giphy logo and the Tenor logo, used in every GIF requests for legal reasons)* are stored in a website made for EasyGif assets only.

Assets are hosted by Netlify and GitHub.

## Copyrights and Legals

**EasyGif's logo is not my property and can be taken down at any time if the legal owner wants to do so.**

**Giphy** is a brand which belongs to Giphy, Inc.

**Tenor GIF** is a brand which belongs to Tenor, Inc.

**MongoDB** is a brand which belongs to MongoDB, Inc.

**Heroku** is a brand which belongs to Salesforce, Inc.

**Netlify** is a brand which belongs to Netlify Co.

**GitHub** is a brand which belongs to GitHub, Inc. (Microsoft)

**Discord** is a brand which belongs to Discord, Inc.

**Python** belongs to the Python Software Foundation

**Rebrand.ly** is a service/brand which belongs to Radiate Capital Limited

### Support Discord Server

I don't have a dedicated support discord server though you can enter my personal discord server and ask me anything:
[Anime no Sekai Discord Server](https://discord.com/invite/cgZWWdQ)

> © Anime no Sekai - 2021 ✨
