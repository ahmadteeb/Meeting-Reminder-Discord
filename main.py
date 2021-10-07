import discord
import os
from discord import client
from discord.ext import tasks
from aioschedule import every, run_pending
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
Client = commands.Bot(command_prefix = '#', intents=intents)

Server_ID = 895440123578187836

@Client.event
async def on_ready():
    every().thursday.at(os.environ['schedule_time']).do(Remind_Members)
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
            embed=discord.Embed(title="Meeting Invitiation", description="t3al wala 3al meeting")
            await member.send(embed=embed)

if __name__ == "__main__":
    Client.run('ODk1NDM2NDI1MjcxNjAzMjMx.YV4iKA.LOVbkDiWUNCqJSPcuqSHUFrxCoo')