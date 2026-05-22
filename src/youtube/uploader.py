import os
import pickle
import logging
from typing import List, Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.config import BASE_DIR

logger = logging.getLogger("YoutubeUploader")

class YouTubeUploader:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.client_secrets_file = BASE_DIR / "client_secret.json"
        self.token_pickle_file = BASE_DIR / "token.pickle"
        self.youtube_client = None

    def authenticate(self) -> bool:
        """Loads cached credentials or initiates the browser OAuth2 flow."""
        creds = None
        
        # Load cached token if it exists
        if self.token_pickle_file.exists():
            try:
                with open(self.token_pickle_file, "rb") as token:
                    creds = pickle.load(token)
                logger.info("Loaded cached YouTube credentials from token.pickle")
            except Exception as e:
                logger.warning(f"Could not load cached credentials: {e}")

        # If no credentials or they are invalid, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    logger.info("Refreshing expired credentials...")
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh YouTube credentials: {e}")
                    creds = None

            if not creds:
                if not self.client_secrets_file.exists():
                    logger.warning("=" * 60)
                    logger.warning("YOUTUBE PUBLISHER API KEY ERROR:")
                    logger.warning(f"Could not find '{self.client_secrets_file.name}' in the project root.")
                    logger.warning("To enable auto-uploading, download your OAuth2 client credentials JSON from:")
                    logger.warning("https://console.cloud.google.com/apis/credentials")
                    logger.warning(f"and save it as '{self.client_secrets_file.name}' in your workspace directory.")
                    logger.warning("=" * 60)
                    return False
                
                try:
                    logger.info("Starting YouTube OAuth2 Web Browser Authentication Flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.client_secrets_file), self.scopes
                    )
                    creds = flow.run_local_server(port=0)
                    
                    # Cache the credentials
                    with open(self.token_pickle_file, "wb") as token:
                        pickle.dump(creds, token)
                    logger.info("Successfully authenticated and cached credentials in token.pickle")
                except Exception as e:
                    logger.error(f"YouTube OAuth2 authentication failed: {e}", exc_info=True)
                    return False

        try:
            self.youtube_client = build("youtube", "v3", credentials=creds)
            return True
        except Exception as e:
            logger.error(f"Failed to build YouTube service client: {e}", exc_info=True)
            return False

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        thumbnail_path: Optional[str] = None,
        privacy_status: str = "private"
    ) -> Optional[str]:
        """Uploads the video to YouTube and assigns a custom thumbnail.
        
        Returns:
            The uploaded YouTube Video ID if successful, otherwise None.
        """
        if not self.youtube_client:
            logger.warning("YouTube service is not authenticated. Skipping publishing.")
            return None

        logger.info(f"Initiating chunked YouTube upload for: {video_path}")
        
        body = {
            "snippet": {
                "title": title[:100],  # Title limit is 100 characters
                "description": description,
                "tags": tags,
                "categoryId": "27"  # Education category ID
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        try:
            # Setup chunked media upload (chunksize of 1024*1024 bytes is perfect)
            media = MediaFileUpload(
                video_path, chunksize=1024 * 1024, mimetype="video/mp4", resumable=True
            )
            
            request = self.youtube_client.videos().insert(
                part="snippet,status", body=body, media_body=media
            )
            
            response = None
            logger.info("Uploading video blocks...")
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Uploaded progress: {int(status.progress() * 100)}%")

            video_id = response.get("id")
            logger.info(f"Video uploaded successfully! YouTube Video ID: {video_id}")

            # Upload Thumbnail if provided
            if video_id and thumbnail_path and os.path.exists(thumbnail_path):
                self._upload_thumbnail(video_id, thumbnail_path)

            return video_id

        except Exception as e:
            logger.error(f"An error occurred during video upload: {e}", exc_info=True)
            return None

    def _upload_thumbnail(self, video_id: str, thumbnail_path: str):
        """Attaches the custom thumbnail to the uploaded YouTube video."""
        logger.info(f"Uploading custom thumbnail: {thumbnail_path} for Video: {video_id}")
        try:
            request = self.youtube_client.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
            )
            request.execute()
            logger.info("Thumbnail applied successfully.")
        except Exception as e:
            logger.error(f"Thumbnail upload failed: {e}", exc_info=True)
