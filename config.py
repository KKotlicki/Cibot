prefix = '!'
pic_dir = 'pics'
res_dir = 'res'
dump_dir = 'dumps'
sv_dir = 'servers'
cogs_dir = 'cogs'
ai_dir = 'ai'
temp_mp3_name = 'yt_audio.mp3'
rasp_dir = 'rbp'
# ydl_opts = {
#     'format': 'bestaudio/best',
#     'noplaylist': True,
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'nocheckcertificate': True,
#     'default_search': 'auto',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
# }
ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ai_receptors = [
    "Docenc",
    "Docent",
    "docenc",
    "docent",
]
ffmpeg_options = {
    'options': '-vn'
}
