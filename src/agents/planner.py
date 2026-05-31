import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from src.config import (
    GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
    ENABLE_SENTIMENT_ANALYSIS, ENABLE_AUTO_EMOJI, logger as config_logger
)

logger = logging.getLogger("YoutubeStoryboardAgent")


class AdvancedStoryboardPlanner:
    """Enhanced storyboard planner with multi-AI provider support, sentiment analysis, and emoji integration."""
    
    def __init__(self, preferred_provider: str = "auto"):
        """
        Initialize the planner with intelligent provider selection.
        
        Args:
            preferred_provider: 'gemini', 'openai', 'anthropic', or 'auto' for smart selection
        """
        self.available_providers = []
        self.preferred_provider = preferred_provider
        
        # Detect available providers
        if GEMINI_API_KEY:
            self.available_providers.append("gemini")
        if OPENAI_API_KEY:
            self.available_providers.append("openai")
        if ANTHROPIC_API_KEY:
            self.available_providers.append("anthropic")
        
        if not self.available_providers:
            logger.warning("No AI providers configured! Will use fallback templates.")
            self.active_provider = None
        else:
            # Smart provider selection
            if preferred_provider == "auto" or preferred_provider not in self.available_providers:
                # Priority: Gemini (fastest/cheapest) > OpenAI > Anthropic
                self.active_provider = next((p for p in ["gemini", "openai", "anthropic"] 
                                            if p in self.available_providers), None)
            else:
                self.active_provider = preferred_provider
        
        logger.info(f"StoryboardPlanner initialized with provider: {self.active_provider}")
        
        # Initialize provider clients
        if self.active_provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-pro")
        elif self.active_provider == "openai":
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        elif self.active_provider == "anthropic":
            import anthropic
            self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze emotional tone of text for better voice and visual matching."""
        if not ENABLE_SENTIMENT_ANALYSIS or not self.active_provider:
            return {"positive": 0.5, "negative": 0.0, "neutral": 0.5, "excitement": 0.5}
        
        try:
            sentiment_prompt = (
                f"Analyze the emotional tone of this text and return ONLY valid JSON:\n"
                f"Text: \"{text[:200]}\"\n\n"
                "Return format: {\"positive\": 0.0-1.0, \"negative\": 0.0-1.0, \"neutral\": 0.0-1.0, "
                "\"excitement\": 0.0-1.0, \"urgency\": 0.0-1.0}"
            )
            
            if self.active_provider == "gemini":
                response = self.model.generate_content(
                    sentiment_prompt,
                    generation_config={"response_mime_type": "application/json", "temperature": 0.3}
                )
                return json.loads(response.text.strip())
            elif self.active_provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": sentiment_prompt}],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return {"positive": 0.5, "negative": 0.0, "neutral": 0.5, "excitement": 0.5}
    
    def enhance_with_emojis(self, text: str, context: str = "") -> str:
        """Intelligently add relevant emojis to text for higher engagement."""
        if not ENABLE_AUTO_EMOJI:
            return text
        
        emoji_map = {
            "secret": "🤫", "amazing": "😱", "shocking": "💥", "incredible": "✨",
            "discover": "🔍", "learn": "📚", "science": "🔬", "technology": "💻",
            "future": "🚀", "money": "💰", "success": "🏆", "danger": "⚠️",
            "warning": "⚠️", "important": "❗", "new": "🆕", "free": "🎁",
            "best": "👑", "worst": "💩", "love": "❤️", "hate": "💔",
            "happy": "😊", "sad": "😢", "angry": "😡", "surprised": "😲",
            "earth": "🌍", "space": "🌌", "ocean": "🌊", "fire": "🔥",
            "time": "⏰", "idea": "💡", "question": "❓", "answer": "✅"
        }
        
        enhanced_text = text
        words = re.findall(r'\b\w+\b', text.lower())
        
        for word in words:
            if word in emoji_map and emoji_map[word] not in enhanced_text:
                # Add emoji after the word (case-insensitive replacement)
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                enhanced_text = pattern.sub(f"{word} {emoji_map[word]}", enhanced_text, count=1)
        
        return enhanced_text
    
    def generate_viral_hooks(self, topic: str, count: int = 5) -> List[str]:
        """Generate multiple viral hook options for A/B testing."""
        hook_templates = [
            f"You won't believe what scientists just discovered about {topic}...",
            f"The {topic} secret they don't want you to know!",
            f"This changes everything we knew about {topic}!",
            f"Why everyone is talking about {topic} right now...",
            f"The truth about {topic} will shock you!",
            f"What happens next with {topic} is insane!",
            f"I bet you didn't know this about {topic}!",
            f"The dark side of {topic} exposed!"
        ]
        
        if self.active_provider:
            try:
                hook_prompt = (
                    f"Generate {count} ultra-viral YouTube hooks about '{topic}'. "
                    "Each hook must be under 12 words, create curiosity, and trigger immediate interest. "
                    "Return ONLY a JSON array of strings."
                )
                
                if self.active_provider == "gemini":
                    response = self.model.generate_content(
                        hook_prompt,
                        generation_config={"response_mime_type": "application/json", "temperature": 0.8}
                    )
                    return json.loads(response.text.strip())
                elif self.active_provider == "openai":
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": hook_prompt}],
                        response_format={"type": "json_object"}
                    )
                    result = json.loads(response.choices[0].message.content)
                    return result.get("hooks", hook_templates[:count])
            except Exception as e:
                logger.warning(f"AI hook generation failed: {e}")
        
        return hook_templates[:count]
    
    def optimize_for_seo(self, title: str, description: str, topic: str) -> Dict[str, Any]:
        """Optimize title, description, and tags for maximum discoverability."""
        if not self.active_provider:
            # Basic SEO optimization
            base_tags = [topic.lower().replace(" ", ""), "ai", "automation", "youtube", "viral"]
            return {
                "optimized_title": title,
                "optimized_description": description,
                "tags": base_tags,
                "hashtags": [f"#{tag}" for tag in base_tags[:5]]
            }
        
        try:
            seo_prompt = (
                f"Optimize this YouTube video for maximum CTR and SEO:\n"
                f"Topic: {topic}\n"
                f"Current Title: {title}\n"
                f"Current Description: {description[:500]}\n\n"
                "Return JSON with: optimized_title (under 60 chars), optimized_description (with keywords), "
                "tags (10-15 relevant tags), hashtags (5 trending hashtags)"
            )
            
            if self.active_provider == "gemini":
                response = self.model.generate_content(
                    seo_prompt,
                    generation_config={"response_mime_type": "application/json", "temperature": 0.7}
                )
                return json.loads(response.text.strip())
            elif self.active_provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": seo_prompt}],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.warning(f"SEO optimization failed: {e}")
            return {
                "optimized_title": title,
                "optimized_description": description,
                "tags": [topic.lower(), "ai", "viral", "trending"],
                "hashtags": ["#viral", "#trending", "#ai"]
            }
    
    def generate_plan(self, prompt: str, format_type: str = "shorts", 
                     voice_profile: str = "default", enable_hooks: bool = True) -> Dict[str, Any]:
        """
        Generate a comprehensive, production-ready storyboard with advanced features.
        
        Args:
            prompt: User's creative topic/prompt
            format_type: 'shorts', 'long-form', or 'square'
            voice_profile: Voice personality to match script tone
            enable_hooks: Whether to generate multiple hook variations
            
        Returns:
            Complete production plan with storyboard, SEO metadata, and engagement optimizations
        """
        import time
        start_time = time.time()
        
        logger.info(f"🎬 Generating advanced storyboard for: '{prompt}' | Format: {format_type}")
        logger.info(f"Active AI Provider: {self.active_provider}")
        
        # Step 1: Generate viral hooks for A/B testing
        viral_hooks = []
        if enable_hooks:
            viral_hooks = self.generate_viral_hooks(prompt, count=5)
            logger.info(f"Generated {len(viral_hooks)} viral hook variations")
        
        # Step 2: Build enhanced system instruction
        # Duration configuration: shorts (30-50s), long-form (5-15 minutes), square (60-90s)
        if format_type == "shorts":
            scene_count = "4 to 8"
            duration_range = "30-50 seconds"
            narration_limit = "15 words"
        elif format_type == "long-form":
            scene_count = "20 to 40"
            duration_range = "5-15 minutes (300-900 seconds)"
            narration_limit = "30-40 words"
        else:  # square
            scene_count = "8 to 12"
            duration_range = "60-90 seconds"
            narration_limit = "20 words"
        
        system_instruction = f"""You are an elite YouTube Content Strategist and Viral Video Expert.
