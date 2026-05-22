import json
import logging
import google.generativeai as genai
from typing import Dict, Any
from src.config import GEMINI_API_KEY

logger = logging.getLogger("YoutubeStoryboardAgent")

class StoryboardPlanner:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured in the environment variables.")
        genai.configure(api_key=GEMINI_API_KEY)
        # Using gemini-1.5-flash as it is exceptionally fast, highly cost-effective, and natively supports JSON output.
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_plan(self, prompt: str, format_type: str = "shorts") -> Dict[str, Any]:
        """Generates a complete storyboarding JSON with scripts, keyword searches, DALL-E prompts, and SEO details.
        
        Args:
            prompt: The user's creative prompt or topic idea.
            format_type: 'shorts' (vertical 9:16) or 'long-form' (horizontal 16:9).
        """
        logger.info(f"Generating dynamic storyboard plan for prompt: '{prompt}' (Format: {format_type})")
        
        system_instruction = (
            "You are a world-class viral YouTube Content Strategist, Professional Scriptwriter, and Creative Director. "
            "Your job is to expand a user prompt into a high-retention, fully structured video production storyboard. "
            "The storyboard must be returned strictly in JSON format. Do not include markdown code block formatting in your response (e.g., do not wrap in ```json). "
            f"The target format is: '{format_type}'. \n"
            "Guidelines based on format:\n"
            "- If format is 'shorts': The video must be extremely fast-paced, high energy, lasting between 30 to 50 seconds in total. "
            "It must start with a massive viral hook in the first 3 seconds. Keep sentences brief (under 8 words per scene), simple, and Punchy. "
            "The storyboard should have 4 to 8 scenes.\n"
            "- If format is 'long-form': The video must have a compelling introduction hook (first 15-30 seconds), "
            "a highly structured educational or narrative body, and a strong call to action at the end. Total length should be around 1 to 2 minutes for testing (8 to 15 scenes).\n\n"
            "For EVERY scene, you must plan:\n"
            "1. narration: The precise spoken script words. Avoid complex numbers or difficult pronunciation. Make it sound natural and conversational.\n"
            "2. pexels_query: A short, simple, standard search query for royalty-free stock videos (e.g., 'vintage spaceship interior', 'dramatic stormy sea'). Do not use punctuation. Keep queries basic.\n"
            "3. ai_image_prompt: A beautiful, highly descriptive prompt for an AI image generator (like DALL-E 3 or Midjourney) to generate a custom 8k cinematic visual if stock video isn't found. Specify the style (e.g., '8k, cinematic lighting, cyberpunk, photorealistic').\n"
            "4. caption_highlights: An array of 1 to 3 words from the narration that should be heavily emphasized/highlighted in yellow or red on screen.\n"
            "5. estimated_duration: Estimated time in seconds the narration will take to read (usually ~2.5 to 3.5 words per second)."
        )

        prompt_instructions = (
            f"Create a production storyboard for the following concept: '{prompt}'.\n\n"
            "Your output must conform EXACTLY to this JSON structure:\n"
            "{\n"
            '  "title": "A highly clickable, high-CTR YouTube video title",\n'
            '  "description": "SEO optimized description containing rich keywords, standard formatting, and tags.",\n'
            '  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],\n'
            '  "storyboard": [\n'
            "    {\n"
            '      "scene_index": 1,\n'
            '      "narration": "First sentence of the script.",\n'
            '      "pexels_query": "royalty-free stock search keywords",\n'
            '      "ai_image_prompt": "DALL-E 3 detailed image prompt",\n'
            '      "caption_highlights": ["HIGHLIGHTED", "WORDS"],\n'
            '      "estimated_duration": 5\n'
            "    }\n"
            "  ]\n"
            "}"
        )

        try:
            response = self.model.generate_content(
                contents=f"{system_instruction}\n\n{prompt_instructions}",
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.75
                }
            )
            
            result_text = response.text.strip()
            # Clean possible markdown wrapping if returned anyway
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            plan_json = json.loads(result_text)
            logger.info("Successfully generated storyboard JSON and validated formatting.")
            return plan_json
            
        except Exception as e:
            logger.error(f"Error during generative storyboard creation: {e}", exc_info=True)
            # Fallback mock storyboard if API error happens so the pipeline remains functional
            logger.warning("Falling back to safety mock storyboard.")
            return {
                "title": f"The Ultimate Truth About {prompt}",
                "description": f"Exploring the incredible details behind {prompt}. Subscribe for more mind-bending automation content! #automation #ai",
                "tags": ["ai", "youtube automation", "shorts", "knowledge"],
                "storyboard": [
                    {
                        "scene_index": 1,
                        "narration": f"Did you know the secret behind {prompt} is changing the world?",
                        "pexels_query": "cyberpunk digital matrix background",
                        "ai_image_prompt": "A glowing digital grid matrix with a bright brain in the center, cinematic, neon, photorealistic, 8k",
                        "caption_highlights": ["SECRET", "CHANGING"],
                        "estimated_duration": 5
                    },
                    {
                        "scene_index": 2,
                        "narration": "Scientists were completely shocked when they discovered this fact.",
                        "pexels_query": "surprised scientist laboratory",
                        "ai_image_prompt": "A modern scientist with safety glasses looking shocked in a futuristic laboratory, warm backlighting, photorealistic, 8k",
                        "caption_highlights": ["SHOCKED", "DISCOVERED"],
                        "estimated_duration": 5
                    },
                    {
                        "scene_index": 3,
                        "narration": "Subscribe now for more mind blowing secrets you won't find anywhere else.",
                        "pexels_query": "subscribe finger pressing button",
                        "ai_image_prompt": "A neon glowing finger pressing a metallic holographic subscribe button, cinematic, particle effects, 8k",
                        "caption_highlights": ["SUBSCRIBE", "SECRETS"],
                        "estimated_duration": 4
                    }
                ]
            }
