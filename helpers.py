import random
import discord
from config import *
import glob
import json


def read_lines(file_name):
    with open(f"{file_name}.txt") as rs:
        return rs.read().splitlines()


async def build_link_list(ctx, embed_var, fname):
    help_json = "".join(read_lines(f'{res_dir}/{fname}'))
    for name, value in json.loads('{' + help_json + '}').items():
        embed_var.add_field(name=f'**{name}**', value=value, inline=False)
    await ctx.send(embed=embed_var)


def fetch_sv_data(guild):
    text_names = []
    voice_names = []
    for channel in guild.text_channels:
        text_names.append(f'{str(channel)} => {channel.id}')
    for channel in guild.voice_channels:
        voice_names.append(f'{str(channel)} => {channel.id}')
    with open(f"{sv_dir}/{guild}.json", "w+") as fn:
        fn.write(json.dumps({"text": text_names, "voice": voice_names}))


# Local functions:


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
