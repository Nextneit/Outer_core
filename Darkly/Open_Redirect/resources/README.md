# A5 - Open Redirect

OWASP Top 10 (2017) vulnerability, classified under A5: Broken Access Control. Social media links on the page pass through an internal endpoint where the `site` parameter controls the final redirect destination without server validation.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

Social media links have this structure:
```
index.php?page=redirect&site=facebook
```

The `site` parameter determines the destination. The backend does something like:
```php
header("Location: " . $site);
```

### 2. Exploit

Change the `site` parameter value to any unexpected value:
```
index.php?page=redirect&site=test
```
The application processes the value without validating it and returns the **flag**.

For a real phishing attack, the value could be an external URL:
```
index.php?page=redirect&site=https://attacker.example/phishing
```

---

## Impact

- **Phishing:** user trusts the legitimate domain and is redirected to a malicious site.
- **Session Theft:** combinable with XSS or social engineering.
- **Navigation Flow Bypass:** alters the expected behavior of the application.

---

## Mitigation

1. **Strict Whitelist on Server:** accept only internal identifiers and resolve destination in backend:
   ```php
   $allowed = [
       'facebook'  => 'https://facebook.com',
       'twitter'   => 'https://twitter.com',
       'instagram' => 'https://instagram.com',
   ];
   $site = $_GET['site'] ?? '';
   if (!array_key_exists($site, $allowed)) {
       http_response_code(400);
       exit('Invalid redirect target');
   }
   header('Location: ' . $allowed[$site]);
   ```
2. **Don't Redirect to Direct User URLs:** accept only internal keys, never raw URLs.
3. **Validate Scheme and Domain:** allow only `https` and approved domains.
4. **Logging:** record unexpected values in `site` to detect abuse.
