import discord
from discord.ext import commands
from helpers import get_text_channel_id_from_name, set_sv_config
from config import SV_PATH
import json
import os
from loguru import logger


class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.send_reaction_role_message()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        if not member.bot:
            if os.path.isfile(f'{SV_PATH}/{member.guild.name+"_config.json"}'):
                with open(f'{SV_PATH}/{member.guild.name+"_config.json"}', encoding='utf-8') as rd:
                    sv_config = json.loads(rd.read())
                if 'role' in sv_config and 'roles_dict' in sv_config:
                    message_channel = sv_config['role']
                    channel_id = get_text_channel_id_from_name(member.guild.name, message_channel)
                    roles_dict = sv_config['roles_dict']
                    for key, value in roles_dict.items():
                        if reaction.message.channel.id == channel_id and reaction.emoji == value:
                            try:
                                role = discord.utils.get(reaction.message.guild.roles, name=key)
                                if role in member.roles:
                                    await member.remove_roles(role)
                                else:
                                    await member.add_roles(role)
                            except AttributeError:
                                print("Role doesn't exist on this server.")
                            break

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(pass_context=True, aliases=['set_roles'])
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, *, message=''):
        if message == '':
            message = ctx.channel.name
        try:
            get_text_channel_id_from_name(ctx.guild.name, message)
        except KeyError:
            await ctx.send("Nie znam takiego kanału.")
        else:
            await ctx.channel.purge(limit=1)
            await set_sv_config(ctx, message, 'role')
            logger.success(f"@{ctx.author.name} in {ctx.guild.name} set role channel to #{message}")
            await ctx.send(f"✅ Kanał na role ustawiony na #{message}")
            await self.send_reaction_role_message()

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(pass_context=True, aliases=['add_roles'])
    @commands.has_permissions(administrator=True)
    async def add_role(self, ctx, role, reaction):
        await ctx.channel.purge(limit=1)
        roles_list = []
        for active_guild_role in ctx.guild.roles:
            roles_list.append(active_guild_role.name)
        if role not in roles_list:
            await ctx.guild.create_role(name=role)
        await set_sv_config(ctx, {role: reaction}, 'roles_dict')
        await ctx.send(f"Dodałem *{role}* jako rolę do wyboru")
        await self.send_reaction_role_message()
        logger.success(f"@{ctx.author.name} in *{ctx.guild.name}* added {role} role.")

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(pass_context=True, aliases=['remove_role', 'del_role', 'delete_role', 'rmv_role'])
    @commands.has_permissions(administrator=True)
    async def rem_role(self, ctx, role):
        await ctx.channel.purge(limit=1)
        if os.path.exists(f'{SV_PATH}/{ctx.message.guild.name}_config.json'):
            with open(f'{SV_PATH}/{ctx.message.guild.name}_config.json', 'r', encoding='utf-8') as r:
                sv_config = json.loads(r.read())
            if 'roles_dict' in sv_config:
                try:
                    del sv_config['roles_dict'][role]
                except KeyError:
                    pass
                else:
                    if not sv_config['roles_dict']:
                        del sv_config['roles_dict']
                    with open(f'{SV_PATH}/{ctx.message.guild.name}_config.json', 'w') as wr:
                        wr.write(json.dumps(sv_config))
                    await ctx.send(f"Usunąłem *{role}* z roli do wyboru")
                    await self.send_reaction_role_message()
                    logger.success(f"@{ctx.author.name} in *{ctx.guild.name}* removed {role} role.")

    async def send_reaction_role_message(self):
        for file in os.listdir(f"{SV_PATH}/"):
            if file.endswith("_config.json"):
                with open(f'{SV_PATH}/{file}', encoding='utf-8') as rd:
                    sv_config = json.loads(rd.read())
                if 'role' in sv_config and 'roles_dict' in sv_config:
                    message_channel = sv_config['role']
                    channel_id = get_text_channel_id_from_name(file[:-12], message_channel)
                    channel = self.bot.get_channel(channel_id)
                    await channel.purge(limit=1)
                    roles_dict = sv_config['roles_dict']
                    roles_list = ""
                    for key, value in roles_dict.items():
                        roles_list += f"\n\n{value}: {key}"
                    text = f"**Wybór Roli:**\n*Zareaguj aby wybrać grupę*{roles_list}"
                    message = await channel.send(text)
                    for key, value in roles_dict.items():
                        await message.add_reaction(value)


def setup(bot):
    bot.add_cog(RoleCog(bot))
