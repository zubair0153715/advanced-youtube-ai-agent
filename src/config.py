import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List
import json

# Load environment variables
load_dotenv()

# Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / os.getenv("TEMP_DIR", "temp")
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
CACHE_DIR = BASE_DIR / os.getenv("CACHE_DIR", "cache")

# Subdirectories for cached assets
TEMP_SCRIPTS = TEMP_DIR / "scripts"
TEMP_AUDIO = TEMP_DIR / "audio"
TEMP_VISUALS = TEMP_DIR / "visuals"
TEMP_SUBTITLES = TEMP_DIR / "subtitles"
TEMP_MUSIC = TEMP_DIR / "music"
THUMBNAIL_CACHE = CACHE_DIR / "thumbnails"
VIDEO_CACHE = CACHE_DIR / "videos"

for directory in [TEMP_DIR, OUTPUT_DIR, TEMP_SCRIPTS, TEMP_AUDIO, TEMP_VISUALS, 
                  TEMP_SUBTITLES, TEMP_MUSIC, CACHE_DIR, THUMBNAIL_CACHE, VIDEO_CACHE]:
    directory.mkdir(parents=True, exist_ok=True)

# Enhanced Logging Setup with JSON structured logging option
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "standard")  # standard or json

if LOG_FORMAT == "json":
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_entry)
    
    json_formatter = JSONFormatter()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    file_handler = logging.FileHandler(TEMP_DIR / "agent.log", encoding="utf-8")
    file_handler.setFormatter(json_formatter)
else:
    standard_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(standard_formatter)
    file_handler = logging.FileHandler(TEMP_DIR / "agent.log", encoding="utf-8")
    file_handler.setFormatter(standard_formatter)

logger = logging.getLogger("YoutubeAgentConfig")
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
logger.handlers.clear()
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Video Configurations - Enhanced with quality presets
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "24"))
VIDEO_QUALITY = os.getenv("VIDEO_QUALITY", "high")  # low, medium, high, ultra
DIMENSIONS_LANDSCAPE = (1920, 1080)  # 16:9 for Long-form
DIMENSIONS_PORTRAIT = (1080, 1920)   # 9:16 for Shorts
DIMENSIONS_SQUARE = (1080, 1080)     # 1:1 for Instagram/Facebook

# Quality preset mappings
QUALITY_PRESETS = {
    "low": {"codec": "libx264", "preset": "ultrafast", "crf": 28, "audio_bitrate": "64k"},
    "medium": {"codec": "libx264", "preset": "medium", "crf": 23, "audio_bitrate": "128k"},
    "high": {"codec": "libx264", "preset": "slow", "crf": 18, "audio_bitrate": "192k"},
    "ultra": {"codec": "libx265", "preset": "slow", "crf": 16, "audio_bitrate": "256k"}
}

# Font Configurations - Enhanced with emoji support
DEFAULT_FONT_PATH = "arial.ttf"
EMOJI_FONT_PATH = "NotoColorEmoji.ttf"  # For emoji rendering
BOLD_FONT_PATH = "arial-bold.ttf"

if os.name != "nt":
    font_paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "bold"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "regular"),
        ("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", "emoji"),
        ("/System/Library/Fonts/Helvetica.ttc", "regular"),
        ("/System/Library/Fonts/Apple Color Emoji.ttc", "emoji"),
        ("/usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf", "emoji"),
    ]
    for path, font_type in font_paths:
        if os.path.exists(path):
            if font_type == "bold":
                BOLD_FONT_PATH = path
            elif font_type == "emoji":
                EMOJI_FONT_PATH = path
            elif DEFAULT_FONT_PATH == "arial.ttf":
                DEFAULT_FONT_PATH = path

# Multi-Provider API Keys - Enhanced AI Provider Support
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Claude support
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgqjVWt2A4mH")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")  # Alternative stock footage
STABILITY_AI_KEY = os.getenv("STABILITY_AI_KEY")  # Stable Diffusion
RUNWAYML_API_KEY = os.getenv("RUNWAYML_API_KEY")  # AI video generation

# Advanced Feature Flags
ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "true").lower() == "true"
ENABLE_AUTO_EMOJI = os.getenv("ENABLE_AUTO_EMOJI", "true").lower() == "true"
ENABLE_SMART_TRANSITIONS = os.getenv("ENABLE_SMART_TRANSITIONS", "true").lower() == "true"
ENABLE_BATCH_PROCESSING = os.getenv("ENABLE_BATCH_PROCESSING", "false").lower() == "true"
ENABLE_ANALYTICS_TRACKING = os.getenv("ENABLE_ANALYTICS_TRACKING", "true").lower() == "true"

# Voice Configuration - Multiple voice profiles
VOICE_PROFILES = {
    "default": {"voice_id": ELEVENLABS_VOICE_ID, "stability": 0.75, "similarity": 0.75},
    "narrator": {"voice_id": os.getenv("ELEVENLABS_NARRATOR_ID", "pNInz6obpgqjVWt2A4mH"), "stability": 0.8, "similarity": 0.8},
    "energetic": {"voice_id": os.getenv("ELEVENLABS_ENERGETIC_ID", "EXAVITQu4vr4xnSDxMaL"), "stability": 0.6, "similarity": 0.9},
    "calm": {"voice_id": os.getenv("ELEVENLABS_CALM_ID", "MF3mGyEYCl7XYWbV9V6O"), "stability": 0.9, "similarity": 0.7}
}

