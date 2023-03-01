import asyncio
import discord
import yt_dlp as youtube_dl
from googleapiclient.discovery import build
import json
import datetime
import os
import random

# Load API keys from configuration file, handling exceptions if the file is not found or does not contain the expected keys
try:
    with open('config.json') as f:
        keys = json.load(f)
    discord_token = keys['DISCORD_TOKEN']
    youtube_api_key = keys['YOUTUBE_API_KEY']
except FileNotFoundError:
    print("Error: Configuration file not found. Make sure the file 'config.json' is located in the same directory as the script.")
    exit()
except KeyError:
    print("Error: Invalid configuration file. Make sure the file 'config.json' contains the keys 'DISCORD_TOKEN' and 'YOUTUBE_API_KEY'.")
    exit()

# Replace YOUR_BOT_TOKEN with your actual Discord bot token
client = discord.Client(intents=discord.Intents.all())  # Add the intents argument here

# Replace YOUTUBE_API_KEY with your actual YouTube Data API key
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Declare the voice_client object as a global variable
voice_client = None

queue = []

@client.event
async def on_message(message):
    global voice_client
    if message.content.startswith('!queue'):
        # Extract the search query or video URL from the message
        query = message.content[7:]

        # Initialize the video ID and URL
        video_id = None
        video_url = None

        # variable to store the current playing time
        current_time = 0


        if 'youtube.com' in query:
            # If a YouTube URL was provided, extract the video ID
            video_id = query.split('watch?v=')[1]
        else:
            # Otherwise, use the YouTube Data API to search for the video
            # and retrieve its URL
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                type='video',
                videoDefinition='high',
                maxResults=1
            ).execute()

            # Extract the URL of the first search result
            video_id = search_response['items'][0]['id']['videoId']

        # Construct the YouTube video URL
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        # Add the song to the queue
        queue.append(video_url)
        await message.channel.send(f'Added song to queue: {video_url}')
    if message.content.startswith('!play'):
        # Extract the search query or video URL from the message
        query = message.content[7:]

        # Initialize the video ID and URL
        video_id = None
        video_url = None

        if 'youtube.com' in query:
            # If a YouTube URL was provided, extract the video ID
            video_id = query.split('watch?v=')[1]
        else:
            # Otherwise, use the YouTube Data API to search for the video
            # and retrieve its URL
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                type='video',
                videoDefinition='high',
                maxResults=1
            ).execute()

            # Extract the URL of the first search result
            video_id = search_response['items'][0]['id']['videoId']

        # Construct the YouTube video URL
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        # Send the video URL to the channel
        await message.channel.send(f'Playing video: {video_url}')

        # Join the voice channel if not already connected
        if not voice_client or not voice_client.is_connected():
            voice_channel = message.author.voice.channel
            voice_client = await voice_channel.connect()

        # Get the path to the /audio folder based on the current working directory
        audio_folder = os.path.join(os.getcwd(), 'audio')

        # Get a list of all the .mp3 files in the /audio folder
        audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

        # Choose a random .mp3 file from the list, excluding the previously played file
        prev_audio_file = None
        if voice_client.source:
            prev_audio_file = os.path.basename(voice_client.source.url)
        random_audio_file = random.choice([f for f in audio_files if f != prev_audio_file])

        # Create a Discord PCMVolumeTransformer object with the random .mp3 file
        player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.path.join(audio_folder, random_audio_file), executable='C:\\ffmpeg\\bin\\ffmpeg.exe'))
        player.volume = 0.5  # Set the volume to half
        voice_client.play(player)

        # Wait for the MP3 file to finish playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Play the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'before_options': [],  # Set the before_options parameter to an empty list
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
        player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=audio_url, executable='C:\\ffmpeg\\bin\\ffmpeg.exe'))
        player.volume = 0.5  # Set the volume to half
        voice_client.play(player)

        # Wait for the YouTube video to finish playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Check if there are more songs in the queue
        if queue:
            # Get the next song in the queue
            next_song = queue.pop(0)

            # Play the next song
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'before_options': [],  # Set the before_options parameter to an empty list
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(next_song, download=False)
                audio_url = info['url']
            player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=audio_url, executable='C:\\ffmpeg\\bin\\ffmpeg.exe'))
            player.volume = 0.5  # Set the volume to half
            voice_client.play(player)
        
    elif message.content == '!stop':
        # Stop the current track
        voice_client.stop()
    if message.content.startswith('!time'):
        # Extract the requested time from the message
        requested_time = message.content[6:]

        # check if player is running
        if voice_client and voice_client.is_playing():
            time_obj = datetime.datetime.strptime(requested_time, '%M:%S')
            current_time = time_obj.second + time_obj.minute*60
            voice_client.source.seek(current_time)
        else:
            await message.channel.send("No song is playing right now.")
# Replace YOUR_BOT_TOKEN with your actual Discord bot token
client.run(discord_token)
