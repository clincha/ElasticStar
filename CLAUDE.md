# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ElasticStar is a personal financial data aggregator that pulls transaction data from Starling Bank and Trading212, then pushes it to Elasticsearch (for Kibana dashboards) and Google Sheets (for budgeting).

## Running the Scripts

```bash
pip install -r requirements.txt

# ETL to Elasticsearch
python starling_to_elastic.py

# ETL to Google Sheets
python starling_to_sheets.py
python trading212_to_sheets.py
```

All scripts require environment variables for credentials (see below).

## Running Tests

```bash
# Unit tests (no credentials needed)
pytest tests/test_starling.py -v

# Integration tests (requires Starling access tokens in env)
pytest tests/test_balance_integration.py -v
```

## Environment Variables

- **Starling Bank**: `PERSONAL_ACCESS_TOKEN`, `BUSINESS_ACCESS_TOKEN`, `JOINT_ACCESS_TOKEN`
- **Elasticsearch**: `ELASTIC_HOST`, `ELASTIC_USERNAME`, `ELASTIC_PASSWORD`
- **Trading212**: `TRADING212_INVEST_API_KEY`, `TRADING212_ISA_API_KEY`
- **Google Sheets**: `GOOGLE_SHEETS_SERVICE_ACCOUNT` (base64-encoded service account JSON)

## Architecture

```
Starling Bank API ──→ starling.py (API client class)
                         ├─→ starling_to_elastic.py → Elasticsearch indices (CLINCHA_STARLING_*)
                         └─→ starling_to_sheets.py  → Google Sheets worksheets

Trading212 API ─────→ trading212_to_sheets.py → Google Sheets worksheets
```

- **starling.py** — Reusable `Starling` class wrapping the bank API. Handles accounts, balances, transaction feeds, saving spaces, and generates Elasticsearch bulk action dicts via a generator. Account balances use the `/accounts/{uid}/balance` endpoint for authoritative values (effectiveBalance, totalEffectiveBalance).
- **starling_to_elastic.py** — Iterates over account types (PERSONAL, BUSINESS, JOINT) defined in `variables.py`, creates Elasticsearch indices, and uses `streaming_bulk` to index transactions.
- **starling_to_sheets.py** — Populates Google Sheets with transaction data, savings goals, and account balances. Writes `effectiveBalance` to P1:Q1 and `totalEffectiveBalance` to P2:Q2 in each `starling-{account}` sheet.
- **trading212_to_sheets.py** — Fetches portfolio positions and embeds `GOOGLEFINANCE` formulas for live P/L and currency conversion.
- **variables.py** — Central config: account type list and Elasticsearch index prefix (`CLINCHA_STARLING_`).
- **tests/** — Unit tests (`test_starling.py`) and integration tests (`test_balance_integration.py`).

## Reading the Finance Spreadsheet (gogcli)

The output Google Sheet is available at:
https://docs.google.com/spreadsheets/d/1yxX_FPescxv4QHqjdhusjZuXSd2nqPDY7b1J7Ua4kUM/edit

Spreadsheet ID: `1yxX_FPescxv4QHqjdhusjZuXSd2nqPDY7b1J7Ua4kUM`

Use the `gog` CLI (gogcli) to read/write this spreadsheet. The account to use is `angus.clinch@gmail.com`.

```bash
# Ensure session env is loaded first
source ~/.claude/session-env/shared/env.sh

# Get spreadsheet metadata (list tabs/sheets)
gog sheets metadata 1yxX_FPescxv4QHqjdhusjZuXSd2nqPDY7b1J7Ua4kUM -a angus.clinch@gmail.com

# Read a range (e.g. first tab, columns A-Z)
gog sheets get 1yxX_FPescxv4QHqjdhusjZuXSd2nqPDY7b1J7Ua4kUM "Sheet1!A:Z" -a angus.clinch@gmail.com

# Read as JSON (for scripting)
gog sheets get 1yxX_FPescxv4QHqjdhusjZuXSd2nqPDY7b1J7Ua4kUM "Sheet1!A:Z" -a angus.clinch@gmail.com -j
```

## CI/CD

Three GitHub Actions workflows in `.github/workflows/`:
- `populate-elastic.yml` — Runs every 15 minutes on a custom self-hosted runner (`github-runners-elasticstar`)
- `populate-spreadsheet.yml` — Runs every 15 minutes on `ubuntu-latest`
- `test.yml` — Runs unit tests on push and PR

## Spreadsheet Layout

The Summary sheet references balance cells written by the pipeline:
- B8 (Starling): `=IFERROR('starling-personal'!Q1, 0)` — effectiveBalance from API
- B9 (Starling spaces): `=SUM('starling-spaces-personal'!E:E)` — summed from savings goals
- B10 (Joint): `=IFERROR('starling-joint'!Q1, 0)`
- B12 (Business): `=IFERROR('starling-business'!Q1, 0)`

Balance cells (P1:Q2) in each `starling-{account}` sheet are written by `starling_to_sheets.py` using the Starling balance API. Do not derive balances from transaction sums — the balance endpoint is authoritative and includes pending transactions.

## Known Gotchas

- **requirements.txt** is UTF-16 encoded. When editing programmatically, decode/encode as UTF-16.
- **Spreadsheet formulas with `gog sheets update`**: The `--values-json` flag has trouble with `!` in formulas (interpreted as JSON escape). Write the JSON to a temp file and pass it via `$(cat /tmp/formula.json)`.
- **Balance vs transaction sums**: Starling's settled transaction feed excludes pending transactions. Never compute balances by summing transactions — always use `get_balance()`.
- **`worksheet.clear()` in `update_transaction_sheet`**: Clears the entire sheet including balance cells. `update_balance_cells` must be called after `update_transaction_sheet` to re-write P1:Q2.
