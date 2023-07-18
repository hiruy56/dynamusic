import time
import youtube_dl
from fastapi import FastAPI, HTTPException
import aiohttp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to DynamusicAPI!"}

@app.get("/extract-audio")
async def extract_audio(url: str):
    start_time = time.time()  # Start the timer

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            info = await response.json()
            formats = info.get('formats', [])
            audio_url = None
            for fmt in formats:
                if fmt.get('acodec') == 'mp4a.40.2':
                    audio_url = fmt.get('url')
                    break

    end_time = time.time()  # End the timer
    response_time = end_time - start_time  # Calculate response time

    return {"audio_url": audio_url, "response_time": response_time}

@app.get("/search/{query}")
async def search_music(query: str):
    # Set the API endpoint URL
    API_URL = "https://music.youtube.com/youtubei/v1/search"

    # Set the request payload
    payload = {
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "0.1"
            }
        },
        "query": query
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as response:
            # Check if the request was successful (status code 200)
            if response.status == 200:
                # Parse the response JSON
                data = await response.json()
                # Extract the search results using the provided path
                try:
                    results = data['contents']['sectionListRenderer']['contents'][0]['musicShelfRenderer']['contents']
                except KeyError:
                    raise HTTPException(status_code=404, detail="No results found")

                # Create a list to store the extracted information
                extracted_results = []

                # Iterate over the results
                for result in results:
                    # Check if the result is a musicResponsiveListItemRenderer
                    if 'musicResponsiveListItemRenderer' in result:
                        # Extract the musicResponsiveListItemRenderer
                        music_item = result['musicResponsiveListItemRenderer']

                        # Extract the title and subtitle
                        title = music_item['title']['runs'][0]['text']
                        subtitle = music_item['subtitle']['runs'][0]['text']

                        # Extract the musicians
                        musicians = []
                        for run in music_item['subtitle']['runs']:
                            if 'navigationEndpoint' in run:
                                musicians.append(run['text'])

                        # Extract the views
                        views = music_item['subtitle']['runs'][-3]['text']

                        # Extract the music length
                        music_length = music_item['subtitle']['runs'][-1]['text']

                        # Extract the thumbnail URL
                        thumbnail_url = music_item['thumbnail']['musicThumbnailRenderer']['thumbnail']['thumbnails'][0]['url']

                        # Create a dictionary to store the extracted information
                        result_info = {
                            "Title": title,
                            "Musicians": musicians,
                            "Views": views,
                            "Music Length": music_length,
                            "Thumbnail URL": thumbnail_url
                        }

                        extracted_results.append(result_info)

                return extracted_results
            else:
                raise HTTPException(status_code=500, detail="Request failed with status code: " + str(response.status))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
