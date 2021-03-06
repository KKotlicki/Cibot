# Cibot

## Description

This repository contains a code of discord bot for college utilities;
The code is universal and cross-platform compatible **(not tested on macOS!)** with a few extra features on Raspberry Pi 4;
The code is ready to be used as your own bot and no changes need to be applied (more on that in MANUAL.txt)


## Setup

Bot uses exclusively python, with heavy dependence on [discord.py](https://discordpy.readthedocs.io/en/latest/api.html) library.


### Installing

The bot uses [Python (3.7+)](https://www.python.org/) and [git](https://git-scm.com/) dependencies installed on your system.

To install, follow the steps below:

1. Download the [latest release](https://github.com/KKotlicki/Cibot/releases/latest) of Cibot

2. (optional) install and add to the system's `path` enviroment variables the following modules:
    - If you're running server on Debian or derived system (eg. Ubuntu, Raspbian), first install pip using `sudo apt-get install python3-pip`.
    - To use youtube commands, install [ffmpeg](https://www.ffmpeg.org/) video converter.
    - To use chess commands, install [gtk3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) runtime.
    - Otherwise, remove `yt_cog.py` or `chess_cog.py` from `cogs/` directory.

3. To install all the python libraries and modules, run `pip install -r /path/to/Cibot/requirements.txt` in terminal. 
    (replace `/path/to/` with path of Cibot)

    **WARNING!** - make sure `python` is the alias for python version 3, not 2. To check the version of the python used, type in `python -V`. If you have both version 2 and 3 installed on your s, replace all `python` in code below with appropriate command. 


### Bot setup

**Once you run cibot.py, you will be asked to provide Token (a special id of the discord bot) and OS python 3 command (usually python3, python or py - you can check which one is it by running it in cmd)**

#### Google drive setup (optional)

To use `drive_cog.py` commands for uploading files to cloud, you need to [create a google application with access to drive api.](https://developers.google.com/drive/api/v3/quickstart/python) (Remember when choosing application type to select "desktop application")
Once you get the `credentials.json` file, place it in main directory. 
If you've already received a `token.json` for your google aplication, place it in main directory too - otherwise bot will open authentication page in browser and create the token once confirmed.

**Warning!** - if system doesn't have a browser (for example `raspbian lite` or any other os without GUI), you may need to first run the bot on system which does to generate `token.json` in bot's main directory, then copy the token file to the selected machine's main Cibot directory.

On top of that, you need to create a `drive_ids.json` file in `servers/` directory containing the drive folder ids as `values` and the aliases for them as `keys` to use, when using Cibot to upload file to specific drive folder.

Example `drive_ids.json` file:

```
{
    "1": "1biD376aaPsDlDZjyg99SBzOXf5Jg8bV-",
    "Directory 2": "1jjsCQ2ds0I8Eu-w1wcf1d2f76QrO3lsW",
    "Music": "43VyiOx5-kGddrzWrIDvg6M-OCN7DLbdv"
}
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
|- roles            # roles for reaction role assignment function
|- status           # custom status descriptions of bot
|- subject_aliases  # alternative call names for <"unofficial" links> command
servers/            # server's data and logs
temp/               # temporary and cached bot files
utils/              # utility scripts
.gitattributes      # Git repo configuration
.gitignore          # ^
cibot.py            # ! - the main bot script
config.py           # bot settings
helpers.py          # custom methods list
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

To commit changes to the main branch and publish your contribution, log in your GitHub account, and send a branch pull request.
Every current command is described in res/help.json and res/adm_help.json


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
import random                              # the library used by "dice" example method


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


**Development Rules:**
1.  name variables by PEP 8 standard
2.  do not create subfolders or add any non-cog files in `cogs/`
3.  if you want to create directory for new features, do so in the main directory
4.  unless you have a good reason, do not change `cibot.py` script
5.  make sure to test your code before uploading
6. remember not to break asynchronicity
7. for every new library or module you add, update `requirements.txt` with them
7. do not duplicate function names, command aliases, or features
8. do not duplicate function names, command aliases, or features

Main bot script is cibot.py. Keep it tidy!
In config.py save data such as relative paths, server settings, etc.
In helpers.py add your local methods.



**ToDo:**

 - **[Major Rewrite]**

```
1. Specific commands' error and exception handling, send info on required arguments on command misuse
2. chess_cog - one board at a time
3. change database from json based to sql
```

 - [Rewrite]

```
1. yt_cog - save queue, load queue, additional queue handling
2. yt_cog change music to pre-bufforing
3. Finish documentation and setup manual
4. chess_cog - takeback offer
5. move chess_cog temporary files location from main to temp/
```

 - **[Major Feature]**

```
1. AI chatbot
2. Unit test script
3. Shogi
```

 - [Feature]

```
1. Calendar of exams
2. Countdown to final exams
3. Send documents (such as subject statues, MUT anthem, magnet links)
4. Points to grade converter by subject
5. Akinator
```

 - [Fix]

```
1. Logging systems
2. Shutdown commands
```


[Major Rewrite] - Changes in dependencies or in code of several different scripts

[Rewrite] - Changes in singular script

[Major Feature] - Entirely new feature requiring a new large script and possibly new cog

[Feature] - A small new feature

[Fix] - A small bug fix

**DO NOT COMMIT CHANGES CONTAINING MAJOR BUGS!**
