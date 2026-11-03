AI Agent: Terms of Service & Privacy Policy Analyzer

An AI agent that reads a company's Terms of Service or privacy policy and returns a short, plain-language report: what the document says overall, plus a list of flagged clauses (data privacy concerns, forced arbitration, liability waivers, unilateral changes, etc.) that people commonly overlook.

This tool helps people understand agreements. It does not replace legal advice.

# Goal for the next 1.5 weeks

## Must have

1.  A working agent: Give policiy (PDF or pasted text) and it returns a report containing a summary and flagged clauses

2.  One user interface: Terminal CLI

---

# How the project connetcs

**Input -> pdf.py -> agent.py -> render.py -> cli.py/user_interface.py**

Each file does one job and hands the results to the next, Allowing us to build in parallel without wiating on one another

# File map

1. schemas.py
   - Objective: Defines the shape of the agent's results, so every other file agrees on what a report is
   - Requirements: Contains result structure (Doc type, summary, list of flagged clauses, verbatim excerpt, plain language explanation, and a severity of low/medium/high). The whole team reviews it.
   - Depends on: Nothing, This is first priority

2. prompts.py
   - Objective: Agent's instructions, list of clause categories it should look for, including data privacy concerns

   - Requirements: Prompt text exist, names every category, tells the agent to quiate the source and never invent clauses, ask for plain langauge, tested on two/three policies and refined

   - Depends on: schemas.py

3. pdf.py
   - Objective: Turns whatever the user supplies into one clean string

   - Requirements: Returns text for a normal PDF, raises a clear error for an empty pdf or non string pdf

   - Depends on: Nothing

4. agent.py
   - Objective: sends the document text plus the system prompt to Anthropic api and returns results that match valid schemas

   - Requirements: Given text and returns valid object with summary and flagged clauses. Handles api errors without crashing

   - Depends on: schemas.py and prompts.py

5. render.py
   - Objective: Converts a result object into a readable markdown report and saves it to a file

   - Requirements: Produces clean report for a result with flagged clauses. Works without the need for an api key and can be tested with custom data

   - Depends on: schemas.py

6. cli.py
   - Objective: Terminal interface and the projgram's entry point

   - Requirements: A command like python cli.py analyze --file policy.pdf prints the report in the terminal and saves the report file

   - Depends on: pdf.py, agent.py, and render.py

7. user_interface.py
   - Objective: Optional Streamlit web interface. File upload, paste box, result display, download button

   - Requirements: Upload or paste, click analyze, see the summary and flagged clauses, download the report

   - Depends on: pdf.py, agent.py, render.py

**The interface files only call other files. No logic should be implemented in them**

# Contracts between files (so we can work in parallel)

- pdf.py exposes one function: path or text in, one text string out.

- agent.py exposes one function: text string in, result object (from schemas.py) out.

- render.py exposes two functions: result object in, Markdown string out; and a way to save that string to a file.

# Work flow

1. Agent and integration: agent.py
2. Data contract and report: schemas.py, render.py
3. Input and prompt quality: pdf.py, prompts.py, samples folder
4. intefaces: cli.py and then user_interface.py last

# Work flow cont.

- Work on your own branch and open a pull request. Another teammate reviews before merging.
- Don't edit a file someone else owns without telling them.
- Keep functions small and documented, so a teammate can pick up your file without a call.

# Setup

1. create and activate a virtual environment, then run `pip install -r requirements.txt`

2. Never commit .env file

# Help resources

### Look for more if help/documentation needed

- Claude structured outputs (how the agent returns data in a guaranteed shape): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Claude API intro: https://platform.claude.com/docs/en/intro
- pypdf (PDF text extraction): https://pypdf.readthedocs.io/en/stable/
- Typer (building the CLI): https://typer.tiangolo.com/tutorial/
- Rich (terminal formatting): https://rich.readthedocs.io/en/stable/introduction.html
- Streamlit (web UI): https://docs.streamlit.io/get-started

# Known limitaitons

- Scanned or image-only PDFs won't work
  Very long documents may be truncated
  Output is AI-generated and should be treated as a guide, not legal analysis. Must be verified

# Status

- Development phase
