# Discord Music Bot

This is a Discord bot that allows users to play YouTube videos in a voice channel. The bot uses the YouTube Data API to search for and retrieve the video URL, and uses the youtube_dl and FFmpeg libraries to play the video's audio in the voice channel.

## Prerequisites

- A Discord account and a Discord server where you have permission to add a bot
- A YouTube Data API key
- The discord, youtube_dl, and google-api-python-client libraries for Python
- FFmpeg installed on your system (if you want to play the audio from YouTube videos)

## Setting up the bot

1. Replace `YOUR_BOT_TOKEN` in the code with your actual Discord bot token.
2. Replace `YOUTUBE_API_KEY` in the code with your actual YouTube Data API key.
3. Install the required libraries using `pip install discord youtube_dl google-api-python-client`.
4. Run the bot using `python bot.py`.

## Using the bot

To play a YouTube video in a voice channel, type `!play` followed by a search query or a YouTube URL in a text channel. The bot will search for the video and play its audio in the voice channel.

To stop the current track, type `!stop` in the text channel.

## Notes

- The free tier of the YouTube Data API has a limit of 10,000 search queries per day.
- If you encounter an error when playing a video, it may be due to the use of an outdated version of FFmpeg or youtube_dl. Updating these libraries may resolve the issue.
