import typer 
from pathlib import Path

#command-line for application
app = typer.Typer()

#runs the function when the CLI starts
@app.callback(invoke_without_command=True)
def main():
    """
    welcome to the AI Polciy Analyzer.
    """
    print("\nWelcome to the AI Terms of Sercive & Privacy Polcy Analyzer!")
    print("This tool helps you understand polices before agreeing to them.\n")

@app.command()
def analyze(file: str = typer.Option(..., help="Path to the PDF policy")):

    # check if the PDf file exists
    pdf_path = Path(file)

    if not pdf_path.exists():
        print("Error: The PDF file could not be found.")
        raise typer.Exit(code=1)

# checks if the file is a PDF
    if pdf_path.suffix.lower() != ".pdf":
        print("Error: Please provide a PDF file.")
        raise typer.Exit(code=1)


    try:

        # getting the text from the pdf
        from pdf import extract_text

        console.print("Reading PDF...")
        document_text = extract_text(pdf_path)

        # analyzing text using claude 
        from agent import analyze_document

        console.print("ANalyzing policy with AI...")
        analysis = analyze_document(document_text)

        # creating and saving the report
        from redner import render_report, save_report

        console.print("Creating report...")
        report = render_report(analysis)
        save_report(report, output)

        # display report 
        console.print("\n[bold green]Analysis complete! [/bold green]")
        console.print(report)
        console.print(f"\nReport saved as: {output}")

    except Exception as error:
        console.print(f"\n[red]An error occured: {error}[/red]")
        raise typer.Exit(code=1)

        print(f"PDF found: {pdf_path.name}")
        print("Ready to analyze the policy!")



if __name__ == "__main__":
    app()