"""
YouTube AI Automation API Server
Provides REST API and Web Interface for real-time video generation
"""

import asyncio
import uuid
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Import our existing pipeline components
try:
    from src.config import Config
    from src.agents.planner import StoryboardPlanner
    from src.main import VideoPipeline
    PIPELINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Pipeline modules not fully available: {e}")
    PIPELINE_AVAILABLE = False
    # Mock classes for development
    class Config:
        @staticmethod
        def load(): return {}
    class StoryboardPlanner:
        def __init__(self, cfg): pass
        async def generate(self, topic, format_type="shorts"): 
            return {"scenes": [], "script": "Mock script", "metadata": {}}
    class VideoPipeline:
        def __init__(self, cfg): pass
        async def run(self, storyboard): 
            return {"status": "success", "output_path": "/tmp/mock_video.mp4"}

# Initialize FastAPI app
app = FastAPI(
    title="YouTube AI Automation API",
    description="Advanced AI-powered YouTube video generation with multi-provider support",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration
OUTPUT_DIR = Path("outputs/api_generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates and static files
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# In-memory job store (use Redis in production)
job_store: Dict[str, Dict[str, Any]] = {}

# ==================== Pydantic Models ====================

class VideoGenerationRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=1000, description="Video topic or prompt")
    format_type: str = Field(default="landscape", enum=["shorts", "standard", "landscape", "long_form"])
    voice_profile: str = Field(default="default", enum=["default", "narrator", "energetic", "calm", "documentary"])
    ai_provider: str = Field(default="auto", enum=["auto", "gemini", "openai", "anthropic"])
    enable_hooks: bool = Field(default=True, description="Generate viral hook variations")
    enable_sentiment: bool = Field(default=True, description="Analyze sentiment for voice/visual matching")
    enable_emoji: bool = Field(default=False, description="Auto-add emojis to script")
    duration_seconds: Optional[int] = Field(default=None, ge=60, le=3600, description="Video duration in seconds (1-60 minutes)")
    quality: str = Field(default="ultra", enum=["low", "medium", "high", "ultra", "4k"], description="Video quality preset")
    batch_count: int = Field(default=1, ge=1, le=5, description="Number of variations to generate")

class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: int  # 0-100
    message: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str

class BatchGenerationRequest(BaseModel):
    topics: List[str] = Field(..., min_items=1, max_items=20)
    format_type: str = Field(default="shorts")
    voice_profile: str = Field(default="default")

# ==================== Helper Functions ====================

def create_job_id() -> str:
    return str(uuid.uuid4())[:8]

def get_timestamp() -> str:
    return datetime.now().isoformat()

async def process_video_generation(job_id: str, request: VideoGenerationRequest):
    """Background task to generate video"""
    job_store[job_id]["status"] = "processing"
    job_store[job_id]["updated_at"] = get_timestamp()
    
    try:
        # Update progress
        job_store[job_id]["progress"] = 10
        job_store[job_id]["message"] = "Initializing AI pipeline..."
        
        # Load configuration
        config_data = Config.load() if PIPELINE_AVAILABLE else {}
        config_data.update({
            "ai_provider": request.ai_provider,
            "voice_profile": request.voice_profile,
            "enable_sentiment_analysis": request.enable_sentiment,
            "enable_auto_emoji": request.enable_emoji,
            "enable_viral_hooks": request.enable_hooks,
        })
        
        # Initialize pipeline
        job_store[job_id]["progress"] = 30
        job_store[job_id]["message"] = "Generating storyboard with AI..."
        
        planner = StoryboardPlanner(config_data)
        
        # Generate storyboard
        storyboard = await planner.generate(
            topic=request.topic,
            format_type=request.format_type
        )
        
        job_store[job_id]["progress"] = 60
        job_store[job_id]["message"] = "Creating video assets and synthesizing voice..."
        
        # Run video pipeline
        pipeline = VideoPipeline(config_data)
        result = await pipeline.run(storyboard)
        
        job_store[job_id]["progress"] = 90
        job_store[job_id]["message"] = "Finalizing video output..."
        
        # Save result
        output_filename = f"video_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = OUTPUT_DIR / output_filename
        
        # Mock output path for now (real implementation would copy actual file)
        if not PIPELINE_AVAILABLE:
            output_path.touch()  # Create empty file for demo
        
        job_store[job_id]["result"] = {
            "output_path": f"/api/videos/{output_filename}",
            "download_url": f"/api/download/{output_filename}",
            "storyboard": storyboard,
            "metrics": result.get("metrics", {}) if isinstance(result, dict) else {},
            "duration_seconds": request.duration_seconds or 300,
            "format": request.format_type,
            "quality": request.quality
        }
        
        job_store[job_id]["progress"] = 100
        job_store[job_id]["status"] = "completed"
        job_store[job_id]["message"] = "Video generation completed successfully!"
        
    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)
        job_store[job_id]["message"] = f"Generation failed: {str(e)}"
        job_store[job_id]["progress"] = 0
    
    job_store[job_id]["updated_at"] = get_timestamp()

