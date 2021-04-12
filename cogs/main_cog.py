import discord
from discord.ext import commands
from helpers import open_help, get_text_channel_id_from_name
from config import RES_PATH, LOGS_PATH, SV_PATH, PREFIX
import json
import os
from loguru import logger


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title=":evergreen_tree: Contributed to Cibot:", description="https://github.com"
                                                                                              "/KKotlicki/Cibot",
                                  color=0xff770f)
        with open(f'{RES_PATH}/credits.json', encoding='utf-8') as rd:
            link_dict = json.loads(rd.read())
        for name, cont in link_dict.items():
            embed_var.add_field(name=f'**{name}**', value=cont, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        await open_help(ctx, "help")

    @commands.command()
    async def bug(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        logger.info("\n<" + str(ctx.author) + "> said:\n<" + message + ">")
        logger.add(f'{LOGS_PATH}/bugs.log', rotation="5 MB")

    '''Role assignment'''
    @commands.Cog.listener()
    async def on_ready(self):
        for file in os.listdir(f"{SV_PATH}/"):
            if file.endswith("_config.json"):
                with open(f'{SV_PATH}/{file}', encoding='utf-8') as rd:
                    channels_dict = json.loads(rd.read())
                if 'role' in channels_dict:
                    message_channel = channels_dict['role']
                    try:
                        channel_id = get_text_channel_id_from_name(file[:-12], message_channel)
                        channel = self.bot.get_channel(channel_id)
                        await channel.purge(limit=1)
                        with open(f'{RES_PATH}/roles.json', encoding='utf-8') as rd:
                            role_json = json.loads(rd.read())
                        roles_list = ""
                        for key, value in role_json.items():
                            roles_list += f"\n\n{value}: {key}"
                        text = f"**Wybór Roli: Grupy**\nZareaguj aby wybrać grupę:{roles_list}"
                        message = await channel.send(text)
                        for key, value in role_json.items():
                            await message.add_reaction(value)
                    except:
                        print(f'No saved data or wrong data about server\'s text channels.\n'
                              f'On all servers using qutomatic roles type in {PREFIX}sv and set role channel again.\n'
                              f'Make sure not to misspell the name of the role channel.')
                        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        if not member.bot:
            channels_list = []
            for file in os.listdir(f"{SV_PATH}/"):
                if file.endswith("_config.json"):
                    with open(f'{SV_PATH}/{file}', encoding='utf-8') as rd:
                        channels_dict = json.loads(rd.read())
                    if 'role' in channels_dict:
                        message_channel = channels_dict['role']
                        try:
                            channel_id = get_text_channel_id_from_name(file[:-12], message_channel)
                            channel = self.bot.get_channel(channel_id)
                            channels_list.append(channel.id)
                        except:
                            print(f'No saved data or wrong data about server\'s text channels.\n'
                                  f'On all servers using qutomatic roles type in '
                                  f'{PREFIX}sv and set role channel again.\n'
                                  f'Make sure not to misspell the name of the role channel.')
                            pass
            with open(f'{RES_PATH}/roles.json', encoding='utf-8') as rd:
                roles_json = json.loads(rd.read())
            role = ''
            for key, value in roles_json.items():
                if reaction.message.channel.id in channels_list and reaction.emoji == value:
                    try:
                        role = discord.utils.get(reaction.message.guild.roles, name=key)
                        if role in member.roles:
                            await member.remove_roles(role)
                        else:
                            await member.add_roles(role)
                    except AttributeError:
                        print("Server doesn't have this role configured.")
                    break



def setup(bot):
    bot.add_cog(MainCog(bot))
