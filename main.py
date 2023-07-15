import youtube_dl
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to DynamusicAPI!"}

@app.get("/extract-audio")
def extract_audio(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'proxy': 'socks4://186.251.255.73:31337'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for fmt in formats:
            if fmt.get('acodec') == 'mp4a.40.2':
                audio_url = fmt.get('url')
                break

    return {"audio_url": audio_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
