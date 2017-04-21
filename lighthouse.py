# -*- coding: latin-1 -*-
import discord
from discord.ext import commands
import random
import secret
import sqlite3
import asyncio
import re
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
logging.info('Database : {} | user: {} | password: {} | host: {} | port: {} '.format(url.path[1:],url.username,url.password,url.hostname,url.port))
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
    count = 0
    newRssFeedPharoUsers = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Users-f1310670.xml")
    newRssFeedPharoDevs = feedparser.parse("http://forum.world.st/Pharo-Smalltalk-Developers-f1294837.xml")
    entryFound= False
    logging.info("\nChecking Pharo-Users\n")
    logging.info("Pharo-users len new: %d", len(newRssFeedPharoUsers))
    for newCount in range(0,len(newRssFeedPharoUsers)-1):
        entryFound = False
        newEntry = newRssFeedPharoUsers["entries"][newCount]
        for oldCount in range(0,len(rssFeedPharoUsers)-1) :
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

    for newCount in range(0,len(newRssFeedPharoDevs)-1):

        newEntry = newRssFeedPharoDevs["entries"][newCount]
        entryFound = False
        for oldCount in range(0,len(rssFeedPharoDevs)-1) :

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

    elif "what is" in message.content.lower() and message.content[0]!='!':
        words = re.split('''.*what is|[ ?.;!"']''',message.content.lower())
        for word in words:
            if word !='':
                search_term=word
                message.content = '!doc '+word



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
    """<search terms seperated with space> Search terms in  pharo documentation"""
    global cur
    for term in search_term:
        query ="""SELECT * FROM search_terms WHERE search_term = '{}';""".format(term.lower())

        result = cur.execute(query)
        row = cur.fetchall()
        logging.info(str(row[0][1]))
        logging.info(type(row))
        await bot.say(str(row[0][1]))


@bot.command(description='add entry to documentation')
async def docadd(*args):
    """<search_term content tags links> Search for pharo documentation"""
    global cur, conn
    logging.info(" args : {}".format(args))
    if len(args)<2 or len(args)>4:
        await bot.say('Wrong syntax used! Too few arguments')
        return
    elif len(args)==2:
        search_term = args[0].lower()
        content = args[1]
        tags = "{''}"
        links = "{''}"
    elif len(args)==3:
        search_term = args[0].lower()
        content = args[1]
        tags = args[2].replace("'",'"')
        links = "{''}"
    elif len(args)==4:
        search_term = args[0].lower()
        content = args[1]
        tags = args[2].replace("'", '"')
        links = args[3].replace("'",'"')
    else:
        await bot.say("Wrong syntax used!Too many arguments")
        return
    sql = """INSERT INTO search_terms (search_term,content,tags,links)
                    VALUES('{}','{}','{}','{}');""".format(search_term, content, tags, links)
    logging.info("sql : {}".format(sql))
    result = cur.execute(sql)
    conn.commit()

    await bot.say('new entry ['+args[0].lower()+'] inserted')

@bot.command(description='add entry to documentation')
async def docremove(search_term):
    sql = """DELETE FROM search_terms WHERE search_terms.search_term='{}';""".format(search_term.lower())
    result = cur.execute(sql)
    conn.commit()
    await bot.say('entry: [ '+search_term.lower()+ ' ] has been removed!')



@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('Welcome {0.name} at {0.joined_at}. If you have any questions, do not hesitate to ask. Type !lhelpme for the bot documentation'.format(member))

@bot.command()
async def helpme():
    """display the detailed bot documentation"""
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
