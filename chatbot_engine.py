import google.genai as genai
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict


class GeminiEngine:
    def __init__(self, model_name="gemini-2.0-flash-001"):
        load_dotenv()
        self._history: List[Dict[str, str]] = []
        self.api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=self.api_key)

    def get_response(self, prompt):
        # Send user input to the Gemini model and get a response
        # Handle potential exceptions during the API call
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )

            # Update chat history in standard format for UI
            self._history.append({"role": "user", "content": prompt})
            self._history.append({"role": "assistant", "content": response.text})
            return response.text
        except Exception as e:
            return f"Error: {e}"

    def get_history(self):
        # Return the chat history so can be show in UI
        return self._history


class GroqEngine:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self._history: List[Dict[str, str]] = []
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        self.model = Groq(api_key=self.api_key)
        self.model_name = model_name

    def get_response(
        self, prompt: str, system_message: str = "You are a helpful assistant."
    ):
        try:
            self._history.append({"role": "user", "content": prompt})
            chat_completion = self.model.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                model=self.model_name,
                temperature=0.5,  # Controls creativity
                max_tokens=1024,  # Limits response length
            )
            response = chat_completion.choices[0].message.content
            self._history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Groq API Error: {str(e)}"

    def get_history(self):
        # Return the chat history so can be show in UI
        return self._history


"""
main_chatbot = GroqChatBot()
response = main_chatbot.get_response("Explain quantum computing in simple terms.")
print("Groq Response:", response)
print("Groq Chat History:", main_chatbot.get_history())
"""
