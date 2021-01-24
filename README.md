# Cibot

## Description

This repository contains a code of Official discord bot of WEITI Telekomunikacja 2020/2021-Z;
The code is universal and cross-platform compatible **(not tested on macOS!)** with a few extra features on Raspberry Pi 4;
The code is ready to be used as your own bot and no changes need to be applied (more on that in MANUAL.txt)
(more on that in MANUAL.txt)


## Setup

Bot uses exclusively python, with heavy dependence on [discord.py](https://discordpy.readthedocs.io/en/latest/api.html) library.


### Installing

To use our bot, you only need [Python (3.7+)](https://www.python.org/) and [git](https://git-scm.com/) dependencies installed on your system.

To download current version of bot, open destination directory, then run terminal and enter following commands:

```
git clone https://github.com/KKotlicki/Cibot.git

```


### Bot setup

**Once you run cibot.py, you will be asked to provide Token (a special id of the discord bot) and OS python 3 call command (usually python3 or py - you can check which one is it by running it in cmd)**


### Required modules

To install all the libraries and modules, run the following script in terminal:

```
python3 -m pip3 install discord
python3 -m pip3 install python.dotenv
python3 -m pip3 install youtube-dl
python3 -m pip3 install loguru
python3 -m pip3 install -U discord.py[voice]
python3 -m pip3 install youtube-search-python

```

### Folder structure

Here is current folder structure for Cibot:

```
ai/                 # (future) ai module resources
cogs/               # command scripts
logs/               # log files
pics/               # pictures and image type resources
rbp/                # resources for raspberry pi module
res/                # text, .json, .xml, Lua and CMS resources
|- adm_help         # descriptions and call names of admin commands
|- credits          # creators and contributors
|- help             # descriptions and call names of user commands
|- linki            # links for <"unofficial" links> command
|- oflinki          # links for <"official" links> command
|- subject_aliases  # alternative call names for <"unofficial" links> command
servers/            # server's data and logs
.gitattributes      # Git repo configuration
.gitignore          # ^
cibot.py            # ! - the main bot script
config.py           # bot settings
helpers.py          # custom methods bank
MANUAL.txt          # instructions for creating and setting up new bot
README.md           # documentation
```


## Development

Cibot is an open-source project. Every contribution is welcome;
To contribute, make your own branch and send Git pull request;
First, connect to your GitHub account, then use the following Git code to create a new branch with your changes:


```
git init
git remote https://github.com/KKotlicki/Cibot
git checkout -b
git add *
git commit *
git push

```

To commit changes to the main branch and publish your contribution, log in your GitHub account, and send a branch pull request


### Language

Here are some keywords concerning structure and code that are used in this manual and in-script comments

 - method                           # function inside class - general python lingua
 - global (data)                    # resources, configurations, variables, functions, that are used by bot in several unrelated functions
 - cogs                             # modules with special syntax containing one class with several bot commands or behavior methods
      

### Structure

**Notice**:	Commits that do not keep to the structure will not be accepted.


#### cibot.py

The main bot script. It has only few functions:

 - creates personal environment file
 - connects to bot's discord API
 - loads config.py file
 - set few of the global settings
 - loads all the cogs from directory
 - defines __update__ command

Main script should not define any other commands;
Keep this code as clear and minimal as possible.


#### module_name_cog.py

The most important element of the bot.
Every cog file is an independent module containing one class in special syntax with several closely related methods.
They dictate bot's behavior, although bot should be able to work with or without any of them.
To add new commands or functionalities, create a cog or add to existing cog.


##### cog syntax

For reference, look at the cogs/ directory to find examples of a code.
Here is one that defines three methods:
 - 1st is being automatically called when bot is going online
 - 2nd when user types in chat <!ping>
 - 3rd when user types in chat <!dice>

```
from discord.ext import commands           # necessary function - loads cog structure commands
import random                              # the library used by an example method


class ExampleCog(commands.Cog):            # the class containing cogs functions; inherits from commands.Cog class
    def __init__(self, client):
        self.client = client
        self.some_variable = "ready"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is {self.some_variable}.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')
    
    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f'The dice rolled: {random.randint(1, 6)}')


def setup(client):                         # necessary function - allows cibot.py to recognize it as cog
    client.add_cog(ExampleCog(client))

```


----------------------WiP------------------------

## Support

### Common Problems

 - synchronicity        


from config import *
from helpers import *


Contents:
cibot.py - Bot's exec script. Do not edit the code unless you know what you're doing. Anyway, keep the code here minimal.
config.py - Script containing setup variables. It contains relative paths and general bot settings (you can add your own).
helpers.py - Script stores local and global functions, that have either too big, too small scope or are too long to be used in cogs under @commands.command.
cogs/ - Place here cogs with your own commands.
res/ - Place here your text, json, xml, CMS files or special images. Do not create any folders in this directory. Create in main instead.
pics/ - Place here your pictures.
README.md - this documentation.
MANUAL.txt - instructions for creating new bot with this code.


hidden files:
 - .env - contains bot TOKEN, OS python 3 prefix and information if your machine is raspberry pi. this information is hidden and will not be shared.

Main bot script is cibot.py. Keep it tidy!
In config.py save data such as relative paths, server settings, etc.
In helpers.py add your local methods.

Data will be updated to 2nd semester soon.


**Development Rules:**
1.  name variables clearly and by this standard: variable_name
2.  name classes clearly and by this standard: ClassName
3.  name files clearly and by this standard: fname_sname.foo
4.  do not create subfolders or add any non-cog file in cogs/
5.  in cogs/ put ONLY cogs file with correct cogs structure
6.  if you want to create directory for something entirely different, do so in the main directory
7.  unless you have a good reason, do not change cibot.py script
8.  do not use __while True__ or similar commands in cogs - they break script asynchronicity


**ToDo:**
1.  Chat chess game (with ELO rating)                                                                               **[Major Feature]**
2.  Calendar of exams                                                                                               [Feature]
3.  Countdown to final exams                                                                                        [Feature]
4.  Send documents (such as subject statues, PW anthem)                                                             [Feature]
5.  Points to grade converter by subject                                                                            [Feature]
6.  yt_cog - play playlists, query, save query, load query                                                          [Rewrite]
7.  Fix logging systems                                                                                             [Fix]
8.  Finish documentation and setup manual                                                                           [Rewrite]
9.  AI chatbot                                                                                                      **[Major Feature]**
10. Move __helpers.py__ to utils directory (most cogs have dependency on it set by relative path!)                  **[Major Rewrite]**
11. Fix shutdown and raspberry temperature shutdown bug (currently restarts after first use, closes after second)   [Fix]
12. Disconnect from voice channel after period of inactivity                                                        [Rewrite]
13. Unit test script                                                                                                **[Major Feature]**
14. Error and exception handling                                                                                    **[Major Rewrite]**


```
[Major Rewrite] - Changes in dependencies or in code of several different scripts
[Rewrite] - Changes in singular script
[Major Feature] - Entirely new feature requiring a new large script and possibly new cog
[Feature] - A small new feature
[Fix] - A small bug fix
```
**DO NOT COMMIT CHANGES CONTAINING MAJOR BUGS!**
