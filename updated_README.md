# Terms of Service & Privacy Policy Analyzer

A command-line AI agent that reads a Terms of Service or privacy policy (PDF) and produces a plain-language Markdown report: an overall summary, a risk level, key takeaways, flagged clauses with verbatim quotes, and the personal data the document says it collects.

This tool helps people understand agreements. It is not legal advice, and its output should be verified.

## What You Need

- Python 3.10 or newer
- An Anthropic API key ([how to get one](https://platform.claude.com/docs/en/get-api-key); usage is billed by Anthropic)
- An internet connection
- A policy as a **text-based PDF** (not a scan)

## Setup

1. Clone the repository and open a terminal in the project folder.

2. Create and activate a virtual environment.

   Windows (PowerShell):

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS / Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project folder containing your key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
   Never commit `.env` add `.env` to `.gitignore`.

## Run

```bash
python cli.py analyze --file sample_TOS.pdf --output report.md
```

| Option     | Short | Description                       | Default     |
| ---------- | ----- | --------------------------------- | ----------- |
| `--file`   | `-f`  | Path to the policy PDF (required) | none        |
| `--output` | `-o`  | Where to save the Markdown report | `report.md` |

The report prints in the terminal and is saved to the `--output` path. `sample_report.md` shows an example of the output.

## How It Works

```
cli.py -> pdf.py -> prompts.py + agent.py -> schemas.py -> render.py
```

| File                | Role                                                                                                                   |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `cli.py`            | Terminal entry point (Typer + Rich); validates the input file                                                          |
| `pdf.py`            | Extracts text from every PDF page with pypdf                                                                           |
| `prompts.py`        | System and user prompts, including the 8 clause categories and the JSON schema                                         |
| `agent.py`          | Sends the text to Claude (`claude-opus-5-5`), validates the JSON reply, and retries up to 3 times on validation errors |
| `schemas.py`        | Pydantic models (`PolicyAnalysis`, `FlaggedClause`) defining the report structure                                      |
| `render.py`         | Turns the validated result into a Markdown report and saves it                                                         |
| `user_interface.py` | Streamlit web UI, **not functional yet**                                                                               |

**Clause categories:** Foreign Jurisdiction, Choice of Foreign Law, Limitation of Liability, Unilateral Termination, Unilateral Modification, Forced Arbitration, Data Sharing with Third Parties, Silent Policy Changes. If you change this list, update it in both `prompts.py` and the `clause_type` description in `schemas.py`.

## Known Limitations

- **Scanned or image-only PDFs fail.** There is no OCR, so no text is found.
- **Local PDFs only.** URLs, `.docx`, and `.txt` files are not supported.
- **Long documents are not chunked.** If the response hits the 8,192-token limit, the run stops with an error.
- **Excerpts are not verified in code.** The model is told to quote verbatim, but nothing checks that each quote exists in the document.
- **Results can vary between runs**, including clause counts and medium vs. high ratings.
- **Privacy:** the full document text is sent to Anthropic's API. Avoid confidential documents.
- **Prompt injection:** document text goes directly into the prompt, so a malicious document could influence the output.
- **No jurisdiction-specific analysis** (GDPR, CCPA, etc.), no linked-policy following, and no version comparison.

## Troubleshooting

| Error                                  | Likely cause                                          |
| -------------------------------------- | ----------------------------------------------------- |
| `No text found in the PDF file`        | The PDF is scanned or image-only                      |
| Authentication error                   | `ANTHROPIC_API_KEY` is missing or wrong in `.env`     |
| `response was truncated`               | The document is too long for the current `max_tokens` |
| `File is not a PDF` / `file not found` | Check the `--file` path and extension                 |

## Roadmap

Finish the Streamlit UI, verify excerpts programmatically, support URLs and other file types, add OCR, offer a local-LLM option, and add jurisdiction-aware analysis and policy version comparison.

## References

**Anthropic API**

- [Get your API key](https://platform.claude.com/docs/en/get-api-key): create a key in the Claude Console (Settings, then API keys)
- [Quickstart](https://platform.claude.com/docs/en/get-started): make your first API request
- [Claude API intro](https://platform.claude.com/docs/en/intro)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Client SDKs overview](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)

**Tools and libraries**

- [pypdf](https://pypdf.readthedocs.io/en/stable/): PDF text extraction
- [Pydantic](https://docs.pydantic.dev/latest/): schema validation
- [Typer](https://typer.tiangolo.com/tutorial/): command-line interface
- [Rich](https://rich.readthedocs.io/en/stable/introduction.html): terminal formatting
- [python-dotenv](https://pypi.org/project/python-dotenv/): loading `.env` files
- [Streamlit](https://docs.streamlit.io/get-started): planned web UI
