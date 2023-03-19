import discord
import os
import openai
from dotenv import load_dotenv
from discord import client
from discord.ext import tasks
from aioschedule import every, run_pending
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix = '.', intents=intents)

openai.organization = "org-PyxSdnTqc76R0bPmDWRAk1Gu"
openai.api_key = os.environ['GPTtoken']
openai.Model.list()

model_engine = "gpt-3.5-turbo"

@client.event
async def on_ready():
    day = os.environ['day']
    if(day == "saturday"):
        every().saturday.at(os.environ['schedule_time']).do(Remind_Members)
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
    await client.wait_until_ready()
    await run_pending()

async def Remind_Members():
    Members = client.get_guild(int(os.environ['server_id'])).members
    for member in Members:
        if(not member.bot):
            embed=discord.Embed(title=os.environ['title'], description=os.environ['desc'])
            await member.send(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    if(before.channel == None):
        Members = client.get_guild(int(os.environ['server_id'])).members

        title = f"{ member.name } Connected"
        desc = f"Channel: { after.channel }"
        embed=discord.Embed(title=title, description=desc)

        for mem in Members:
            if(not mem.bot and mem.id != member.id):
                await mem.send(embed=embed)

@client.command()
async def chat(ctx, arg):
   
    chatCompletion = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
        {'role': "user", 'content': arg},
        ]
    )

    result = ''

    for choice in chatCompletion.choices:
        result += choice.message.content

    await ctx.send(result)

if __name__ == "__main__":
    client.run(os.environ['token'])