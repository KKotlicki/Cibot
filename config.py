PREFIX = '$'
PIC_PATH = 'pics'
RES_PATH = 'res'
LOGS_PATH = 'logs'
SV_PATH = 'servers'
TEMP_PATH = 'temp'
COGS_PATH = 'cogs'
AI_PATH = 'ai'
BUFFERED_MP3_FILENAME = 'yt_audio.mp3'
RPI_PATH = 'rbp'
BAN_EMOJIS = 'no'
REACT_AT_RANDOM = 'no'
CHESS_OPTIONS = {
    'starting_elo': 1200,
    'elo_change_constant': 50,
    'time_modes': {
            "bullet": 3,
            "blitz": 10,
            "quick": 20,
            "standard": 60,
            "long": 120,
        }
}
YTDL_OPTIONS = {
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
REACT_TO_MESSAGE_CONTENT = [
    "geodezja",
    "geodezji",
    "geodeci",
    "gik",
    "a co to kurwa jest",
    "a co to kurwa jest?"
    "a co to kurwa jest?!",
    "a co to kurwa jest!?"
]
FFMPEG_OPTIONS = {
    'options': '-vn'
}
WIKI_OPTIONS = {
    'sentences': '5',
    'chars': '1500'
}
