import typer
import pandas as pd
from pubmed_scraper.core import fetch_pubmed_ids, fetch_pubmed_metadata
from rich import print

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed search query"),
    file: str = typer.Option(None, "-f", "--file", help="CSV file to save results"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug output")
):
    if debug:
        print(f"[bold green]Fetching results for query:[/bold green] {query}")

    try:
        ids = fetch_pubmed_ids(query)
        if debug: print(f"[cyan]Found {len(ids)} articles[/cyan]")
        data = fetch_pubmed_metadata(ids)
        df = pd.DataFrame(data)

        if file:
            df.to_csv(file, index=False)
            print(f"[bold green]Saved {len(df)} results to {file}[/bold green]")
        else:
            print(df.to_markdown(index=False))

    except Exception as e:
        print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    app()
