"""This will be the home code for the agent setup"""

import anthropic
import os

from pydantic import ValidationError

from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, USER_PROMPT
from schemas import PolicyAnalysis

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def analyze_document(document_text: str, max_retries: int = 3) -> PolicyAnalysis:
    """Analyze a document and return the analysis as a PolicyAnalysis object."""

    messages = [
        {
            "role": "user",
            "content": USER_PROMPT.format(document_text=document_text),
        }
    ]


    for attempt in range(max_retries):
        try:

            response = client.messages.create(
                model="claude-opus-5-5",
                max_tokens=16384,
                messages=messages,
                system=SYSTEM_PROMPT,
            )

            if response.stop_reason == "max_tokens":
                raise ValueError(
                    "Claude's response was truncated because it reached the maximum token limit."
                    "Try increasing max_tokens."
                )

            raw_analysis = ""
            for block in response.content:
                if block.type == "text":
                    raw_analysis += block.text
                    
            if not raw_analysis:
                raise ValueError("No text block found in Claude's response.")

            cleaned_analysis = raw_analysis.strip()

            if cleaned_analysis.startswith("```json"):
                cleaned_analysis = cleaned_analysis[7:]

            elif cleaned_analysis.startswith("```"):
                cleaned_analysis = cleaned_analysis[3:]

            if cleaned_analysis.endswith("```"):
                cleaned_analysis = cleaned_analysis[:-3]

            cleaned_analysis = cleaned_analysis.strip()

            validated_analysis = PolicyAnalysis.model_validate_json(cleaned_analysis)

            return validated_analysis

        except ValidationError as e:

            if attempt == max_retries - 1:
                raise Exception(f"Failed to validate analysis after {max_retries} attempts: {e}")

            messages.append({
                "role": "assistant",
                "content": raw_analysis,
            })

            messages.append({
                "role": "user",
                "content": f"Validation error: {e}. Please provide a valid JSON response.",
            })



