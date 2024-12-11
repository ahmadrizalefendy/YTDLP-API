
Here’s a description for an API endpoint using yt-dlp to download audio:

Endpoint: /audio?url={yturl}
This endpoint allows users to download audio from a YouTube video using the powerful yt-dlp library.

Request
Method: GET
Query Parameter:
url (required): The URL of the YouTube video from which the audio will be extracted.
Response
Status Codes:

200 OK: Successful download. The audio file is returned in the requested format.
400 Bad Request: Invalid or missing url parameter.
500 Internal Server Error: An error occurred while processing the request.
Response Body:

Content-Type: Based on the extracted audio format (e.g., audio/mpeg for MP3).
The audio file is streamed as a response.
Features
Audio Formats: Extracts audio in a high-quality MP3 format by default.
Automatic Conversion: Ensures compatibility with most media players by converting audio if needed.
Fast Processing: Utilizes yt-dlp for rapid extraction and minimal processing delays.
Error Handling: Returns clear error messages for invalid or unsupported URLs.
Example Usage
bash
Copy code
```
curl -X GET "http://api.example.com/audio?url=https://www.youtube.com/watch?v=example123" --output song.mp3
```
Notes
Ensure proper URL encoding when passing the yturl parameter.
The API respects copyright and fair use policies; users are responsible for ensuring legal use.


Upload to cookies from Browser as NetScape Format Then Upload as cookies.txt
Check Port and Host IP if Required  on app.py 

# Build cmd
```
bash run.sh
```
# run
```
python3 app.py
```
