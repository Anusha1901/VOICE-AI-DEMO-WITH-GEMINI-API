import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.GOOGLE_SHEETS_CREDS_PATH = os.getenv('GOOGLE_SHEETS_CREDS_PATH')
        self.GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'YOUR SHEET NAME')
        
        # Voice Configuration
        self.SPEECH_RATE = int(os.getenv('SPEECH_RATE', 150))
        self.LISTEN_TIMEOUT = int(os.getenv('LISTEN_TIMEOUT', 10))
        
        # Validate required configurations
        self.validate_config()
    
    def validate_config(self):
        """Validate that all required configurations are present"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Get it from: https://makersuite.google.com/app/apikey")
        
        if not self.GOOGLE_SHEETS_CREDS_PATH:
            raise ValueError("GOOGLE_SHEETS_CREDS_PATH is required for Google Sheets integration")
        
        if not os.path.exists(self.GOOGLE_SHEETS_CREDS_PATH):
            raise FileNotFoundError(f"Google Sheets credentials file not found: {self.GOOGLE_SHEETS_CREDS_PATH}")
    
    def get_config_info(self):
        """Return configuration information for debugging"""
        return {
            "gemini_api_configured": bool(self.GEMINI_API_KEY),
            "google_sheets_creds_path": self.GOOGLE_SHEETS_CREDS_PATH,
            "google_sheet_name": self.GOOGLE_SHEET_NAME,
            "speech_rate": self.SPEECH_RATE,
            "listen_timeout": self.LISTEN_TIMEOUT
        }
