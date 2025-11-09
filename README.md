# TBD - Assistive Memory System

An intelligent assistive memory system that combines facial recognition, audio/video analysis, and AI-powered summarization to help users remember and track their daily interactions.

## Features

### 🧠 Facial Recognition
- Upload and store facial profiles with personal information
- Real-time face detection using OpenCV
- MongoDB-based profile storage with facial embeddings
- Raspberry Pi camera integration for live recognition

### 🎙️ Audio Analysis
- Audio transcription using OpenAI Whisper
- AI-powered conversation summarization with Grok
- Concise 3-sentence summaries of interactions

### 🎥 Video Analysis
- Frame-by-frame video processing
- AI-powered visual event detection and summarization
- Temporal flow analysis of activities

### 🔊 Text-to-Speech
- ElevenLabs voice synthesis integration
- Matilda voice as default
- PCM audio format support for real-time playback
- Streaming and batch audio generation

## Tech Stack

### Backend
- **Python 3.14**
- **Flask** - REST API framework
- **MongoDB** - Profile and timeline storage
- **OpenCV** - Face detection and image processing
- **NumPy** - Array operations for embeddings

### AI Services
- **OpenAI Whisper** - Audio transcription
- **Grok (xAI)** - Video/audio summarization
- **ElevenLabs** - Text-to-speech synthesis

## Project Structure

```
tbd/
├── backend/
│   ├── app.py                  # Flask API for facial profiles
│   ├── api.py                  # AI service integrations (Grok, Whisper)
│   ├── elevenlabs_client.py    # Text-to-speech functionality
│   ├── memory_schema.py        # MongoDB database operations
│   ├── data_processing.py      # Data processing utilities
│   └── uploads/                # Uploaded photos storage
├── frontend/
│   └── main.py                 # Frontend application
└── .env                        # API keys (gitignored)
```

## Installation

### Prerequisites
- Python 3.14+
- MongoDB installed and running
- API keys for:
  - OpenAI (Whisper)
  - Grok (xAI)
  - ElevenLabs

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Christinetrr/tbd.git
cd tbd
```

2. **Install dependencies**
```bash
pip install flask pymongo opencv-python numpy pillow werkzeug openai elevenlabs
```

3. **Configure environment variables**

Create a `.env` file in the project root:
```
GROK_API_KEY=your_grok_api_key
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

4. **Start MongoDB**
```bash
mongod --dbpath /path/to/your/data/directory
```

5. **Run the Flask server**
```bash
cd backend
python app.py
```

The server will start on `http://127.0.0.1:5001`

## API Endpoints

### Facial Profile Management

#### Setup Facial Profile
```http
POST /api/profiles/setup
Content-Type: multipart/form-data

{
  "name": "John Doe",
  "relation": "Friend",
  "photo": <file>
}
```

#### Recognize Face (Raspberry Pi)
```http
POST /api/profiles/recognize
Content-Type: application/json

{
  "embedding": [128-dimensional array]
}
```

#### Get All Profiles
```http
GET /api/profiles
```

#### Get Specific Profile
```http
GET /api/profiles/<name>
```

#### Delete Profile
```http
DELETE /api/profiles/<name>
```

#### Health Check
```http
GET /api/health
```

## Usage Examples

### Facial Profile Setup
```python
import requests

url = "http://127.0.0.1:5001/api/profiles/setup"
files = {"photo": open("person.jpg", "rb")}
data = {"name": "Jane Smith", "relation": "Friend"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Audio Summarization
```python
from api import summarize_audio

with open("conversation.mp3", "rb") as audio_file:
    summary = summarize_audio(audio_file)
    print(summary)
```

### Text-to-Speech
```python
from elevenlabs_client import text_to_speech

audio_data = text_to_speech(
    "Hello, how are you doing today?",
    output_path="greeting.pcm"
)
```

### Video Frame Analysis
```python
from api import summarize_frames
import cv2

# Read frames from video
frames = []
cap = cv2.VideoCapture("video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

# Get summary
summary = summarize_frames(frames)
print(summary)
```

## Database Schema

### Profiles Collection
```javascript
{
  "name": "John Doe",
  "relation": "Friend",
  "conversations": [
    {
      "timestamp": ISODate("2025-11-09T12:00:00Z"),
      "summary": "Discussed weekend plans"
    }
  ],
  "embedding": [128-dimensional array],
  "metadata": {
    "created_at": ISODate("2025-11-09T10:00:00Z"),
    "last_seen": ISODate("2025-11-09T12:00:00Z")
  }
}
```

### Timelines Collection
```javascript
{
  "date": "2025-11-09",
  "events": [
    {
      "time": "14:30",
      "type": "interaction",
      "description": "Met with John Doe",
      "duration": 30
    }
  ]
}
```

## Hardware Integration

### Raspberry Pi Setup
The system supports Raspberry Pi camera integration for real-time facial recognition:

1. Capture face from Pi camera
2. Extract facial embedding on Pi
3. Send embedding to `/api/profiles/recognize` endpoint
4. Receive matched profile information

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team

- **Andrea Sato** - Facial recognition API & MongoDB integration
- **Christinetrr** - API integration & video batching
- **shrenik** - Audio capture & Raspberry Pi integration

## License

This project is part of an academic assignment.

## Acknowledgments

- OpenAI for Whisper transcription API
- xAI for Grok video/audio analysis
- ElevenLabs for natural voice synthesis
- OpenCV for computer vision capabilities
