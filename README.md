# 🎙️ Voice AI Demo with Gemini & Google Sheets

A complete voice-powered AI assistant that combines speech recognition, Google's Gemini AI, text-to-speech, and automatic conversation logging to Google Sheets. Talk to AI naturally and keep track of all your conversations!

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

- 🎤 **Real-time Speech Recognition** - Converts your voice to text using Google Speech API
- 🤖 **Gemini AI Integration** - Powered by Google's advanced Gemini Pro model
- 🔊 **Natural Voice Responses** - Text-to-speech with customizable voice settings
- 📊 **Google Sheets Logging** - Automatically logs all conversations with timestamps
- 🔄 **Session Management** - Organized conversation tracking with unique session IDs
- ⚡ **Real-time Processing** - Fast response times with conversation context
- 🛡️ **Error Handling** - Robust error management and retry mechanisms
- 🎯 **Easy Setup** - Simple configuration with environment variables

## 🎬 Demo

```
🎤 Listening... Speak now!
👤 You said: 'Tell me a joke about programming'
🤖 AI Response: 'Why do programmers prefer dark mode? Because light attracts bugs!'
🔊 Speaking response...
✅ Conversation logged to Google Sheets
```

## 📁 Project Structure

```
voice-ai-demo/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── voice_handler.py         # Speech recognition & TTS
│   ├── ai_handler.py            # Gemini AI integration
│   └── sheets_handler.py        # Google Sheets logging
├── credentials/
│   └── google_sheets_credentials.json  # Service account key
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── main.py                      # Main application
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/voice-ai-demo-with-gemini-api.git
cd voice-ai-demo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get API Keys & Credentials

#### Gemini API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for later use

#### Google Sheets Credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **Service Account**:
   - Go to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Name: `voice-ai-sheets-access`
   - Create and download JSON key
5. Rename the downloaded file to `google_sheets_credentials.json`
6. Move it to the `credentials/` folder

### 4. Configure Environment

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEETS_CREDS_PATH=credentials/google_sheets_credentials.json
GOOGLE_SHEET_NAME=YOUR SHEET NAME
SPEECH_RATE=150
LISTEN_TIMEOUT=10
```

### 5. Run the Application

```bash
python main.py
```

## 🎯 Usage

1. **Start the application**: Run `python main.py`
2. **Wait for initialization**: The system will calibrate your microphone and connect to services
3. **Listen for the prompt**: Wait for "🎤 Listening... Speak now!"
4. **Speak clearly**: Say your message into the microphone
5. **Get AI response**: The AI will respond with voice and text
6. **Continue conversation**: Keep talking or say "quit" to exit
7. **Check Google Sheets**: All conversations are automatically logged

### Voice Commands to Try:

- "Hello, how are you?"
- "Tell me a joke"
- "What's 15 multiplied by 23?"
- "Explain quantum computing in simple terms"
- "What can you help me with?"
- "quit" / "exit" / "stop" (to end session)

## 📊 Google Sheets Output

The application creates a spreadsheet with these columns:

| Timestamp | User Input | AI Response | Session ID |
|-----------|------------|-------------|------------|
| 2024-01-15 14:30:22 | Hello there | Hi! How can I help you today? | 20240115_143022 |
| 2024-01-15 14:30:45 | Tell me a joke | Why don't scientists trust atoms?... | 20240115_143022 |

## ⚙️ Configuration Options

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Gemini API key | Required |
| `GOOGLE_SHEETS_CREDS_PATH` | Path to service account JSON | `credentials/google_sheets_credentials.json` |
| `GOOGLE_SHEET_NAME` | Name of the Google Sheet | `YOUR SHEET NAME` |
| `SPEECH_RATE` | Text-to-speech speed (words/minute) | `150` |
| `LISTEN_TIMEOUT` | Microphone timeout (seconds) | `10` |

### Voice Settings

You can customize the voice in `src/voice_handler.py`:

```python
# Change voice properties
self.tts_engine.setProperty('rate', 150)    # Speed
self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Change voice (if multiple voices available)
voices = self.tts_engine.getProperty('voices')
self.tts_engine.setProperty('voice', voices[0].id)  # Female voice
self.tts_engine.setProperty('voice', voices[1].id)  # Male voice
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. JWT Authentication Error
```
Error: invalid_grant: Invalid JWT: Token must be a short-lived token
```
**Solution:** Synchronize your system time
```bash

# Windows
w32tm /resync
```

#### 2. Microphone Not Working
```
Error: Could not request results from Google Speech Recognition service
```
**Solutions:**
- Check microphone permissions in system settings
- Test microphone: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`
- Ensure internet connection (uses Google Speech API)

#### 3. PyAudio Installation Issues
```
Error: Microsoft Visual C++ 14.0 is required
```
**Solutions:**
- **Windows**: Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

#### 4. Gemini API Errors
```
Error: API key not valid
```
**Solutions:**
- Verify API key in `.env` file
- Check API quota at [Google AI Studio](https://makersuite.google.com/)
- Ensure billing is set up if required

#### 5. Google Sheets Access Denied
```
Error: The caller does not have permission
```
**Solutions:**
- Share your Google Sheet with the service account email
- Check that both Google Sheets API and Google Drive API are enabled
- Verify credentials file path in `.env`

### Debug Commands

```bash

# Test microphone
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('Say something:'); print(r.recognize_google(r.listen(sr.Microphone())))"

# Check credentials
python -c "import json; print(json.load(open('credentials/google_sheets_credentials.json'))['client_email'])"

# Test Gemini API
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('API key works!')"
```

## 🔒 Security & Privacy

- **API Keys**: Store in `.env` file, never commit to version control
- **Credentials**: Service account JSON should be kept secure
- **Voice Data**: Processed by Google Speech Recognition API
- **Conversations**: Logged to your private Google Sheets
- **Local Storage**: No sensitive data stored locally

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/voice-ai-demo-with-gemini-api.git
cd voice-ai-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

## 🙏 Acknowledgments

- **Google Gemini AI** - For the powerful language model
- **Google Speech Recognition** - For accurate speech-to-text
- **gspread** - For easy Google Sheets integration
- **pyttsx3** - For cross-platform text-to-speech
- **SpeechRecognition** - For microphone input handling


## 🔮 Future Features

- [ ] Multiple language support
- [ ] Custom wake words
- [ ] Voice training for better recognition
- [ ] Export conversations to different formats
- [ ] Integration with other AI models
- [ ] Mobile app version
- [ ] Real-time transcription display
- [ ] Conversation analytics dashboard

## 📈 Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Basic voice recognition and AI response
- Google Sheets integration
- Error handling and retry mechanisms

---


