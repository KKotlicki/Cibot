import random
import discord
from config import *
import glob
import json
import youtube_dl
import asyncio


def read_lines(fname):
    with open(f"{fname}.txt", encoding='utf-8') as rs:
        return rs.read().splitlines()


async def open_help(ctx, file_name):
    embed_var = discord.Embed(title=":ledger: Komendy:", color=0xff770f)
    with open(f'{res_dir}/{file_name}.json', encoding='utf-8') as rd:
        help_json = json.loads(rd.read())
    for name, value in help_json.items():
        embed_var.add_field(name=f'**{name}**', value=f'```{prefix}{value}```', inline=False)
    await ctx.send(embed=embed_var)


async def fetch_sv_data(ctx):
    text_names = []
    voice_names = []
    for channel in ctx.message.guild.text_channels:
        text_names.append(f'{str(channel)} => {channel.id}')
    for channel in ctx.message.guild.voice_channels:
        voice_names.append(f'{str(channel)} => {channel.id}')
    with open(f"{sv_dir}/{ctx.message.guild}.json", "w+") as fn:
        fn.write(json.dumps({"text": text_names, "voice": voice_names}))
    await ctx.send("Zapisałem pomyślnie")


# Local functions:

async def build_link_list(ctx, embed_var, fname, message):
    with open(f'{res_dir}/{fname}.json', encoding='utf-8') as rd:
        link_dict = json.loads(rd.read())
    for name, value in {**link_dict[message], **link_dict["all"]}.items():
        embed_var.add_field(name=f'**{name}**', value=value, inline=False)
    await ctx.send(embed=embed_var)


def get_random_number_unless_specified(question):
    if question == '1':
        return '1'
    elif question == '2':
        return '2'
    return f'{random.randint(1, 8)}'


async def send_pic_or_txt_on_choice(ctx, choice):
    if choice == '1':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{pic_dir}/*.jpg"))))
    elif choice == '2':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{pic_dir}/*.png"))))
    else:
        responses = read_lines(f'{res_dir}/responses')
        await ctx.send(f'{random.choice(responses)}')


def env_config():
    token = input("Bot Token:\n\n")
    raspberry_pi_check = input("\n\nIs host raspberry pi:\n\n(Y/N): ")
    python_prefix_check = input("\n\nOS python 3 call command (usually is python3):\n\n")
    with open(f'.env', 'w') as wr:
        wr.write(f"TOKEN={token}\nRASPBERRY_PI={raspberry_pi_check}\nOS_PYTHON_PREFIX={python_prefix_check}")


def sort_dict_by_value(dict):
    sorted_values = sorted(dict.values(), key=None, reverse=True)  # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dict.keys():
            if dict[k] == i:
                sorted_dict[k] = dict[k]
                break
    return sorted_dict

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: youtube_dl.YoutubeDL(ytdl_options).extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else youtube_dl.YoutubeDL(ytdl_options).prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
