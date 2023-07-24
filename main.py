import time
import youtube_dl
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to DynamusicAPI!"}

@app.get("/search-youtube-music")
def search_youtube_music(query: str):
    url = "https://music.youtube.com/youtubei/v1/search?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL"

    headers = {
        "User-Agent": "uwu",
        "Content-Type": "application/json",
    }

    data = {
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "1.20230508.01.01",
                "osName": "Linux"
            }
        },
        "query": query
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

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
