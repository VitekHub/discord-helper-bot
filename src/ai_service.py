import google.generativeai as genai
from .config import GOOGLE_API_KEY

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def get_ai_summary(text):
    """Get summary from Google AI"""
    prompt = f"Please provide a concise summary of the following conversation:\n\n{text}"

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

async def get_vital_info(text):
    """Extract vital information from messages"""
    prompt = f"""Prosím analyzuj následující konverzaci a najdi a extrahuj pouze důležité informace a klíčová sdělení. Odstraň zbytečné části konverzace a small talk. Pokud najdeš obzvláště důležité zprávy, zkopíruj je doslovně. Pokud je to relevantní, zdůrazni termíny, deadliny nebo úkoly.

Text konverzace:

{text}"""

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Chyba při generování analýzy: {str(e)}"