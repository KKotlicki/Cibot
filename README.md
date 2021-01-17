Official discord bot of WEITI Telekomunikacja 2020/2021-Z

To add links, go to 'resources'
Main bot script is cibot.py. Keep it tidy!
In config.py save data, such as relative paths, server settings, etc.
In 'cogs' directory, add your modules (class structure is preffered).
In helpers.py, add your local methods.

Data will be updated to 2nd semester soon.


How to create bot:

First, create a ".env" file and provide the data in the following format:
DSC_BOT_KEY=#################################
RESPONSE_CHANNEL=##################                              -(Optional)

To obtain DSC_BOT_KEY, go to your bot site on discord.com/developers/applications/,
choose your bot or create a new one (remember to provide admin permission).
Next go to Bot section and under TOKEN section click button "Copy".

(Optional) To obtain RESPONSE_CHANNEL, log in on your browser,
go to the text channel and from the url copy the last number.

(Optional) To use Youtube commands, create an empty directory and set it's path in config under mp3_config.

Startup: The bot won't work, until it prints out the message on console.

You can change every file in "resources" folder to personalize the bot.
You can also add any .jpg or .png pictures to "co_memes" directory.

Command names are under @client.event. To change the command call name, change name in code below.
To remove command, just comment it out or remove code. They are independent from each other.
