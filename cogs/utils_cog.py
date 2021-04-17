import discord
from datetime import datetime
from discord.ext import commands, tasks
from helpers import fetch_sv_data, remove_data
from loguru import logger
from config import LOGS_PATH, RES_PATH, SV_PATH
import os
import wikipedia
import asyncio
from urllib.request import urlopen
from urllib.error import URLError
from dotenv import load_dotenv
from platform import system
import json
load_dotenv()


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_channel = ""

    @commands.Cog.listener()
    async def on_ready(self):
        self.connection_timeout.start()
        with open(f'{RES_PATH}/status.json', encoding='utf-8') as rd:
            statuses = json.loads(rd.read())
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(statuses['active']))
        logger.success(f"Logged in as {self.bot.user}")
        logger.add(f'{LOGS_PATH}/errors.log', level="ERROR", rotation="500 MB")
        logger.add(f'{LOGS_PATH}/history.log', level="SUCCESS", rotation="500 MB")
        await asyncio.sleep(60)
        self.automatic_update.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await fetch_sv_data(guild)
        logger.success(f"Joined *{guild.name}* guild")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        remove_data(guild)
        logger.success(f"Removed from *{guild.name}* guild")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            logger.error("Invalid command used.")
            await ctx.send("Nie znam tej komendy.")
        elif isinstance(err, commands.MissingPermissions):
            logger.error("Permission warning.")
            await ctx.send("Komenda tylko dla adminów.")
        elif isinstance(err, commands.BotMissingPermissions):
            logger.error("Bot permission warning.")
            await ctx.send("Nie mam odpowiednich uprawnień.")
        elif isinstance(err, commands.MissingRequiredArgument):
            logger.error("Missing required argument.")
            await ctx.send("Komenda wymaga argumentu.")
        elif isinstance(err, commands.CommandOnCooldown):
            logger.error("Cooldown warning")
            await ctx.send("Za szybko używasz komend.")
        elif not isinstance(err, wikipedia.DisambiguationError):
            logger.error(err)


    @tasks.loop(minutes=2.0)
    async def connection_timeout(self):
        try:
            urlopen('http://216.58.192.142', timeout=20)
        except URLError:
            logger.error("Disconnected")
            logger.add(f'{LOGS_PATH}/errors.log', rotation="10 MB")
            os.system(f'cd utils\n{os.getenv("OS_PYTHON_PREFIX")} server_down.py\n')
            print('shutting down')
            await self.bot.close()

    @tasks.loop(minutes=1.0)
    async def automatic_update(self):
        now = datetime.now()
        if now.hour == 4:
            if not now.minute:
                ''':)'''
                await self.bot.change_presence(status=discord.Status.dnd,
                                               activity=discord.Game("follow the white rabbit 🐇"))
            if now.minute == 20:
                await self.update_fun()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def update(self, ctx):
        await ctx.channel.purge(limit=1)
        await self.update_fun()

    async def update_fun(self):
        with open(f'{RES_PATH}/status.json', encoding='utf-8') as rd:
            statuses = json.loads(rd.read())
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(statuses['update']))

        py_prefix = os.getenv("OS_PYTHON_PREFIX")
        os_system = system()
        print("updating...")
        if os_system == 'Windows':
            # with open(f'{res_dir}/update_ms.txt', 'r') as rd:
            #     updater = rd.read().replace('<python>', py_prefix).replace('<path>', os.getcwd())
            with open(os.getcwd() + '/update.bat', 'w') as wr:
                wr.write(f'Taskkill /IM \"python.exe\" /F\ngit pull\ncd {os.getcwd()}\n{py_prefix} cibot.py\n')
            os.system('update.bat')

        elif os_system == 'Linux':
            os.system(f"sudo pkill '{py_prefix} cibot.py'\ngit pull\n{py_prefix} cibot.py\n")


def setup(bot):
    bot.add_cog(UtilityCog(bot))
