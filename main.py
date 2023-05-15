import discord
from discord.ext import commands
import random
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
from requests import get
import openai
from discord.ext.commands import MemberConverter
import json
import requests
import yt_dlp
from discord.voice_client import VoiceClient
from pydub import AudioSegment
import asyncio
import logging
load_dotenv()
discordtoken = os.getenv("TOKEN")
openai_api_key = os.getenv("API_KEY")
openai.api_key = openai_api_key
news_key = os.getenv("NEWS_API_KEY")
weather_key = os.getenv("OPEN_WEATHER_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

@bot.event
async def on_ready() -> None:
    logging.basicConfig(filename='discordBot.errors', level=logging.ERROR)
    print("Bot is online!")
    print("error will be logged to a file named discordBot.errors")
    print("-"*100)

@bot.event
async def on_member_join(member):
    # Customize the welcome message here
    welcome_channel = discord.utils.get(member.guild.channels, name="welcome")
    welcome_message = f"Welcome {member.mention} to the server! We're glad to have you here."

    if welcome_channel is not None:
        await welcome_channel.send(welcome_message)

@bot.command()
async def doc(ctx):
    embed = discord.Embed(title="List of available commands:", color=discord.Color.blue())
    embed.add_field(name="$chat", value="This command lets you have a conversation with the bot. Usage: $chat [message]")
    embed.add_field(name="$meme", value="This command sends a random meme. Usage: $meme")
    embed.add_field(name="$play", value="This command plays a YouTube video in the voice channel you are in. Usage: $play [YouTube video URL]")
    embed.add_field(name="$pause", value="This command pauses the currently playing YouTube video. Usage: $pause")
    embed.add_field(name="$resume", value="This command resumes the currently paused YouTube video. Usage: $resume")
    embed.add_field(name="$stop", value="This command stops the currently playing YouTube video. Usage: $stop")
    embed.add_field(name="$rdog", value="This command sends a random dog image. Usage: $rdog")
    embed.add_field(name="$news", value="This command displays the latest news for the given keyword. Usage: $news [keyword]")
    embed.add_field(name="$imggen", value="This command generates an image from the given text. Usage: $imggen [text]")
    embed.add_field(name="$weather", value="This command dispalys the weather in you city Usage: $weather [city name]")
    embed.add_field(name="$rnum", value="This command sends a random number between 1 and a random number you want. Usage: $rnum [any number]")
    embed.add_field(name="$remind", value="This command lets your create a reminder. Usage: $remind [time in seconds] [message]")
    embed.add_field(name="$math", value="A simple calculator. Usage: $math [Number + Number]")
    embed.add_field(name="$ping", value="This Command lets you check the bot latency. Usage: $ping")
    embed.add_field(name="$vote", value="Create a poll that users can vote on using reactions. Usage: $vote '[title]' [description]")
    embed.add_field(name="$check_votes", value="Check the number of thumbs up and thumbs down votes for a given voting poll with the specified embed title. Usage: $check_votes '[embed_title]'")
    await ctx.send(embed=embed)


@bot.command(help="This command lets you have a conversation with the bot. Usage: $chat [message]")
async def chat(ctx, *, message: str = None):
    if message is None:
        await ctx.send(f"please enter somthing after **$chat** {ctx.message.author.mention}.")
        return
    try:        
        response = openai.Completion.create(engine="text-davinci-002", prompt=message)
        await ctx.send(f"{response.choices[0].text} ~{ctx.message.author.mention}")
        return
    except Exception as e:
        await ctx.send(f"opps something went wrong. Please try again.")
        logging.error(f"Error in {ctx.command}: {e}")
        

@bot.command(help="This command sends a random meme. Usage: $meme")
async def meme(ctx):
    content = get("https://meme-api.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.send(embed=meme)
    return

@bot.command(help="This command plays a YouTube video in the voice channel you are in. Usage: $play [YouTube video URL]")
async def play(ctx, url: str):
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_client.encoder_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        info = ytdl.extract_info(url, download=False)
        audio_url = info["url"]
        voice_client.play(discord.FFmpegPCMAudio(audio_url))

    except AttributeError:
        await ctx.send(f"johin a voice channel")
    except UnboundLocalError:
        await ctx.send(f"music is allready playing please use the $stop command and try again")
    except Exception as e:
        logging.error(f"Error in {ctx.command}: {e}")

@bot.command(help="This command pauses the currently playing YouTube video. Usage: $pause")
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send(f"Paused the current song {ctx.message.author.mention}.")
    else:
        await ctx.send(f"Not playing any song {ctx.message.author.mention}.")

@bot.command(help="This command resumes the currently paused YouTube video. Usage: $resume")
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        voice_client.resume()
        await ctx.send(f"resume the current song {ctx.message.author.mention}.")
    else:
        await ctx.send(f"Not playing any song {ctx.message.author.mention}.")

@bot.command(help="This command stops the currently playing YouTube video. Usage: $stop")
async def stop(ctx):
       try:
            voice_client = ctx.voice_client
            await voice_client.disconnect()
       except:
            await ctx.send(f"not in a voice channel {ctx.message.author.mention}.")


@bot.command(help="This command sends a random dog image. Usage: $rdog")
async def rdog(ctx):
    try:
        const = requests.get("https://random.dog/woof.json")
        stuff = json.loads(const.text)
        embed = discord.Embed(title=f"URL: {stuff['url']}", color = discord.Color.random())
        embed.set_image(url=f"{stuff['url']}")
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in {ctx.command}: {e}")
        await ctx.send(f"Please make sure that you have internet connection")

@bot.command(help="This command displays the latest news for the given keyword. Usage: $news [keyword]")
async def news(ctx, innews):
    news = requests.get(f"https://newsapi.org/v2/everything?q={innews}&apiKey={news_key}").json()
    thnews = news["articles"]
    if news["status"] == "ok":
        for i , article in enumerate(thnews):
            if i < 5:
                emend = discord.Embed(title=article["title"], description=article["description"], url=article["url"],color=discord.Color.blue())
                await ctx.send(embed=emend)
            else:
                break
    else:
        await ctx.send(f"{innews} not found please try again")

@bot.command(help="This command generates an image from the given text. Usage: $imggen [text]")
async def imggen(ctx, *, text: str = None):
    try:
        if text is None:
            await ctx.send("please enter some text")
            return
        await ctx.send("please wait a second genarting image" , ctx.message.author.mention)
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="256x256",

        )
        await ctx.send(response["data"][0]["url"])
    except Exception as e:
        await ctx.send("nsfw images are not allowed")
        logging.error(f"Error in {ctx.command}: {e}")

@bot.command(help="This command dispalys the weather in you city Usage: $weather [city name]")
async def weather(ctx, *, city: str = None):
    try:
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={weather_key}")
        if weather_data.json()['cod'] == '404':
           await ctx.send(f"city {city} not found")
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        country_name = weather_data.json()['sys']['country']
        celsius = (temp - 32) * 5/9
        int_celsius = int(celsius)
        await ctx.send(f"""
    The Weather in {city} is {weather} , country: {country_name}
    The temperature in {city} is around: {temp}ºF or {int_celsius}°C
    """)
    except Exception as e:
        logging.error(f"Error in {ctx.command}: {e}")

@bot.command(help="This command sends a random number between 1 and a random number you want. Usage: $rnum [any number]")
async def rnum(ctx , *, randeom_num: int = None):
    try:
        randrom_number = random.randint(1, randeom_num)
        await ctx.send(f"your random number is {randrom_number} ~ {ctx.message.author.mention}")
    except ValueError:
        await ctx.send(f"{randeom_num} is not a number please try again with a valid number ~ {ctx.message.author.mention}")

@bot.command(help="This command lets you set a reminder. Usage: $remind [time in seconds]")
async def remind(ctx, time, *, message):
    server_name = ctx.guild.name
    try:
        await ctx.send(f"your reminder is set you will get notifed {time} seconds")
        await asyncio.sleep(int(time))
        await ctx.author.send(f"""
reminder: {message}

from the {server_name} server
    """)
    except ValueError:
        await ctx.send(f"{time} is not a number please try again with a valid number ~ {ctx.message.author.mention}")
    except Exception as e:
        await ctx.send(f"oops somthing went wong please try again later {ctx.message.author.mention}")
        logging.error(f"Error in {ctx.command}: {e}")

@bot.command(help="This command lets you calculate the given expression. Usage: $math [expression]")
async def math(ctx, *,  expression: str = None):
    try:
        await ctx.send(f"{eval(expression)}")
    except SyntaxError:
        await ctx.send(f"{expression} is not a valid expression, Supported expressions '+ for addition', '- for subtraction', '* for Multiplication' and '/ for Division'  there are other too but thiese are the most Common~ {ctx.message.author.mention}")
    except NameError:
        await ctx.send(f"{expression} NameError please make sure you are using the correct syntax~ {ctx.message.author.mention}")
    except ZeroDivisionError:
        await ctx.send(f"number/0 is not allowed , Didn't you pay attention in math class? {ctx.message.author.mention}")

@bot.command(help="This Command lets you check the bot latency. Usage: $ping")
async def ping(ctx):
    await ctx.send(f"Bot latency: {round(bot.latency * 1000)}ms")

@bot.command(help="Create a poll that users can vote on using reactions. Usage: $vote '[title]' [description]")
async def vote(ctx, name,*, svote):
    embend = discord.Embed(title=name, color = discord.Color.random())
    embend.add_field(name=name, value=svote)
    vote_massege = await ctx.send(embed=embend)
    await vote_massege.add_reaction('\N{THUMBS UP SIGN}')
    await vote_massege.add_reaction('\N{THUMBS DOWN SIGN}')

@bot.command(help="Check the number of thumbs up and thumbs down votes for a given voting poll with the specified embed title. Usage: $check_votes '[embed_title]'")
async def check_votes(ctx, vote_title):
    try:
        async for message in ctx.channel.history():
            if message.embeds and message.embeds[0].title == vote_title: 
                thumbs_up = 0
                thumbs_down = 0
                for reaction in message.reactions:
                    if str(reaction.emoji) == '👍':
                        thumbs_up = reaction.count - 1  # subtract bot's reaction
                    elif str(reaction.emoji) == '👎':
                        thumbs_down = reaction.count - 1  # subtract bot's reaction
                    await ctx.send(f'There are {thumbs_up} thumbs up and {thumbs_down} thumbs down votes and total votes: {reaction.count - 1}.')
                    return
        await ctx.send(f"{vote_title} not found, please try again")
    except Exception as e:
        logging.error(f"Error in {ctx.command}: {e}")

bot.run(discordtoken)
