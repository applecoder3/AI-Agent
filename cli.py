from pathlib import Path
from rich.console import Console

from agent import analyze_document
from pdf import extract_text_from_pdf
from render import format_markdown_report, save_report

import typer
import traceback

# Initialize the rich console
console = Console()
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main():
    console.print("\n[bold cyan]Welcome to the AI Terms of Service & Privacy Policy Analyzer![/bold cyan]")
    console.print("This tool helps you understand policies before agreeing to them.\n")


@app.command()
def analyze(
    file: str = typer.Option(..., "--file", "-f", help="Path to the PDF policy"),
    output: str = typer.Option("report.md", "--output", "-o", help="Path to save the Markdown report")
):
    """ Analyze a PDF policy and generate a Markdown report."""

    pdf_path = Path(file)

    # Validate the PDF file exists
    if not pdf_path.exists():
        console.print(f"[red]Error: PDF file not found: {pdf_path}[/red]")
        raise typer.Exit(code=1)

    # Checking if the file is a PDF
    if pdf_path.suffix.lower() != ".pdf":
        console.print(f"[red]Error: File is not a PDF: {pdf_path}[/red]")
        raise typer.Exit(code=1)
    
    # Extract text from the PDF file
    try:
        console.print(f"[green]Analyzing PDF file: {pdf_path.name}[/green]...")
        document_text = extract_text_from_pdf(str(pdf_path))

        # Using claude to analyze the extracted text
        console.print("[green]Analyzing document text with Claude...[/green]")
        analysis_report = analyze_document(document_text)

        # Rendering the analysis report to the console and saving the Markdown file
        console.print("Creating report...")
        report = format_markdown_report(analysis_report)
        saved_path = save_report(analysis_report, output)
        
        # Display report
        console.print("\n[bold green]Analysis complete![/bold green]\n")
        console.print(report)
        console.print(f"[green]Report saved to:[/green] {saved_path.resolve()}")

    except Exception as e:
        traceback.print_exc()
        console.print(f"[red]Error Occurred: {e}[/red]")
        raise typer.Exit(code=1)




if __name__ == "__main__":
    app()