import os
import time
import logging
import requests
from typing import Dict, Any, List
from moviepy import AudioFileClip
from src.config import (
    ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID,
    OPENAI_API_KEY, TEMP_AUDIO
)

logger = logging.getLogger("YoutubeAudioSynthesizer")

class AudioSynthesizer:
    def __init__(self):
        self.elevenlabs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        self.openai_url = "https://api.openai.com/v1/audio/speech"

    def synthesize(self, text: str, scene_index: int) -> Dict[str, Any]:
        """Synthesizes voiceover narration and generates precise timing alignment for subtitles.
        
        Args:
            text: Narration script text.
            scene_index: The numerical index of the scene (used for file naming).
            
        Returns:
            A dictionary containing:
              - 'audio_path': Absolute path to the saved MP3 file.
              - 'duration': The exact duration of the audio in seconds.
              - 'word_timings': A list of word timings for dynamic subtitles.
        """
        output_file = TEMP_AUDIO / f"scene_{scene_index}.mp3"
        logger.info(f"Synthesizing narration for scene {scene_index}: '{text[:40]}...'")

        # Try ElevenLabs first if API Key is set
        success = False
        if ELEVENLABS_API_KEY:
            try:
                headers = {
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                    "accept": "audio/mpeg"
                }
                data = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.75,
                        "similarity_boost": 0.75
                    }
                }
                response = requests.post(self.elevenlabs_url, json=data, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Successfully generated ElevenLabs voiceover for scene {scene_index}")
                    success = True
                else:
                    logger.error(f"ElevenLabs API failed with status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Error calling ElevenLabs API: {e}", exc_info=True)

        # Fallback to OpenAI TTS if ElevenLabs failed or is not configured
        if not success and OPENAI_API_KEY:
            try:
                logger.info(f"Falling back to OpenAI TTS for scene {scene_index}...")
                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "tts-1",
                    "input": text,
                    "voice": "alloy"  # alloy, echo, fable, onyx, nova, shimmer
                }
                response = requests.post(self.openai_url, json=data, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Successfully generated OpenAI TTS voiceover for scene {scene_index}")
                    success = True
                else:
                    logger.error(f"OpenAI TTS failed with status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Error calling OpenAI TTS API: {e}", exc_info=True)

        # Local fallback using standard free gTTS (Google Text-To-Speech) if no premium API keys are set
        if not success:
            try:
                logger.info(f"Generating 100% free voiceover using gTTS for scene {scene_index}...")
                from gtts import gTTS
                tts = gTTS(text=text, lang="en")
                tts.save(str(output_file))
                logger.info(f"Successfully generated free Google TTS voiceover for scene {scene_index}")
                success = True
            except Exception as e:
                logger.warning(f"Free gTTS generation failed: {e}. Falling back to silent dummy audio...")

        # If everything failed, create silent dummy audio as emergency
        if not success:
            logger.warning("All TTS systems failed. Generating local mock silent audio.")
            try:
                from moviepy import AudioArrayClip
                import numpy as np
                # Generate 4 seconds of silence at 44100Hz
                silence_arr = np.zeros((44100 * 4, 2))
                silence_clip = AudioArrayClip(silence_arr, fps=44100)
                silence_clip.write_audiofile(str(output_file), fps=44100, logger=None)
                logger.info(f"Successfully generated dummy silent audio for scene {scene_index}")
                success = True
            except Exception as e:
                logger.error(f"Failed to create dummy silent audio: {e}", exc_info=True)
                raise RuntimeError("All TTS audio generation and fallbacks failed.")

        # Load file with MoviePy to get precise duration
        audio_clip = AudioFileClip(str(output_file))
        duration = audio_clip.duration
        audio_clip.close()

        # Calculate high-accuracy word timings based on duration and punctuation pauses
        word_timings = self._align_word_timings(text, duration)
        
        return {
            "audio_path": str(output_file),
            "duration": duration,
            "word_timings": word_timings
        }

    def _align_word_timings(self, text: str, total_duration: float) -> List[Dict[str, Any]]:
        """Splits text and assigns precise start and end times to each word.
        Takes into account word length and punctuation pauses (commas, periods) to make timings natural.
        """
        words = text.strip().split()
        if not words:
            return []

        # Step 1: Assign raw weights to each word based on character length
        # Punctuation gets extra weight as a natural speaking pause
        weights = []
        for word in words:
            weight = len(word)
            if word.endswith(('.', '!', '?')):
                weight += 4.5  # Heavy pause for end of sentence
            elif word.endswith((',', ';', ':', '-')):
                weight += 2.5  # Medium pause
            weights.append(weight)

        total_weight = sum(weights)
        if total_weight == 0:
            total_weight = 1

        # Step 2: Distribute duration proportionally
        timings = []
        current_time = 0.0
        
        for i, word in enumerate(words):
            # Clean word from punctuation for subtitle matching
            clean_word = "".join(char for char in word if char.isalnum() or char in ["'", "-"]).upper()
            
            # Word duration proportional to its weight
            word_dur = (weights[i] / total_weight) * total_duration
            
            # Subtitle highlight start and end times
            start_time = current_time
            end_time = current_time + word_dur
            
            timings.append({
                "word": clean_word,
                "raw_word": word,
                "start": start_time,
                "end": end_time
            })
            
            current_time = end_time

        return timings
