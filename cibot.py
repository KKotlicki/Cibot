from discord.ext import commands
from dotenv import load_dotenv
import os.path
from config import prefix, cogs_dir, rasp_dir
from helpers import env_config


if not os.path.exists('.env'):
    env_config()
load_dotenv()
bot = commands.Bot(command_prefix=prefix)


if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{cogs_dir}.{filename[:-3]}')
    if os.getenv("RASPBERRY_PI") == "Y":
        bot.load_extension(f'{rasp_dir}.raspberry_cog')


bot.run(os.getenv("TOKEN"))
