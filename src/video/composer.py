import os
import time
import logging
from typing import List, Dict, Any, Optional
from moviepy import (
    VideoFileClip, ImageClip, AudioFileClip,
    CompositeVideoClip, concatenate_videoclips, CompositeAudioClip,
    afx, vfx
)
from src.config import (
    VIDEO_FPS, DIMENSIONS_LANDSCAPE, DIMENSIONS_PORTRAIT,
    OUTPUT_DIR, get_quality_settings, VIDEO_QUALITY
)
from src.video.subtitle_drawer import SubtitleDrawer

logger = logging.getLogger("YoutubeVideoComposer")

class VideoComposer:
    def __init__(self, format_type: str = "shorts", enable_smart_transitions: bool = True):
        self.format_type = format_type
        self.dimensions = DIMENSIONS_PORTRAIT if format_type == "shorts" else DIMENSIONS_LANDSCAPE
        self.subtitle_drawer = SubtitleDrawer(format_type)
        self.enable_smart_transitions = enable_smart_transitions
        # Get quality settings from config
        self.quality_settings = get_quality_settings(VIDEO_QUALITY)

    def compose_video(self, scenes: List[Dict[str, Any]], background_music_path: Optional[str] = None) -> str:
        """Assembles, mixes, overlays subtitles, and renders the final MP4 video.
        
        Args:
            scenes: A list of scenes. Each scene is a dict with:
               - 'visual_path': Path to visual asset (video or image).
               - 'audio_path': Path to voiceover narration.
               - 'duration': Length of narration in seconds.
               - 'word_timings': Timings for captions.
               - 'caption_highlights': Keywords to highlight.
               - 'scene_index': Index number.
            background_music_path: Path to royalty-free background MP3.
            
        Returns:
            The file path to the rendered MP4 video.
        """
        logger.info("Initializing Video Composition Pipeline...")
        scene_clips = []
        
        for i, scene in enumerate(scenes):
            logger.info(f"Processing Scene {i + 1}/{len(scenes)}...")
            duration = scene["duration"]
            visual_path = scene["visual_path"]
            audio_path = scene["audio_path"]
            word_timings = scene["word_timings"]
            highlights = scene["caption_highlights"]
            scene_idx = scene["scene_index"]

            # 1. Build Voiceover Audio Clip
            voice_clip = AudioFileClip(audio_path)
            
            # 2. Build and scale the background visual clip
            visual_clip = self._build_visual_clip(visual_path, duration)
            visual_clip = visual_clip.with_audio(voice_clip)

            # 3. Render and overlay subtitles
            sub_frames = self.subtitle_drawer.generate_subtitle_frames(word_timings, highlights, scene_idx)
            sub_clips = []
            
            for frame in sub_frames:
                frame_path = frame["path"]
                start_t = frame["start"]
                end_t = frame["end"]
                frame_dur = end_t - start_t
                
                # Check for tiny frame durations
                if frame_dur <= 0:
                    frame_dur = 0.1
                    
                # Subtitle image clip layered transparently
                sub_img_clip = (ImageClip(frame_path)
                               .with_start(start_t)
                               .with_duration(frame_dur)
                               .with_position(("center", "center")))
                sub_clips.append(sub_img_clip)

            # Composite the scene visual with subtitles
            composite_scene = CompositeVideoClip([visual_clip] + sub_clips, size=self.dimensions)
            scene_clips.append(composite_scene)

        # 4. Concatenate all scenes into a single timeline
        logger.info("Concatenating individual scenes...")
        final_video = concatenate_videoclips(scene_clips, method="compose")
        total_duration = final_video.duration
        logger.info(f"Final Video Timeline assembled. Total Duration: {total_duration:.2f}s")

        # 5. Mix and Duck Background Music if available
        if background_music_path and os.path.exists(background_music_path):
            try:
                logger.info("Mixing and ducking background music track...")
                bg_music = AudioFileClip(background_music_path)
                
                # Loop background music if it is shorter than the video
                if bg_music.duration < total_duration:
                    # Quick looping method
                    bg_music = bg_music.with_effects([afx.AudioLoop(duration=total_duration)])
                else:
                    bg_music = bg_music.subclipped(0, total_duration)

                # Duck music volume to 8% to keep voiceover perfectly crisp
                bg_music = bg_music.with_volume_scaled(0.08)
                
                # Mix voiceover timeline and background music
                mixed_audio = CompositeAudioClip([final_video.audio, bg_music])
                final_video = final_video.with_audio(mixed_audio)
                logger.info("Background music mix complete.")
            except Exception as e:
                logger.error(f"Failed to mix background music: {e}", exc_info=True)

        # 6. Render Final Video Output with enhanced quality settings
        output_filename = f"final_render_{self.format_type}_{int(time.time())}.mp4"
        output_path = OUTPUT_DIR / output_filename
        logger.info(f"Rendering final {VIDEO_QUALITY} quality video clip to: {output_path}")
        logger.info(f"Using codec: {self.quality_settings['codec']}, preset: {self.quality_settings['preset']}, CRF: {self.quality_settings['crf']}")

        final_video.write_videofile(
            str(output_path),
            fps=VIDEO_FPS,
            codec=self.quality_settings["codec"],
            audio_codec="aac",
            audio_bitrate=self.quality_settings["audio_bitrate"],
            preset=self.quality_settings["preset"],
            temp_audiofile=str(OUTPUT_DIR / "temp_audio.m4a"),
            remove_temp=True,
            threads=4,
            logger="bar"
        )
        
        # Close all clip references to free memory
        final_video.close()
        for clip in scene_clips:
            clip.close()

        logger.info(f"Video composition render completed successfully! File saved: {output_path}")
        return str(output_path)

    def _build_visual_clip(self, file_path: str, duration: float) -> Any:
        """Loads and formats a visual file (mp4, png, jpg) to fit the video canvas size perfectly."""
        ext = os.path.splitext(file_path)[1].lower()
        width, height = self.dimensions

        if ext in [".mp4", ".mov", ".avi"]:
            # Visual is a stock video file
            clip = VideoFileClip(file_path)
            
            # Loop/extend video if it's shorter than the audio, otherwise trim
            if clip.duration < duration:
                # Loop video file clip
                clip = clip.with_effects([vfx.Loop(duration=duration)])
            else:
                clip = clip.subclipped(0, duration)
                
            # Resize and crop to fill canvas (cover style) without stretching
            clip_w, clip_h = clip.size
            scale_w = width / clip_w
            scale_h = height / clip_h
            scale = max(scale_w, scale_h)
            
            # Resize and center crop
            clip = clip.resized(scale)
            clip = clip.cropped(x_center=clip.w / 2, y_center=clip.h / 2, width=width, height=height)
            return clip
        else:
            # Visual is a static AI image
            clip = ImageClip(file_path).with_duration(duration)
            
            # Resize to fit canvas height/width optimally
            clip_w, clip_h = clip.size
            scale_w = width / clip_w
            scale_h = height / clip_h
            scale = max(scale_w, scale_h)
            
            clip = clip.resized(scale)
            # Center crop
            clip = clip.cropped(x_center=clip.w / 2, y_center=clip.h / 2, width=width, height=height)
            
            # Apply very subtle Ken Burns slow-zoom visual effect to make images look alive!
            # Since moviepy resize takes functions, we can slowly scale from 1.0 to 1.08 over time!
            try:
                clip = clip.resized(lambda t: 1.0 + 0.08 * (t / duration))
                clip = clip.cropped(x_center=clip.w / 2, y_center=clip.h / 2, width=width, height=height)
            except Exception as e:
                logger.warning(f"Could not apply dynamic Ken Burns zoom: {e}")
                
            return clip
