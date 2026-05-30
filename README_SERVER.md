# 🚀 YouTube AI Studio - Complete Server & API Documentation

**Your professional YouTube video generation platform with real-time web interface and REST API!**

This comprehensive guide covers everything you need to run, share, and deploy your AI-powered YouTube studio.

---

## 📖 Table of Contents

1. [Quick Start](#quick-start)
2. [Web Interface Guide](#web-interface-guide)
3. [Complete API Reference](#complete-api-reference)
4. [Sharing & Access](#sharing--access)
5. [Production Deployment](#production-deployment)
6. [Advanced Configuration](#advanced-configuration)
7. [Code Examples](#code-examples)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)
10. [Performance Optimization](#performance-optimization)

---

## ⚡ Quick Start

### 1-Minute Setup

```bash
# Step 1: Install dependencies (if not done)
pip install -r requirements.txt

# Step 2: Set your API keys
export GEMINI_API_KEY="your-gemini-key-here"

# Step 3: Start the server
python -m src.api_server

# Step 4: Open browser
# Navigate to: http://localhost:8000
```

**That's it!** You're now running a full-stack AI video generation platform! 🎉

---

## 🖥️ Web Interface Guide

### Dashboard Walkthrough

When you open **http://localhost:8000**, you'll see a modern, intuitive interface:

#### 📝 Input Section

**Topic Field**
- Enter any topic (5-500 characters)
- Examples:
  - "10 Amazing Facts About Space"
  - "How Quantum Computers Work"
  - "The History of Artificial Intelligence"
  - "5 Minute Morning Routine for Success"

**Format Selection**
- 📱 **Shorts (9:16)** - Vertical video for YouTube Shorts, TikTok, Instagram Reels
  - Resolution: 1080x1920
  - Best for: Quick tips, facts, viral content
  
- 📺 **Standard (1:1)** - Square format
  - Resolution: 1080x1080
  - Best for: Instagram posts, product showcases
  
- 🎬 **Landscape (16:9)** - Traditional YouTube format
  - Resolution: 1920x1080
  - Best for: Long-form content, tutorials, documentaries

**Voice Profile**
- 🤖 **Default** - Balanced, neutral tone
- 📖 **Narrator** - Slower, authoritative (speed: 0.9, pitch: -2)
- ⚡ **Energetic** - Fast, enthusiastic (speed: 1.1, pitch: +2)
- 🧘 **Calm** - Relaxed, soothing (speed: 0.85, pitch: -1)

#### 🎛️ AI Features Toggles

**🎣 Viral Hooks**
- Generates 3 different opening variations
- A/B test to find the most engaging intro
- Recommended for: All content types

**😊 Sentiment Analysis**
- Analyzes emotional tone of script
- Matches voice modulation to content emotion
- Adjusts visual pacing accordingly
- Recommended for: Storytelling, emotional content

**😄 Auto Emoji**
- Intelligently inserts relevant emojis
- Increases engagement by up to 30%
- Context-aware placement
- Recommended for: Shorts, social media content

**🎬 Smart Transitions**
- AI-suggested scene transitions
- Smooth fades, cuts, and effects
- Professional polish
- Recommended for: All videos

#### ⚙️ Advanced Settings

**AI Provider Selection**
- **Auto** (Recommended) - Automatically selects best available provider
  - Priority: Gemini → OpenAI → Anthropic
  - Falls back gracefully if one fails
  
- **Gemini** - Google's latest AI
  - Fastest response times
  - Great for factual content
  - Free tier available
  
- **OpenAI** - GPT-4 powered
  - Excellent creative writing
  - Best for storytelling
  - Higher cost
  
- **Anthropic** - Claude models
  - Strong reasoning capabilities
  - Best for complex topics
  - Medium cost

**Duration Slider**
- Range: 10-600 seconds
- Recommended:
  - Shorts: 30-60 seconds
  - Standard: 60-120 seconds
  - Landscape: 120-300 seconds

**Batch Count**
- Generate 1-10 videos simultaneously
- Useful for:
  - A/B testing different hooks
  - Creating series content
  - Bulk content creation

#### 📊 Progress Tracker

Real-time visualization of the generation pipeline:

1. **Planning** (5-10s)
   - Topic research
   - Outline generation
   - Scene planning

2. **Script Writing** (10-20s)
   - Full script generation
   - Hook creation
   - SEO optimization

3. **Voice Synthesis** (10-30s)
   - Text-to-speech conversion
   - Emotion matching
   - Audio processing

4. **Visual Generation** (15-40s)
   - Image/video creation
   - Stock footage selection
   - Thumbnail generation

5. **Video Editing** (10-20s)
   - Scene assembly
   - Transitions
   - Music integration
   - Subtitle syncing

6. **Finalizing** (5-10s)
   - Quality check
   - Encoding
   - Upload preparation

**Total Time: 30-90 seconds** (varies by duration and features)

#### 💾 Download Section

Once complete, you get:
- **Video File** (MP4, H.264 codec)
- **Thumbnail** (JPG, 1280x720)
- **Script** (TXT, full text)
- **Metadata** (JSON, titles, descriptions, tags)

---

## 🔌 Complete API Reference

### Base Information

**Base URL:** `http://localhost:8000/api`

**Authentication:** Currently open (add auth for production)

**Rate Limits:** Configurable (default: 100 requests/hour)

**Response Format:** JSON

### Endpoints

#### 1. Generate Video

**Endpoint:** `POST /api/generate`

**Description:** Start a new video generation job

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "topic": "string (required, 5-500 chars)",
  "format_type": "shorts|standard|landscape",
  "voice_profile": "default|narrator|energetic|calm",
  "ai_provider": "auto|gemini|openai|anthropic",
  "enable_hooks": true|false,
  "enable_sentiment": true|false,
  "enable_emoji": true|false,
  "enable_transitions": true|false,
  "duration_seconds": 10-600,
  "batch_count": 1-10,
  "quality_preset": "low|medium|high|ultra",
  "include_thumbnail": true|false,
  "include_subtitles": true|false
}
```

**Success Response (202 Accepted):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Job queued successfully",
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T10:31:30Z",
  "queue_position": 2
}
```

**Error Responses:**

*400 Bad Request:*
```json
{
  "error": "Validation failed",
  "details": {
    "topic": "Topic is too short (minimum 5 characters)"
  }
}
```

*429 Too Many Requests:*
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 3600
}
```

*500 Internal Server Error:*
```json
{
  "error": "Internal server error",
  "message": "Detailed error message"
}
```

---

#### 2. Check Job Status

**Endpoint:** `GET /api/status/{job_id}`

**Description:** Get current status and progress of a generation job

**Path Parameters:**
- `job_id` (string, UUID): The job identifier

**Success Response (200 OK):**

*While Processing:*
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 65,
  "current_stage": "visual_generation",
  "message": "Generating visuals for scene 3 of 5...",
  "stages_completed": ["planning", "scripting", "voice_synthesis"],
  "stages_remaining": ["video_editing", "finalizing"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:45Z",
  "estimated_completion": "2024-01-15T10:31:30Z"
}
```

*Completed:*
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "message": "Video generation complete!",
  "result": {
    "video_url": "/api/videos/video_550e8400.mp4",
    "video_filename": "video_550e8400.mp4",
    "download_url": "/api/download/video_550e8400.mp4",
    "thumbnail_url": "/thumbnails/thumb_550e8400.jpg",
    "thumbnail_filename": "thumb_550e8400.jpg",
    "script_url": "/scripts/script_550e8400.txt",
    "duration_seconds": 60,
    "resolution": "1080x1920",
    "file_size_mb": 15.4,
    "metadata": {
      "title": "10 Mind-Blowing Space Facts",
      "description": "Discover amazing facts about space...",
      "tags": ["space", "science", "facts", "education"],
      "hook_variations": ["Hook 1...", "Hook 2...", "Hook 3..."]
    }
  },
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:31:28Z"
}
```

*Failed:*
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "progress": 45,
  "message": "Video generation failed",
  "error": "API rate limit exceeded for Gemini API",
  "error_code": "API_RATE_LIMIT",
  "retry_recommended": true,
  "retry_after_seconds": 60,
  "created_at": "2024-01-15T10:30:00Z",
  "failed_at": "2024-01-15T10:30:35Z"
}
```

---

#### 3. Download Video

**Endpoint:** `GET /api/download/{filename}`

**Description:** Download the generated video file

**Path Parameters:**
- `filename` (string): Video filename from job result

**Response:**
- Content-Type: video/mp4
- Content-Disposition: attachment; filename="video.mp4"
- Binary video data

**Example:**
```bash
curl -O http://localhost:8000/api/download/video_550e8400.mp4
```

---

#### 4. Stream Video

**Endpoint:** `GET /api/videos/{filename}`

**Description:** Stream video directly in browser (no download)

**Path Parameters:**
- `filename` (string): Video filename

**Features:**
- Supports HTTP range requests (seekable playback)
- Compatible with HTML5 video player
- Chunked transfer for large files

**HTML Example:**
```html
<video controls width="100%">
  <source src="http://localhost:8000/api/videos/video_550e8400.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

---

#### 5. List All Jobs

**Endpoint:** `GET /api/jobs`

**Description:** Get list of all generation jobs (with filtering)

**Query Parameters:**
- `limit` (integer, default: 20): Max results to return
- `offset` (integer, default: 0): Pagination offset
- `status` (string, optional): Filter by status (pending/processing/completed/failed)
- `format_type` (string, optional): Filter by format

**Success Response (200 OK):**
```json
{
  "total": 156,
  "limit": 20,
  "offset": 0,
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "topic": "Space Facts",
      "status": "completed",
      "format_type": "shorts",
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:31:28Z"
    },
    // ... more jobs
  ],
  "has_more": true
}
```

---

#### 6. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check server health and API key status

**Success Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "active_jobs": 3,
  "completed_jobs_today": 47,
  "failed_jobs_today": 2,
  "avg_generation_time_seconds": 52,
  "api_keys_configured": {
    "gemini": true,
    "openai": true,
    "anthropic": false,
    "elevenlabs": true
  },
  "system_resources": {
    "cpu_usage_percent": 35.2,
    "memory_usage_percent": 62.1,
    "disk_free_gb": 125.4
  }
}
```

---

#### 7. Cancel Job

**Endpoint:** `POST /api/cancel/{job_id}`

**Description:** Cancel a pending or processing job

**Path Parameters:**
- `job_id` (string, UUID): Job to cancel

**Success Response (200 OK):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cancelled",
  "message": "Job cancelled successfully",
  "cancelled_at": "2024-01-15T10:30:15Z"
}
```

---

#### 8. Delete Job

**Endpoint:** `DELETE /api/jobs/{job_id}`

**Description:** Delete a job and its associated files

**Path Parameters:**
- `job_id` (string, UUID): Job to delete

**Success Response (200 OK):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Job and associated files deleted successfully",
  "files_deleted": ["video.mp4", "thumbnail.jpg", "script.txt"]
}
```

---

### Interactive Documentation

The server includes built-in interactive API docs:

**Swagger UI:** http://localhost:8000/api/docs
- Test endpoints directly in browser
- View request/response schemas
- See example values
- Authenticate (when enabled)

**ReDoc:** http://localhost:8000/api/redoc
- Clean, readable documentation
- Search functionality
- Print-friendly format

---

## 🌍 Sharing & Access

### Local Network Access

Anyone on your WiFi network can access your server:

#### Step 1: Find Your Local IP

**Linux/Mac:**
```bash
# Method 1
ipconfig getifaddr en0

# Method 2
ip addr show | grep inet

# Method 3
hostname -I | awk '{print $1}'
```

**Windows:**
```cmd
ipconfig | findstr IPv4
```

**Example Output:** `192.168.1.100`

#### Step 2: Share the URL

Tell users to visit:
```
http://192.168.1.100:8000
```

#### Step 3: Firewall Configuration (if needed)

**Ubuntu/Debian:**
```bash
sudo ufw allow 8000/tcp
```

**Windows Defender:**
1. Open Windows Defender Firewall
2. Advanced settings → Inbound Rules
3. New Rule → Port → TCP → 8000
4. Allow the connection

**macOS:**
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /path/to/python
```

---

### Public Internet Access

#### Option 1: ngrok (Easiest - Recommended for Testing)

**Installation:**
```bash
# macOS
brew install ngrok

# Windows
choco install ngrok

# Linux
npm install -g ngrok

# Or download from: https://ngrok.com/download
```

**Usage:**
```bash
# Start your server first
python -m src.api_server

# In a new terminal, expose it
ngrok http 8000
```

**Output:**
```
Forwarding    https://abc123def456.ngrok.io -> http://localhost:8000
```

**Share:** `https://abc123def456.ngrok.io`

**Pros:**
- ✅ Free tier available
- ✅ HTTPS automatically included
- ✅ No configuration needed
- ✅ Works behind NAT/firewalls
- ✅ Built-in inspection dashboard (http://127.0.0.1:4040)

**Cons:**
- ❌ URL changes on restart (paid plans offer reserved domains)
- ❌ Rate limits: 40 connections/min on free tier
- ❌ Single user on free tier (paid for more)

**Pro Tips:**
```bash
# Use a specific region
ngrok http 8000 --region=eu

# Add basic auth
ngrok http 8000 --basic-auth="username:password"

# Reserve a subdomain (paid)
ngrok http 8000 --subdomain=my-youtube-studio
```

---

#### Option 2: Cloudflare Tunnel (Free & Secure)

**Installation:**

**macOS:**
```bash
brew install cloudflared
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://pkg.cloudflare.com/cloudflared.gpg | sudo apt-key add -
echo "deb https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared
```

**Windows:**
```powershell
winget install cloudflare.cloudflared
```

**Quick Tunnel (No Account Needed):**
```bash
cloudflared tunnel --url http://localhost:8000
```

**Output:**
```
https://random-name.trycloudflare.com
```

**Permanent Tunnel (Requires Cloudflare Account):**
```bash
# Login
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create my-tunnel

# Configure
cloudflared tunnel route dns my-tunnel youtube.yourdomain.com

# Run
cloudflared tunnel run my-tunnel
```

**Config File (`~/.cloudflared/config.yml`):**
```yaml
tunnel: my-tunnel
credentials-file: /home/user/.cloudflared/my-tunnel.json

ingress:
  - hostname: youtube.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

**Pros:**
- ✅ Completely free
- ✅ Unlimited bandwidth
- ✅ Custom domain support
- ✅ DDoS protection
- ✅ SSL/TLS included
- ✅ Multiple users

**Cons:**
- ❌ Requires Cloudflare account for permanent tunnels
- ❌ Slightly more setup than ngrok

---

#### Option 3: Render.com (Free Cloud Hosting)

**Steps:**

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create account** at https://render.com

3. **New Web Service:**
   - Connect your GitHub repository
   - Choose branch: `main`
   - Root Directory: `/` (or leave blank)
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.api_server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

4. **Environment Variables:**
   ```
   GEMINI_API_KEY=your-key
   OPENAI_API_KEY=your-key
   ELEVENLABS_API_KEY=your-key
   PORT=8000
   ```

5. **Deploy!**

**Free Tier Limits:**
- 750 hours/month (enough for 24/7)
- 512 MB RAM
- Shared CPU
- Auto-sleep after 15 min inactivity (upgrade to prevent)

**Paid Plans:** From $7/month

---

#### Option 4: Railway.app

**Steps:**

1. Visit https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub repo
4. Add environment variables
5. Automatic deployment!

**Free Tier:**
- $5 trial credit
- Pay-as-you-go after
- Very affordable for low traffic

---

#### Option 5: Hugging Face Spaces

**Great for demos and sharing with community**

1. Create account at https://huggingface.co
2. New Space → Docker SDK
3. Upload code
4. Add secrets (API keys)
5. Deploy with GPU option if needed

**Free Tier:**
- CPU: 2 vCPU, 16GB RAM
- GPU: Available (limited hours)
- Public by default

---

#### Option 6: Google Colab (Temporary Public Access)

**For quick demos:**

```python
# In Colab cell
!pip install -r requirements.txt
!pip install pyngrok

from pyngrok import ngrok

# Start server in background
get_ipython().system('python -m src.api_server &')

# Expose
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")
```

**Limitations:**
- Session expires after ~12 hours
- Need to rerun on disconnect
- Not suitable for production

---

## 🛠️ Production Deployment

### Docker Deployment

#### Dockerfile

Create `Dockerfile` in root directory:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p output cache temp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "src.api_server:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

#### Build and Run

```bash
# Build image
docker build -t youtube-ai-studio:latest .

# Run container
docker run -d \
  --name youtube-ai \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key_here \
  -e OPENAI_API_KEY=your_key_here \
  -e ELEVENLABS_API_KEY=your_key_here \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/cache:/app/cache \
  --restart unless-stopped \
  youtube-ai-studio:latest

# View logs
docker logs -f youtube-ai

# Stop container
docker stop youtube-ai

# Remove container
docker rm youtube-ai
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  youtube-ai:
    build: .
    container_name: youtube-ai-studio
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - PEXELS_API_KEY=${PEXELS_API_KEY}
      - HOST=0.0.0.0
      - PORT=8000
      - MAX_CONCURRENT_JOBS=5
    volumes:
      - ./output:/app/output
      - ./cache:/app/cache
      - ./temp:/app/temp
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G

  # Optional: Redis for job queue (future enhancement)
  redis:
    image: redis:7-alpine
    container_name: youtube-ai-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

**Run with Docker Compose:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

### Kubernetes Deployment (Advanced)

For enterprise-scale deployments:

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: youtube-ai-studio
spec:
  replicas: 3
  selector:
    matchLabels:
      app: youtube-ai
  template:
    metadata:
      labels:
        app: youtube-ai
    spec:
      containers:
      - name: youtube-ai
        image: your-registry/youtube-ai-studio:latest
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: gemini
        - name: MAX_CONCURRENT_JOBS
          value: "5"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: youtube-ai-service
spec:
  selector:
    app: youtube-ai
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## ⚙️ Advanced Configuration

### Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GEMINI_API_KEY` | string | None | Google Gemini API key |
| `OPENAI_API_KEY` | string | None | OpenAI API key |
| `ANTHROPIC_API_KEY` | string | None | Anthropic Claude API key |
| `ELEVENLABS_API_KEY` | string | None | ElevenLabs voice API key |
| `PEXELS_API_KEY` | string | None | Pexels stock footage API key |
| `PIXABAY_API_KEY` | string | None | Pixabay API key |
| `HOST` | string | `0.0.0.0` | Server bind address |
| `PORT` | integer | `8000` | Server port |
| `MAX_CONCURRENT_JOBS` | integer | `5` | Max parallel generations |
| `JOB_TIMEOUT_SECONDS` | integer | `600` | Job timeout (10 min) |
| `ENABLE_AUTHENTICATION` | boolean | `false` | Enable API auth |
| `API_KEY_SECRET` | string | None | Secret for JWT tokens |
| `RATE_LIMIT_PER_HOUR` | integer | `100` | API rate limit |
| `LOG_LEVEL` | string | `INFO` | Logging level |
| `ENABLE_JSON_LOGS` | boolean | `false` | JSON structured logs |
| `OUTPUT_DIRECTORY` | string | `./output` | Video output path |
| `CACHE_DIRECTORY` | string | `./cache` | Cache path |
| `CLEANUP_OLD_JOBS_HOURS` | integer | `24` | Auto-delete old jobs |

### config.py Customization

Edit `src/config.py` for advanced settings:

```python
# AI Provider Configuration
AI_PROVIDER_PRIORITY = ["gemini", "openai", "anthropic"]
AI_RETRY_ATTEMPTS = 3
AI_TIMEOUT_SECONDS = 30

# Video Generation Settings
DEFAULT_DURATION = 60
MIN_DURATION = 10
MAX_DURATION = 600
DEFAULT_FORMAT = "shorts"

# Quality Presets
QUALITY_PRESETS = {
    "low": {
        "resolution": "480p",
        "bitrate": "1000k",
        "fps": 24
    },
    "medium": {
        "resolution": "720p",
        "bitrate": "2500k",
        "fps": 30
    },
    "high": {
        "resolution": "1080p",
        "bitrate": "5000k",
        "fps": 30
    },
    "ultra": {
        "resolution": "4k",
        "bitrate": "15000k",
        "fps": 60
    }
}

# Voice Configuration
VOICE_PROFILES = {
    "default": {"speed": 1.0, "pitch": 0, "volume": 1.0},
    "narrator": {"speed": 0.9, "pitch": -2, "volume": 1.1},
    "energetic": {"speed": 1.1, "pitch": 2, "volume": 1.2},
    "calm": {"speed": 0.85, "pitch": -1, "volume": 0.9}
}

# Feature Flags
FEATURES = {
    "sentiment_analysis": True,
    "auto_emoji": True,
    "viral_hooks": True,
    "smart_transitions": True,
    "batch_processing": True,
    "analytics_tracking": True,
    "seo_optimization": True,
    "thumbnail_generation": True,
    "subtitle_generation": True
}

# Pipeline Settings
PIPELINE_TIMEOUT = 600  # 10 minutes
STAGE_TIMEOUTS = {
    "planning": 30,
    "scripting": 60,
    "voice_synthesis": 90,
    "visual_generation": 120,
    "video_editing": 60,
    "finalizing": 30
}

# Storage Settings
MAX_STORAGE_GB = 50
AUTO_CLEANUP = True
CLEANUP_INTERVAL_HOURS = 6
KEEP_COMPLETED_JOBS_DAYS = 7
```

---

## 💻 Code Examples

### Python Client Library

Create a reusable client:

```python
# youtube_ai_client.py
import requests
import time
from typing import Optional, Dict, Any

class YouTubeAIClient:
    """Client for YouTube AI Studio API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def generate_video(
        self,
        topic: str,
        format_type: str = "shorts",
        voice_profile: str = "default",
        enable_hooks: bool = True,
        enable_sentiment: bool = True,
        enable_emoji: bool = True,
        duration: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """Start video generation"""
        
        payload = {
            "topic": topic,
            "format_type": format_type,
            "voice_profile": voice_profile,
            "enable_hooks": enable_hooks,
            "enable_sentiment": enable_sentiment,
            "enable_emoji": enable_emoji,
            "duration_seconds": duration,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_status(self, job_id: str) -> Dict[str, Any]:
        """Check job status"""
        
        response = self.session.get(
            f"{self.base_url}/api/status/{job_id}"
        )
        response.raise_for_status()
        
        return response.json()
    
    def wait_for_completion(
        self,
        job_id: str,
        poll_interval: int = 2,
        timeout: int = 600
    ) -> Dict[str, Any]:
        """Poll until job completes or fails"""
        
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Job {job_id} timed out")
            
            status = self.get_status(job_id)
            
            if status['status'] == 'completed':
                return status
            elif status['status'] == 'failed':
                raise Exception(f"Job failed: {status.get('error', 'Unknown error')}")
            
            print(f"Progress: {status['progress']}% - {status['message']}")
            time.sleep(poll_interval)
    
    def download_video(
        self,
        filename: str,
        save_path: str = "."
    ) -> str:
        """Download video file"""
        
        response = self.session.get(
            f"{self.base_url}/api/download/{filename}",
            stream=True
        )
        response.raise_for_status()
        
        filepath = f"{save_path}/{filename}"
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        
        return filepath
    
    def create_video(
        self,
        topic: str,
        save_path: str = ".",
        **kwargs
    ) -> Dict[str, Any]:
        """Complete workflow: generate, wait, download"""
        
        print(f"Starting generation for: {topic}")
        
        # Start generation
        job = self.generate_video(topic=topic, **kwargs)
        job_id = job['job_id']
        
        print(f"Job ID: {job_id}")
        print("Generating video...")
        
        # Wait for completion
        result = self.wait_for_completion(job_id)
        
        # Download
        video_filename = result['result']['video_filename']
        filepath = self.download_video(video_filename, save_path)
        
        print(f"Video saved to: {filepath}")
        
        return {
            'job_id': job_id,
            'filepath': filepath,
            'metadata': result['result']['metadata']
        }

# Usage Example
if __name__ == "__main__":
    client = YouTubeAIClient()
    
    try:
        result = client.create_video(
            topic="10 Mind-Blowing Quantum Physics Facts",
            format_type="shorts",
            voice_profile="energetic",
            enable_hooks=True
        )
        print(f"Success! Video: {result['filepath']}")
    except Exception as e:
        print(f"Error: {e}")
```

### Node.js Client

```javascript
// youtube-ai-client.js
const axios = require('axios');

class YouTubeAIClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.client = axios.create({ baseURL: baseUrl });
  }

  async generateVideo(options) {
    const response = await this.client.post('/api/generate', options);
    return response.data;
  }

  async getStatus(jobId) {
    const response = await this.client.get(`/api/status/${jobId}`);
    return response.data;
  }

  async waitForCompletion(jobId, pollInterval = 2000, timeout = 600000) {
    const startTime = Date.now();
    
    while (true) {
      if (Date.now() - startTime > timeout) {
        throw new Error(`Job ${jobId} timed out`);
      }
      
      const status = await this.getStatus(jobId);
      
      if (status.status === 'completed') {
        return status;
      } else if (status.status === 'failed') {
        throw new Error(`Job failed: ${status.error}`);
      }
      
      console.log(`Progress: ${status.progress}% - ${status.message}`);
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  }

  async downloadVideo(filename, savePath) {
    const response = await this.client.get(`/api/download/${filename}`, {
      responseType: 'stream'
    });
    
    const fs = require('fs');
    const writer = fs.createWriteStream(`${savePath}/${filename}`);
    
    response.data.pipe(writer);
    
    return new Promise((resolve, reject) => {
      writer.on('finish', () => resolve(`${savePath}/${filename}`));
      writer.on('error', reject);
    });
  }

  async createVideo(topic, options = {}) {
    console.log(`Starting generation for: ${topic}`);
    
    const job = await this.generateVideo({ topic, ...options });
    console.log(`Job ID: ${job.job_id}`);
    
    const result = await this.waitForCompletion(job.job_id);
    const filepath = await this.downloadVideo(
      result.result.video_filename,
      '.'
    );
    
    console.log(`Video saved to: ${filepath}`);
    
    return {
      jobId: job.job_id,
      filepath,
      metadata: result.result.metadata
    };
  }
}

// Usage
(async () => {
  const client = new YouTubeAIClient();
  
  try {
    const result = await client.createVideo(
      "10 Amazing Space Facts",
      { format_type: "shorts", voice_profile: "energetic" }
    );
    console.log('Success!', result);
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

### cURL Examples

```bash
# Generate video
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Quantum Computing Explained",
    "format_type": "landscape",
    "voice_profile": "narrator",
    "duration_seconds": 120
  }'

# Check status
curl http://localhost:8000/api/status/550e8400-e29b-41d4-a716-446655440000

# Download video
curl -O http://localhost:8000/api/download/video_550e8400.mp4

# List all jobs
curl "http://localhost:8000/api/jobs?limit=10&status=completed"

# Health check
curl http://localhost:8000/api/health

# Cancel job
curl -X POST http://localhost:8000/api/cancel/550e8400-e29b-41d4-a716-446655440000

# Delete job
curl -X DELETE http://localhost:8000/api/jobs/550e8400-e29b-41d4-a716-446655440000
```

---

## 🆘 Troubleshooting

### Common Issues & Solutions

#### 1. Server Won't Start

**Error: Address already in use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 $(lsof -t -i:8000)

# Or change port
export PORT=8001
python -m src.api_server
```

**Error: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade --force-reinstall
```

**Error: FFmpeg not found**
```bash
# Install FFmpeg
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

#### 2. API Key Issues

**Error: API key invalid**
- Double-check key in `.env` file
- Ensure no extra spaces or quotes
- Verify key has correct permissions
- Check billing is enabled (OpenAI requires credit card)

**Error: Rate limit exceeded**
```python
# Implement retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_with_retry():
    # Your API call here
    pass
```

**Error: Quota exceeded**
- Upgrade API plan
- Reduce batch size
- Implement request queuing
- Use multiple API keys (rotate)

#### 3. Video Generation Failures

**Error: Out of disk space**
```bash
# Check disk usage
df -h

# Clean old files
rm -rf output/* cache/* temp/*

# Or set auto-cleanup
export CLEANUP_OLD_JOBS_HOURS=12
```

**Error: Memory error**
```bash
# Reduce concurrent jobs
export MAX_CONCURRENT_JOBS=2

# Lower quality preset
# In request: "quality_preset": "medium"
```

**Error: Timeout**
```bash
# Increase timeout
export JOB_TIMEOUT_SECONDS=900

# Or reduce video duration
# In request: "duration_seconds": 30
```

#### 4. Network Access Issues

**Can't access from other devices**
```bash
# Verify server is listening on 0.0.0.0
netstat -tlnp | grep 8000

# Should show: 0.0.0.0:8000
# If shows 127.0.0.1:8000, set:
export HOST=0.0.0.0
```

**Firewall blocking**
```bash
# Ubuntu
sudo ufw allow 8000/tcp
sudo ufw status

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# Windows
netsh advfirewall firewall add rule name="YouTube AI" dir=in action=allow protocol=TCP localport=8000
```

#### 5. Performance Issues

**Slow generation**
- Use Gemini (fastest provider)
- Reduce video duration
- Lower quality preset
- Disable unnecessary features
- Increase server resources

**High CPU usage**
```bash
# Monitor resources
htop

# Limit workers
export WORKERS=2

# Or use lighter gunicorn config
gunicorn src.api_server:app --workers 2 --threads 2
```

#### 6. Debugging

**Enable debug logging**
```bash
export LOG_LEVEL=DEBUG
python -m src.api_server
```

**View detailed logs**
```bash
# Application logs
tail -f temp/agent.log

# Server logs
tail -f /tmp/server.log

# Docker logs
docker logs -f youtube-ai
```

**Test individual components**
```bash
# Test AI connection
python -c "from src.agents.planner import AIPlanner; print(AIPlanner().test_connection())"

# Test video pipeline
python -m tests.test_pipeline

# Test API endpoint
curl http://localhost:8000/api/health | jq
```

---

## 🔒 Security Best Practices

### For Production Deployments

#### 1. Enable Authentication

**Add API Key Auth:**
```python
# In api_server.py
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY_SECRET")
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key

@app.post("/api/generate")
async def generate(api_key: str = Depends(get_api_key)):
    # Protected endpoint
    pass
```

**Usage:**
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"topic": "..."}'
```

#### 2. Enable HTTPS

**With Let's Encrypt:**
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d youtube.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

**With nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name youtube.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name youtube.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/youtube.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/youtube.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. Rate Limiting

```python
from slowapi import SlowAPI, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

app.state.limiter = SlowAPI()
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/generate")
@rate_limit("10/minute")
async def generate():
    pass
```

#### 4. Input Validation

```python
from pydantic import BaseModel, Field, validator

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=500)
    format_type: str = Field(default="shorts")
    duration_seconds: int = Field(default=60, ge=10, le=600)
    
    @validator('topic')
    def validate_topic(cls, v):
        # Sanitize input
        v = v.strip()
        if not v:
            raise ValueError("Topic cannot be empty")
        return v
