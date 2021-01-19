
# Cibot

## Description

This repository contains a code of Official discord bot of WEITI Telekomunikacja 2020/2021-Z;
The code is universal, so there's no need to tweak the code to run it as your own new bot.
(more on that in MANUAL.txt)


## Setup

Bot uses exclusively python, with heavy dependence on [discord.py](https://discordpy.readthedocs.io/en/latest/api.html) library.


### Installing

In order to use this bot you only need [Python (3.5+)](https://www.python.org/) and [git](https://git-scm.com/) dependencies installed on your system;

To download current version of bot, open destination directory, run terminal and run the following commands:

```
git clone https://github.com/KKotlicki/Cibot.git

```


### Required modules

To install all the libraries and modules, run the following script in terminal:


#### Windows OS

```
py -m pip install discord
py -m pip install dotenv
py -m pip install json
py -m pip install glob
py -m pip install random
py -m pip install os

```


#### Unix/macOS

```
python -m pip install discord
python -m pip install dotenv
python -m pip install json
python -m pip install glob
python -m pip install random
python -m pip install os

```


### Folder structure

Here's current folder structure for Cibot:

```
cogs/            # command scripts
dumps/           # temporary and dump files
pics/            # pictures and image type resources
res/             # commands' .text, .json, .lua, .xml and .cms resources
|- adm_help      # descriptions and call names of admin commands
|- credits       # creators and contributors
|- help          # descriptions and call names of user commands
|- linki         # links for <"unofficial" links> command
|- oflinki       # links for <"official" links> command
.gitattributes   # git repo configuration
.gitignore       # ^
MANUAL.txt       # instructions for creating and setting up new bot
README.md        # Documentation
cibot.py         # the main bot script
config.py        # bot settings
helpers.py       # custom methods bank
```


## Development

Cibot is an open source project. Every contribution is welcome.
To contribute, make your own branch and send git pull request.
First, connect to your github account; then following git code can be used to create a new branch with your changes:

```
git init
git remote https://github.com/KKotlicki/Cibot
git checkout -b
git add *
git commit *
git push

```

To commit changes to bot and publish your contribution, log in your github and send a branch pull request 


### Lanugage

Here are some keywords concerning structure and code that used in this manual and in-script comments

 - method                           # function inside class - general python lingua
 - global (data)                    # resources, configurations, variables, functions, that are used by bot in several unrelated functions
 - cogs                             # modules with special syntax containing one class with several bot command or behaviour methods
 - asynchronic, asyn functions      # functions that are executed simultaneously; if a child function is asynchronic, then every parent must be as well

### Structure

**Notice**  Commits that don't keep to the structure won't be accepted. The integrity and plurality is the key element of Cibot.


#### cibot.py

The main bot script. It has few only functions:

 - connects to bot's discord api
 - loads config.py file
 - set some global settings
 - loads all the cogs from directory

main script should't contain any commands
keep code here as clear, tidy and minimal as possible


#### module_name_cog.py

The most important element of the bot.
Every cog file is independent module, containing one class in special syntax with several closely related methods.
They dictate bot behaviour, but bot should be able to work with or without any of them.
To add new commands or functionalities, create a cog or add to existing cog.

##### cog syntax

For refference, look at the cogs/ directory to find examples of code.
Here's a cog example;
It creates three methods:
 - 1st is automaticaly called when bot is going online
 - 2nd when user types in chat <!ping>
 - 3rd when user types in chat <!dice>

```
from discord.ext import commands           # necessary function, that loads
import random                              # the library used by internal method


class ExampleCog(commands.Cog):            # the class containing cogs functions
    def __init__(self, client):
        self.client = client
        self.some_variable = 3

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')
    
        @commands.command()
    async def dice(self, ctx):
        await ctx.send(f'The dice rolled: {random.randint(1, 6)}')


def setup(client):                         # necessary function, that alows cibot.py to read it as cog
    client.add_cog(ExampleCog(client))

```


----------------------WiP------------------------



from config import *
from helpers import *


Contents:
cibot.py - Bot's exec script. Do not edit the code, unless you know what you're doing. Anyway, keep the code here minimal.
config.py - Script containing setup variables. It contains relative paths and general bot settings (you can add your own).
helpers.py - Script stores local and global functions, that have either too big, too small scope or are too long to be used in cogs under @commands.command.
cogs/ - Place here cogs with your own commands.
res/ - Place here your text, json, xml, cms files or special images. Do not create any folders in this directory. Create in main instead.
pics/ - Place here your pictures.
README.md - this documentation.
MANUAL.txt - instructions for creating new bot with this code.


hidden files:
.env - contains bot TOKEN. psst, it's secret...
servers/ - contains some server data and specific settings
ytaudio/ - contains temporary music files (downloads music from youtube in there, then plays it)

Main bot script is cibot.py. Keep it tidy!
In config.py save data such as relative paths, server settings, etc.
In helpers.py add your local methods.

Data will be updated to 2nd semester soon.


Ground Rules:
1.  call variables clearly and by this standard: variable_name
2.  call classes clearly and by this standard: ClassName
3.  call files clearly and by this standard: fname_sname.foo
4.  do not create subfolders in resources/ and cogs/
5.  in cogs/ put ONLY cogs file with correct cogs syntax
6.  if you want to create directory for something else than pictures, do so in main directory
7.  unless you have a good reason, do not change cibot.py script
8.  do not use <while True> or simmilar commands - they break script asynchronicity
9.  do not use purge methods (or only for authenticated users)


ToDo:
1. Bot Status (WiP)
2. Calendar of exams
3. Time to final exams (countdown)
4. Send documents (such as subject statues)
5. Points to grade converter (by subject)
6. Youtube play by keyword
7. !help and link cogs need to read polish characters
8. Change everywhere __client__ object to __bot__
9. Rewrite or format documentation - this one sucks!
