# 🚀 YouTube AI Studio - Real-Time Video Generation Server

Your YouTube AI automation pipeline is now accessible in **real-time** via a modern web interface and REST API!

## ✅ What's Been Added

### 1. **Web Interface** (No coding required!)
- Beautiful, responsive UI for generating videos
- Real-time progress tracking
- Download generated videos instantly
- Configure all AI features visually

### 2. **REST API** (For developers)
- Full programmatic access to video generation
- Swagger/OpenAPI documentation
- Job queue management
- Status polling endpoints

### 3. **Multi-User Support**
- Share the server URL with anyone on your network
- Multiple concurrent jobs supported
- Job isolation with unique IDs

---

## 🎯 How to Use It

### Option 1: Web Interface (Easiest)

1. **Start the server:**
   ```bash
   python -m src.api_server
   ```

2. **Open your browser:**
   - Local: http://localhost:8000
   - From other devices: http://YOUR_IP:8000

3. **Generate videos:**
   - Enter your topic
   - Choose format (Shorts/Standard/Landscape)
   - Select voice profile
   - Toggle AI features (hooks, sentiment, emoji)
   - Click "Generate Video"
   - Watch real-time progress
   - Download when complete!

### Option 2: REST API (For Developers)

**Start a generation job:**
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of Quantum Computing",
    "format_type": "shorts",
    "voice_profile": "energetic",
    "ai_provider": "auto",
    "enable_hooks": true,
    "enable_sentiment": true,
    "enable_emoji": true
  }'
```

**Check job status:**
```bash
curl http://localhost:8000/api/status/{job_id}
```

**Download video:**
```bash
curl -O http://localhost:8000/api/download/{filename}
```

**Interactive API Docs:**
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## 🌐 Making It Accessible to Others

### Local Network Access
The server already binds to `0.0.0.0:8000`, so anyone on your network can access it:

1. **Find your IP address:**
   ```bash
   # Linux/Mac
   ip addr show | grep inet
   
   # Windows
   ipconfig
   ```

2. **Share this URL with others:**
   ```
   http://YOUR_LOCAL_IP:8000
   ```
   Example: `http://192.168.1.100:8000`

### Public Internet Access (Recommended for remote users)

#### Using ngrok (Easiest - Free tier available)
```bash
# Install ngrok
npm install -g ngrok

# Start your server first, then expose it
ngrok http 8000
```
This gives you a public URL like: `https://abc123.ngrok.io`

#### Using Cloudflare Tunnel (Free & Secure)
```bash
# Install cloudflared
cloudflared tunnel --url http://localhost:8000
```

#### Deploy to Cloud Platforms
- **Render.com**: Free tier, auto-deploy from GitHub
- **Railway.app**: Easy deployment with $5 credit
- **Hugging Face Spaces**: Free GPU options
- **Google Colab**: Run temporarily with public URL

---

## 📋 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/generate` | POST | Start video generation |
| `/api/status/{job_id}` | GET | Check job status |
| `/api/download/{filename}` | GET | Download video |
| `/api/videos/{filename}` | GET | Stream video |
| `/api/health` | GET | Health check |
| `/api/jobs` | GET | List all jobs |
| `/api/docs` | GET | Swagger UI documentation |
| `/api/redoc` | GET | ReDoc documentation |

---

## 🔧 Configuration Options

### Video Generation Parameters

| Parameter | Type | Options | Default |
|-----------|------|---------|---------|
| `topic` | string | Any text (5-500 chars) | Required |
| `format_type` | string | shorts, standard, landscape | shorts |
| `voice_profile` | string | default, narrator, energetic, calm | default |
| `ai_provider` | string | auto, gemini, openai, anthropic | auto |
| `enable_hooks` | boolean | true/false | true |
| `enable_sentiment` | boolean | true/false | true |
| `enable_emoji` | boolean | true/false | true |
| `duration_seconds` | integer | 10-600 | 60 |
| `batch_count` | integer | 1-10 | 1 |

---

## 🎨 Features Included

✅ **Real-time Progress Tracking** - Watch generation live  
✅ **Background Processing** - Non-blocking job queue  
✅ **Multiple AI Providers** - Auto-fallback between Gemini, GPT-4, Claude  
✅ **Viral Hook Generation** - A/B test multiple openings  
✅ **Sentiment Analysis** - Match voice/visuals to emotion  
✅ **Auto-Emoji** - Intelligent emoji insertion  
✅ **Voice Profiles** - Different personality tones  
✅ **Format Options** - Shorts, Standard, Landscape  
✅ **Download Links** - Direct video downloads  
✅ **API Documentation** - Interactive Swagger UI  
✅ **Health Monitoring** - System status endpoint  
✅ **Job Management** - Track all generation jobs  

---

## 🛠️ Production Deployment Tips

### For High Traffic:
1. **Use Redis** instead of in-memory job store
2. **Add authentication** (JWT tokens, API keys)
3. **Implement rate limiting**
4. **Use a task queue** (Celery + Redis/RabbitMQ)
5. **Add database** for persistent job history
6. **Enable HTTPS** with Let's Encrypt
7. **Set up monitoring** (Prometheus + Grafana)

### Environment Variables:
```bash
export GEMINI_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export ELEVENLABS_API_KEY="your-key"
export HOST="0.0.0.0"
export PORT="8000"
export MAX_CONCURRENT_JOBS="5"
```

---

## 🎬 Example Usage Flow

### Via Web Interface:
1. Open http://localhost:8000
2. Enter: "10 Mind-Blowing Facts About Space"
3. Select: Format = Shorts, Voice = Energetic
4. Enable: Viral Hooks ✓, Sentiment ✓, Emoji ✓
5. Click "Generate Video"
6. Wait ~30-60 seconds
7. Download your video!

### Via API (Python):
```python
import requests

# Start generation
response = requests.post('http://localhost:8000/api/generate', json={
    'topic': '10 Mind-Blowing Facts About Space',
    'format_type': 'shorts',
    'voice_profile': 'energetic'
})
job_id = response.json()['job_id']

# Poll for completion
import time
while True:
    status = requests.get(f'http://localhost:8000/api/status/{job_id}')
    data = status.json()
    
    if data['status'] == 'completed':
        print(f"Done! Download: {data['result']['download_url']}")
        break
    elif data['status'] == 'failed':
        print(f"Failed: {data['error']}")
        break
    
    print(f"Progress: {data['progress']}% - {data['message']}")
    time.sleep(2)
```

---

## 🆘 Troubleshooting

**Server won't start?**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
kill -9 $(lsof -t -i:8000)

# Restart server
python -m src.api_server
```

**Can't access from other devices?**
- Check firewall settings
- Ensure you're on the same network
- Try: `http://YOUR_IP:8000` instead of localhost

**Jobs stuck in "pending"?**
- Check API keys are configured
- Verify internet connection
- Check server logs: `tail -f /tmp/server.log`

---

## 📞 Next Steps

1. **Test locally**: http://localhost:8000
2. **Share with team**: Use your local IP
3. **Go public**: Use ngrok or deploy to cloud
4. **Customize**: Modify the UI or add new features
5. **Scale up**: Add Redis, auth, and monitoring for production

**Enjoy your AI-powered YouTube studio! 🎉**
