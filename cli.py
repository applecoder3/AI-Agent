import typer 
from pathlib import Path
from rich.console import Console

from pdf import extract_text_from_pdf
from agent import analyze_document
from render import format_markdown_report, save_report

#command-line for application
app = typer.Typer()
console = Console()

#runs the function when the CLI starts
@app.callback(invoke_without_command=True)
def main():
    """
    welcome to the AI Polciy Analyzer.
    """
    print("\nWelcome to the AI Terms of Sercive & Privacy Polcy Analyzer!")
    print("This tool helps you understand polices before agreeing to them.\n")

@app.command()
def analyze(
    file: str = typer.Option(None, help ="Path to a PDF Policy"),
    text: str = typer.Option(None, help ="Paste Policy text"),
    output: str = typer.Option("report.md", help = "Name of the output report"),
):
    """Analyze a PDF or pasted policy text. """

    # check that user provided one input only 
    if bool(file) == bole(text):
        console.print("[red]Please provide either --file or --text, not both[/red]")
        raise typer.Exit(code=1)
    
    try:
        # get text from the pdf or user input
        if file:
            pdf_path = Path(file)

            if not pdf_path.exists():
                console.print("[red]Error: PDF file not found.[/red]")
                raise typer.Exit(code=1)

            if pdf_path.suffix.lower() != ".pdf":
                console.print("[red]Error: Please provide PDF file.[/red]")
                raise typer.Exit(code =1)

            console.print("[green] Reading PDF...[/green]")
            document_text = extract_text_from_pdf(str(pdf_path))

        else:
            document_text = text.strip()

            if not document_text:
                console.print("[red] Error: Policy text cannot be empty.[/red]")
                raise typer.Exit(code =1)

        console.print("[yellow]Analyzing policy with AI...")
        analysis = analyze_document(document_text)

        report = format-markdown_report(analysis)

        console.print("\n[bold green]Analysis complete![/bold green]")
        console.print(report)

        svaed_file = save_report(analysis, output)
        console.print(f"\n[bold green]Report saved to: {saved_file}[/bold green]")

    except typer.Exit:
        raise

    except Exception as error:
        console.print(f"\n[red]An error occurred: {error}[/red]")
        raise typer.Exit(code = 1)

if __name__ == "__main__":
    app()    