import os
import time
import logging
import requests
from PIL import Image, ImageDraw, ImageFont
from src.config import (
    OPENAI_API_KEY, OUTPUT_DIR, DEFAULT_FONT_PATH
)

logger = logging.getLogger("YoutubeThumbnailGenerator")

class ThumbnailGenerator:
    def __init__(self):
        self.openai_dalle_url = "https://api.openai.com/v1/images/generations"
        self.width = 1280
        self.height = 720

    def generate_thumbnail(self, title: str, visual_prompt: str) -> str:
        """Generates a high-click-through-rate (CTR) YouTube thumbnail.
        
        Args:
            title: The main textual hook to overlay on the thumbnail.
            visual_prompt: The detailed image generation prompt for the background.
            
        Returns:
            The absolute path of the generated thumbnail image.
        """
        logger.info("Starting Thumbnail Design Stage...")
        bg_image_path = OUTPUT_DIR / "temp_thumbnail_bg.png"
        bg_success = False

        # 1. Try DALL-E 3 to draw high quality custom background
        if OPENAI_API_KEY:
            try:
                logger.info("Generating professional background via DALL-E 3...")
                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "dall-e-3",
                    "prompt": f"{visual_prompt}. Must be a cinematic, highly-detailed, ultra-clear landscape concept background suitable for a YouTube thumbnail with empty space on the left for text overlay.",
                    "n": 1,
                    "size": "1024x1024", # Resize to 1280x720 later
                    "quality": "standard"
                }
                
                response = requests.post(self.openai_dalle_url, json=data, headers=headers, timeout=45)
                if response.status_code == 200:
                    img_url = response.json().get("data", [{}])[0].get("url")
                    if img_url:
                        img_resp = requests.get(img_url, timeout=30)
                        if img_resp.status_code == 200:
                            with open(bg_image_path, "wb") as f:
                                f.write(img_resp.content)
                            bg_success = True
                            logger.info("Successfully fetched DALL-E 3 background.")
                else:
                    logger.error(f"OpenAI DALL-E failed for thumbnail with status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Error generating DALL-E thumbnail background: {e}", exc_info=True)

        # 2. Local Fallback Background: Design a gorgeous dark glowing gradient backdrop
        if not bg_success:
            logger.warning("Using local artistic fallback gradient for thumbnail background...")
            img = Image.new("RGB", (self.width, self.height), color=(15, 15, 20))
            draw = ImageDraw.Draw(img)
            
            # Draw beautiful diagonal gradient glow
            for i in range(self.width):
                r = int(15 + (i / self.width) * 45)
                g = int(15 + (i / self.width) * 15)
                b = int(20 + (i / self.width) * 90)
                draw.line([(i, 0), (i, self.height)], fill=(r, g, b))
                
            # Draw circular glowing lights
            draw.ellipse([self.width - 400, -100, self.width + 200, 500], fill=(88, 86, 214, 50))
            
            img.save(bg_image_path)
            logger.info("Saved local glowing fallback backdrop.")

        # 3. Add high-impact text overlay using Pillow
        logger.info("Overlaying high-contrast hook text onto thumbnail...")
        thumbnail_img = Image.open(bg_image_path).resize((self.width, self.height))
        draw = ImageDraw.Draw(thumbnail_img)
        
        # Load modern extra-bold font at large scale
        font_size = 90
        try:
            font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
        except Exception as e:
            logger.warning(f"Could not load custom font for thumbnail: {e}")
            font = ImageFont.load_default()

        # Simplify title into a punchy short phrase (3-4 words max)
        words = title.upper().split()
        if len(words) > 4:
            words = words[:4]
        punchy_text = " ".join(words)
        
        # Wrap text into two lines if long
        lines = []
        if len(words) > 2:
            lines.append(" ".join(words[:2]))
            lines.append(" ".join(words[2:]))
        else:
            lines.append(punchy_text)

        # Draw each line aligned to the left-center side of the thumbnail
        y_offset = 200
        x_pos = 80
        
        for line in lines:
            # Measure text size
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            
            # Thick black backdrop shadow
            shadow_offset = 8
            draw.text((x_pos + shadow_offset, y_offset + shadow_offset), line, fill=(0, 0, 0, 255), font=font)
            
            # Draw Outline border
            border_width = 4
            for dx in range(-border_width, border_width + 1):
                for dy in range(-border_width, border_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x_pos + dx, y_offset + dy), line, fill=(0, 0, 0, 255), font=font)

            # Draw glowing yellow text
            draw.text((x_pos, y_offset), line, fill=(255, 220, 0, 255), font=font)
            
            y_offset += text_h + 30

        # Save finalized high-retention thumbnail
        final_thumbnail_path = OUTPUT_DIR / f"thumbnail_{int(time.time())}.jpg"
        # Convert to RGB to save as JPEG
        thumbnail_img.convert("RGB").save(final_thumbnail_path, "JPEG", quality=95)
        
        # Clean temporary background file
        try:
            if bg_image_path.exists():
                os.remove(bg_image_path)
        except Exception as e:
            logger.warning(f"Could not delete temp thumbnail file: {e}")
            
        logger.info(f"Thumbnail design complete! File saved: {final_thumbnail_path}")
        return str(final_thumbnail_path)
