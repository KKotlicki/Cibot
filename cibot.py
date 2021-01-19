from discord.ext import commands
from dotenv import load_dotenv
import os
from config import *
load_dotenv()


client = commands.Bot(command_prefix=prefix)
if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            client.load_extension(f'{cogs_dir}.{filename[:-3]}')
    

client.run(os.getenv("DSC_BOT_KEY"))
