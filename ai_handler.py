import google.generativeai as genai
from src.config import Config

class AIHandler:
    def __init__(self, config: Config):
        self.config = config
        
        # Configure Gemini AI
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        # Conversation context
        self.conversation_history = []
        
        print("🤖 Gemini AI initialized successfully!")
    
    def generate_response(self, user_input):
        """Generate AI response using Gemini"""
        try:
            print("🤖 Generating AI response...")
            
            # Build conversation context
            context = self._build_context()
            
            # Create prompt with context
            prompt = f"""
            {context}
            
            Current user input: {user_input}
            
            Instructions:
            - Respond naturally and conversationally
            - Keep responses concise but helpful (1-3 sentences)
            - Be friendly and engaging
            - If asked about your capabilities, mention you're powered by Gemini AI
            
            Your response:
            """
            
            response = self.model.generate_content(prompt)
            ai_response = response.text.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                'user': user_input,
                'ai': ai_response
            })
            
            # Keep only last 5 exchanges to manage context length
            if len(self.conversation_history) > 5:
                self.conversation_history = self.conversation_history[-5:]
            
            print(f"🤖 AI Response: '{ai_response}'")
            return ai_response
            
        except Exception as e:
            error_response = f"Sorry, I encountered an error while thinking. Could you please repeat that?"
            print(f"❌ Gemini AI Error: {e}")
            return error_response
    
    def _build_context(self):
        """Build conversation context from history"""
        if not self.conversation_history:
            return "You are a helpful AI assistant powered by Gemini. This is the start of a new conversation."
        
        context = "Previous conversation context:\n"
        for exchange in self.conversation_history[-3:]:  # Last 3 exchanges
            context += f"User: {exchange['user']}\n"
            context += f"AI: {exchange['ai']}\n"
        
        return context
    
    def get_conversation_summary(self):
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation yet."
        
        total_exchanges = len(self.conversation_history)
        return f"Conversation had {total_exchanges} exchanges."
