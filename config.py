prefix = '!'
pic_dir = 'pics'
res_dir = 'res'
dump_dir = 'dumps'
sv_dir = 'servers'
cogs_dir = 'cogs'
ai_dir = 'ai'
temp_mp3_name = 'yt_audio.mp3'
rasp_dir = 'rbp'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
ai_receptors = [
    "Docenc",
    "Docent",
    "docenc",
    "docent",
]
