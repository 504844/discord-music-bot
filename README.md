# Discord Music Bot

This is a Discord bot that allows users to play YouTube videos in a voice channel. The bot uses the YouTube Data API to search for and retrieve the video URL, and uses the youtube_dl and FFmpeg libraries to play the video's audio in the voice channel.

In addition, the bot can play a random intro audio file before playing the actual YouTube video music.

## Prerequisites

- A Discord account and a Discord server where you have permission to add a bot
- Python 3.x installed on your system (https://www.python.org/downloads/)
- FFmpeg installed on your system (https://ffmpeg.org/download.html)
- The discord, youtube_dl, and google-auth libraries for Python (can be installed using `pip install discord youtube_dl google-auth`)
- The asyncio library for Python (should already be included with Python on Windows)

## Setting up the bot

1. Replace `YOUR_BOT_TOKEN` in the code with your actual Discord bot token.
2. Replace `YOUTUBE_API_KEY` in the code with your actual YouTube Data API key.
3. Place your MP3 files in a directory named `audio` in the same directory as `bot.py`. Optionally, include an intro audio file/files named `intro.mp3`.
4. Run `pip install discord youtube_dl google-auth` in a command prompt to install the required libraries.
5. Run the bot using `python bot.py` in a command prompt.

## Using the bot

To play a YouTube video in a voice channel, type `!play` followed by a search query or a YouTube URL in a text channel. The bot will search for the video and play its audio in the voice channel, preceded by the intro audio file/files that are chosen in random order.
To stop the current track, type `!stop` in the text channel.

## Notes

- The free tier of the YouTube Data API has a limit of 10,000 search queries per day.
- If you encounter an error when playing a video, it may be due to the use of an outdated version of FFmpeg or youtube_dl. Updating these libraries may resolve the issue.
