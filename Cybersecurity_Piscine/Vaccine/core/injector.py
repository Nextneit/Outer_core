import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from payloads.detection import TIME_THRESHOLD

def _vprint(enabled: bool, message: str):
    if enabled:
        print(message)


def inject_payload(
    session: requests.Session,
    url: str,
    method: str,
    payload: str,
    target_param: str | None = None,
    verbose: bool = False,
) -> requests.Response:
    parsed   = urlparse(url)
    params   = parse_qs(parsed.query, keep_blank_values=True)

    def _build_param_map() -> dict:
        if target_param is None:
            return {k: payload for k in params}

        modified = {}
        for k, values in params.items():
            if k == target_param:
                modified[k] = payload
            else:
                modified[k] = values[0] if values else ""
        return modified

    modified_params = _build_param_map()

    if method.upper() == "GET":
        new_query = urlencode(modified_params)
        new_url   = urlunparse(parsed._replace(query=new_query))
        _vprint(verbose, f"[verbose] GET {new_url}")
        return session.get(new_url, timeout=TIME_THRESHOLD + 2)
    else:
        base_url = urlunparse(parsed._replace(query=""))
        _vprint(verbose, f"[verbose] POST {base_url} body={modified_params}")
        return session.post(base_url, data=modified_params, timeout=TIME_THRESHOLD + 2)
