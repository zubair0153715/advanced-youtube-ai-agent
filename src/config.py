import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / os.getenv("TEMP_DIR", "temp")
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")

# Subdirectories for cached assets
TEMP_SCRIPTS = TEMP_DIR / "scripts"
TEMP_AUDIO = TEMP_DIR / "audio"
TEMP_VISUALS = TEMP_DIR / "visuals"
TEMP_SUBTITLES = TEMP_DIR / "subtitles"

for directory in [TEMP_DIR, OUTPUT_DIR, TEMP_SCRIPTS, TEMP_AUDIO, TEMP_VISUALS, TEMP_SUBTITLES]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(TEMP_DIR / "agent.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("YoutubeAgentConfig")

# Video Configurations
VIDEO_FPS = 24
DIMENSIONS_LANDSCAPE = (1920, 1080)  # 16:9 for Long-form
DIMENSIONS_PORTRAIT = (1080, 1920)   # 9:16 for Shorts

# Font Configurations
# Fallback search for a clean sans font depending on OS
DEFAULT_FONT_PATH = "arial.ttf"  # Default on Windows
if os.name != "nt":
    # On Linux/macOS try standard clean fonts
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Helvetica.ttc", "LiberationSans-Bold.ttf"]:
        if os.path.exists(path):
            DEFAULT_FONT_PATH = path
            break

# Env validation settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgqjVWt2A4mH")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def validate_environment() -> bool:
    """Checks and logs warnings for missing critical keys in .env."""
    warnings = []
    
    if not GEMINI_API_KEY:
        warnings.append("GEMINI_API_KEY is missing! Scriptwriting & creative storyboard planning will fail.")
        
    if not PEXELS_API_KEY:
        warnings.append("PEXELS_API_KEY is missing! Automatic stock video downloads will be disabled; falling back to AI generated illustrations.")
        
    if not ELEVENLABS_API_KEY:
        if not OPENAI_API_KEY:
            warnings.append("Both ELEVENLABS_API_KEY and OPENAI_API_KEY are missing! Premium Text-to-Speech narration will fail.")
        else:
            logger.info("ElevenLabs key is missing, but OpenAI key is found. Narration will fall back to OpenAI TTS.")
            
    if not OPENAI_API_KEY:
        warnings.append("OPENAI_API_KEY is missing! DALL-E 3 visual asset generation and TTS backup will be unavailable.")

    if warnings:
        logger.warning("=" * 60)
        logger.warning("ENVIRONMENT WARNINGS:")
        for warn in warnings:
            logger.warning(f" - {warn}")
        logger.warning("Please configure your .env file to enable all advanced features.")
        logger.warning("=" * 60)
        return False
        
    logger.info("All core environment configurations loaded successfully.")
    return True
