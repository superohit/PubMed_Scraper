# PubMed Pharma Paper Scraper

This tool fetches PubMed papers and filters those with authors from pharmaceutical or biotech companies.

## Features

- Supports full PubMed query syntax
- Filters out academic affiliations using heuristics
- Outputs to CSV or console
- CLI flags: `--file`, `--debug`, `--help`

### Commands to run the code
> python cli.py "cancer treatment" --debug --file cancer_results.csv 
