Official discord bot of WEITI Telekomunikacja 2020/2021-Z

The code uses python, with heavy dependance on discord.py library.
To quickstart, look at the cogs/ directory to find examples of code.

It is recomended to familiarize yourself with:
async def function() - These functions can be used simultanously. Always end with <await> <some_code>.
cogs - modules containing one class with several command functions
commands - to create one, go to the cogs/ directory and create a .py script containing one class and cog syntax.

Minimal cog example: (creates one function, that is automaticaly called when bot is going online, and the other when user types in chat <!ping>)
<
from discord.ext import commands


class SomeCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.some_variable = 3

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(SomeCog(client))

>

main libraries and iside modules used:

import discord
from discord.ext import commands
import os
import json
import random

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

To add links go to 'resources' Main bot script is cibot.py. Keep it tidy!
In config.py save data such as relative paths, server settings, etc.
In 'cogs' directory add your modules (class structure is preffered).
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
8. Rewrite or format documentation - this one sucks!
