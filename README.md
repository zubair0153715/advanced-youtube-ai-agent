# 🎬 YouTube AI Studio - Complete Video Automation Platform

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![AI Providers](https://img.shields.io/badge/AI-Gemini%2C%20GPT--4%2C%20Claude-orange.svg)](https://ai.google.dev/)

**Transform any topic into professional YouTube videos with one click!** 

The most advanced AI-powered YouTube automation platform featuring multi-modal AI generation, real-time web interface, REST API, and support for both Shorts and long-form content.

---

## 🌟 Key Features

### 🤖 Advanced AI Capabilities
- **Multi-Provider Intelligence**: Auto-switches between Google Gemini, OpenAI GPT-4, and Anthropic Claude
- **Sentiment Analysis**: Matches voice tone and visuals to script emotion
- **Viral Hook Generator**: Creates multiple opening variations for A/B testing
- **Auto-Emoji Integration**: Intelligently adds engaging emojis
- **SEO Optimization**: AI-generated titles, descriptions, and tags
- **Smart Transitions**: AI-suggested scene transitions

### 🎨 Content Creation
- **Multiple Formats**: YouTube Shorts (9:16), Standard (1:1), Landscape (16:9)
- **Voice Profiles**: Default, Narrator, Energetic, Calm personalities
- **Batch Processing**: Generate multiple videos simultaneously
- **Thumbnail Generation**: AI-created eye-catching thumbnails
- **Background Music**: Royalty-free music integration
- **Subtitle Generation**: Auto-synced captions

### 🌐 Accessibility
- **Web Interface**: Beautiful, responsive UI - no coding required
- **REST API**: Full programmatic access with Swagger docs
- **Real-Time Progress**: Live generation tracking
- **Multi-User Support**: Share with team or public
- **Mobile Friendly**: Works on all devices

---

## 🚀 Quick Start Guide

### Step 1: Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd advanced-youtube-ai-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Create a `.env` file in the root directory:

```bash
# Required: At least one AI provider
GEMINI_API_KEY=your_google_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: For voice synthesis
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Optional: For stock footage
PEXELS_API_KEY=your_pexels_key_here
PIXABAY_API_KEY=your_pixabay_key_here
```

**Get your API keys:**
- Google Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- ElevenLabs: https://elevenlabs.io/app/settings/api-keys

### Step 3: Start the Web Server

```bash
python -m src.api_server
```

The server will start at: **http://localhost:8000**

### Step 4: Generate Your First Video!

1. Open http://localhost:8000 in your browser
2. Enter a topic (e.g., "10 Amazing Facts About Space")
3. Choose format: Shorts, Standard, or Landscape
4. Select voice profile and enable AI features
5. Click "Generate Video"
6. Wait 30-60 seconds
7. Download your video!

---

## 📖 Detailed Documentation

### 📚 Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Configuration Guide](#configuration-guide)
3. [Using the Web Interface](#using-the-web-interface)
4. [API Reference](#api-reference)
5. [Command Line Usage](#command-line-usage)
6. [Making It Public](#making-it-public)
7. [Deployment Options](#deployment-options)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## 🔧 Configuration Guide

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes (at least one) | `AIzaSy...` |
| `OPENAI_API_KEY` | OpenAI API key | No | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | No | `sk-ant-...` |
| `ELEVENLABS_API_KEY` | Voice synthesis API key | No | `...` |
| `PEXELS_API_KEY` | Stock video API key | No | `...` |
| `HOST` | Server bind address | No | `0.0.0.0` |
| `PORT` | Server port | No | `8000` |
| `MAX_CONCURRENT_JOBS` | Max parallel generations | No | `5` |

### config.py Settings

Edit `src/config.py` to customize:

```python
# AI Provider Priority
AI_PROVIDER_PRIORITY = ["gemini", "openai", "anthropic"]

# Video Quality Presets
QUALITY_PRESETS = {
    "low": {"resolution": "480p", "bitrate": "1000k"},
    "medium": {"resolution": "720p", "bitrate": "2500k"},
    "high": {"resolution": "1080p", "bitrate": "5000k"},
    "ultra": {"resolution": "4k", "bitrate": "15000k"}
}

# Voice Profiles
VOICE_PROFILES = {
    "default": {"speed": 1.0, "pitch": 0},
    "narrator": {"speed": 0.9, "pitch": -2},
    "energetic": {"speed": 1.1, "pitch": 2},
    "calm": {"speed": 0.85, "pitch": -1}
}

# Feature Flags
ENABLE_SENTIMENT_ANALYSIS = True
ENABLE_AUTO_EMOJI = True
ENABLE_VIRAL_HOOKS = True
ENABLE_SMART_TRANSITIONS = True
ENABLE_BATCH_PROCESSING = True
ENABLE_ANALYTICS_TRACKING = True
```

---

## 🖥️ Using the Web Interface

### Dashboard Overview

When you open http://localhost:8000, you'll see:

1. **Topic Input**: Enter your video topic (5-500 characters)
2. **Format Selector**: Choose aspect ratio
   - 📱 **Shorts** (9:16) - Perfect for TikTok, Reels, YouTube Shorts
   - 📺 **Standard** (1:1) - Square format for Instagram
   - 🎬 **Landscape** (16:9) - Traditional YouTube videos
3. **Voice Profile**: Select narrator personality
4. **AI Features Toggle**:
   - 🎣 Viral Hooks - Generate multiple openings
   - 😊 Sentiment Analysis - Match emotion to content
   - 😄 Auto Emoji - Add engaging emojis
   - 🎬 Smart Transitions - Smooth scene changes
5. **Advanced Settings**:
   - AI Provider (Auto/Gemini/OpenAI/Claude)
   - Duration (10-600 seconds)
   - Batch Count (1-10 videos)
6. **Generate Button**: Start creation
7. **Progress Tracker**: Real-time status updates
8. **Download Link**: Get your finished video

### Example Workflow

**Creating a YouTube Short:**

1. Topic: `"5 Mind-Blowing Quantum Physics Facts"`
2. Format: `Shorts (9:16)`
3. Voice: `Energetic`
4. Enable: Viral Hooks ✓, Sentiment ✓, Emoji ✓
5. Duration: `60 seconds`
6. Click **Generate Video**
7. Watch progress: Planning → Script → Voice → Visuals → Editing → Complete
8. Download and share!

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000/api
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Endpoints

#### 1. Generate Video
```http
POST /api/generate
Content-Type: application/json

{
  "topic": "string (required, 5-500 chars)",
  "format_type": "shorts|standard|landscape",
  "voice_profile": "default|narrator|energetic|calm",
  "ai_provider": "auto|gemini|openai|anthropic",
  "enable_hooks": boolean,
  "enable_sentiment": boolean,
  "enable_emoji": boolean,
  "duration_seconds": integer (10-600),
  "batch_count": integer (1-10)
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Job queued successfully",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 2. Check Status
```http
GET /api/status/{job_id}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing|completed|failed",
  "progress": 75,
  "message": "Generating visuals...",
  "result": {
    "video_url": "/api/videos/filename.mp4",
    "download_url": "/api/download/filename.mp4",
    "thumbnail_url": "/thumbnails/filename.jpg",
    "script": "Full script text...",
    "metadata": {...}
  },
  "error": null
}
```

#### 3. Download Video
```http
GET /api/download/{filename}
```

#### 4. Stream Video
```http
GET /api/videos/{filename}
```

#### 5. List All Jobs
```http
GET /api/jobs
```

#### 6. Health Check
```http
GET /api/health
```

### Python Client Example

```python
import requests
import time

class YouTubeAIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def generate(self, topic, **kwargs):
        """Start video generation"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"topic": topic, **kwargs}
        )
        return response.json()
    
    def wait_for_completion(self, job_id, poll_interval=2):
        """Poll until job completes"""
        while True:
            status = requests.get(
                f"{self.base_url}/api/status/{job_id}"
            ).json()
            
            if status['status'] == 'completed':
                return status
            elif status['status'] == 'failed':
                raise Exception(f"Job failed: {status['error']}")
            
            print(f"Progress: {status['progress']}% - {status['message']}")
            time.sleep(poll_interval)
    
    def download(self, filename, save_path="."):
        """Download completed video"""
        response = requests.get(
            f"{self.base_url}/api/download/{filename}",
            stream=True
        )
        
        with open(f"{save_path}/{filename}", 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        
        return f"{save_path}/{filename}"

# Usage
client = YouTubeAIClient()

# Generate video
job = client.generate(
    topic="10 Space Facts That Will Blow Your Mind",
    format_type="shorts",
    voice_profile="energetic",
    enable_hooks=True
)

print(f"Job ID: {job['job_id']}")

# Wait for completion
result = client.wait_for_completion(job['job_id'])

# Download
video_path = client.download(result['result']['video_url'].split('/')[-1])
print(f"Video saved to: {video_path}")
```

---

## 💻 Command Line Usage

For advanced users who prefer CLI:

```bash
# Basic usage
python -m src.main --prompt "Your Topic Here"

# With options
python -m src.main \
  --prompt "The Future of AI" \
  --format shorts \
  --voice-profile energetic \
  --ai-provider auto \
  --enable-hooks \
  --enable-sentiment \
  --enable-emoji \
  --duration 60

# Batch processing
python -m src.main \
  --prompt "Quantum Computing Explained" \
  --batch-count 5 \
  --format landscape

# View all options
python -m src.main --help
```

### CLI Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--prompt` | `-p` | Video topic | Required |
| `--format` | `-f` | shorts/standard/landscape | shorts |
| `--voice-profile` | `-v` | default/narrator/energetic/calm | default |
| `--ai-provider` | `-a` | auto/gemini/openai/anthropic | auto |
| `--duration` | `-d` | Video length in seconds | 60 |
| `--batch-count` | `-b` | Number of videos | 1 |
| `--enable-hooks` | `-h` | Generate viral hooks | False |
| `--enable-sentiment` | `-s` | Sentiment analysis | False |
| `--enable-emoji` | `-e` | Auto emoji insertion | False |
| `--output-dir` | `-o` | Output directory | ./output |

---

## 🌍 Making It Public

### Option 1: Local Network Access

Anyone on your WiFi can access:

1. Find your IP:
   ```bash
   # Linux/Mac
   ipconfig getifaddr en0
   
   # Windows
   ipconfig | findstr IPv4
   ```

2. Share: `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

### Option 2: ngrok (Public Internet - Easiest)

```bash
# Install ngrok
npm install -g ngrok

# Start server in one terminal
python -m src.api_server

# Expose in another terminal
ngrok http 8000
```

You'll get a public URL like: `https://abc123.ngrok.io`

**Pros:** 
- ✅ Free tier available
- ✅ HTTPS included
- ✅ No configuration needed

**Cons:**
- ❌ URL changes on restart (unless paid)
- ❌ Rate limits on free tier

### Option 3: Cloudflare Tunnel (Free & Secure)

```bash
# Install cloudflared
# macOS
brew install cloudflared

# Ubuntu/Debian
curl -fsSL https://pkg.cloudflare.com/cloudflared.gpg | sudo apt-key add -
echo "deb https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared

# Run tunnel
cloudflared tunnel --url http://localhost:8000
```

### Option 4: Deploy to Cloud

#### Render.com (Free Tier)

1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect your repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python -m src.api_server`
6. Set environment variables (API keys)
7. Deploy!

#### Railway.app

1. Visit railway.app
2. Deploy from GitHub
3. Add environment variables
4. Automatic deployment

#### Hugging Face Spaces

1. Create new Space (Docker type)
2. Upload code
3. Add secrets (API keys)
4. Deploy with GPU option

---

## 🚀 Deployment Options

### Development
```bash
python -m src.api_server --reload
```

### Production with Gunicorn

```bash
# Install
pip install gunicorn uvicorn

# Run
gunicorn src.api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "src.api_server:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t youtube-ai-studio .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  youtube-ai-studio
```

### Docker Compose

```yaml
version: '3.8'

services:
  youtube-ai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
    volumes:
      - ./output:/app/output
      - ./cache:/app/cache
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Server Won't Start

**Problem:** Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 $(lsof -t -i:8000)

# Restart
python -m src.api_server
```

**Problem:** Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

#### 2. API Errors

**Problem:** Invalid API key
- Verify key in `.env` file
- Check key has correct permissions
- Ensure billing is enabled (for OpenAI)

**Problem:** Rate limits
- Wait and retry
- Upgrade API plan
- Implement exponential backoff

#### 3. Video Generation Fails

**Problem:** FFmpeg not installed
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

**Problem:** Out of disk space
```bash
# Check space
df -h

# Clean cache
rm -rf cache/* temp/*
```

#### 4. Can't Access from Other Devices

- Check firewall settings
- Ensure server binds to `0.0.0.0` not `127.0.0.1`
- Verify same network
- Try disabling antivirus temporarily

#### 5. Slow Performance

- Reduce batch count
- Lower video quality preset
- Use faster AI provider (Gemini typically fastest)
- Increase server resources

### Checking Logs

```bash
# Server logs
tail -f /tmp/server.log

# Application logs
cat temp/agent.log

# Python debug mode
python -m src.api_server --log-level debug
```

---

## ❓ FAQ

### Q: Is this free to use?
**A:** The code is free, but AI APIs have costs:
- Google Gemini: Free tier available (60 requests/min)
- OpenAI: Pay-per-use (~$0.01-0.10 per video)
- Anthropic: Pay-per-use
- ElevenLabs: Free tier (10k chars/month)

### Q: How long does video generation take?
**A:** Typically 30-90 seconds depending on:
- Video length
- AI provider speed
- Server resources
- Enabled features

### Q: Can I use this commercially?
**A:** Yes! But ensure:
- You have rights to generated content
- Comply with AI provider ToS
- Use royalty-free music/footage

### Q: What's the maximum video length?
**A:** Configurable up to 600 seconds (10 minutes). Edit `config.py` for longer.

### Q: Does it work offline?
**A:** No, requires internet for AI APIs. Once generated, videos work offline.

### Q: Can I customize the AI prompts?
**A:** Yes! Edit prompt templates in `src/agents/planner.py`

### Q: How do I add custom voices?
**A:** Modify voice profiles in `src/config.py` or integrate custom TTS in `src/audio/`

### Q: Can I upload my own footage?
**A:** Currently uses AI-generated/stock footage. Custom footage support coming soon.

### Q: Does it auto-upload to YouTube?
**A:** Not yet. Manual download for now. YouTube API integration planned.

### Q: Multiple users simultaneously?
**A:** Yes! Supports concurrent jobs. Configure `MAX_CONCURRENT_JOBS` in env.

---

## 📊 Performance Benchmarks

| Configuration | Avg Generation Time | Cost per Video |
|---------------|---------------------|----------------|
| Shorts, Gemini, Basic | 30-45s | ~$0.01 |
| Shorts, GPT-4, All Features | 45-60s | ~$0.05 |
| Landscape, Claude, Premium | 60-90s | ~$0.10 |
| Batch x5, Mixed | 3-5 min total | ~$0.15 |

*Costs vary by API provider and usage tier*

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Setup

```bash
# Clone fork
git clone https://github.com/YOUR_USERNAME/advanced-youtube-ai-agent.git

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Code formatting
black src/

# Type checking
mypy src/
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Patent use

Required:
- ⚠️ Include license and copyright notice
- ⚠️ State changes made

---

## 🙏 Acknowledgments

Built with:
- [Google Gemini](https://ai.google.dev/) - AI content generation
- [OpenAI GPT-4](https://openai.com/) - Alternative AI provider
- [Anthropic Claude](https://anthropic.com/) - Advanced reasoning
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [ElevenLabs](https://elevenlabs.io/) - Voice synthesis
- [Pexels/Pixabay](https://pexels.com/) - Stock footage

---

## 📞 Support & Community

- **Documentation**: This README + `/workspace/README_SERVER.md`
- **Issues**: GitHub Issues tab
- **Discussions**: GitHub Discussions tab
- **Email**: your-email@example.com

### Additional Resources

- [API Documentation](http://localhost:8000/api/docs)
- [Server Guide](README_SERVER.md)
- [Configuration Examples](examples/)
- [Video Tutorials](tutorials/) *(coming soon)*

---

## 🎯 Roadmap

### v1.0 (Current)
- ✅ Multi-provider AI support
- ✅ Web interface
- ✅ REST API
- ✅ Real-time progress
- ✅ Multiple formats

### v1.1 (Next Release)
- 🔄 YouTube auto-upload
- 🔄 Custom footage upload
- 🔄 Template library
- 🔄 User authentication
- 🔄 Payment integration

### v2.0 (Future)
- 📋 Multi-language support
- 📋 Advanced editing UI
- 📋 Collaboration features
- 📋 Analytics dashboard
- 📋 Mobile app

---

**Made with ❤️ by the YouTube AI Studio Team**

*Transform your ideas into viral videos with AI!*

🚀 **Get started now:** `python -m src.api_server`
