from datetime import datetime
from pathlib import Path
from schemas import PolicyAnalysis


#Level of severity badges for flagged clauses
SEVERITY_BADGES = {
    "high": " High",
    "medium": " Medium",
    "low": " Low",
}

#Overall risk level badges for the report header
RISK_BADGES = {
    "high": " HIGH RISK",
    "medium": " MEDIUM RISK",
    "low": " LOW RISK",
}

#Function to format the PolicyAnalysis object into a Markdown report
def format_markdown_report(analysis: PolicyAnalysis) -> str:
    """Takes a validated PolicyAnalysis object and renders a clean Markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    company = analysis.company_name or "Unknown Company"
    risk_display = RISK_BADGES.get(analysis.risk_level, analysis.risk_level.upper())

    lines = [
        f"# {analysis.document_type}: {company}",
        "",
        f"**Overall Risk Level:** {risk_display}  ",
        f"**Generated:** {timestamp}",
        "",
        "---",
        "",
        "## Executive Summary",
        analysis.overall_summary.strip(),
        "",
        "## Key Takeaways",
    ]

    #Key Takeaways Section
    if analysis.key_takeaways:
        for takeaway in analysis.key_takeaways:
            lines.append(f"- {takeaway}")
    else:
        lines.append("- No specific key takeaways provided.")
    lines.append("")

    #Flagged Clauses Section
    lines.append(f"## Flagged Clauses ({len(analysis.flagged_clauses)})")
    lines.append("")

    if analysis.flagged_clauses:
        severity_order = {"high": 0, "medium": 1, "low": 2}
        sorted_clauses = sorted(
            analysis.flagged_clauses,
            key=lambda c: severity_order.get(c.severity, 3)
        )

        for i, clause in enumerate(sorted_clauses, 1):
            badge = SEVERITY_BADGES.get(clause.severity, clause.severity.upper())
            lines.extend([
                f"### {i}. {clause.clause_type} ({badge})",
                "",
                "**What this means for you:**",
                clause.why_flagged.strip(),
                "",
                "**Verbatim Excerpt:**",
                f"> \"{clause.excerpt.strip()}\"",
                "",
            ])
    else:
        lines.extend([
            "No concerning or unusual clauses were flagged in this document.",
            "",
        ])

    #Personal Data Collected Section
    lines.append("## Personal Data Collected")
    if analysis.data_collected:
        for item in analysis.data_collected:
            lines.append(f"- {item}")
    else:
        lines.append("- No personal data collection explicitly mentioned.")
    lines.append("")

    return "\n".join(lines)

#Saves the formatted Markdown report to a specified file path
def save_report(analysis: PolicyAnalysis, output_path: str | Path) -> Path:
    """Formats the PolicyAnalysis object and writes it to a .md file."""
    markdown_text = format_markdown_report(analysis)
    file_path = Path(output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(markdown_text, encoding="utf-8")
    return file_path


#Tester
if __name__ == "__main__":
    from schemas import PolicyAnalysis

    mock_clean_analysis = PolicyAnalysis(
        document_type="Privacy Policy",
        company_name="OpenNotebook App",
        overall_summary=(
            "OpenNotebook's privacy policy outlines straightforward data practices for a local-first note-taking application. "
            "The document explicitly states that all user notes are encrypted locally on the device, telemetry data is "
            "completely anonymized, and no personal information is ever sold or shared with third-party advertisers."
        ),
        risk_level="low",
        key_takeaways=[
            "All personal notes are encrypted locally on your device.",
            "Analytics tracking is minimal, anonymized, and opt-out by default.",
            "No personal data or document content is sold or shared with third parties."
        ],
        flagged_clauses=[],  # Tests how render.py handles an empty list of clauses
        data_collected=[
            "Anonymized crash reports",
            "App version and operating system type"
        ]
    )

    output_file_clean = save_report(mock_clean_analysis, "reports/test_clean_report.md")
    print(f"Second test render successful! Clean report saved to: {output_file_clean.resolve()}")