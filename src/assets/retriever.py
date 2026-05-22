import os
import logging
import requests
from typing import Dict, Any, Optional
from src.config import (
    PEXELS_API_KEY, OPENAI_API_KEY,
    TEMP_VISUALS, TEMP_AUDIO
)

logger = logging.getLogger("YoutubeAssetRetriever")

class AssetRetriever:
    def __init__(self):
        self.pexels_video_search_url = "https://api.pexels.com/videos/search"
        self.openai_dalle_url = "https://api.openai.com/v1/images/generations"

    def fetch_visual(self, query: str, ai_prompt: str, scene_index: int, format_type: str = "shorts") -> str:
        """Fetches a visual asset for the scene. Prefers stock video (Pexels), falls back to DALL-E 3 image.
        
        Args:
            query: Pexels stock video search keywords.
            ai_prompt: OpenAI DALL-E 3 detailed visual prompt.
            scene_index: The numerical index of the scene.
            format_type: 'shorts' (vertical 9:16) or 'long-form' (horizontal 16:9).
            
        Returns:
            The absolute file path of the downloaded asset (.mp4 or .png).
        """
        orientation = "portrait" if format_type == "shorts" else "landscape"
        
        # 1. Try Pexels Stock Video first if configured
        if PEXELS_API_KEY:
            try:
                logger.info(f"Searching Pexels video for query: '{query}' ({orientation})")
                headers = {"Authorization": PEXELS_API_KEY}
                params = {
                    "query": query,
                    "per_page": 5,
                    "orientation": orientation,
                    "size": "medium"  # medium/large are perfect for HD
                }
                
                response = requests.get(self.pexels_video_search_url, params=params, headers=headers, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    videos = data.get("videos", [])
                    if videos:
                        # Select the best quality video file under HD/1080p
                        video = videos[0]
                        video_files = video.get("video_files", [])
                        best_file = self._select_best_video(video_files, orientation)
                        
                        if best_file:
                            download_url = best_file.get("link")
                            output_file = TEMP_VISUALS / f"scene_{scene_index}.mp4"
                            logger.info(f"Downloading Pexels video from: {download_url}")
                            
                            vid_resp = requests.get(download_url, timeout=45)
                            if vid_resp.status_code == 200:
                                with open(output_file, "wb") as f:
                                    f.write(vid_resp.content)
                                logger.info(f"Successfully saved stock video for scene {scene_index}")
                                return str(output_file)
                    logger.warning(f"No matching stock videos found on Pexels for: '{query}'")
                else:
                    logger.error(f"Pexels Video API failed with status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Error calling Pexels Video API: {e}", exc_info=True)

        # 2. Fallback to OpenAI DALL-E 3 Image Generation
        if OPENAI_API_KEY:
            try:
                logger.info(f"Generating custom AI image for scene {scene_index} using DALL-E 3...")
                aspect_ratio = "1024x1792" if format_type == "shorts" else "1792x1024"  # Modern HD standards
                
                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "dall-e-3",
                    "prompt": ai_prompt,
                    "n": 1,
                    "size": aspect_ratio,
                    "quality": "standard"
                }
                
                response = requests.post(self.openai_dalle_url, json=data, headers=headers, timeout=45)
                if response.status_code == 200:
                    img_data = response.json()
                    img_url = img_data.get("data", [{}])[0].get("url")
                    if img_url:
                        output_file = TEMP_VISUALS / f"scene_{scene_index}.png"
                        logger.info(f"Downloading generated image from: {img_url}")
                        
                        img_resp = requests.get(img_url, timeout=30)
                        if img_resp.status_code == 200:
                            with open(output_file, "wb") as f:
                                f.write(img_resp.content)
                            logger.info(f"Successfully saved generated image for scene {scene_index}")
                            return str(output_file)
                else:
                    logger.error(f"OpenAI DALL-E 3 API failed with status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Error calling OpenAI DALL-E API: {e}", exc_info=True)

        # 3. Emergency Local Fallback: Draw a beautifully styled colored slide with text if no API keys work
        logger.warning(f"All online visual retrieval systems failed for scene {scene_index}. Creating beautiful local backdrop.")
        from PIL import Image, ImageDraw
        width, height = (1080, 1920) if format_type == "shorts" else (1920, 1080)
        
        # Draw a luxurious dark radial gradient or deep colorful frame
        img = Image.new("RGB", (width, height), color=(18, 18, 24))
        draw = ImageDraw.Draw(img)
        # Add simple modern border frame
        draw.rectangle([20, 20, width - 20, height - 20], outline=(88, 86, 214), width=4)
        
        output_file = TEMP_VISUALS / f"scene_{scene_index}.png"
        img.save(output_file)
        logger.info(f"Saved solid local emergency slide for scene {scene_index}")
        return str(output_file)

    def download_background_music(self) -> Optional[str]:
        """Downloads a beautiful, low-tempo copyright-free background music track."""
        bg_music_file = TEMP_AUDIO / "background_music.mp3"
        if bg_music_file.exists():
            logger.info("Background music already cached locally.")
            return str(bg_music_file)
            
        # Download royalty-free high-quality corporate/cinematic background ambient track
        # Standard stable open archive link for a royalty free piano/ambient MP3
        music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        logger.info(f"Downloading license-free background music from: {music_url}")
        
        try:
            response = requests.get(music_url, stream=True, timeout=60)
            if response.status_code == 200:
                with open(bg_music_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info("Successfully downloaded background music track.")
                return str(bg_music_file)
            else:
                logger.error(f"Failed to download background music: Status {response.status_code}")
        except Exception as e:
            logger.error(f"Error downloading background music: {e}", exc_info=True)
            
        return None

    def _select_best_video(self, video_files: list, orientation: str) -> Optional[Dict[str, Any]]:
        """Filters and selects the standard high-definition mp4 video file."""
        if not video_files:
            return None
            
        # Prioritize 'mp4' files with a good size and width/height matching orientation
        best_candidate = None
        for f in video_files:
            file_type = f.get("file_type", "")
            width = f.get("width")
            height = f.get("height")
            
            if "mp4" in file_type.lower():
                if width and height:
                    # Match orientation
                    if orientation == "portrait" and height > width:
                        return f
                    elif orientation == "landscape" and width > height:
                        return f
                best_candidate = f
                
        return best_candidate
