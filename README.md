# Socio-legal Trajectories Dataset and Analyses

This repository contains data collected, and analyses based on that  data, by the project "Socio-legal Trajectories in Germany and the UK: Cultures, Actors and Institutions", a Research Network at the Max Planck Institute for Legal History and Legal Theory (mpilhlt). PIs: Christian Boulanger (mpilhlt), Naomi Creutzfeldt (University of Kent), Jen Hendry (Chinese University of Hong Kong).

For the moment, the repository contains only the code, the data will be published in full together with the book in 2027.

The notebooks in this repo use **PandasAI** with an OpenAI-compatible inference endpoint
to answer natural-language questions about the SLT survey dataset.

PandasAI generates **executable Python code** for each query, so every answer is fully
reproducible without re-running the LLM.

## Data

The original survey data is in `data/results-for-socio-legal-t-2021-12-14-1607.xlsx` (sheet: *Raw data*).
For use in the notebooks it has been converted to CSV with column names sanitized to valid SQL/Python identifiers:

| File | Description |
|---|---|
| `data/slt_raw_data.csv` | Survey responses with sanitized column names |
| `data/slt_column_mapping.csv` | Maps each sanitized column name back to the original survey question |

To regenerate the CSV files from the Excel source:

```bash
uv run python convert_data.py
```

## Setup instructions

1. Copy `.env.example` → `.env` and fill in your API key and endpoint.
2. Run `uv sync` to install dependencies.
3. Start JupyterLab with `uv run jupyter lab`.