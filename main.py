from functools import total_ordering
import discord
import guilded
import os
import pickle
from dotenv import load_dotenv
import multiprocessing

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD']
GUILDED_TOKEN = os.environ['GUILDED']

#DATA.PICKLE FORMATTING: [total, discord total, guilded total]
def totals(option):
    global total, dtotal, gtotal
    if option == 1:
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)
            data['count'][0] += 1
            data['count'][1] += 1
        
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    elif option == 2:
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)
            data['count'][0] += 1
            data['count'][2] += 1
        
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)
        return(data['count'][0], data['count'][1], data['count'][2])


def DiscordBot():
    dbot = discord.Client()
    @dbot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(dbot))

    @dbot.event
    async def on_message(message):
        if message.author == dbot.user:
            return

        msg = message.content
        msg = msg.lower()
        print(msg)
        if (msg[0] == 'i') and (((msg[1]=="'" or msg[1] =="’") and msg[2] == "m") or msg[1]== 'm'):
            msg = message.content

            cntnt = msg[3:]
            if cntnt.startswith(' '):
                cntnt = cntnt[1:]
            totals(1)

            await message.channel.send("Hi %s, I'm Dad" %cntnt)
        
        if message.content == "dad stats" or message.content == "Dad stats":
            thetotals = totals(3)
            embedvar = discord.Embed(title="Dad bot stats", description="Total messages sent: `%s`\nFrom discord: `%s`\nFrom Guilded: `%s`"%(thetotals[0], thetotals[1], thetotals[2]))
            await message.channel.send(embed=embedvar)
    dbot.run(DISCORD_TOKEN)

    
def guildedbot():
    gbot = guilded.Client()
    @gbot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(gbot))
    @gbot.event
    async def on_message(ctx):
        global total, dtotal, gtotal
        if ctx.author == gbot.user:
            return
        msg = ctx.content
        msg = msg.lower()
        print(msg)
        if (msg[0] == 'i') and (((msg[1]=="'" or msg[1] =="’") and msg[2] == "m") or msg[1]== 'm'):
            msg = ctx.content
            cntnt = msg[3:]
            if cntnt.startswith(' '):
                cntnt = cntnt[1:]
            totals(2)
            await ctx.channel.send("Hi %s, I'm Dad" %cntnt)
        
        if ctx.content == "dad stats" or ctx.content == "Dad stats":
            thetotals = totals(3)
            embedvar = guilded.Embed(title="Dad bot stats", description="Total messages sent: `%s`\nFrom discord: `%s`\nFrom Guilded: `%s`"%(thetotals[0], thetotals[1], thetotals[2]))
            await ctx.channel.send(embed=embedvar)

    gbot.run(GUILDED_TOKEN)

if __name__ == '__main__':
    pgbot = multiprocessing.Process(name='pgbot', target=DiscordBot)
    pdbot = multiprocessing.Process(name='pdbot', target=guildedbot)
    pgbot.start()
    pdbot.start()