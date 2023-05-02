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
`$translate` does not work properly

`$play` you cant play soutube shorts and the bot wont disconnect automatically

# usage
you can use the `$doc` command for the documentation

all other  information is <a  href="https://github.com/forceCpp/openDiscordBot/blob/main/documentation.txt">hier</a> available
