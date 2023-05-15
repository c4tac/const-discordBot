# Install
you need to have **<a  href="https://www.python.org/">python</a>** and **<a  href="https://ffmpeg.org/download.html">ffmpeg</a>** installed

```
git clone https://github.com/forceCpp/openDiscordBot.git
cd  openDiscordBot
pip install -r requirements.txt
```

# setup

add this to the `.env` file
> if you cant find the .env file it might be hidded

```
API_KEY =your_openai_api_key
TOKEN=discord_token
NEWS_API_KEY=news_api_key
OPEN_WEATHER_KEY=open_weather_key
```
you can create a discord bot and get you token at **https://discord.com/developers/applications**
for a openai API key visit **https://beta.openai.com/signup/**
for news api visit **https://newsapi.org/**
> only Requests 1,000 are allowed per day for the news api

for the open weather API key visit **https://openweathermap.org/appid**

# Features

* Play Music 

* **Chat Command**: The bot can have conversations with users using the `$chat` command.
* **Meme Command**: The bot can send a random meme using the `$meme` command.
* **Play Command**: The bot can play YouTube, SoundCloud and etc videos in the voice channel using the `$play` command.
* **Vote Command**: The bot can create a poll that users can vote on using the `$vote` command.
>There are many other cool commands too that you can use.

# Run 

**Windows**
`python main.py`

**Linux/Mac**
`python3 main.py`

# preview
[![Watch the video](https://github.com/forceCpp/openDiscordBot/blob/main/preview/chat.png)](https://raw.githubusercontent.com/forceCpp/openDiscordBot/main/preview/chat.mp4)

[![Watch the video](https://github.com/forceCpp/openDiscordBot/blob/main/preview/meme.png)](https://raw.githubusercontent.com/forceCpp/openDiscordBot/main/preview/meme.mp4)

# try
give the bot a <a  href="https://discord.com/api/oauth2/authorize?client_id=1068497688628305970&permissions=8&scope=bot">try</a>

` https://discord.com/api/oauth2/authorize?client_id=1068497688628305970&permissions=8&scope=bot `

# issues
`$play` you cant play soutube shorts and the bot wont disconnect automatically

# usage
you can use the `$doc` command for the documentation
