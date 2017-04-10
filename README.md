# lighthouse
A bot for Discord used in my Pharo server

# Dependencies 
This bot depends on python 3.6 and discord.py

python 3.6 (or more recent) can be download from here 

https://www.python.org/downloads/

discord.py can be installed from terminal after python is installed with

```bash
python3 -m pip install -U discord.py
```

# How to use
just clone the repo make sure you have add (from inside Discord) a bot application to your server and execute. Copy paste the authorisation token that will be given to you after you create the bot application. Then authorise your bot.

inside the folder create a secret.py , the token must remain a secret for security reason this is why this python module is not inside this repo. Add to secret.py the following code

```python
token = "replace this string with your token"
```
then you are ready to start the bot with 

```bash
python3 lighthouse.py
```

# Contributions

I welcome any addition or bug fix for Lighthouse, however for security reasons I will accept them only through pull requests. Of course any improvement you do will be added to the running instance of the bot in the Pharo server as soon as I find time to accept your pull request. 