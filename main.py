from pytube import YouTube
from fastapi import FastAPI

app = FastAPI()

@app.get("/audio_stream")
def get_audio_stream_url(url: str):
    try:
        # Get the first available audio stream URL
        audio_url = YouTube(url).streams.filter(only_audio=True).first().url
        return {"audio_stream_url": audio_url}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
