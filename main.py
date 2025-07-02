"""
Voice AI Demo - Main Application
Integrates voice input, Gemini AI, voice output, and Google Sheets logging
"""

import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.voice_handler import VoiceHandler
from src.ai_handler import AIHandler
from src.sheets_handler import SheetsHandler

class VoiceAIDemo:
    def __init__(self):
        print("🚀 Initializing Voice AI Demo...")
        
        try:
            # Load configuration
            self.config = Config()
            print("✅ Configuration loaded")
            
            # Initialize handlers
            self.voice_handler = VoiceHandler(self.config)
            self.ai_handler = AIHandler(self.config)
            self.sheets_handler = SheetsHandler(self.config)
            
            # Generate session ID
            self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            print("✅ All components initialized successfully!")
            print(f"📊 Google Sheet URL: {self.sheets_handler.get_sheet_url()}")
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            sys.exit(1)
    
    def run_conversation_loop(self):
        """Main conversation loop"""
        print("\n" + "="*60)
        print("🎙️ VOICE AI DEMO STARTED")
        print("="*60)
        print("💡 Instructions:")
        print("   - Speak clearly into your microphone")
        print("   - Say 'quit', 'exit', or 'stop' to end")
        print("   - All conversations are logged to Google Sheets")
        print("="*60 + "\n")
        
        conversation_count = 0
        
        # Welcome message
        welcome_msg = "Hello! I'm your AI assistant powered by Gemini. How can I help you today?"
        print(f"🤖 {welcome_msg}")
        self.voice_handler.speak_text(welcome_msg)
        
        while True:
            try:
                print(f"\n--- Conversation {conversation_count + 1} ---")
                
                # Step 1: Listen for voice input
                user_input = self.voice_handler.listen_for_speech()
                
                if user_input is None:
                    # If no input received, continue listening
                    continue
                
                # Step 2: Check for exit commands
                if self.voice_handler.is_exit_command(user_input):
                    farewell_msg = "Goodbye! Thanks for chatting with me. Check the Google Sheet for our conversation log!"
                    print(f"🤖 {farewell_msg}")
                    self.voice_handler.speak_text(farewell_msg)
                    
                    # Log farewell
                    self.sheets_handler.log_conversation(
                        user_input, 
                        farewell_msg, 
                        self.session_id
                    )
                    break
                
                # Step 3: Generate AI response using Gemini
                ai_response = self.ai_handler.generate_response(user_input)
                
                # Step 4: Speak the AI response
                self.voice_handler.speak_text(ai_response)
                
                # Step 5: Log conversation to Google Sheets
                success = self.sheets_handler.log_conversation(
                    user_input, 
                    ai_response, 
                    self.session_id
                )
                
                if success:
                    conversation_count += 1
                    print(f"📊 Total conversations logged: {conversation_count}")
                
                print("\n" + "-"*50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation interrupted by user (Ctrl+C)")
                break
                
            except Exception as e:
                print(f"❌ Unexpected error in conversation loop: {e}")
                error_msg = "Sorry, I encountered an error. Let's try again."
                self.voice_handler.speak_text(error_msg)
                continue
        
        # Final summary
        self.print_session_summary(conversation_count)
    
    def print_session_summary(self, conversation_count):
        """Print session summary"""
        print("\n" + "="*60)
        print("📊 SESSION SUMMARY")
        print("="*60)
        print(f"🗣️  Total conversations: {conversation_count}")
        print(f"🆔 Session ID: {self.session_id}")
        print(f"📊 Google Sheet: {self.sheets_handler.get_sheet_url()}")
        print(f"📈 Total logged conversations: {self.sheets_handler.get_conversation_count()}")
        print("="*60)
        print("✅ Voice AI Demo completed successfully!")

def main():
    """Main entry point"""
    try:
        # Create and run the demo
        demo = VoiceAIDemo()
        demo.run_conversation_loop()
        
    except KeyboardInterrupt:
        print("\n👋 Demo terminated by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()