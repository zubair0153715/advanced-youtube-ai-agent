import os
import sys
import argparse
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import (
    validate_environment, TEMP_DIR, OUTPUT_DIR, CACHE_DIR,
    PipelineMetrics, ENABLE_BATCH_PROCESSING, logger as config_logger
)
from src.agents.planner import AdvancedStoryboardPlanner
from src.audio.synthesizer import AudioSynthesizer
from src.assets.retriever import AssetRetriever
from src.video.composer import VideoComposer
from src.thumbnail.generator import ThumbnailGenerator
from src.youtube.uploader import YouTubeUploader

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(TEMP_DIR / "pipeline.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("YoutubeOrchestrator")


def run_pipeline(prompt: str, format_type: str = "shorts", auto_upload: bool = False, 
                 privacy_status: str = "private", voice_profile: str = "default",
                 enable_hooks: bool = True, ai_provider: str = "auto",
                 batch_prompts: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Orchestrates the entire advanced YouTube automation pipeline with enhanced features.
    
    Args:
        prompt: Main creative topic/prompt for video generation
        format_type: 'shorts', 'long-form', or 'square'
        auto_upload: Whether to auto-upload to YouTube
        privacy_status: YouTube privacy setting ('private', 'unlisted', 'public')
        voice_profile: Voice personality ('default', 'narrator', 'energetic', 'calm')
        enable_hooks: Generate viral hook variations
        ai_provider: Preferred AI provider ('auto', 'gemini', 'openai', 'anthropic')
        batch_prompts: Optional list of prompts for batch processing
        
    Returns:
        Dictionary containing pipeline results and metrics
    """
    # Initialize metrics tracking
    metrics = PipelineMetrics()
    metrics.start_timer()
    
    logger.info("=" * 80)
    logger.info("  🚀 ADVANCED YOUTUBE AI AGENT - NEXT GENERATION EDITION  ")
    logger.info("  Powered by Multi-Modal AI | Sentiment Analysis | Smart Optimization  ")
    logger.info("=" * 80)
    
    # Handle batch processing
    if batch_prompts or (ENABLE_BATCH_PROCESSING and batch_prompts is not None):
        return _run_batch_pipeline(
            batch_prompts, format_type, auto_upload, privacy_status,
            voice_profile, enable_hooks, ai_provider, metrics
        )
    
    # Single video pipeline
    try:
        # Stage 0: Environment & Configuration Check
        logger.info("\n📋 STAGE 0: SYSTEM INITIALIZATION")
        config_valid = validate_environment()
        metrics.record_stage("initialization", time.time() - metrics.metrics["start_time"])
        
        # Initialize AI-powered modules
        logger.info("\n🤖 Initializing Advanced AI Modules...")
        planner = AdvancedStoryboardPlanner(preferred_provider=ai_provider)
        synthesizer = AudioSynthesizer(voice_profile=voice_profile)
        retriever = AssetRetriever(enable_sentiment_analysis=True)
        composer = VideoComposer(format_type, enable_smart_transitions=True)
        thumbnail_gen = ThumbnailGenerator(enable_ai_enhancement=True)
        uploader = YouTubeUploader()
        
        # Stage 1: Generative Storyboarding with AI Enhancement
        logger.info("\n🎬 STAGE 1: AI-POWERED CREATIVE PLANNING & STORYBOARDING")
        stage_start = time.time()
        plan = planner.generate_plan(
            prompt=prompt,
            format_type=format_type,
            voice_profile=voice_profile,
            enable_hooks=enable_hooks
        )
        metrics.record_stage("storyboarding", time.time() - stage_start)
        
        # Extract plan details
        video_title = plan.get("title", f"The Secrets of {prompt}")
        video_desc = plan.get("description", "An AI-generated masterpiece. Subscribe for more!")
        video_tags = plan.get("tags", ["ai", "automation", "viral"])
        storyboard = plan.get("storyboard", [])
        viral_hooks = plan.get("viral_hooks", [])
        metadata = plan.get("metadata", {})
        
        # Display viral hooks for A/B testing
        if viral_hooks:
            logger.info(f"\n🎣 Generated {len(viral_hooks)} Viral Hooks for A/B Testing:")
            for i, hook in enumerate(viral_hooks[:3], 1):
                logger.info(f"   {i}. {hook}")
        
        logger.info(f"\n✅ SEO-Optimized Title: '{video_title}'")
        logger.info(f"📊 Storyboard contains {len(storyboard)} scenes (~{metadata.get('estimated_duration', 0)}s)")
        logger.info(f"🎯 Target Audience: {plan.get('target_audience', 'General')}")
        logger.info(f"🏷️ Category: {plan.get('category', 'Education')}")
        
        metrics.add_output_file(str(OUTPUT_DIR / "storyboard.json"), "storyboard")
        
        # Stage 2: Multi-Modal Synthesis and Asset Retrieval
        logger.info("\n🎨 STAGE 2: VOICE SYNTHESIS & VISUAL ASSET GENERATION")
        stage_start = time.time()
        processed_scenes = []
        
        for idx, scene in enumerate(storyboard):
            scene_idx = scene.get("scene_index", idx + 1)
            text = scene.get("narration", "")
            pexels_q = scene.get("pexels_query", prompt)
            ai_prompt = scene.get("ai_image_prompt", f"Cinematic {prompt}")
            highlights = scene.get("caption_highlights", [])
            emotion = scene.get("emotion_tag", "neutral")
            sentiment = scene.get("sentiment", {})
            
            logger.info(f"\n🎞️ Processing Scene {scene_idx}/{len(storyboard)} [{emotion}]")
            
            # Adaptive voice synthesis based on sentiment
            voice_settings = None
            if sentiment:
                if sentiment.get("excitement", 0) > 0.7:
                    voice_settings = {"stability": 0.6, "similarity": 0.9}
                elif sentiment.get("urgency", 0) > 0.7:
                    voice_settings = {"stability": 0.7, "similarity": 0.85}
            
            audio_details = synthesizer.synthesize(
                text=text,
                scene_index=scene_idx,
                voice_settings=voice_settings
            )
            
            # Intelligent visual retrieval with fallback chain
            visual_path = retriever.fetch_visual(
                query=pexels_q,
                ai_prompt=ai_prompt,
                scene_index=scene_idx,
                format_type=format_type,
                emotion_hint=emotion
            )
            
            processed_scenes.append({
                "scene_index": scene_idx,
                "duration": audio_details.get("duration", 5),
                "audio_path": audio_details.get("audio_path"),
                "word_timings": audio_details.get("word_timings", []),
                "visual_path": visual_path,
                "caption_highlights": highlights,
                "emotion": emotion,
                "transition": scene.get("transition_suggestion", "fade")
            })
            
            metrics.record_api_call("synthesis", "tts", bool(audio_details.get("audio_path")))
            metrics.record_api_call("retrieval", "visual", bool(visual_path))
        
        # Download and process background music
        bg_music = retriever.download_background_music(style="ambient_cinematic")
        
        metrics.record_stage("asset_generation", time.time() - stage_start)
        
        # Stage 3: Professional Video Composition
        logger.info("\n🎥 STAGE 3: VIDEO COMPOSITION & SMART TRANSITIONS")
        stage_start = time.time()
        final_video_path = composer.compose_video(
            scenes=processed_scenes,
            background_music_path=bg_music,
            add_transitions=True,
            color_grade=True
        )
        metrics.record_stage("video_composition", time.time() - stage_start)
        metrics.add_output_file(final_video_path, "video")
        
        # Stage 4: High-CTR Thumbnail Generation
        logger.info("\n🖼️ STAGE 4: AI-ENHANCED THUMBNAIL DESIGN")
        stage_start = time.time()
        thumb_visual_prompt = storyboard[0].get("ai_image_prompt", "cinematic abstract background") if storyboard else "cinematic background"
        thumbnail_path = thumbnail_gen.generate_thumbnail(
            title=video_title,
            visual_prompt=thumb_visual_prompt,
            alternative_titles=plan.get("alternative_titles", [])
        )
        metrics.record_stage("thumbnail_generation", time.time() - stage_start)
        metrics.add_output_file(thumbnail_path, "thumbnail")
        
        # Stage 5: YouTube Publishing (Optional)
        youtube_url = None
        if auto_upload:
            logger.info("\n📤 STAGE 5: YOUTUBE AUTO-PUBLISHING")
            stage_start = time.time()
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
                    logger.info(f"✅ Successfully published! Video URL: {youtube_url}")
                    
                    # Upload A/B test thumbnails if available
                    if plan.get("alternative_titles"):
                        logger.info("💡 Tip: Consider A/B testing with alternative thumbnails")
                else:
                    logger.error("❌ Upload failed during processing")
                
                metrics.record_stage("youtube_upload", time.time() - stage_start)
            else:
                logger.warning("⚠️ YouTube authentication failed. Skipping upload.")
        
        # Final Summary
        total_time = time.time() - metrics.metrics["start_time"]
        metrics.record_stage("total_pipeline", total_time)
        
        logger.info("\n" + "=" * 80)
        logger.info("  🎉 PIPELINE EXECUTION COMPLETED SUCCESSFULLY  ")
        logger.info("=" * 80)
        logger.info(f"⏱️ Total Processing Time: {total_time:.2f}s")
        logger.info(f"📹 Rendered Video: {final_video_path}")
        logger.info(f"🖼️ Thumbnail: {thumbnail_path}")
        if youtube_url:
            logger.info(f"🔗 YouTube Link: {youtube_url}")
        logger.info(f"📊 Scenes Processed: {len(processed_scenes)}")
        logger.info(f"🎯 Video Duration: ~{sum(s['duration'] for s in processed_scenes):.1f}s")
        logger.info("=" * 80)
        
        # Save metrics report
        metrics.save_report()
        
        # Cleanup temporary assets
        _cleanup_temp_assets()
        
        return {
            "success": True,
            "video_path": final_video_path,
            "thumbnail_path": thumbnail_path,
            "youtube_url": youtube_url,
            "metrics": metrics.generate_report(),
            "plan": plan
        }
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed with error: {e}", exc_info=True)
        metrics.add_error(str(e))
        metrics.save_report()
        return {
            "success": False,
            "error": str(e),
            "metrics": metrics.generate_report()
        }

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
        choices=["shorts", "long-form", "square"],
        default="long-form",
        help="Target video format (shorts: portrait 9:16 ~30-50s, long-form: landscape 16:9 ~5-15min, square: 1:1 ~60-90s). Default is long-form for longer videos."
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
    parser.add_argument(
        "--quality",
        type=str,
        choices=["low", "medium", "high", "ultra"],
        default="ultra",
        help="Video output quality preset (default: ultra for best quality)."
    )
    
    args = parser.parse_args()
    run_pipeline(args.prompt, args.format, args.upload, args.privacy)
