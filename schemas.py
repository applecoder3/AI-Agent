from pydantic import BaseModel, Field
from typing import Literal


"""
Category list in clause_type needs to match the one in prompts.py
"""


class FlaggedClause(BaseModel):
    clause_type: str = Field(..., description="The category of this clause. Choose one of: Foreign Jurisdiction, Choice of Foreign Law, Limitation of Liability, Unilateral Termination, Unilateral Modification, Forced Arbitration, Data Sharing with Third Parties, Silent Policy Changes. Use a short, clear label of your own only if none of these fit.")

    excerpt: str = Field(..., description="A short verbatim quote of 1 to 3 sentences copied exactly from the document that contains this clause. Never paraphrase or invent text.")

    why_flagged: str = Field(..., description="A plain-language explanation, written for someone with no legal training, of what this clause means in practice for the user and why it is easy to overlook. 1 to 3 sentences.")

    severity: Literal["low", "medium", "high"] = Field(..., 
        description=(
            'How much this clause could affect an average consumer compared to industry norms. '
            'Use "high" ONLY for severe or predatory terms (e.g., selling personal data to brokers, '
            'perpetual AI-training licenses on private user content, or mandatory arbitration with NO opt-out). '
            'Use "medium" for common but restrictive boilerplate (e.g., standard liability caps, '
            'arbitration with an opt-out or small-claims exception, unilateral termination/modification, '
            'or foreign jurisdiction). '
            'Use "low" for minor or unusual terms with limited practical impact.'
            ),
    )

class PolicyAnalysis(BaseModel):
    document_type: str = Field(..., description="The kind of document, such as \"Terms of Service\", \"Privacy Policy\", or \"End User License Agreement\". If it is none of these, say what it actually is.")
    
    company_name: str | None = Field(None, description="The name of the company that published the document. Leave empty if the document does not clearly state it.")

    overall_summary: str = Field(..., description="A plain-language summary of what the document covers, about 150 to 250 words, written at an average adult reading level with little to no legal jargon.")

    risk_level: Literal["low", "medium", "high"] = Field(..., 
        description=(
            'The overall risk to an average consumer, weighing BOTH flagged clauses and mitigating '
            'protections (such as minimal data collection, opt-out rights, or preserved statutory rights). '
            'Use "high" only if the document has multiple severe "high" clauses (such as broad data '
            'monetization/selling alongside major rights waivers) with few consumer protections. '
            'Use "medium" if it contains standard restrictive tech boilerplate (like liability caps '
            'or opt-out arbitration) without aggressive data exploitation. '
            'Use "low" if it is largely consumer-friendly with minimal data collection and no major rights waivers.'
            ),
    )

    key_takeaways: list[str] = Field(..., description="The 3 to 5 most important things a user should know before agreeing, each as one short plain-language sentence.")

    flagged_clauses: list[FlaggedClause] = Field(..., description="Clauses that are commonly overlooked but have real consequences for the user. Only include clauses actually present in the text. Return an empty list if there are none.")

    data_collected: list[str] = Field(..., description="The types of personal data the document says it collects, such as \"email address\", \"or location history\". List only what the document states. Return an empty list if there is nothing collected/said in the document")
