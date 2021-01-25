prefix = '!'
pic_dir = 'pics'
res_dir = 'res'
logs_dir = 'logs'
sv_dir = 'servers'
temp_dir = 'temp'
cogs_dir = 'cogs'
ai_dir = 'ai'
temp_mp3_name = 'yt_audio.mp3'
rasp_dir = 'rbp'
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
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
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
