# -*- coding: latin-1 -*-
import discord
from discord.ext import commands
import random
import secret

import asyncio

import logging

import feedparser
import aiohttp
# import requests

respond = aiohttp.ClientSession()
#yield from respond.post(secret.webhDevelopment,data="{\"username\" : \"Pharo Twitter\" , \"text\" : \" something something something\" , \"attachments\": [ { \"author_name\" : \" some dude \", \"fields\":[{\"title\":\"The title\",\"value\": \" i cant get no satisfaction\" }]}]} ")

rssFeedPharoUsers = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Users-f1310670.xml")
rssFeedPharoDevs = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Developers-f1294837.xml")
rssFeedPharoUsers = {"entries":[0,1,2,3,4,5,6,7,8,9,10]}
loop = asyncio.get_event_loop()
async def sendEmbMessage(message,channel):
    if channel=="general":
        async with aiothttp.ClientSession() as requests:
            await requests.post(secret.webhGeneral,data=message)

        logging.info("message sent to general")
    if channel == "development":
        requests.post(secret.webhDevelopment, data=message )

        logging.info("message sent to development")


async def checkRSSFeed():
    global rssFeedPharoUsers, rssFeedPharoDevs
    logging.info("checking RSS feeds")
    count = 0
    newRssFeedPharoUsers = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Users-f1310670.xml")
    newRssFeedPharoDevs = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Developers-f1294837.xml")

    for oldCount in range(-10,-9):
        logging.info("oldEntry: %d",oldCount)
        oldEntry = rssFeedPharoUsers["entries"][oldCount]
        for newCount in range(-10,-9) :
            logging.info("newEntry: %d",newCount)
            newEntry = newRssFeedPharoUsers["entries"][newCount]
            if oldEntry != newEntry:
                count = count + 1
                logging.info("\n%d)Found a new entry in the Pharo-Users rss\n",count)
                entry = newEntry
                message ="".join([ "{\"username\":\"Pharo-Users\", \"text\":\"", entry["link"], "\",\"attachments\": [ { \"author_name\": \"", entry["author"], "\", \"fields\": [{\"title\": \"" , entry["title"] , "\", \"value\": \" click link for content \" }]}]} "])
                logging.info("will send message: "+message)
                sendEmbMessage(message,"general")
    count = 0
    rssFeedPharoUsers = newRssFeedPharoUsers


    """ for oldEntry in rssFeedPharoDevs["entries"]:
        for newEntry in newRssFeedPharoDevs["entries"]:
            if oldEntry != newEntry:
                count = count + 1
                logging.info("\n%d)Found a new entry in the Pharo-Devs rss\n",count)
                entry = newEntry
                message ="".join([ "{\"username\" : \"Pharo-Users\" , \"text\" : \"" , entry["link"] , "\",\"attachments\": [ { \"author_name\" : \"" , entry["author"] , "\", \"fields\": [{\"title\": \"" , entry["title"] , "\", \"value\":  \" click link for content \" }]}]} "])

                logging.info("will send message: "+message)
                sendEmbMessage(message,"development")"""

    rssFeedPharoDevs = newRssFeedPharoDevs

# Enable info level logging
logging.basicConfig(level=logging.INFO)


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    global loop
    await checkRSSFeed()


    if "love pharo" in message.content.lower():

        await bot.send_message(message.channel, 'Pharo is amazing :)')




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


bot.run(secret.token)
