prefix = '!'
mp3_dir = 'yt_audio'
pic_dir = 'pics'
res_dir = 'resources'
temp_mp3_name = 'song.mp3'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