```

#### 5. Environment Security

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use secrets management
# AWS Secrets Manager, HashiCorp Vault, etc.

# Restrict file permissions
chmod 600 .env
```

---

## ⚡ Performance Optimization

### Tuning for Speed

#### 1. Optimize AI Calls

```python
# Use streaming responses
response = model.generate_content(prompt, stream=True)

# Parallel processing
import asyncio
results = await asyncio.gather(
    generate_script(),
    generate_images(),
    generate_voice()
)
```

#### 2. Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_ai_response(prompt_hash):
    # Return cached result
    pass
```

#### 3. Resource Management

```python
# Limit concurrent operations
import asyncio
semaphore = asyncio.Semaphore(5)

async def process_with_limit():
    async with semaphore:
        await process()
```

#### 4. Database Optimization (Future)

```python
# Use PostgreSQL instead of in-memory storage
# Add indexes for faster queries
# Implement connection pooling
```

---

## 📊 Monitoring & Analytics

### Add Monitoring

```python
# Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

# Access metrics at: /metrics
```

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🎓 Learning Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Docker Best Practices**: https://docs.docker.com/develop/
- **API Design Guide**: https://cloud.google.com/apis/design
- **Production Checklist**: https://fastapi.tiangolo.com/deployment/

---

## 📞 Support

**Need Help?**

- 📖 Read main README.md for general overview
- 🐛 Report bugs on GitHub Issues
- 💬 Ask questions in GitHub Discussions
- 📧 Email: support@example.com

**Contributing:**
We welcome contributions! See CONTRIBUTING.md for guidelines.

---

**Made with ❤️ | YouTube AI Studio v1.0**

*Empowering creators with AI-powered video generation*
