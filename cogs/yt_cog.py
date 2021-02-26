import discord
import youtube_dl
from discord.ext import commands
from helpers import YTDLSource
from youtubesearchpython import VideosSearch
from config import res_dir
import json
import asyncio

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue_size = 0
        self.queue_list = []
        self.skip_song = False

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # @commands.command()
    # async def local(self, ctx, *, query):
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send(f'Now playing: {query}')

    # @commands.command()
    # async def qp(self, ctx, *, title):
    #
    #     for fname in os.listdir('.'):
    #         if fname.endswith('.webm') or fname.endswith('.zip'):
    #             os.remove(fname)
    #
    #     url = VideosSearch(str(title), limit=1).result()['result'][0]['link']
    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #         ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send(f'Now playing: {player.title}')

    @commands.command(aliases=['p', 'graj'])
    async def play(self, ctx, *, title):

        video_data = VideosSearch(str(title), limit=1).result()['result'][0]
        async with ctx.typing():
            url = video_data['link']
            song_title = video_data['title']
            song_duration = video_data['duration']
            self.queue_list.append([url, song_title])
            self.queue_size = len(self.queue_list)
        embed = discord.Embed(title=f":notes: Dodałem do kolejki:  {song_title}",
                              description=f"Długość:  {song_duration} minut",
                              color=discord.Color.dark_green())
        await ctx.send(embed=embed)
        if not ctx.voice_client.is_playing() and self.queue_size == 1:
            await self.play_yt(ctx)

    @commands.command()
    async def volume(self, ctx, volume: int):

        if ctx.voice_client is None:
            return await ctx.send("Nie jesteś podłączony do kanału głosowego.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Zmieniłem głośność na {}%".format(volume))

    @commands.command(aliases=['qc', 'clear_queue'])
    async def qclear(self, ctx):

        await ctx.voice_client.disconnect()
        with open(f'{res_dir}/status.json', encoding='utf-8') as rd:
            statuses = json.loads(rd.read())
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(statuses['active']))
        self.queue_list = []

    # @load.before_invoke
    # @qp.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                with open(f'{res_dir}/status.json', encoding='utf-8') as rd:
                    statuses = json.loads(rd.read())
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(statuses['voice']))
            else:
                await ctx.send("Nie jesteś podłączony do kanału głosowego.")
                raise commands.CommandError("Author not connected to a voice channel.")

    @commands.command()
    async def play_yt(self, ctx):
        if not ctx.voice_client.is_playing() and len(self.queue_list) != 0:
            player = await YTDLSource.from_url(self.queue_list[0][1], loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            while True:
                if ctx.voice_client.is_playing() is False:
                    break
                elif self.skip_song is True:
                    self.skip_song = False
                    break
                await asyncio.sleep(2)
            ctx.voice_client.stop()
            self.queue_list.pop(0)
            await self.play_yt(ctx)
        elif not ctx.voice_client.is_playing() and len(self.queue_list) == 0:
            ctx.voice_client.stop()
            self.bot.loop.create_task(self.voice_out_timer(ctx))

    @commands.command(aliases=['q', 'kolejka'])
    async def queue(self, ctx):
        embed_var = discord.Embed(title=":roll_of_paper: Kolejka:", color=0xff770f)
        for song in self.queue_list:
            if self.queue_list.index(song) == 0:
                embed_var.add_field(name=f':notes: Teraz gra:', value=f'**{song[1]}**', inline=False)
            else:
                embed_var.add_field(name=f'nr. {self.queue_list.index(song)}:', value=f'**{song[1]}**', inline=False)
        await ctx.send(embed=embed_var)

    @commands.command(aliases=['s', 'kurwaskipu'])
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Nic teraz nie gra.")
        elif ctx.voice_client.is_playing() is False:
            await ctx.send("Nic teraz nie gra.")
        else:
            self.skip_song = True

    async def voice_out_timer(self, ctx):
        time = 0
        while time < 60:
            if ctx.voice_client.is_playing():
                return
            await asyncio.sleep(5)
            time += 1
        await ctx.voice_client.disconnect()
        with open(f'{res_dir}/status.json', encoding='utf-8') as rd:
            statuses = json.loads(rd.read())
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(statuses['active']))


def setup(bot):
    bot.add_cog(Music(bot))
