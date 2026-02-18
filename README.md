# AI CI Failure Analyzer

A simple prototype tool that uses a local Large Language Model (via Ollama) to analyze CI/CD logs and generate structured diagnostics, including probable root cause and suggested actions.

This project explores practical applications of AI for developer productivity and reliability engineering.

## Requirements

- Python 3.9+
- Ollama running locally
- An installed model (for example: `llama3.1`)

Install a model:

```bash
ollama pull llama3.1

## Install Python dependencies:

```bash
pip install requests

## Usage

Run the analyzer with default settings:

```bash
python analyzer.py


You can specify a different model or input log file using CLI arguments: 

```bash
python analyzer.py --model llama3.1 --input mylog.txt

The results will be saved in the `output/` directory, with the
filename indicating which model was used (e.g., `output/result_llama3.1.json`)
