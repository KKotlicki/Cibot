from discord.ext import commands
from dotenv import load_dotenv
import os
from config import *
from platform import system

load_dotenv()

bot = commands.Bot(command_prefix=prefix)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def update(ctx):
    updater='./updater_linux.sh'
    if system()=='Windows':
        updater='updater_windows.bat'
    os.system(updater)


if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{cogs_dir}.{filename[:-3]}')

bot.run(os.getenv("DSC_BOT_KEY"))
