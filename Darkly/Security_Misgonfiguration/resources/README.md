# A6 - Security Misconfiguration

OWASP Top 10 (2017) vulnerability. The server publicly exposes the `.hidden` directory in the webroot, which contains over 35,000 README files distributed in a labyrinthine directory structure. The flag is buried among them.

---

## Steps to Obtain the Flag

### 1. Discover the Exposed Directory

During reconnaissance (nmap, web enumeration) detect:
```
http://<IP>/.hidden/
```
The server lists the contents instead of denying access.

### 2. Automate the Search

The depth and volume make manual searching unfeasible. Use the `scraper.py` script (Playwright) to recursively traverse all subdirectories, collect README content in memory, and filter those appearing infrequently (possible flags).

```bash
python3 scraper.py
```

The script saves in `.hidden/` only files with unique or rare content (≤5 occurrences), which are flag candidates.

### 3. Why It Works

- The server doesn't restrict access to dotfiles (files/folders starting with `.`).
- Directory listing (`autoindex`) is enabled, allowing navigation of the entire structure.
- "Security by obscurity" (hiding the flag among thousands of files) is not a real control: an attacker with basic scraping tools finds it.

---

## Impact

- **Information Leakage:** exposure of files that should be inaccessible.
- **Facilitated Reconnaissance:** reveals server internal structure, making it easier to find `.git`, `.env`, `.htaccess` and other critical files.
- **Expanded Attack Surface:** any sensitive data placed under the assumption "no one will find it" is exposed.

---

## Mitigation

1. **Deny Access to Dotfiles in Nginx:**
   ```nginx
   location ~ /\.(.*) {
       deny all;
   }
   ```
   **In Apache (.htaccess):**
   ```apache
   RedirectMatch 404 /\..*$
   ```

2. **Disable Directory Listing:**
   - Nginx: `autoindex off;`
   - Apache: `Options -Indexes`

3. **Whitelist Policy:** server should only serve necessary assets (HTML, JS, CSS, images). Any other path returns `403` or `404`.

4. **Remove Non-Essential Content Before Production:** apply principle of minimal attack surface; delete test directories, temporary files, and non-functional structures.
