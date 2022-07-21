from functools import total_ordering
import discord, guilded, os, pickle, requests
import requests
from dotenv import load_dotenv
import multiprocessing

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD']
GUILDED_TOKEN = os.environ['GUILDED']
WEBHOOK_URL = os.environ['WEBHOOK_URL']

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
            await dbot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='Your complaints (dad complaint)'))
            return

        msg = message.content
        msg = msg.lower()
        if len(msg) < 2:
            return
        elif (msg[0] == 'i') and (((msg[1]=="'" or msg[1] =="’") and msg[2] == "m") or msg[1]== 'm'):
            msg = message.content

            cntnt = msg[3:]
            if cntnt.startswith(' '):
                cntnt = cntnt[1:]
            totals(1)

            await message.channel.send("Hi %s, I'm Dad" %cntnt)
        
        elif msg == "dad stats":
            thetotals = totals(3)
            embedvar = discord.Embed(title="Dad bot stats", description="Total messages sent: `%s`\nFrom discord: `%s`\nFrom Guilded: `%s`"%(thetotals[0], thetotals[1], thetotals[2]))
            embedvar.set_footer
            await message.channel.send(embed=embedvar)
        
        elif msg.startswith('dad complaint'):
            ctnt = message.content[13:]
            data = {"content" : "-------------------------------\n" + ctnt + "\n\nFrom: "+ str(message.author) + "  (from discord)\n-------------------------------","username" : "dad bot complaint"}
            await message.channel.send('Your complaint has been noted')
            requests.post(WEBHOOK_URL, json=data)
        elif msg == 'dad help':
            embedvar = discord.Embed(title="Dad bot help",)
            embedvar.add_field(name="About", value="Just a simple bot that tells the age old hi x I'm dad joke \nIf this is not to your liking, use 'dad complaint' to send a complaint to me\nThe source code is available at https://github.com/Mushrrom/Dad-jokes-bot", inline=False)
            embedvar.add_field(name="Commands", value= "**dad stats**: Shows stats about the bot\n**dad complaint**: Sends me a complaint")
            await message.channel.send(embed=embedvar)
        elif msg == 'dad ping':
            embedVar = discord.Embed(title="Pong", description="Pong", color=0x00ff00)
            embedVar.add_field(name="Latency", value=str(round(dbot.latency * 1000)), inline=False)
            await message.channel.send(embed=embedVar)
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
        if (msg[0] == 'i') and (((msg[1]=="'" or msg[1] =="’") and msg[2] == "m") or msg[1]== 'm'):
            msg = ctx.content
            cntnt = msg[3:]
            if cntnt.startswith(' '):
                cntnt = cntnt[1:]
            totals(2)
            await ctx.channel.send("Hi %s, I'm Dad" %cntnt)
        
        if msg == "dad stats":
            thetotals = totals(3)
            embedvar = guilded.Embed(title="Dad bot stats", description="Total messages sent: `%s`\nFrom discord: `%s`\nFrom Guilded: `%s`"%(thetotals[0], thetotals[1], thetotals[2]))
            await ctx.channel.send(embed=embedvar)
        if msg.startswith('dad complaint'):
            ctnt = ctx.content
            ctnt = ctnt[13:]
            data = {"content" : "-------------------------------\n" + ctnt + "\n\nFrom: "+ str(ctx.author) + "  (from guilded)\n-------------------------------","username" : "dad bot complaint"}
            await ctx.channel.send('Your complaint has been noted')
            requests.post(WEBHOOK_URL, json=data)
        if msg == 'dad help':
            embedvar = guilded.Embed(title="Dad bot help",)
            embedvar.add_field(name="About", value="Just a simple bot that tells the age old hi x I'm dad joke \nIf this is not to your liking, use 'dad complaint' to send a complaint to me\nThe source code is available at https://github.com/Mushrrom/Dad-jokes-bot", inline=False)
            embedvar.add_field(name="Commands", value= "Dad stats: Shows stats about the bot\ndad complaint: Sends me a complaint")
            await ctx.channel.send(embed=embedvar)
    gbot.run(GUILDED_TOKEN)

if __name__ == '__main__':
    pgbot = multiprocessing.Process(name='pgbot', target=DiscordBot)
    pdbot = multiprocessing.Process(name='pdbot', target=guildedbot)
    pgbot.start()
    pdbot.start()