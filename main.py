import discord
from discord.ext import commands
import random
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
from requests import get
import openai
import json
import requests
import re
import yt_dlp
from discord.voice_client import VoiceClient
from pydub import AudioSegment
from googletrans import Translator
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

#with open('badworlds.txt', 'r') as f:
#    badworlds = f.read().splitlines()

@bot.event
async def on_ready():
    print("bot is ready")

#@bot.event
#async def on_message(message):
    #code//

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
    embed.add_field(name="$weather", value="this command dispalys the weather in you city Usage: $weather [city_name]")
    await ctx.send(embed=embed)


@bot.command()
async def chat(ctx, *, message: str = None):
    if message is None:
        await ctx.send(f"please enter somthing after **$chat** {ctx.message.author.mention}.")
        return
    try:        
        response = openai.Completion.create(engine="text-davinci-002", prompt=message)
        await ctx.send(f"{response.choices[0].text} ~{ctx.message.author.mention}")
        return
    except:
        await ctx.send(f"**AuthenticationError** Incorrect API key provided You can find your API key at https://platform.openai.com/account/api-keys. And please make your that you have internet connection")
        

@bot.command()
async def meme(ctx):
    content = get("https://meme-api.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.send(embed=meme)
    return

@bot.command()
async def play(ctx, url: str):
    try:
        voice_client = await ctx.author.voice.channel.connect()
        info = ytdl.extract_info(url, download=False)
        audio_url = info["url"]
        voice_client.play(discord.FFmpegPCMAudio(audio_url))
        #sound = AudioSegment.from_file(audio_url, format="mp3")youtube_dl
        #voice_client.play(discord.FFmpegPCMAudio(sound))
        if voice_client is None:
            voice_client = ctx.voice_client
            await voice_client.disconnect()
        
    except discord.errors.ClientException:
        await voice_client.disconnect()
    except AttributeError:
        await ctx.send(f"johin a voice channel")

@bot.command()
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send(f"Paused the current song {ctx.message.author.mention}.")
    else:
        await ctx.send(f"Not playing any song {ctx.message.author.mention}.")
@bot.command()
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        voice_client.resume()
        await ctx.send(f"resume the current song {ctx.message.author.mention}.")
    else:
        await ctx.send("fNot playing any song {ctx.message.author.mention}.")

@bot.command()
async def stop(ctx):
       try:
            voice_client = ctx.voice_client
            await voice_client.disconnect()
       except:
            await ctx.send(f"not in a voice channel dont fool me {ctx.message.author.mention}.")

@bot.command()
async def rdog(ctx):
    const = requests.get("https://random.dog/woof.json")
    stuff = json.loads(const.text)
    embed = discord.Embed(title=f"URL: {stuff['url']}", color = discord.Color.random())
    embed.set_image(url=f"{stuff['url']}")
    await ctx.send(embed=embed)


@bot.command()
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

@bot.command()
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
    except:
        await ctx.send("nsfw images are not allowed")

@bot.command()
async def weather(ctx, *, city: str = None):
    try:
        weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={weather_key}")
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        celsius = (temp - 32) * 5/9
        int_celsius = int(celsius)

        if weather_data.json()['code'] == '404':
           await ctx.send(f"city {city} not found")

        await ctx.send(f"""
The Weather in {city} is {weather}
The temperature in {city} is around: {temp}ºF or {int_celsius}°C
""")
    except KeyError:
        print("are you missing api key?")
        await ctx.send(f"oops somthing went wong i think {city} does not exist")

bot.run(discordtoken)
