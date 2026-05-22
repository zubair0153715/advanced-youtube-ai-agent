import os
import sys
import logging
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import validate_environment, TEMP_VISUALS, TEMP_AUDIO
from src.video.subtitle_drawer import SubtitleDrawer
from src.video.composer import VideoComposer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestPipeline")

def test_imports_and_env():
    logger.info("Testing environment imports and validations...")
    validate_environment()
    logger.info("Successfully imported all core config managers.")

def test_subtitle_drawing():
    logger.info("Testing transparent Pillow dynamic subtitle generator...")
    drawer = SubtitleDrawer("shorts")
    
    word_timings = [
        {"word": "HELLO", "raw_word": "Hello", "start": 0.0, "end": 1.0},
        {"word": "WORLD", "raw_word": "World!", "start": 1.0, "end": 2.0}
    ]
    
    frames = drawer.generate_subtitle_frames(
        word_timings=word_timings,
        highlights=["WORLD"],
        scene_index=999
    )
    
    assert len(frames) > 0, "No subtitle frames were generated!"
    assert os.path.exists(frames[0]["path"]), "Frame file does not exist on disk!"
    logger.info(f"Pillow Dynamic Subtitle Frame generated successfully at: {frames[0]['path']}")

def test_quick_moviepy_render():
    logger.info("Testing quick 2-scene MoviePy render engine (without relying on online APIs)...")
    
    # 1. Build two local dummy colorful visual images
    from PIL import Image, ImageDraw
    
    img1_path = TEMP_VISUALS / "test_scene_1.png"
    img2_path = TEMP_VISUALS / "test_scene_2.png"
    
    # Create two visual backdrops
    for path, color in [(img1_path, (34, 139, 34)), (img2_path, (138, 43, 226))]:
        img = Image.new("RGB", (1080, 1920), color=color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 1030, 1870], outline=(255, 255, 255), width=8)
        img.save(path)
        
    # 2. Build two dummy silent voiceover clips using moviepy
    from moviepy import AudioArrayClip
    import numpy as np
    
    audio1_path = TEMP_AUDIO / "test_audio_1.mp3"
    audio2_path = TEMP_AUDIO / "test_audio_2.mp3"
    
    # Render 3 seconds of silent audio array
    silence_arr = np.zeros((44100 * 3, 2))
    for path in [audio1_path, audio2_path]:
        silence_clip = AudioArrayClip(silence_arr, fps=44100)
        silence_clip.write_audiofile(str(path), fps=44100, logger=None)
        silence_clip.close()

    # 3. Formulate mock scenes
    scenes = [
        {
            "scene_index": 1,
            "duration": 3.0,
            "audio_path": str(audio1_path),
            "visual_path": str(img1_path),
            "caption_highlights": ["AMAZING"],
            "word_timings": [
                {"word": "THIS", "raw_word": "This", "start": 0.0, "end": 1.0},
                {"word": "IS", "raw_word": "is", "start": 1.0, "end": 2.0},
                {"word": "AMAZING", "raw_word": "amazing!", "start": 2.0, "end": 3.0}
            ]
        },
        {
            "scene_index": 2,
            "duration": 3.0,
            "audio_path": str(audio2_path),
            "visual_path": str(img2_path),
            "caption_highlights": ["FUTURE"],
            "word_timings": [
                {"word": "WELCOME", "raw_word": "Welcome", "start": 0.0, "end": 1.0},
                {"word": "TO", "raw_word": "to", "start": 1.0, "end": 2.0},
                {"word": "FUTURE", "raw_word": "future.", "start": 2.0, "end": 3.0}
            ]
        }
    ]

    # Compose video
    composer = VideoComposer("shorts")
    final_mp4 = composer.compose_video(scenes, background_music_path=None)
    
    assert os.path.exists(final_mp4), "The final output MP4 does not exist!"
    logger.info(f"MoviePy quick composition successfully completed! Render saved at: {final_mp4}")
    
    # Cleanup test assets
    for p in [img1_path, img2_path, audio1_path, audio2_path]:
        if os.path.exists(p):
            os.remove(p)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("   LAUNCHING PIPELINE SANITY INTEGRATION CHECKS   ")
    logger.info("=" * 60)
    
    test_imports_and_env()
    test_subtitle_drawing()
    test_quick_moviepy_render()
    
    logger.info("\n" + "=" * 60)
    logger.info("     ALL SANITY TESTS COMPLETED SUCCESSFULLY!     ")
    logger.info("=" * 60)
