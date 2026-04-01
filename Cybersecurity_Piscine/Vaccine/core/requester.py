import requests

DVWA_USERNAME   = "admin"
DVWA_PASSWORD   = "password"

def _vprint(enabled: bool, message: str):
    if enabled:
        print(message)


def login(session: requests.Session, base_url: str, verbose: bool = False) -> bool:
    try:
        login_url = f"{base_url}/login.php"
        _vprint(verbose, f"[verbose] GET {login_url}")
        r = session.get(login_url, timeout=10)
        r.raise_for_status()

        token = ""
        for line in r.text.splitlines():
            if "user_token" in line and "value" in line:
                start = line.find("value='") + 7
                end   = line.find("'", start)
                if end != -1:
                    token = line[start:end]
                else:
                    start = line.find("value=\"") + 7
                    end   = line.find("\"", start)
                    token = line[start:end]
                break

        if token:
            _vprint(verbose, "[verbose] CSRF token obtenido para login")
        else:
            _vprint(verbose, "[verbose] No se encontró CSRF token en login.php")

        payload = {
            "username":   DVWA_USERNAME,
            "password":   DVWA_PASSWORD,
            "Login":      "Login",
            "user_token": token,
        }
        _vprint(verbose, f"[verbose] POST {login_url} con usuario '{DVWA_USERNAME}'")
        r = session.post(login_url, data=payload, timeout=10)

        # Set security level to low (DVWA)
        security_url = f"{base_url}/security.php"
        _vprint(verbose, f"[verbose] GET {security_url}")
        session.get(security_url, timeout=10)
        _vprint(verbose, f"[verbose] POST {security_url} para fijar security=low")
        session.post(
            security_url,
            data={"security": "low", "seclev_submit": "Submit", "user_token": token},
            timeout=10,
        )

        success = "logout" in r.text or "Welcome" in r.text.lower() or "admin" in r.text.lower()
        _vprint(verbose, f"[verbose] Resultado login: {'OK' if success else 'FALLIDO'}")
        return success

    except requests.RequestException as e:
        print(f"[!] Error de conexión durante el login: {e}")
        return False
