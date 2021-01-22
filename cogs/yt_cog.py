import discord
import youtube_dl
from discord.ext import commands
from helpers import YTDLSource
from youtubesearchpython import VideosSearch
from loguru import logger
from config import dump_dir
import os

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # @commands.command()
    # async def load(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def qp(self, ctx, *, title):
        """Plays from a url (almost anything youtube_dl supports)"""

        for fname in os.listdir('.'):
            if fname.endswith('.webm'):
                os.remove(fname)
                break
        logger.info("\n<" + str(ctx.author) + "> said:\n<" + title + ">")
        logger.add(f'{dump_dir}/yt_history.log', rotation="5 MB")
        url = VideosSearch(str(title), limit=1).result()['result'][0]['link']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def p(self, ctx, *, title):
        """Streams from a url (same as yt, but doesn't predownload)"""

        logger.info("\n<" + str(ctx.author) + "> said:\n<" + title + ">")
        logger.add(f'{dump_dir}/yt_history.log', rotation="5 MB")
        url = VideosSearch(str(title), limit=1).result()['result'][0]['link']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Teraz gram: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Nie jesteś podłączony do kanału głosowego.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Zmieniłem głośność na {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('infiltruje discorda'))

    # @load.before_invoke
    @qp.before_invoke
    @p.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await self.bot.change_presence(
                    status=discord.Status.online, activity=discord.Game('podsłuchuje studentów'))
            else:
                await ctx.send("Nie jesteś podłączony do kanału głosowego.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))
