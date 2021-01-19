from discord.ext import commands
from dotenv import load_dotenv
import os
from config import *
load_dotenv()


bot = commands.Bot(command_prefix=prefix)
if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{cogs_dir}.{filename[:-3]}')

bot.run(os.getenv("DSC_BOT_KEY"))
