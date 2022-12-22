import discord
import youtube_dl
from googleapiclient.discovery import build

# Replace YOUR_BOT_TOKEN with your actual Discord bot token
client = discord.Client(intents=discord.Intents.all())  # Add the intents argument here

# Replace YOUTUBE_API_KEY with your actual YouTube Data API key
youtube = build('youtube', 'v3', developerKey='YOUTUBE_API_KEY')

# Declare the voice_client object as a global variable
voice_client = None

@client.event
async def on_message(message):
    global voice_client
    if message.content.startswith('!play'):
        # Extract the search query or video URL from the message
        query = message.content[6:]

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

        # Play the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
        player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=audio_url, executable='C:\\ffmpeg\\bin\\ffmpeg.exe'))
        player.volume = 0.5  # Set the volume to half
        voice_client.play(player)
    elif message.content == '!stop':
        # Stop the current track
        voice_client.stop()


# Replace YOUR_BOT_TOKEN with your actual Discord bot token
client.run('YOUR_BOT_TOKEN')
