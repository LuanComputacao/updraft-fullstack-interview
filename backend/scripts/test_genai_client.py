import os
import sys


def main() -> int:
    # Map LLM_GOOGLE_API_KEY to GEMINI_API_KEY if not already set
    if not os.getenv("GEMINI_API_KEY") and os.getenv("LLM_GOOGLE_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["LLM_GOOGLE_API_KEY"]

    try:
        from google import genai  # type: ignore
    except Exception as e:
        print(f"Import error: {e}", file=sys.stderr)
        return 2

    client = genai.Client()
    model = os.getenv("TEST_GENAI_MODEL", "gemini-2.5-flash")

    try:
        response = client.models.generate_content(
            model=model, contents="Explain how AI works in a few words"
        )
        print(response.text)
        return 0
    except Exception as e:
        print(f"Request error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