Create a high-retention storyboard optimized for {format_type} format ({duration_range} total).

CRITICAL REQUIREMENTS:
1. Start with an IRRESISTIBLE hook in the first 3 seconds that creates curiosity
2. Each scene must have clear visual direction and emotional pacing
3. Include pattern interrupts every 3-5 seconds to maintain attention
4. End with a strong CTA (Call To Action)
5. Use simple, conversational language (grade 6-8 reading level)
6. For long-form videos: Create comprehensive content with deep dives, examples, and storytelling

SCENE STRUCTURE (each scene must include):
- narration: Natural spoken script (max {narration_limit})
- pexels_query: Simple 2-4 word stock footage search term
- ai_image_prompt: Detailed DALL-E prompt with style (cinematic, 8k, dramatic lighting)
- caption_highlights: 2-3 power words to emphasize visually
- estimated_duration: Realistic timing in seconds (5-8s for shorts, 8-15s for long-form)
- emotion_tag: Primary emotion (curiosity, excitement, surprise, urgency, etc.)
- transition_suggestion: Suggested transition to next scene (fade, zoom, wipe, etc.)

OUTPUT FORMAT: Return ONLY valid JSON matching this exact schema:"""

        json_schema = """{
  "title": "Ultra-clickable title under 60 characters",
  "alternative_titles": ["Option B", "Option C"],
  "description": "SEO-rich description with keywords and timestamps",
  "tags": ["tag1", "tag2", ...],
  "hashtags": ["#hashtag1", "#hashtag2", ...],
  "category": "Education|Entertainment|Science|Technology|News",
  "target_audience": "Description of ideal viewer",
  "thumbnail_concept": "Visual description for thumbnail design",
  "storyboard": [
    {
      "scene_index": 1,
      "narration": "Script text here",
      "pexels_query": "search terms",
      "ai_image_prompt": "Detailed visual prompt",
      "caption_highlights": ["WORD1", "WORD2"],
      "estimated_duration": 4,
      "emotion_tag": "curiosity",
      "transition_suggestion": "zoom_in",
      "on_screen_text": "Optional text overlay"
    }
  ],
  "engagement_hooks": {
    "opening_hook": "First 3-second attention grabber",
    "midpoint_retention": "Pattern interrupt at 50%",
    "closing_cta": "Strong call-to-action"
  }
}"""

        full_prompt = f"{system_instruction}\n\nJSON Schema:\n{json_schema}\n\nCreate storyboard for topic: {prompt}"

        # Step 3: Call AI provider
        try:
            if self.active_provider == "gemini":
                response = self.model.generate_content(
                    full_prompt,
                    generation_config={
                        "response_mime_type": "application/json",
                        "temperature": 0.75,
                        "top_p": 0.9
                    }
                )
                result_text = response.text.strip()
            elif self.active_provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a JSON-only assistant. Return only valid JSON."},
                        {"role": "user", "content": full_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.75
                )
                result_text = response.choices[0].message.content.strip()
            elif self.active_provider == "anthropic":
                response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": full_prompt}]
                )
                result_text = response.content[0].text.strip()
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result_text = json_match.group()
            else:
                raise Exception("No AI provider available")
            
            # Clean markdown formatting
            if result_text.startswith("```"):
                result_text = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
                result_text = result_text.group(1).strip() if result_text else result_text
            
            plan = json.loads(result_text)
            
            # Step 4: Post-process and enhance
            logger.info("✨ Enhancing storyboard with emojis and sentiment analysis...")
            
            for scene in plan.get("storyboard", []):
                # Add emojis to narration
                if ENABLE_AUTO_EMOJI:
                    scene["narration"] = self.enhance_with_emojis(
                        scene.get("narration", ""),
                        scene.get("emotion_tag", "")
                    )
                
                # Analyze sentiment for voice matching
                if ENABLE_SENTIMENT_ANALYSIS:
                    scene["sentiment"] = self.analyze_sentiment(scene.get("narration", ""))
            
            # Add viral hooks
            if viral_hooks:
                plan["viral_hooks"] = viral_hooks
            
            # Optimize SEO
            seo_data = self.optimize_for_seo(
                plan.get("title", prompt),
                plan.get("description", ""),
                prompt
            )
            plan.update(seo_data)
            
            # Calculate total duration
            total_duration = sum(scene.get("estimated_duration", 5) for scene in plan.get("storyboard", []))
            plan["metadata"] = {
                "total_scenes": len(plan.get("storyboard", [])),
                "estimated_duration": total_duration,
                "format": format_type,
                "voice_profile": voice_profile,
                "generation_time_seconds": round(time.time() - start_time, 2),
                "ai_provider": self.active_provider
            }
            
            logger.info(f"✅ Storyboard generated successfully in {plan['metadata']['generation_time_seconds']}s")
            logger.info(f"   • Scenes: {plan['metadata']['total_scenes']}")
            logger.info(f"   • Duration: ~{total_duration}s")
            logger.info(f"   • Title: {plan.get('title', 'N/A')}")
            
            return plan
            
        except Exception as e:
            logger.error(f"❌ AI storyboard generation failed: {e}", exc_info=True)
            return self._generate_fallback_plan(prompt, format_type, viral_hooks)
    
    def _generate_fallback_plan(self, prompt: str, format_type: str, viral_hooks: List[str] = None) -> Dict[str, Any]:
        """Generate a functional fallback plan when AI providers fail."""
        logger.warning("⚠️ Using fallback template storyboard")
        
        # Duration configuration for fallback plans
        if format_type == "shorts":
            scene_duration_base = 4
            num_scenes = 6
        elif format_type == "long-form":
            scene_duration_base = 12
            num_scenes = 30  # More scenes for longer videos
        else:  # square
            scene_duration_base = 6
            num_scenes = 10
        
        scenes = []
        # Generate dynamic number of scenes based on format type
        for i in range(num_scenes):
            if i == 0:
                narration = f"🤯 You won't believe the truth about {prompt}!"
                emotion = "curiosity"
                duration = scene_duration_base + 2
            elif i == num_scenes - 1:
                narration = f"👉 Subscribe for more mind-blowing secrets!"
                emotion = "urgency"
                duration = scene_duration_base - 1
            else:
                narrations = [
                    f"🔍 Scientists made a SHOCKING discovery...",
                    f"💡 This changes EVERYTHING we knew!",
                    f"✨ The results will blow your mind!",
                    f"🚀 Here's what happens next...",
                    f"⚠️ But there's a catch...",
                    f"🎯 The real secret is...",
                    f"🌟 This could change your life!",
                    f"📊 The data shows something amazing...",
                    f"🔥 Why everyone's talking about this...",
                    f"💰 The implications are huge!"
                ]
                narration = narrations[i % len(narrations)]
                emotion = ["surprise", "excitement", "curiosity", "amazement"][i % 4]
                duration = scene_duration_base + (i % 3)
            
            scenes.append({
                "scene_index": i + 1,
                "narration": narration,
                "pexels_query": "cinematic background",
                "ai_image_prompt": f"Cinematic visual for {prompt}, dramatic lighting, 8k, professional quality",
                "caption_highlights": ["AMAZING", "SECRET"] if i == 0 else ["DISCOVER", "TRUTH"],
                "estimated_duration": duration,
                "emotion_tag": emotion,
                "transition_suggestion": ["zoom_in", "wipe_right", "fade", "zoom_out"][i % 4],
                "sentiment": {"positive": 0.5 + (i * 0.05), "excitement": 0.8, "urgency": 0.6 if i == num_scenes - 1 else 0.5}
            })
        
        return {
            "title": f"The {prompt.title()} Secret They Don't Want You To Know",
            "alternative_titles": viral_hooks if viral_hooks else [
                f"Why Everyone's Talking About {prompt}",
                f"The Dark Truth About {prompt}"
            ],
            "description": f"Discover the incredible secrets behind {prompt}. This video will change how you see everything! 🔥\n\n👍 Like, Comment & Subscribe for more!\n\n#{prompt.replace(' ', '')} #viral #trending #ai",
            "tags": [prompt.lower().replace(" ", ""), "viral", "trending", "ai", "automation", "secrets", "knowledge"],
            "hashtags": ["#viral", "#trending", "#fyp", "#ai", "#knowledge"],
            "category": "Education",
            "target_audience": "Curious learners aged 16-35 interested in cutting-edge topics",
            "thumbnail_concept": f"Dramatic close-up with bold text '{prompt.upper()[:20]}...' and shocking expression",
            "storyboard": scenes,
            "engagement_hooks": {
                "opening_hook": "Start with shocking statement or question",
                "midpoint_retention": "Reveal unexpected twist at 50% mark",
                "closing_cta": "Strong subscribe call with value proposition"
            },
            "metadata": {
                "total_scenes": len(scenes),
                "estimated_duration": sum(s["estimated_duration"] for s in scenes),
                "format": format_type,
                "voice_profile": "default",
                "generation_time_seconds": 0.1,
                "ai_provider": "fallback_template",
                "is_fallback": True
            }
        }
