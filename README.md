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
```

## Usage

Run the analyzer with default settings (uses `llama3.1` and `example_logs/failure1.txt`):

```bash
python analyzer.py
```

### Advanced Options

You can specify a different model, input log file, or temperature:

```bash
python analyzer.py --model llama3.1 --input mylog.txt --temperature 0.5
```

### Multiple Runs

You can execute the same analysis multiple times to evaluate output consistency:

```bash
python analyzer.py --runs 3
```
Each run will produce a separate output file.

### Comparing Models

The `--compare` flag allows you to run multiple models against the same log file for side-by-side evaluation:

```bash
python analyzer.py --compare llama3.1 codellama qwen2.5 --input failure_log.txt
```

When using comparison mode:
1. Individual results for each model are saved in the `output/` directory.
2. A global `comparison_summary_tempX_X.json` is generated, containing all results for easy comparison.

Output files are written to the `output/` directory and include:

- input log name
- model name
- temperature
- run number (if using `--runs`)

Example:

output/result_failure1_llama3.1_temp0_0_run1.json
