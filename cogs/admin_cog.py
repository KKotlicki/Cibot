import discord
from discord.ext import commands
from loguru import logger
from helpers import fetch_sv_data, open_help, set_sv_config, get_valid_text_channel_id, get_text_channel_id_from_name


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["adm_help", "admin_help"])
    @commands.has_permissions(administrator=True)
    async def adm(self, ctx):
        await ctx.channel.purge(limit=1)
        await open_help(ctx, "adm_help")

    @commands.command(pass_context=True, aliases=['exit'])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        logger.info(f"@{ctx.author.name} closed the process.")
        await self.bot.close()

    @commands.command(pass_context=True, aliases=["c"])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        logger.info(f"@{ctx.author.name} cleared {amount} messages")

    @commands.command(pass_context=True, aliases=["save"])
    @commands.has_permissions(administrator=True)
    async def sv(self, ctx):
        await ctx.channel.purge(limit=1)
        await fetch_sv_data(ctx)
        logger.info(f"@{ctx.author.name} in {ctx.guild.name} saved server data")

    @commands.command(pass_context=True, aliases=['set_answer', 'set_ans'])
    @commands.has_permissions(administrator=True)
    async def set_answ(self, ctx, *, message=''):
        if message == '':
            message = ctx.channel.name
        try:
            get_text_channel_id_from_name(ctx.guild.name, message)
        except KeyError:
            await ctx.send("Nie znam takiego kanału.")
        else:
            await ctx.channel.purge(limit=1)
            await set_sv_config(ctx, message, 'answ')
            logger.info(f"@{ctx.author.name} in {ctx.guild.name} set answer channel to #{message}")
            await ctx.send(f"✅ Kanał na ogłoszenia ustawiony na #{message}")

    @commands.command(pass_context=True, aliases=['set_games'])
    @commands.has_permissions(administrator=True)
    async def set_game(self, ctx, *, message=''):
        if message == '':
            message = ctx.channel.name
        try:
            get_text_channel_id_from_name(ctx.guild.name, message)
        except KeyError:
            await ctx.send("Nie znam takiego kanału.")
        else:
            await ctx.channel.purge(limit=1)
            await set_sv_config(ctx, message, 'game')
            logger.info(f"@{ctx.author.name} in {ctx.guild.name} set game channel to #{message}")
            await ctx.send(f"✅ Kanał na gry ustawiony na #{message}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        channel_id = get_valid_text_channel_id(ctx, 'answ')
        channel = self.bot.get_channel(channel_id)
        embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
        await channel.send(embed=embed_var)
        logger.info(f"@{ctx.author.name} in {ctx.guild.name} used bot to speak")


def setup(bot):
    bot.add_cog(AdminCog(bot))
