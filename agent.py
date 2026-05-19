import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()


class SREFixSchema(BaseModel):
    error_analysis: str
    corrected_code_file: str


def get_api_key() -> str:
    api_key = (
        os.getenv("GEMINI_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )
    if not api_key:
        raise RuntimeError("Set GEMINI_KEY in your .env file")
    return api_key


def run_autonomous_sre():
    client = genai.Client(api_key=get_api_key())

    if not os.path.exists("crash_log.txt"):
        print("Error: Run 'python app.py' first to generate crash_log.txt")
        return

    with open("crash_log.txt", "r", encoding="utf-8") as f:
        crash_log = f.read()

    with open("app.py", "r", encoding="utf-8") as f:
        app_source = f.read()

    print("Agent: Reading logs and calculating hot-patch...")

    system_instruction = """
    You are an Automated Site Reliability Engineer. Analyze the Python crash log.
    You must output a JSON object matching the requested schema.
    In 'corrected_code_file', rewrite the ENTIRE content of app.py with the variable misspellings fixed perfectly.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            f"Fix this system crash:\n\n{crash_log}\n\n"
            f"Current app.py source:\n\n{app_source}"
        ),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=SREFixSchema,
        ),
    )

    result = response.parsed
    if result is None:
        raise RuntimeError(f"Gemini returned no structured output: {response.text}")

    print(f"\n[AGENT ANALYSIS]: {result.error_analysis}")
    print("[AUTONOMOUS ACTION]: Applying hot-patch directly to app.py...")

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(result.corrected_code_file)

    print("Patch successfully deployed! app.py has been updated automatically.")


if __name__ == "__main__":
    run_autonomous_sre()
