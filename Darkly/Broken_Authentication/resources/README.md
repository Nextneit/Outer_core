# A2 - Broken Authentication (Reset Password)

OWASP Top 10 (2017) vulnerability. In the password reset screen, the target email travels in a hidden form field that the server accepts without validation, allowing password reset redirection to any account.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

In the recovery form, the target email is in a `hidden` field:
```html
<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">
```
Although not visually editable, it can be modified from the browser's DevTools or by intercepting the request.

### 2. Exploit

1. Open the developer tools (F12) and inspect the form.
2. Locate the `mail` field.
3. Change its value to:
   ```
   root@borntosec.co
   ```
4. Submit the form → the application processes the reset for that email and returns the **flag**.

### 3. Why It Works

- The restriction was only on the client (HTML/UI).
- The backend does not verify the identity or authorization of the received email.
- It accepts the manipulated parameter without checking its origin.

---

## Impact

- **Account Takeover:** password reset on privileged accounts without authorization.
- **Privilege Escalation:** if an admin user is compromised.
- **Loss of Confidentiality:** access to accounts with sensitive data.

---

## Mitigation

1. **Don't trust client fields for sensitive identity:** the target email should be determined on the server (e.g., from the session), never from manipulable parameters.
2. **Robust Tokens:** random, single-use, with short expiration and tied to a specific account.
3. **Don't use `hidden` fields for sensitive data:** they are completely modifiable by the user.
4. **Rate limiting and logging** of anomalous reset attempts.
5. **Generic Messages:** don't reveal whether an email exists in the system or not.
