# A7 - Cross-Site Scripting (XSS)

OWASP Top 10 (2017) vulnerability. The feedback form validates input only on the client (JavaScript). The server does not sanitize the input, allowing JavaScript code injection that executes in the browser.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

The feedback form has client-side validation with `validate_form()`. This validation is trivially bypassable without touching the server.

### 2. Exploit

**Option A – Bypass Validation from Console (F12):**
```js
function validate_form(thisform) {
    with (thisform) {
        if (validate_required(txtName,"Name can not be empty.")==false)
        {txtName.focus();return true;}
        if (validate_required(mtxMessage,"Message can not be empty.")==false)
        {mtxtMessage.focus();return true;}
    }
}
```
After redefining the function, submit the form with any payload (e.g., `<script>alert("XSS")</script>`) → the server returns the **flag**.

**Option B – Burp Suite:**
Intercept the POST and send directly:
```
txtName=<script>alert("XSS")</script>&mtxtMessage=test
```

### 3. Why It Works

Client-side validation is easily bypassable. The server applies no `htmlspecialchars`, escaping, or filtering on received data, so the payload is processed and the flag is displayed.

> **Note:** The HTML code uses `mtxtMessage` as the textarea name, but the JS references `mtxMessage` (without the `t`). This bug causes validation to fail internally, which in practice also allows bypassing it without modifying anything.

---

## Impact

- **Cookie/Session Theft:** `document.cookie` exposed to attackers.
- **Phishing:** injection of fake forms to capture credentials.
- **Malicious Redirection:** sending users to phishing sites.
- **Actions on Behalf of User:** authenticated requests without user knowledge.

---

## Mitigation

1. **Sanitize on Server:**
   ```php
   $feedback = htmlspecialchars($_POST['feedback'], ENT_QUOTES, 'UTF-8');
   ```
2. **Use Sanitization Libraries** (e.g., HTML Purifier) for rich content.
3. **Content Security Policy (CSP):**
   ```html
   <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
   ```
4. **Never Trust Client-side Validation** for security; it's only for UX.
5. **Modern Frameworks:** use templating engines that automatically escape output.
