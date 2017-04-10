# -*- coding: latin-1 -*-
import discord
from discord.ext import commands
import random
import secret

import asyncio

import logging

import feedparser
import aiohttp
import html2text
# import requests

respond = aiohttp.ClientSession()
#yield from respond.post(secret.webhDevelopment,data="{\"username\" : \"Pharo Twitter\" , \"text\" : \" something something something\" , \"attachments\": [ { \"author_name\" : \" some dude \", \"fields\":[{\"title\":\"The title\",\"value\": \" i cant get no satisfaction\" }]}]} ")

rssFeedPharoUsers = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Users-f1310670.xml")
rssFeedPharoDevs = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Developers-f1294837.xml")
#rssFeedPharoUsers = {"entries":[0,1,2,3,4,5,6,7,8,9,10]}
loop = asyncio.get_event_loop()
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)
lighthouse_channel = discord.Object(id=secret.channels["lighthouse"])
general_channel =  discord.Object(id=secret.channels["general"])
development_channel = discord.Object(id=secret.channels["development"])
mailing_lists_channel = discord.Object(id=secret.channels["mailing-lists"])

async def sendEmbMessage(message,channel):
        await bot.send_message(channel, embed=message)

        logging.info("message sent")

async def checkRSSFeed(channel):
    global rssFeedPharoUsers, rssFeedPharoDevs
    logging.info("checking RSS feeds")
    count = 0
    newRssFeedPharoUsers = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Users-f1310670.xml")
    newRssFeedPharoDevs = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Developers-f1294837.xml")
    entryFound= False
    logging.info("\nChecking Pharo-Users\n")
    logging.info("Pharo-users len new: %d", len(newRssFeedPharoUsers))
    for newCount in range(0,len(newRssFeedPharoUsers)-1):
        logging.info("[Pharo-Users] newEntry: %d",newCount)
        entryFound = False
        newEntry = newRssFeedPharoUsers["entries"][newCount]
        for oldCount in range(0,len(rssFeedPharoUsers)-1) :
            logging.info("[Pharo-Users] oldEntry: %d",oldCount)
            oldEntry = rssFeedPharoUsers["entries"][oldCount]
            if oldEntry["id"] == newEntry["id"] :
                entryFound = True
                break
            entry = newEntry
        if not entryFound:
            count = count + 1
            logging.info("\n%d)Found a new entry in the Pharo-Users rss\n",count)
            content = html2text.html2text(entry["content"][0]["value"])
            content = content[0:100]+" ... (click title for more)"
            message = discord.Embed(title="[Pharo-Users] "+entry["title"], url=entry["link"] ,colour = 14088353,  description = content )
            message.set_author(name=entry["author"])
            await sendEmbMessage(message,mailing_lists_channel)
            count = 0

    rssFeedPharoUsers = newRssFeedPharoUsers

    logging.info("\nChecking Pharo-Devs\n")
    for newCount in range(0,len(newRssFeedPharoDevs)-1):
        logging.info("[Pharo-Devs] newEntry: %d",newCount)
        newEntry = newRssFeedPharoDevs["entries"][newCount]
        entryFound = False
        for oldCount in range(0,len(rssFeedPharoDevs)-1) :
            logging.info("[Pharo-Devs] oldEntry: %d",oldCount)
            oldEntry = rssFeedPharoDevs["entries"][oldCount]
            if oldEntry["id"] == newEntry["id"]:
                entryFound = True
                break

            entry = newEntry
        if not entryFound:
            count = count + 1

            logging.info("\n%d)Found a new entry in the Pharo-Devs rss\n",count)
            content = html2text.html2text(entry["content"][0]["value"])
            content = content[0:100]+" ... (click title for more)"
            message = discord.Embed(title="[Pharo-Devs] "+entry["title"], url=entry["link"] ,colour = 14088353,  description = content)
            message.set_author(name=entry["author"])

            await sendEmbMessage(message,mailing_lists_channel)
            count = 0
    rssFeedPharoDevs = newRssFeedPharoDevs

# Enable info level logging
logging.basicConfig(level=logging.INFO)




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    global loop

    await bot.process_commands(message)

    if "love pharo" in message.content.lower():

        await bot.send_message(message.channel, 'Pharo is amazing :)')

    elif "hate pharo" in message.content.lower():

        await bot.send_message(message.channel, ':(  .... why ???')
    else:
        return




@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

async def main():
     await checkRSSFeed(lighthouse_channel)

async def my_background_task():
    await bot.wait_until_ready()
    counter = 0

    while not bot.is_closed:
        await main()
        await asyncio.sleep(60) # task runs every 60 seconds




bot.loop.create_task(my_background_task())
bot.run(secret.token)
