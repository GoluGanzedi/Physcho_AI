import google.generativeai as genai
from .config import API_KEY

# Configure the AI client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
