import discord
import os
from discord import client
from discord.ext import tasks
from aioschedule import every, run_pending
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
Client = commands.Bot(command_prefix = '#', intents=intents)


@Client.event
async def on_ready():
    day = os.environ['day']
    if(day == "saterday"):
        every().saterday.at(os.environ['schedule_time']).do(Remind_Members)
    elif(day == "sunday"):
        every().sunday.at(os.environ['schedule_time']).do(Remind_Members)
    elif(day == "monday"):
        every().monday.at(os.environ['schedule_time']).do(Remind_Members)
    elif(day == "tuesday"):
        every().tuesday.at(os.environ['schedule_time']).do(Remind_Members)
    elif(day == "wednsday"):
        every().wednsday.at(os.environ['schedule_time']).do(Remind_Members)
    elif(day == "thursday"):
        every().thursday.at(os.environ['schedule_time']).do(Remind_Members)
    else:
        every().friday.at(os.environ['schedule_time']).do(Remind_Members)
    loop.start()
    print("I'm Ready")

@tasks.loop(seconds=0)
async def loop():
    await Client.wait_until_ready()
    await run_pending()

async def Remind_Members():
    Members = Client.get_guild(int(os.environ['server_id'])).members
    for member in Members:
        if(not member.bot):
            embed=discord.Embed(title=os.environ['title'], description=os.environ['desc'])
            await member.send(embed=embed)

if __name__ == "__main__":
    Client.run(os.environ['token'])