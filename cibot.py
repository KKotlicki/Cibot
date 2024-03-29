from discord.ext import commands
from dotenv import load_dotenv
import os.path
from config import PREFIX, COGS_PATH, RPI_PATH
from helpers import env_config
from utils.drive_oauth import build_oauth_service


if not os.path.exists('.env'):
    env_config()
load_dotenv()

is_drive = None
if os.path.exists('credentials.json'):
    is_drive = build_oauth_service()

bot = commands.Bot(command_prefix=PREFIX)


if __name__ == '__main__':

    for filename in os.listdir(f'{COGS_PATH}'):
        if filename.endswith('.py'):
            if is_drive or filename != 'drive_cog.py':
                bot.load_extension(f'{COGS_PATH}.{filename[:-3]}')

    if os.getenv("RASPBERRY_PI") == "Y":
        bot.load_extension(f'{RPI_PATH}.raspberry_cog')


bot.run(os.getenv("TOKEN"))
