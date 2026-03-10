from db.models import CategoryEnum
from typing import Final
import logging


# The system prompt that instructs the LLM how to categorize user queries.
# Uses Few-Shot prompting for high precision and strict formatting.
logger = logging.getLogger(__name__)
DEFAULT_CATEGORY: Final = CategoryEnum.GENERAL
MAX_RETRIES: Final = 1
CLASSIFIER_PROMPT = """
You are a highly precise classification API for a university campus assistant.
Your ONLY job is to classify the student's input into exactly one of the allowed categories.

ALLOWED CATEGORIES:
- SCHEDULE: Questions about course times, lecturers, exam dates, or room locations.
- GENERAL: Questions about administration, scholarships, library hours, parking, or campus facilities.
- TECHNICAL: Questions about Wi-Fi connection, Moodle access, or broken equipment (projectors, PCs).
- OUT_OF_CONTEXT: Questions completely unrelated to the university, studying, or campus life.

STRICT RULES:
1. Output NOTHING BUT the exact category name. No punctuation, no explanations, no markdown formatting.
2. If the query is ambiguous, default to GENERAL.

EXAMPLES:
User: "באיזה חדר יש לי שיעור מבני נתונים?"
SCHEDULE

User: "איך מגישים בקשה למלגת הצטיינות?"
GENERAL

User: "האינטרנט באולם 101 לא מתחבר לי"
TECHNICAL

User: "מה מזג האוויר מחר בתל אביב?"
OUT_OF_CONTEXT

User: "{question}"
"""


async def classify_question(question: str) -> CategoryEnum:
    """
    Analyzes the user's question using an LLM and maps it to a predefined CategoryEnum.
    Returns CategoryEnum.GENERAL as a fallback in case of errors.
    """
    # Local imports to prevent circular dependency issues
    from ai.llm_client import ask_llm

    # Use safer string replacement instead of .format() to prevent template injection
    # Replace {question} placeholder directly
    prompt = CLASSIFIER_PROMPT.replace("{question}", question)
    # Request a deterministic response (temperature 0.0) from the LLM
    for attempt in range(MAX_RETRIES + 1):
        raw_response = await ask_llm(prompt, temperature=0.0)
        if raw_response == "FALLBACK_ERROR":
            print(f"⚠️ Classifier attempt {attempt + 1} failed. Retrying...")
            continue
        clean_res = raw_response.strip().upper()
        try:
            return CategoryEnum(clean_res.lower())
        except ValueError:
            print(f"⚠️ Failed to parse category: '{clean_res}', falling back to GENERAL")
            return CategoryEnum.GENERAL

    logger.warning("Classifier exhausted all retries. Defaulting to GENERAL.")
    return CategoryEnum.GENERAL
