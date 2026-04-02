# vaccine

SQL Injection detection and extraction tool for the Cybersecurity Piscine subject.

## Description

This project runs the scanner locally with Python and targets vulnerable web apps deployed with Docker Compose.

Current capabilities:

- Injection detection methods: Error-based, Union-based, Boolean-based, Time-based
- HTTP methods: GET and POST
- Engine fingerprinting: MySQL and SQLite
- Extraction phase: vulnerable parameters, payload traces, database names, table names, column names and dump data

## Requirements

- Python 3.10+
- pip
- Docker and Docker Compose (for local test targets)

Install Python dependency:

```bash
pip install -r requirements.txt
```

## Usage

Run locally:

```bash
python3 vaccine.py "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"
```

Examples:

```bash
# POST mode
python3 vaccine.py -X POST "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"

# Custom output file
python3 vaccine.py -o output/my_report.txt "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"

# Verbose
python3 vaccine.py -v "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"
```

Options:

- -X, --method: GET or POST (default GET)
- -o, --output: output file path (default output/results.txt)
- -v, --verbose: detailed request and detection trace

## Local Target Environments (DVWA + sqlite_lab)

Start local test targets:

```bash
make start
```

Available URLs:

1. DVWA (MySQL): http://localhost:8080
2. sqlite_lab (Flask + SQLite): http://localhost:5001

DVWA first-time setup:

1. Open http://localhost:8080
2. Login with admin / password
3. Go to Setup / Reset DB and click Create / Reset Database
4. Go to DVWA Security and set level to Low
5. Login again with admin / password

Stop/clean environment:

```bash
make stop
make clean
```

## Makefile Targets

- make or make start: create .venv, install requirements and start DVWA + sqlite_lab
- make stop: stop containers
- make down: remove containers and networks
- make clean: full docker cleanup plus Python cache cleanup
- make logs: follow DVWA + sqlite_lab logs
- make run URL="...": run vaccine locally against URL
- make test: run unit tests
- make check: start targets and run unit tests
- make re: clean and start again

## Project Structure

```text
Vaccine/
├── vaccine.py
├── requirements.txt
├── docker-compose.yml
├── Makefile
├── README.md
├── core/
│   ├── cli.py
│   ├── requester.py
│   ├── detector.py
│   ├── injector.py
│   ├── extractor.py
│   └── reporter.py
├── payloads/
│   ├── detection.py
│   ├── error_based.py
│   └── union_based.py
└── tests/
    ├── test_cli.py
    ├── test_detector.py
    ├── test_extractor.py
    └── test_reporter.py
```

## Test Battery

Run all unit tests:

```bash
make test
```

or:

```bash
python3 -m unittest discover -s tests -v
```

Coverage includes:

- CLI options parsing
- Detection routines
- Engine fingerprinting helpers and extraction helpers
- Report formatting/output handling

## Legal Notice

Use this tool only on systems you own or where you have explicit authorization. The intended targets for this repository are the local DVWA and sqlite_lab environments defined in docker-compose.yml.
