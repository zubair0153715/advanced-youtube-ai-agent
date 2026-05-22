import os
import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.video.subtitle_drawer import SubtitleDrawer

def test_pillow_dynamic_renderer():
    print("=" * 60)
    print(" TESTING IMAGE-MAGICK FREE PILLOW SUBTITLE RENDERER ")
    print("=" * 60)
    
    drawer = SubtitleDrawer("shorts")
    
    # 2-word sample segment
    word_timings = [
        {"word": "HELLO", "raw_word": "Hello", "start": 0.0, "end": 1.0},
        {"word": "WORLD", "raw_word": "World!", "start": 1.0, "end": 2.0}
    ]
    
    frames = drawer.generate_subtitle_frames(
        word_timings=word_timings,
        highlights=["WORLD"],
        scene_index=888
    )
    
    print(f"Total dynamic subtitle frames generated: {len(frames)}")
    for i, frame in enumerate(frames):
        print(f" - Frame {i}: Path: {frame['path']} ({frame['start']}s -> {frame['end']}s)")
        assert os.path.exists(frame["path"]), f"Frame {i} is missing from disk!"
        
    print("=" * 60)
    print("     ALL PILLOW SUBTITLE TESTS PASSED SUCCESSFULLY!    ")
    print("=" * 60)

if __name__ == "__main__":
    test_pillow_dynamic_renderer()
