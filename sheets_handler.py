import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from src.config import Config

class SheetsHandler:
    def __init__(self, config: Config):
        self.config = config
        self.sheet = None
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            print("📊 Setting up Google Sheets connection...")
            
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Authenticate using service account
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.config.GOOGLE_SHEETS_CREDS_PATH, 
                scope
            )
            client = gspread.authorize(creds)
            
            # Open or create the spreadsheet
            try:
                spreadsheet = client.open(self.config.GOOGLE_SHEET_NAME)
                self.sheet = spreadsheet.sheet1
                print(f"✅ Connected to existing sheet: '{self.config.GOOGLE_SHEET_NAME}'")
                
            except gspread.SpreadsheetNotFound:
                print(f"📝 Creating new spreadsheet: '{self.config.GOOGLE_SHEET_NAME}'")
                spreadsheet = client.create(self.config.GOOGLE_SHEET_NAME)
                self.sheet = spreadsheet.sheet1
                
                # Set up headers
                headers = ["Timestamp", "User Input", "AI Response", "Session ID"]
                self.sheet.append_row(headers)
                
                # Format headers
                self.sheet.format('A1:D1', {
                    "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 1.0},
                    "textFormat": {"bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}
                })
                
                print("✅ New spreadsheet created with headers!")
            
            # Make sheet shareable (optional)
            try:
                spreadsheet.share('', perm_type='anyone', role='reader')
                print(f"🔗 Sheet URL: {spreadsheet.url}")
            except:
                print("ℹ️ Sheet created but not made publicly shareable")
                
        except Exception as e:
            raise Exception(f"Failed to setup Google Sheets: {e}")
    
    def log_conversation(self, user_input, ai_response, session_id=None):
        """Log conversation to Google Sheets"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if session_id is None:
                session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            
            row_data = [timestamp, user_input, ai_response, session_id]
            
            self.sheet.append_row(row_data)
            print("✅ Conversation logged to Google Sheets")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to log to Google Sheets: {e}")
            return False
    
    def get_conversation_count(self):
        """Get total number of conversations logged"""
        try:
            return len(self.sheet.get_all_records())
        except:
            return 0
    
    def get_sheet_url(self):
        """Get the URL of the Google Sheet"""
        try:
            return self.sheet.spreadsheet.url
        except:
            return "URL not available"
