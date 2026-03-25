# A5 - Broken Access Control

OWASP Top 10 (2017) vulnerability. In the `survey` section, a form with a `<select>` limits values from 1 to 10 only on the client. The server does not validate that the received value belongs to that range.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

The form sends a POST with the `valeur` parameter restricted to the range 1-10 by HTML, but the server accepts any value without validation.

### 2. Exploit

**Option A – DevTools:**
1. F12 → inspect the `<select name="valeur">` element.
2. Change the value of an existing option to `4218.19`.
3. Select it and submit the form → the **flag** appears.

**Option B – Burp Suite:**
Intercept the POST and change the parameter:
```
valeur=4218.19
```

**Option C – cURL:**
```bash
curl -X POST "http://<IP>/index.php?page=survey" \
     -d "valeur=4218.19&sujet=1"
```

---

## Impact

- **Integrity:** the attacker modifies data they shouldn't be able to alter.
- **Confidentiality:** through privilege escalation, access to restricted information.
- **Weak Authorization:** trusting only client-side validation is trivially bypassable.

---

## Mitigation

1. **Server-side validation with whitelist:**
   ```php
   $allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   if (!in_array($_POST['valeur'], $allowed)) die('Invalid value');
   ```
2. **Never trust client data:** every business logic restriction must be applied in the backend.
3. **Principle of Least Privilege:** validate on each request that the action is allowed for that user.
4. **Logging:** record submissions with values outside the expected range.
