prefix = 'c!'
mp3_dir = 'ytaudio'
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
