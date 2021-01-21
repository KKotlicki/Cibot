from discord.ext import commands
import discord
import youtube_dl
import os
from config import *


class YtLinkAudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        channel = str(ctx.author.voice.channel)
        if channel is None:
            await ctx.send(":slight_frown: Nie jesteś w kanale głosowym")
        elif 'list=' in url:
            await ctx.send(":slight_frown: Nie można odtwarzać playlist")
        else:
            song_there = os.path.isfile(f"{dump_dir}/{temp_mp3_name}")
            try:
                if song_there:
                    os.remove(f"{dump_dir}/{temp_mp3_name}")
            except PermissionError:
                await ctx.send(
                    ":slight_frown: Zaczekaj aż skończy się aktualny utwór, lub zakończ go komendą \"stop\".")
                return
            await ctx.send(":satellite: Buforuję...")
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('podłsuchuje telekomune'))
            await self.download_and_play_video(ctx, channel, url)

    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('infiltruje discorda'))
        else:
            await ctx.send(":slight_frown: Nie jestem podłączony do kanału głosowego.")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send(":slight_frown: Na ten moment nie gra żadne audio.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send(":slight_frown: Na ten moment nie gra żadne audio.")

    async def download_and_play_video(self, ctx, channel, url):
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
        await voice_channel.connect()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir(f"./"):
            if file.endswith(".mp3"):
                os.rename(file, temp_mp3_name)
        os.replace(temp_mp3_name, f"{dump_dir}/{temp_mp3_name}")
        print(discord.utils.get(self.bot.voice_clients, guild=ctx.guild))
        print(str(discord.utils.get(self.bot.voice_clients, guild=ctx.guild)))
        voice.play(discord.FFmpegPCMAudio(f"{dump_dir}/{temp_mp3_name}"))


def setup(bot):
    bot.add_cog(YtLinkAudioCog(bot))
