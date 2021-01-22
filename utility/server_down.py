import os
import time
from urllib.request import urlopen
from dotenv import load_dotenv
load_dotenv()

while True:
    time.sleep(60)
    try:
        print('retrying connection')
        urlopen('http://216.58.192.142', timeout=20)
    finally:
        os.system(f'cd ..\n{os.getenv("OS_PYTHON_PREFIX")} cibot.py\n')
        break
