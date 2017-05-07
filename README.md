<<<<<<< HEAD
# lighthouse
A bot for Discord used in my Pharo server

# Dependencies 
=======
# 1. Documentation

## 1.1 About
A bot for Discord used in my Pharo server. Lighthouse has several useful commands that can be to perform a wide array of task. 

## 1.2 Bot Commands
Bot commands have to be prefixed with the "!" symbol

### 1.2.1 roll \<no of times\>d\<no of values\>
The roll command is a game of roll dice that works using syntax "roll NdN" for example "!roll 3d6" this will throw the dice 3 time with values from 0-6

### 1.2.2 helpme
Will send you to this documentation

### 1.2.3 doc \<search_term\>
A documentation command that help you find a search term (the terms can be one or more words separated by space) in pharo documentation. For example
```
!doc roassal  
``` 
This command will search for term roassal and will return separate results for each. 
You can also accomplish the same result with **what is** keywords. Case is ignored. For example
```
what is pharo
```
adding a questionmark in the end is also acceptable
```
what is pharo ?
```
Bare in mind that **what is** will search documentation for the first word after the keywords seperated by space. 

# 2. Dependencies 
>>>>>>> 47c7e344dcc5a1fc9265fa36e9e8b5a7a7971f9d
This bot depends on python 3.6 and discord.py

python 3.6 (or more recent) can be download from here 

https://www.python.org/downloads/

discord.py can be installed from terminal after python is installed with

```bash
python3 -m pip install -U discord.py
```

<<<<<<< HEAD
# How to use
=======
# 3. How to use
>>>>>>> 47c7e344dcc5a1fc9265fa36e9e8b5a7a7971f9d
just clone the repo make sure you have add (from inside Discord) a bot application to your server and execute. Copy paste the authorisation token that will be given to you after you create the bot application. Then authorise your bot.

inside the folder create a secret.py , the token must remain a secret for security reason this is why this python module is not inside this repo. Add to secret.py the following code

```python
token = "replace this string with your token"
```
then you are ready to start the bot with 

```bash
python3 lighthouse.py
```

<<<<<<< HEAD
# Contributions
=======
# 4. Contributions
>>>>>>> 47c7e344dcc5a1fc9265fa36e9e8b5a7a7971f9d

I welcome any addition or bug fix for Lighthouse, however for security reasons I will accept them only through pull requests. Of course any improvement you do will be added to the running instance of the bot in the Pharo server as soon as I find time to accept your pull request. 
