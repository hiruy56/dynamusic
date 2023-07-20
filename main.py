import time
import youtube_dl
from fastapi import FastAPI, HTTPException
from ytmusicapi import YTMusic

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to DynamusicAPI!"}

@app.get("/search-youtube")
def search_youtube(query: str):
    ytmusic = YTMusic(location="US")
    search_results = ytmusic.search(query=query, filter="songs")
    return search_results

@app.get("/extract-audio")
def extract_audio(url: str):
    start_time = time.time()  # Start the timer

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        audio_url = None
        for fmt in formats:
            if fmt.get('acodec') == 'mp4a.40.2':
                audio_url = fmt.get('url')
                break

    end_time = time.time()  # End the timer
    response_time = end_time - start_time  # Calculate response time

    return {"audio_url": audio_url, "response_time": response_time}
