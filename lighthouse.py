# -*- coding: latin-1 -*-
import discord
from discord.ext import commands
import random
import secret
import sqlite3
import asyncio

import logging

import feedparser
import aiohttp
import html2text

import os
import psycopg2
import urlparse3
from urllib.parse import urlparse

# Enable info level logging
logging.basicConfig(level=logging.INFO)

#urlparse3.uses_netloc.append("postgres")
url = urlparse("postgres://hftqnpriogavfy:3cc3a7d53d679911cede3a24243aa82c0c977ce1b831b87eca60f56e3806b7bc@ec2-54-228-235-185.eu-west-1.compute.amazonaws.com:5432/de4g4ikug101fh")

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()
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
bot = commands.Bot(command_prefix='!', description=description)
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
#logging.basicConfig(level=logging.INFO)




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    global loop



    if "love pharo" in message.content.lower():

        await bot.send_message(message.channel, 'Pharo is amazing :)')

    elif "hate pharo" in message.content.lower():

        await bot.send_message(message.channel, ':(  .... why ???')


    await bot.process_commands(message)





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


@bot.command(description='main documentation command')
async def doc(*search_term : str):
    """Search for pharo documentation"""
    global cur
    for term in search_term:
        query ="""SELECT * FROM search_terms WHERE search_term = '{}';""".format(term)

        result = cur.execute(query)
        row = cur.fetchall()
        logging.info(str(query))
        logging.info(type(row))
        await bot.say(str(row[1]))


@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('Welcome {0.name} at {0.joined_at}. If you have any questions, do not hesitate to ask. Type !lhelpme for the bot documentation'.format(member))

@bot.command()
async def helpme():
    """display the bot documentation"""
    await bot.say('https://github.com/kilon/lighthouse/blob/master/README.md')



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
