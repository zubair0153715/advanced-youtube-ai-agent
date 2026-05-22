import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, List
from src.config import TEMP_SUBTITLES, DEFAULT_FONT_PATH

logger = logging.getLogger("YoutubeSubtitleDrawer")

class SubtitleDrawer:
    def __init__(self, format_type: str = "shorts"):
        self.format_type = format_type
        # Dimensions matching the video canvas
        self.width = 1080 if format_type == "shorts" else 1920
        self.height = 1920 if format_type == "shorts" else 1080
        
        # Subtitle positioning (e.g., lower-middle screen: 65% down for Shorts, 80% down for landscape)
        self.vertical_ratio = 0.65 if format_type == "shorts" else 0.80
        
        # Load high-impact bold font
        font_size = 72 if format_type == "shorts" else 48
        try:
            self.font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
            logger.info(f"Loaded dynamic font from {DEFAULT_FONT_PATH} at size {font_size}")
        except Exception as e:
            logger.warning(f"Could not load custom font, falling back to default: {e}")
            self.font = ImageFont.load_default()

    def generate_subtitle_frames(self, word_timings: List[Dict[str, Any]], highlights: List[str], scene_index: int) -> List[Dict[str, Any]]:
        """Renders transparent subtitle PNGs and returns a list of frame timing mappings.
        
        For high visual engagement:
        - Groups words into 3-word chunks.
        - Center-aligns them on the canvas.
        - Highlights the currently spoken word in bright yellow.
        - Renders an outline border on the text for contrast on any background.
        
        Returns:
            A list of dicts: [{'path': 'path/to/frame.png', 'start': 0.0, 'end': 0.4}]
        """
        if not word_timings:
            return []

        logger.info(f"Rendering Pillow subtitle frames for scene {scene_index}...")
        highlights_upper = [w.upper() for w in highlights]
        
        # Group word timings into chunks of 3 words max for fast readability
        chunks = []
        chunk_size = 3 if self.format_type == "shorts" else 5
        for i in range(0, len(word_timings), chunk_size):
            chunks.append(word_timings[i:i + chunk_size])

        frame_mappings = []
        frame_counter = 0

        for chunk_idx, chunk in enumerate(chunks):
            # Time range for this chunk
            chunk_start = chunk[0]["start"]
            chunk_end = chunk[-1]["end"]
            
            # We want to create frames for each word's active speak time within this chunk
            for active_word in chunk:
                # Active window for the highlighted word
                start_t = active_word["start"]
                end_t = active_word["end"]
                
                # Create a blank transparent image
                img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Render all words in the current chunk on this frame
                self._draw_word_chunk(draw, chunk, active_word["word"], highlights_upper)
                
                # Save the transparent frame
                frame_path = TEMP_SUBTITLES / f"scene_{scene_index}_frame_{frame_counter}.png"
                img.save(frame_path, "PNG")
                
                frame_mappings.append({
                    "path": str(frame_path),
                    "start": start_t,
                    "end": end_t
                })
                frame_counter += 1

        logger.info(f"Generated {frame_counter} custom subtitle frames for scene {scene_index}")
        return frame_mappings

    def _draw_word_chunk(self, draw: ImageDraw.ImageDraw, chunk: List[Dict[str, Any]], active_word: str, highlights: List[str]):
        """Draws a horizontal block of words centered, highlighting the active word and strategic keywords."""
        words_to_draw = [item["word"] for item in chunk]
        
        # Calculate horizontal sizes of words to center them as a block
        word_sizes = []
        spacing = 20 # Pixel gap between words
        
        for w in words_to_draw:
            # Measure bounding box of each word
            bbox = draw.textbbox((0, 0), w, font=self.font)
            w_width = bbox[2] - bbox[0]
            w_height = bbox[3] - bbox[1]
            word_sizes.append((w_width, w_height))
            
        total_width = sum(w[0] for w in word_sizes) + spacing * (len(words_to_draw) - 1)
        
        # Start drawing coordinate (X centers the block)
        x_start = (self.width - total_width) // 2
        y_pos = int(self.height * self.vertical_ratio)
        
        current_x = x_start
        for i, word in enumerate(words_to_draw):
            w_w, w_h = word_sizes[i]
            
            # Select color based on active state or preset highlights
            if word == active_word:
                text_color = (255, 204, 0, 255) # Vibrant Yellow
            elif word in highlights:
                text_color = (255, 80, 80, 255)  # Electric Red for special keywords
            else:
                text_color = (255, 255, 255, 255) # Crisp White
                
            # Draw strong outline border for extreme contrast
            outline_color = (0, 0, 0, 255)
            outline_width = 5
            
            # Draw outline by offsetting text in all directions
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((current_x + dx, y_pos + dy), word, fill=outline_color, font=self.font)
                        
            # Draw main colored text
            draw.text((current_x, y_pos), word, fill=text_color, font=self.font)
            current_x += w_w + spacing
