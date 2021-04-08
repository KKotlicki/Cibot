import discord
import json
import os
from discord.ext import commands
from config import res_dir, sv_dir, prefix
from helpers import fetch_sv_data, open_help, set_sv_config, get_valid_text_channel_id, get_text_channel_id_from_name


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["adm_help", "admin_help"])
    @commands.has_permissions(administrator=True)
    async def adm(self, ctx):
        await ctx.channel.purge(limit=1)
        await open_help(ctx, "adm_help")

    @commands.command(aliases=['exit'])
    @commands.has_permissions(administrator=True)
    async def shutdown(self):
        await self.bot.close()

    @commands.command(pass_context=True, aliases=["c"])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command(pass_context=True, aliases=["save"])
    @commands.has_permissions(administrator=True)
    async def sv(self, ctx):
        await ctx.channel.purge(limit=1)
        await fetch_sv_data(ctx)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_answ(self, ctx, *, message=''):
        if message == '':
            message = ctx.guild.name
        await ctx.channel.purge(limit=1)
        await set_sv_config(ctx, message, 'answ')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_game(self, ctx, *, message=''):
        if message == '':
            message = ctx.guild.name
        await ctx.channel.purge(limit=1)
        await set_sv_config(ctx, message, 'game')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, *, message=''):
        if message == '':
            message = ctx.guild.name
        await ctx.channel.purge(limit=1)
        await set_sv_config(ctx, message, 'role')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        channel_id = get_valid_text_channel_id(ctx, 'answ')
        channel = self.bot.get_channel(channel_id)
        embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
        await channel.send(embed=embed_var)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx):
        await ctx.channel.purge(limit=1)
        with open(f'{res_dir}/roles.json', encoding='utf-8') as rd:
            help_json = json.loads(rd.read())
        roles_list = ""
        for key, value in help_json.items():
            roles_list += f"\n\n{value}: {key}"
        message = await ctx.send(f"**Wybór Roli: Grupy**\nZareaguj aby wybrać grupę:{roles_list}")
        for key, value in help_json.items():
            await message.add_reaction(value)

    @commands.Cog.listener()
    async def on_ready(self):
        for file in os.listdir(f"{sv_dir}/"):
            if file.endswith("_config.json"):
                with open(f'{sv_dir}/{file}', encoding='utf-8') as rd:
                    channels_dict = json.loads(rd.read())
                if 'role' in channels_dict:
                    message_channel = channels_dict['role']
                    try:
                        channel_id = get_text_channel_id_from_name(file[:-12], message_channel)
                        channel = self.bot.get_channel(channel_id)
                        with open(f'{res_dir}/roles.json', encoding='utf-8') as rd:
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
                              f'On all servers using qutomatic roles type in {prefix}sv and set role channel again.\n'
                              f'Make sure not to misspell the name of the role channel.')
                        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            channels_list = []
            for file in os.listdir(f"{sv_dir}/"):
                if file.endswith("_config.json"):
                    with open(f'{sv_dir}/{file}', encoding='utf-8') as rd:
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
                                  f'{prefix}sv and set role channel again.\n'
                                  f'Make sure not to misspell the name of the role channel.')
                            pass
            with open(f'{res_dir}/roles.json', encoding='utf-8') as rd:
                roles_json = json.loads(rd.read())
            for key, value in roles_json.items():
                if reaction.message.channel.id in channels_list and reaction.emoji == value:
                    try:
                        role = discord.utils.get(reaction.message.guild.roles, name=key)
                        await user.add_roles(role)
                    except AttributeError:
                        print("Server doesn't have this role configured.")
                    return


def setup(bot):
    bot.add_cog(AdminCog(bot))