# Music & Audio Settings
BACKGROUND_MUSIC_VOLUME = float(os.getenv("BACKGROUND_MUSIC_VOLUME", "0.08"))
AUDIO_NORMALIZATION = os.getenv("AUDIO_NORMALIZATION", "true").lower() == "true"
AUDIO_DUCKING_ENABLED = os.getenv("AUDIO_DUCKING_ENABLED", "true").lower() == "true"

# Transition Effects Library
TRANSITION_EFFECTS = [
    "fade", "wipe_left", "wipe_right", "zoom_in", "zoom_out",
    "blur", "glitch", "slide_up", "slide_down", "circle_open"
]

def get_quality_settings(quality: str = None) -> Dict[str, Any]:
    """Returns encoding settings based on quality preset."""
    quality = quality or VIDEO_QUALITY
    return QUALITY_PRESETS.get(quality, QUALITY_PRESETS["high"])

def validate_environment() -> bool:
    """Comprehensive environment validation with detailed diagnostics."""
    warnings = []
    info_messages = []
    available_providers = []
    
    # Check AI Planning Providers
    ai_providers = {
        "Gemini": GEMINI_API_KEY,
        "OpenAI": OPENAI_API_KEY,
        "Anthropic": ANTHROPIC_API_KEY
    }
    
    active_ai = [name for name, key in ai_providers.items() if key]
    if active_ai:
        available_providers.extend(active_ai)
        info_messages.append(f"AI Planning providers available: {', '.join(active_ai)}")
    else:
        warnings.append("No AI planning provider configured! Storyboard generation will fail.")
    
    # Check TTS Providers
    tts_providers = {
        "ElevenLabs": ELEVENLABS_API_KEY,
        "OpenAI": OPENAI_API_KEY
    }
    active_tts = [name for name, key in tts_providers.items() if key]
    
    if not active_tts:
        warnings.append("No premium TTS configured! Will use free gTTS fallback.")
    else:
        info_messages.append(f"TTS providers available: {', '.join(active_tts)}")
    
    # Check Visual Generation
    visual_providers = {
        "DALL-E 3": OPENAI_API_KEY,
        "Stable Diffusion": STABILITY_AI_KEY,
        "RunwayML": RUNWAYML_API_KEY
    }
    active_visual = [name for name, key in visual_providers.items() if key]
    
    if not active_visual and not PEXELS_API_KEY and not PIXABAY_API_KEY:
        warnings.append("No visual generation APIs configured! Will use local fallback graphics.")
    else:
        sources = []
        if PEXELS_API_KEY:
            sources.append("Pexels")
        if PIXABAY_API_KEY:
            sources.append("Pixabay")
        if active_visual:
            sources.extend(active_visual)
        info_messages.append(f"Visual sources available: {', '.join(sources)}")
    
    # Log info messages
    for msg in info_messages:
        logger.info(f"✓ {msg}")
    
    # Log available features
    feature_status = []
    if ENABLE_SENTIMENT_ANALYSIS:
        feature_status.append("Sentiment Analysis")
    if ENABLE_AUTO_EMOJI:
        feature_status.append("Auto Emoji")
    if ENABLE_SMART_TRANSITIONS:
        feature_status.append("Smart Transitions")
    if ENABLE_BATCH_PROCESSING:
        feature_status.append("Batch Processing")
    if ENABLE_ANALYTICS_TRACKING:
        feature_status.append("Analytics Tracking")
    
    if feature_status:
        logger.info(f"Advanced features enabled: {', '.join(feature_status)}")
    
    if warnings:
        logger.warning("=" * 70)
        logger.warning("CONFIGURATION WARNINGS:")
        for warn in warnings:
            logger.warning(f" ⚠ {warn}")
        logger.warning("=" * 70)
        logger.info("💡 Tip: Create a .env file with your API keys for full functionality")
        return False
    
    logger.info("✅ All core systems operational. Ready for production.")
    return True


class PipelineMetrics:
    """Track pipeline performance metrics for optimization."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "start_time": None,
            "stage_times": {},
            "api_calls": {},
            "errors": [],
            "warnings": [],
            "output_files": [],
            "total_duration_seconds": 0,
            "video_length_seconds": 0
        }
    
    def start_timer(self):
        import time
        self.metrics["start_time"] = time.time()
    
    def record_stage(self, stage_name: str, duration: float):
        self.metrics["stage_times"][stage_name] = duration
    
    def record_api_call(self, provider: str, endpoint: str, success: bool):
        if provider not in self.metrics["api_calls"]:
            self.metrics["api_calls"][provider] = {"success": 0, "failed": 0}
        if success:
            self.metrics["api_calls"][provider]["success"] += 1
        else:
            self.metrics["api_calls"][provider]["failed"] += 1
    
    def add_error(self, error: str):
        self.metrics["errors"].append(error)
    
    def add_warning(self, warning: str):
        self.metrics["warnings"].append(warning)
    
    def add_output_file(self, filepath: str, file_type: str):
        self.metrics["output_files"].append({
            "path": filepath,
            "type": file_type
        })
    
    def generate_report(self) -> Dict[str, Any]:
        import time
        if self.metrics["start_time"]:
            self.metrics["total_duration_seconds"] = time.time() - self.metrics["start_time"]
        return self.metrics
    
    def save_report(self, output_path: Optional[Path] = None):
        output_path = output_path or (OUTPUT_DIR / "pipeline_metrics.json")
        report = self.generate_report()
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Pipeline metrics saved to: {output_path}")
        return report
