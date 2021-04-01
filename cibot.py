import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import os.path
from config import *
from helpers import env_config
from platform import system
import json


if not os.path.exists('.env'):
    env_config()
load_dotenv()


bot = commands.Bot(command_prefix=prefix)


@bot.command()
@commands.has_permissions(administrator=True)
async def update(ctx):
    with open(f'{res_dir}/status.json', encoding='utf-8') as rd:
        statuses = json.loads(rd.read())
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(statuses['update']))

    py_prefix = os.getenv("OS_PYTHON_PREFIX")
    os_system = system()

    if os_system == 'Windows':
        with open(f'{res_dir}/update_ms.txt', 'r') as rd:
            updater = rd.read().replace('<python>', py_prefix).replace('<path>', os.getcwd())
        with open(os.getcwd()+'/update.bat', 'w') as wr:
            wr.write(updater)
        os.system('update.bat')

    elif os_system == 'Linux':
        os.system(f"sudo pkill '{py_prefix} cibot.py'\ngit pull\n{py_prefix} cibot.py\n")


if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{cogs_dir}.{filename[:-3]}')
    if os.getenv("RASPBERRY_PI") == "Y":
        bot.load_extension(f'{rasp_dir}.raspberry_cog')


bot.run(os.getenv("TOKEN"))
