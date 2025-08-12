# Prompt templates and helpers for Summary feature
from __future__ import annotations

from typing import Optional

# System instruction used by legacy google-generativeai client
SYSTEM_INSTRUCTION_HTML = (
    "You are an assistant that produces concise, well-structured HTML. "
    "Return valid HTML fragments only, no code fences."
)

# Default instruction appended to the user content when building prompts
DEFAULT_SUMMARY_INSTRUCTION = "Summarize the following HTML into concise, well-structured HTML paragraphs. Try to reduce the content to 40% of its original length, trying to keep the most important information."


def build_summary_prompt(content_html: str, instruction: Optional[str] = None) -> str:
    """Compose the LLM prompt for summarization.

    Keeping this in a dedicated module makes it easy to tweak tone, length,
    style constraints, and guardrails without touching provider code.
    """
    instr = instruction or DEFAULT_SUMMARY_INSTRUCTION
    return f"{instr}\n\n{content_html}"
