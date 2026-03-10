import os
import logging
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ Error: GEMINI_API_KEY is missing in .env file!")

# Initialize the client. This is the NEW way to configure the SDK.
client = genai.Client(api_key=GEMINI_API_KEY)


async def ask_llm(
    prompt: str, system_instruction: str = None, temperature: float = 0.7
) -> str:
    """
    Core function to communicate with the LLM using the current google-genai SDK.
    Includes timeout protection and fallback error handling.
    """
    try:
        print(f"📡 Sending request to Gemini (Temp: {temperature})...")

        # Build the configuration object for the model
        config = types.GenerateContentConfig(
            temperature=temperature, system_instruction=system_instruction
        )

        # Use the asynchronous client (.aio) to make the non-blocking API call
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config,
            ),
            timeout=5.0,
        )

        return response.text

    except asyncio.TimeoutError:
        logger.error("🛑 Timeout: AI API took too long to respond.")
        return "FALLBACK_ERROR"

    except Exception as e:
        logger.error(f"❌ LLM API Error: {e}")
        return "FALLBACK_ERROR"
