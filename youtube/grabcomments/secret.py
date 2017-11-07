from googleapiclient.discovery import build_from_document, build
from googleapiclient.errors import HttpError
CLIENT_SECRETS_FILE = "client_secrets.json"
DEVELOPER_KEY = "AIzaSyCXnEFcvqXBSneWmx0ldq3HlIJcJCvjqbA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


