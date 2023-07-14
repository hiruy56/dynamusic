# import youtube_dl

# def extract_info(url):
#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'headers': {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     },
# }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         return info_dict

# # Replace '<URL>' with the YouTube video URL you provided
# url = 'https://music.youtube.com/watch?v=r7Rn4ryE_w8'
# info = extract_info(url)

# # Print the extracted information
# print(info)


from pytube import YouTube
from fastapi import FastAPI
from fastapi.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI()
app.add_middleware(ProxyHeadersMiddleware)

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


# import time
# import youtube_dl

# start_time = time.time()

# # URL of the YouTube video
# url = "https://music.youtube.com/watch?v=eFV2QHqiUww"

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
# }

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
#     formats = info.get('formats', [])
#     for fmt in formats:
#         if fmt.get('acodec') == 'mp3a.40.2':
#             audio_url = fmt.get('url')
#             break

# end_time = time.time()

# execution_time = end_time - start_time

# print("Audio stream URL:", audio_url)
# print("Execution time: {:.2f} seconds".format(execution_time))

