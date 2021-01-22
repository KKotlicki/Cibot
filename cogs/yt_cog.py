import discord
import youtube_dl
# from youtube_search import YoutubeSearch
from discord.ext import commands
from helpers import YTDLSource

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

    # @commands.command()
    # async def yt(self, ctx, *, url):
    #     """Plays from a url (almost anything youtube_dl supports)"""
    #
    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #         ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def p(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

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

    # @load.before_invoke
    # @yt.before_invoke
    @p.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Nie jesteś podłączony do kanału głosowego.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))



# try:
#     yt_id = str(json.loads(YoutubeSearch(search, max_results=1).to_json())['videos'][0]['id'])
#     yt_url = 'https://www.youtube.com/watch?v='+yt_id
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([yt_url])
#         info = ydl.extract_info(yt_url)
#         songname = info.get('title', None) + "-" + yt_id + ".mp3"
#         if os.path.isfile(songname):
#             print("Song Downloaded: " + songname)
#         else:
#             print("Error: " + songname)
# except:
#     pass
#     print(traceback.print_exc())
#     print("no results")