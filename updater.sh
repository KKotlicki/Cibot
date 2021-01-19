#cd /home/pi/bot/cibot
pkill 'python3 cibot.py'
git pull cibot main
python3 cibot.py