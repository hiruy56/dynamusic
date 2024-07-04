# DynamusicAPI Documentation

DynamusicAPI is a simple and efficient API to search music on YouTube Music and extract audio from YouTube videos. The API is built using FastAPI and leverages `youtube_dl` for extracting audio. This documentation provides details on how to use the API endpoints.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Root](#root)
  - [Search YouTube Music](#search-youtube-music)
  - [Extract Audio](#extract-audio)
- [License](#license)

## Installation

To install and run DynamusicAPI, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/hiruy32/dynamusicapi.git
    cd dynamusicapi
    ```

2. **Install dependencies:**
    ```bash
    pip install fastapi uvicorn requests youtube_dl
    ```

3. **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

## Usage

Once the server is running, you can access the API at `http://127.0.0.1:8000`. You can use tools like `curl`, Postman, or your web browser to interact with the API endpoints.

## Endpoints

### Root

#### `GET /`

Returns a welcome message.

**Response:**
```json
{
    "message": "Welcome to DynamusicAPI!"
}
```

### Search YouTube Music

#### `GET /search-youtube-music`

Searches for music on YouTube Music based on the query provided.

**Parameters:**
- `query` (str): The search query.

**Response:**
- JSON response from YouTube Music API.

**Example:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search-youtube-music?query=your_search_query' \
  -H 'accept: application/json'
```

**Response Example:**
```json
{
    "contents": [...]
}
```

### Extract Audio

#### `GET /extract-audio`

Extracts audio from a YouTube video URL and provides the direct URL to the audio stream.

**Parameters:**
- `url` (str): The YouTube video URL.

**Response:**
- `audio_url` (str): The direct URL to the audio stream.
- `response_time` (float): The time taken to process the request.

**Example:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/extract-audio?url=your_youtube_video_url' \
  -H 'accept: application/json'
```

**Response Example:**
```json
{
    "audio_url": "http://audio.url",
    "response_time": 2.34
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

