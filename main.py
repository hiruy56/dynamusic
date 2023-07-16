import time
import youtube_dl
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to DynamusicAPI!"}

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
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for fmt in formats:
            if fmt.get('acodec') == 'mp4a.40.2':
                audio_url = fmt.get('url')
                break

    end_time = time.time()  # End the timer
    response_time = end_time - start_time  # Calculate response time

    return {"audio_url": audio_url, "response_time": response_time}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
