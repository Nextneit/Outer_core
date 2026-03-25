# A6 - Sensitive Data Exposure (Admin Credentials)

OWASP Top 10 (2017) vulnerability. Admin credentials are exposed in a publicly accessible file, discovered through the server's `robots.txt`.

---

## Steps to Obtain the Flag

### 1. Reconnaissance

Scanning with nmap reveals two routes in `robots.txt`:
```
/whatever
/.hidden
```

These routes attempt to hide from search engines, but are accessible without authentication.

### 2. Access `/whatever`

```
http://<IP>/whatever/
```

The directory contains a file with plain text credentials:
```
root:437394baff5aa33daa618be47b75cb49
```

### 3. Decrypt the Password

The hash `437394baff5aa33daa618be47b75cb49` is MD5 → decrypts to `qwerty123@`.

> Tool: [md5decrypt.net](https://md5decrypt.net/en/)

### 4. Access the Admin Panel

1. Navigate to `http://<IP>/admin`
2. Enter the credentials:
   - **Username:** `root`
   - **Password:** `qwerty123@`
3. Access granted → the **flag** is displayed.

---

## Attack Flow

```
Nmap → robots.txt → /whatever → credentials → /admin → flag
```

---

## Impact

- **Credential Exposure:** passwords stored in public files.
- **Weak Encryption:** MD5 is trivially reversible with rainbow tables.
- **robots.txt as a Clue:** listing sensitive routes in `robots.txt` makes them obvious to attackers.
- **Complete Compromise:** full access to the admin panel.

---

## Mitigation

1. **Never store credentials in files within the webroot.**
2. **Use strong hashing:** `password_hash($pass, PASSWORD_ARGON2ID)` instead of MD5.
3. **Don't list sensitive resources in `robots.txt`:** protect them with real authentication, not by hiding them.
4. **Use environment variables** for secrets instead of hardcoding them.
5. **Regular Audits:** search for exposed `.txt`, `.bak`, `.old` files in the webroot.
   ```bash
   find /var/www/html -name "*.txt" -o -name "*.bak" -o -name "*.old"
   ```
