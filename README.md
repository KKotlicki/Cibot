# Cibot

## Description

This repository contains a code of discord bot for college utilities;
The code is universal and cross-platform compatible **(not tested on macOS)** with a few extra features on Raspberry Pi 4;
The code is ready to be used as your own bot and no script changes need to be applied.

## Setup

Bot uses exclusively python, with heavy dependence on [discord.py](https://discordpy.readthedocs.io/en/latest/api.html) library.


### Installing

The bot uses [Python (3.7+)](https://www.python.org/) and [git](https://git-scm.com/) dependencies installed on your system.

To install, follow the steps below:

1. Download the [latest release](https://github.com/KKotlicki/Cibot/releases/latest) of Cibot

2. (optional) install and add to the system's `path` enviroment variables the following modules:
    - If you are running server on Debian or derived system (eg. Ubuntu, Raspbian), first install pip using `sudo apt-get install python3-pip`.
    - To use youtube commands, install [ffmpeg](https://www.ffmpeg.org/) video converter.
    - If you are running bot on Windows, to use chess commands, install [gtk3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer).
    - Otherwise, remove `yt_cog.py` or `chess_cog.py` from `cogs/` directory.

3. To install all the python libraries and modules, run `pip install -r /path/to/Cibot/requirements.txt` in terminal. 

### Bot setup

**Once you run cibot.py, you will be asked to provide Token (a special id of the discord bot) and OS python 3 command (usually python3, python or py)**

To obtain Bot Token, go to your [bot's site](discord.com/developers/applications/), choose your bot or create a new one (remember to provide admin permission).

Next go to Bot section and under "TOKEN" click button "Copy".

#### Google drive setup (optional)

To use `drive_cog.py` commands for uploading files to cloud, you need to create a [google application with access to drive api](https://developers.google.com/drive/api/v3/quickstart/python). (Choose application type "desktop application")
Once you get the `credentials.json` file, place it in main directory. 
If you've already received a `token.json` for your google aplication, place it in main directory too - otherwise bot will open authentication page in browser and create the token once authentication was completed.

**Warning!** - if system doesn't have a browser (for example any OS without GUI), you may need to first run the bot on system which does to generate `token.json` in bot's main directory, then copy the token file to the selected machine's main Cibot directory.

If you want to use drive file upload command, you need to create a `drive_ids.json` file in `servers/` directory containing the drive folder ids as `values` and the aliases for them as `keys` to use, when using Cibot to upload file to specific drive folder.

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

Every current command is described in res/help.json and res/adm_help.json

**Notice**:	Commits that do not keep to the structure will not be accepted.


### cibot.py

The main bot script:

 - generates personal environment file (first time use only)
 - generates drive token file (if drive credentials.json exists)
 - connects to bot's discord API
 - loads the cogs from directory

Main script should not define any other commands;
Keep this code as clean and minimal as possible.


### module_name_cog.py

The most important element of the bot.
Every cog file is an independent module containing one class in special syntax with several closely related methods.
They dictate bot's behavior, although bot should be able to work with or without any of them.
To add new commands or functionalities, create a cog or add to existing cog.


#### cog syntax

For reference, look at the cogs/ directory to find examples of a code.
Here is one that defines three methods:
 - on_ready() is being automatically called when bot is going online
 - ping() when user types in chat <!ping>
 - dice() when user types in chat <!dice>

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


**Development Rules:**
1.  adhere to PEP 8 standard
2.  do not create subfolders or add any non-cog files in `cogs/`
3.  if you want to create directory for new features, do so in the main directory
4.  unless you have a good reason, do not change `cibot.py` script
5.  make sure to test your code before uploading
6.  remember not to break asynchronicity
7.  for every new library or module you add, update `requirements.txt` with them
8.  for every new command you add, update help.json or adm_help.json respectively.
9.  do not duplicate function names, command aliases, or features
10.  do not duplicate function names, command aliases, or features

Main bot script is cibot.py. Keep it tidy!
In config.py save user specific data such as relative paths, server settings, etc.
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
2. yt_cog change $play to pre-bufforing (downloading, then streaming) by default, but leave direct streaming if query result is stream
3. Finish documentation
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