# ==================== API Routes ====================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube AI Studio - Real-Time Video Generation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #444;
        }
        input[type="text"], select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .checkbox-group {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .status-card {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
            width: 0%;
        }
        .result-section {
            margin-top: 30px;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 12px;
            display: none;
        }
        .download-btn {
            display: inline-block;
            background: #4caf50;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 15px;
            font-weight: 600;
        }
        .api-info {
            margin-top: 40px;
            padding: 20px;
            background: #fff3cd;
            border-radius: 12px;
            border-left: 4px solid #ffc107;
        }
        .api-info a {
            color: #667eea;
            font-weight: 600;
        }
        .grid-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 YouTube AI Studio - Pro</h1>
        <p class="subtitle">Generate professional long-form videos (5-60 minutes) with AI in real-time</p>
        
        <form id="videoForm">
            <div class="form-group">
                <label for="topic">Video Topic / Prompt *</label>
                <textarea id="topic" name="topic" rows="3" placeholder="e.g., Complete Guide to Machine Learning - Full Documentary" required></textarea>
            </div>
            
            <div class="grid-options">
                <div class="form-group">
                    <label for="format_type">Format</label>
                    <select id="format_type" name="format_type">
                        <option value="landscape" selected>Landscape (16:9) - YouTube</option>
                        <option value="shorts">Shorts (9:16) - TikTok/Reels</option>
                        <option value="standard">Standard (1:1) - Instagram</option>
                        <option value="long_form">Long Form (16:9) - Documentary</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="voice_profile">Voice Profile</label>
                    <select id="voice_profile" name="voice_profile">
                        <option value="default">Default</option>
                        <option value="narrator">Narrator</option>
                        <option value="energetic">Energetic</option>
                        <option value="calm">Calm</option>
                        <option value="documentary">Documentary</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="quality">Quality</label>
                    <select id="quality" name="quality">
                        <option value="low">Low (480p)</option>
                        <option value="medium">Medium (720p)</option>
                        <option value="high" selected>High (1080p)</option>
                        <option value="ultra">Ultra (2K)</option>
                        <option value="4k">4K Ultra HD</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="duration_seconds">Duration (minutes)</label>
                    <select id="duration_minutes" name="duration_minutes">
                        <option value="5">5 minutes</option>
                        <option value="10">10 minutes</option>
                        <option value="15">15 minutes</option>
                        <option value="20">20 minutes</option>
                        <option value="30">30 minutes</option>
                        <option value="45">45 minutes</option>
                        <option value="60">60 minutes (1 hour)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="ai_provider">AI Provider</label>
                    <select id="ai_provider" name="ai_provider">
                        <option value="auto">Auto (Best Available)</option>
                        <option value="gemini">Google Gemini</option>
                        <option value="openai">OpenAI GPT-4</option>
                        <option value="anthropic">Anthropic Claude</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label>AI Features</label>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="enable_hooks" name="enable_hooks" checked>
                        <label for="enable_hooks" style="margin:0; font-weight:normal;">Viral Hooks</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="enable_sentiment" name="enable_sentiment" checked>
                        <label for="enable_sentiment" style="margin:0; font-weight:normal;">Sentiment Analysis</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="enable_emoji" name="enable_emoji">
                        <label for="enable_emoji" style="margin:0; font-weight:normal;">Auto Emoji</label>
                    </div>
                </div>
            </div>
            
            <button type="submit" id="generateBtn">🚀 Generate Video</button>
        </form>
        
        <div id="statusCard" class="status-card" style="display: none;">
            <h3>Generation Status</h3>
            <p id="statusMessage">Starting...</p>
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill"></div>
            </div>
            <p>Progress: <span id="progressText">0</span>%</p>
        </div>
        
        <div id="resultSection" class="result-section">
            <h3>✅ Video Generated Successfully!</h3>
            <p id="resultDetails"></p>
            <a id="downloadLink" class="download-btn" href="#" download>📥 Download Video</a>
        </div>
        
        <div class="api-info">
            <h3>🔌 Developer API Access</h3>
            <p>Integrate this into your own applications:</p>
            <ul style="margin: 10px 0 10px 20px;">
                <li>REST API Docs: <a href="/api/docs" target="_blank">/api/docs</a></li>
                <li>ReDoc Interface: <a href="/api/redoc" target="_blank">/api/redoc</a></li>
                <li>Health Check: <a href="/api/health" target="_blank">/api/health</a></li>
            </ul>
            <p style="font-size: 14px; color: #666;">Share the server URL with others to let them use it too!</p>
        </div>
    </div>
    
    <script>
        let jobId = null;
        let pollInterval = null;
        
        document.getElementById('videoForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.textContent = '⏳ Generating...';
            
            // Reset status
            document.getElementById('statusCard').style.display = 'block';
            document.getElementById('resultSection').style.display = 'none';
            
            const payload = {
                topic: document.getElementById('topic').value,
                format_type: document.getElementById('format_type').value,
                voice_profile: document.getElementById('voice_profile').value,
                ai_provider: document.getElementById('ai_provider').value,
                enable_hooks: document.getElementById('enable_hooks').checked,
                enable_sentiment: document.getElementById('enable_sentiment').checked,
                enable_emoji: document.getElementById('enable_emoji').checked,
                quality: document.getElementById('quality').value,
                duration_seconds: parseInt(document.getElementById('duration_minutes').value) * 60
            };
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                jobId = data.job_id;
                
                // Start polling
                pollInterval = setInterval(checkStatus, 2000);
                
            } catch (error) {
                alert('Error starting generation: ' + error.message);
                btn.disabled = false;
                btn.textContent = '🚀 Generate Video';
            }
        });
        
        async function checkStatus() {
            if (!jobId) return;
            
            try {
                const response = await fetch(`/api/status/${jobId}`);
                const data = await response.json();
                
                document.getElementById('statusMessage').textContent = data.message;
                document.getElementById('progressFill').style.width = data.progress + '%';
                document.getElementById('progressText').textContent = data.progress;
                
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    showResult(data);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').textContent = '🚀 Generate Another Video';
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    alert('Generation failed: ' + data.error);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').textContent = '🚀 Generate Video';
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        }
        
        function showResult(data) {
            const resultSection = document.getElementById('resultSection');
            const resultDetails = document.getElementById('resultDetails');
            const downloadLink = document.getElementById('downloadLink');
            
            const durationMinutes = Math.round(data.result.duration_seconds / 60);
            resultDetails.innerHTML = `
                <strong>Format:</strong> ${data.result.format}<br>
                <strong>Quality:</strong> ${data.result.quality || 'High'}<br>
                <strong>Duration:</strong> ${durationMinutes} minutes (${data.result.duration_seconds}s)<br>
                <strong>Scenes:</strong> ${data.result.storyboard.scenes?.length || 0}<br>
                <strong>Status:</strong> Ready to download!
            `;
            
            downloadLink.href = data.result.download_url;
            downloadLink.textContent = '📥 Download Video (' + (data.result.quality || 'HD') + ')';
            resultSection.style.display = 'block';
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/generate", response_model=Dict[str, str])
async def start_generation(request: VideoGenerationRequest, background_tasks: BackgroundTasks):
    """Start video generation job"""
    job_id = create_job_id()
    
    job_store[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "message": "Job queued",
        "request": request.dict(),
        "created_at": get_timestamp(),
        "updated_at": get_timestamp(),
        "result": None,
        "error": None
    }
    
    # Start background processing
    background_tasks.add_task(process_video_generation, job_id, request)
    
    return {"job_id": job_id, "status": "pending", "message": "Video generation started"}

@app.get("/api/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get job status"""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(**job_store[job_id])

@app.get("/api/videos/{filename}")
async def serve_video(filename: str):
    """Serve generated video"""
    video_path = OUTPUT_DIR / filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path, media_type="video/mp4", filename=filename)

@app.get("/api/download/{filename}")
async def download_video(filename: str):
    """Download generated video with proper headers"""
    video_path = OUTPUT_DIR / filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": get_timestamp(),
        "pipeline_available": PIPELINE_AVAILABLE,
        "active_jobs": len([j for j in job_store.values() if j["status"] in ["pending", "processing"]])
    }

@app.get("/api/jobs")
async def list_jobs(status: Optional[str] = None):
    """List all jobs (optionally filtered by status)"""
    jobs = list(job_store.values())
    if status:
        jobs = [j for j in jobs if j["status"] == status]
    return {"jobs": jobs, "count": len(jobs)}

if __name__ == "__main__":
    print("🚀 Starting YouTube AI Studio Server...")
    print("📱 Web Interface: http://localhost:8000")
    print("🔌 API Docs: http://localhost:8000/api/docs")
    print("🌐 Shareable: Use your machine's IP or ngrok for public access")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
