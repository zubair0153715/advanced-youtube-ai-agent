import os
import argparse
import logging
import shutil
from typing import List, Dict, Any
from src.config import (
    validate_environment, TEMP_DIR, OUTPUT_DIR, logger as config_logger
)
from src.agents.planner import StoryboardPlanner
from src.audio.synthesizer import AudioSynthesizer
from src.assets.retriever import AssetRetriever
from src.video.composer import VideoComposer
from src.thumbnail.generator import ThumbnailGenerator
from src.youtube.uploader import YouTubeUploader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YoutubeOrchestrator")

def run_pipeline(prompt: str, format_type: str, auto_upload: bool, privacy_status: str):
    """Orchestrates the entire advanced YouTube automation pipeline."""
    logger.info("=" * 60)
    logger.info("  ULTIMATE ADVANCED YOUTUBE AUTOMATION AGENT - INITIATING  ")
    logger.info("=" * 60)

    # 1. Environment Verification
    validate_environment()

    # Initialize Modules
    planner = StoryboardPlanner()
    synthesizer = AudioSynthesizer()
    retriever = AssetRetriever()
    composer = VideoComposer(format_type)
    thumbnail_gen = ThumbnailGenerator()
    uploader = YouTubeUploader()

    # 2. Stage 1: Generative Storyboarding & Script Writing
    logger.info("\n--- STAGE 1: CREATIVE PLANNING & STORYBOARDING ---")
    plan = planner.generate_plan(prompt, format_type)
    
    video_title = plan.get("title", f"The Secrets of {prompt}")
    video_desc = plan.get("description", "A fully automated AI masterpiece. Subscribe for more!")
    video_tags = plan.get("tags", ["automation", "ai"])
    storyboard = plan.get("storyboard", [])

    logger.info(f"Generated SEO Title: '{video_title}'")
    logger.info(f"Timeline Storyboard has {len(storyboard)} planned scenes.")

    # 3. Stage 2: Synthesis and Media Retrieval
    logger.info("\n--- STAGE 2: GENERATING VOICE & GATHERING VISUALS ---")
    processed_scenes = []

    for scene in storyboard:
        scene_idx = scene["scene_index"]
        text = scene["narration"]
        pexels_q = scene["pexels_query"]
        ai_prompt = scene["ai_image_prompt"]
        highlights = scene["caption_highlights"]

        logger.info(f"\nProcessing Scene {scene_idx}...")
        
        # Audio Synthesis
        audio_details = synthesizer.synthesize(text, scene_idx)
        
        # Visual Asset Retrieval
        visual_path = retriever.fetch_visual(pexels_q, ai_prompt, scene_idx, format_type)
        
        processed_scenes.append({
            "scene_index": scene_idx,
            "duration": audio_details["duration"],
            "audio_path": audio_details["audio_path"],
            "word_timings": audio_details["word_timings"],
            "visual_path": visual_path,
            "caption_highlights": highlights
        })

    # Download Background Ambient Track
    bg_music = retriever.download_background_music()

    # 4. Stage 3: Render Composite Video
    logger.info("\n--- STAGE 3: VIDEO COMPOSING & CAPTION RENDERING ---")
    final_video_path = composer.compose_video(processed_scenes, bg_music)

    # 5. Stage 4: High-CTR Thumbnail Design
    logger.info("\n--- STAGE 4: THUMBNAIL DESIGN ---")
    # Take the DALL-E prompt from the first scene to guide the thumbnail concept background
    thumb_visual_prompt = storyboard[0]["ai_image_prompt"] if storyboard else "A cinematic abstract glowing background"
    thumbnail_path = thumbnail_gen.generate_thumbnail(video_title, thumb_visual_prompt)

    # 6. Stage 5: YouTube Publishing
    youtube_url = None
    if auto_upload:
        logger.info("\n--- STAGE 5: YOUTUBE AUTO-PUBLISHING ---")
        if uploader.authenticate():
            logger.info("Uploading video and thumbnail to YouTube...")
            video_id = uploader.upload_video(
                video_path=final_video_path,
                title=video_title,
                description=video_desc,
                tags=video_tags,
                thumbnail_path=thumbnail_path,
                privacy_status=privacy_status
            )
            if video_id:
                youtube_url = f"https://youtu.be/{video_id}"
                logger.info(f"Auto-publishing successful! Video link: {youtube_url}")
            else:
                logger.error("Auto-publishing failed during upload.")
        else:
            logger.warning("YouTube authentication failed or skipped. Skipping upload.")

    # 7. Final Pipeline Summary
    logger.info("\n" + "=" * 60)
    logger.info("             PIPELINE COMPLETED SUCCESSFULLY             ")
    logger.info("=" * 60)
    logger.info(f" Rendered Video:  {final_video_path}")
    logger.info(f" Designed Thumbnail: {thumbnail_path}")
    if youtube_url:
        logger.info(f" YouTube Link:       {youtube_url}")
    logger.info("=" * 60)

    # Optional clean-up: remove raw scene audios/subtitles to save disk space
    _clean_temp_assets()

def _clean_temp_assets():
    """Wipes the temporary folders to keep the workspace lightweight."""
    logger.info("Cleaning temporary video files and subtitle assets to save space...")
    for folder in ["audio", "visuals", "subtitles"]:
        dir_path = TEMP_DIR / folder
        if dir_path.exists():
            for filename in os.listdir(dir_path):
                # Retain background music cache
                if filename == "background_music.mp3":
                    continue
                file_path = dir_path / filename
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.warning(f"Could not delete temp file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultimate YouTube Automation AI Agent CLI Dashboard")
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Creative prompt/topic to generate full video script and footage for."
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["shorts", "long-form"],
        default="shorts",
        help="Target video format (shorts: portrait 9:16 or long-form: landscape 16:9)."
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="If set, automatically authenticates and uploads final video to YouTube."
    )
    parser.add_argument(
        "--privacy",
        type=str,
        choices=["private", "unlisted", "public"],
        default="private",
        help="Upload privacy visibility status on YouTube (default: private)."
    )
    
    args = parser.parse_args()
    run_pipeline(args.prompt, args.format, args.upload, args.privacy)
