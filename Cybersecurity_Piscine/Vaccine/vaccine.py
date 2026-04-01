import sys
import requests
from core.cli import parse_args
from core.requester import login
from core.detector import detect_error_based, detect_union_based, detect_boolean_based, detect_time_based
from core.extractor import run_extraction
from core.reporter import format_results, save_results


def vprint(enabled: bool, message: str):
    if enabled:
        print(message)

def main():
    args = parse_args()

    print(f"\n[*] Iniciando vaccine.py")
    print(f"[*] URL     : {args.url}")
    print(f"[*] Método  : {args.method}")
    vprint(args.verbose, "[*] Modo verbose activado")

    session = requests.Session()
    session.headers.update({"User-Agent": "vaccine/1.0"})
    vprint(args.verbose, f"[verbose] User-Agent: {session.headers.get('User-Agent')}")

    print("[*] Autenticando en DVWA...")
    
    # Extract base URL from the target URL (e.g., http://localhost:8080)
    from urllib.parse import urlparse
    parsed_url = urlparse(args.url)
    base_host = parsed_url.hostname or ""
    base_port = f":{parsed_url.port}" if parsed_url.port else ""

    base_url = f"{parsed_url.scheme}://{base_host}{base_port}"
    vprint(args.verbose, f"[verbose] Base URL detectada: {base_url}")
    
    if not login(session, base_url, verbose=args.verbose):
        print("[!] Login fallido. Verifica las credenciales en el script.")
        sys.exit(1)
    print("[*] Sesión iniciada correctamente.\n")

    findings = []

    print("[*] Probando inyección basada en errores...")
    if detect_error_based(session, args.url, args.method, verbose=args.verbose):
        findings.append("Error-based")

    print("[*] Probando inyección UNION-based...")
    if detect_union_based(session, args.url, args.method, verbose=args.verbose):
        findings.append("Union-based")

    print("[*] Probando inyección booleana...")
    if detect_boolean_based(session, args.url, args.method, verbose=args.verbose):
        findings.append("Boolean-based")

    print("[*] Probando inyección temporal (puede tardar unos segundos)...")
    if detect_time_based(session, args.url, args.method, verbose=args.verbose):
        findings.append("Time-based")

    extraction = None
    if findings:
        print("[*] Iniciando fase de extracción...")
        extraction = run_extraction(
            session,
            args.url,
            args.method,
            verbose=args.verbose,
        )

    output = format_results(args.url, findings, extraction=extraction)
    print(f"\n{output}")
    save_results(output, args.output)

if __name__ == "__main__":
    main()
