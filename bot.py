import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import datetime

@dataclass
class Session:
    is_activate: bool = False
    start_time: int = 0    

BOT_TOKEN = "INSERT BOT TOKEN HERE AS THE STRING"
CHANNEL_ID = 1113515685654581248
MAX_SESSION_TIME = 1

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

#create session
session = Session()

@tasks.loop(minutes=MAX_SESSION_TIME,count=2)
async def break_remainder():

    #ignore the first noop
    if break_remainder.current_loop == 0:
        return
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Great Focus!** You have been working for {MAX_SESSION_TIME} minutes. ")
    


@bot.event
async def on_ready():
    print("Hello! Raccon study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello!, Raccon is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!!")

@bot.command()
async def add(ctx, *args):
    result = 0
    for i in args:
        result += int(i)
    await ctx.send(f"Result is: {result}")


@bot.command()
async def start(ctx):
    if session.is_activate:
        await ctx.send("A session is already active!")
        return
    
    session.is_activate = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_remainder.start()
    await ctx.send(f"New session created at: {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_activate:
        await ctx.send("No session is active!")
        return
    session.is_activate = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_remainder.stop()
    await ctx.send(f"Session ended after {human_readable_duration} seconds.") 

bot.run(BOT_TOKEN)