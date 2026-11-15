import json
from schemas import PolicyAnalysis


ALLOWED_CLAUSES_TYPES = [
    "Foreign Jurisdiction",
    "Choice of Foreign Law",
    "Limitation of Liability",
    "Unilateral Termination",
    "Unilateral Modification",
    "Forced Arbitration",
    "Data Sharing with Third Parties",
    "Silent Policy Changes"
]

OUTPUT_SCHEMA_JSON = json.dumps(
    PolicyAnalysis.model_json_schema(), 
    indent=3
    )

SYSTEM_PROMPT = (
    "You are an legal analysis agent specializing in consumer advocacy. "
    "Your mission is to analyze legal documents (such as terms of service or privacy policies) and identify potentially unfair or problematic clauses and translate them into clear, transparent language for everyday consumers "
    "When identifying clauses, you must strictly map them to one of the following standard types: " 
    f"Whenever possible: \n{', '.join(ALLOWED_CLAUSES_TYPES)}.\n\n "
    "Output Requirements:\n "
    "You must return your complete analysis strictly as a single json object. Do not include conversation filler, markdown formatting (like ```json), or wrapping text. Your output must validate perfectly against the following json schema: \n\n "
    f"{OUTPUT_SCHEMA_JSON}"
)

USER_PROMPT = (
    "Please analyze the following legal document and extract all key takeaways. "
    "risk profiles, data tracking policies, and flagged clauses. \n\n "
    "--- DOCUMENT START ---\n"
    "{document_text}\n"
    "--- DOCUMENT END ---\n"
)