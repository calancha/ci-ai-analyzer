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

```bash
python analyzer.py
