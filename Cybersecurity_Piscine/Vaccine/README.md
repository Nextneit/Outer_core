# vaccine

SQL Injection detection and extraction tool for the Cybersecurity Piscine subject.

## Description

This project runs the scanner locally with Python and targets a vulnerable web app deployed with Docker Compose.

Current capabilities:

- Injection detection methods: Error-based, Union-based, Boolean-based, Time-based
- HTTP methods: GET and POST
- Engine fingerprinting: MySQL and SQLite
- Extraction phase: vulnerable parameters, payload traces, database names, table names, column names and dump data

## Requirements

- Python 3.10+
- pip
- Docker and Docker Compose (only for DVWA target)

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

## Local Target Environment (DVWA)

Start DVWA:

```bash
make start
```

Then complete first-time setup in browser:

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

- make or make start: start DVWA
- make stop: stop containers
- make down: remove containers and networks
- make clean: full docker cleanup plus Python cache cleanup
- make logs: follow DVWA logs
- make run URL="...": run vaccine locally against URL
- make test: run unit tests
- make check: start DVWA and run unit tests
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

Use this tool only on systems you own or where you have explicit authorization. The intended target for this repository is the local DVWA environment defined in docker-compose.yml.
