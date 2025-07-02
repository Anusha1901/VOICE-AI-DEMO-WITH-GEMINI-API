import speech_recognition as sr
import pyttsx3
from src.config import Config

class VoiceHandler:
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', config.SPEECH_RATE)
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("🎤 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone calibrated!")
    
    def listen_for_speech(self):
        """Capture and convert speech to text"""
        print("🎤 Listening... Speak now!")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.config.LISTEN_TIMEOUT, 
                    phrase_time_limit=15
                )
            
            print("🔄 Converting speech to text...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            error_msg = "⏰ Timeout: I didn't hear anything. Please try again."
            print(error_msg)
            return None
            
        except sr.UnknownValueError:
            error_msg = "❓ Sorry, I couldn't understand what you said. Please speak clearly."
            print(error_msg)
            return None
            
        except sr.RequestError as e:
            error_msg = f"🌐 Network error: Could not request results from Google Speech Recognition service; {e}"
            print(error_msg)
            return None
    
    def speak_text(self, text):
        """Convert text to speech and play it"""
        if not text:
            return
            
        print(f"🔊 Speaking: '{text}'")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error in text-to-speech: {e}")
    
    def is_exit_command(self, text):
        """Check if the user wants to exit"""
        if not text:
            return False
        
        exit_commands = ['quit', 'exit', 'stop', 'goodbye', 'bye', 'end']
        return text.lower().strip() in exit_commands
