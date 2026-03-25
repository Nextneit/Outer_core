# Darkly — Flags & Write-ups

Documentation of vulnerabilities found and exploited in the **Darkly** challenge, based on OWASP Top 10 (2017).

---

## Index

| # | Vulnerability | OWASP Category | Write-up |
|---|---|---|---|
| 1 | SQL Injection (I) | A1 - Injection | [View](SQL_Injection/resources/README.md) |
| 2 | SQL Injection (II) | A1 - Injection | [View](SQL_injection_II/resources/README.md) |
| 3 | Broken Authentication (Reset Password) | A2 - Broken Authentication | [View](Broken_Authentication/resources/README.md) |
| 4 | Broken Authentication (Cookie Manipulation) | A2 - Broken Authentication | [View](Cookie_Authentication/resources/README.md) |
| 5 | Broken Authentication (Brute Force) | A2 - Broken Authentication | [View](Brute_Force_Authentication/resources/README.md) |
| 6 | Insecure File Upload | A4 - Insecure Direct Object References | [View](Insecure_File_Upload/resources/README.md) |
| 7 | Broken Access Control (Survey) | A5 - Broken Access Control | [View](Broken_Access_Control/resources/README.md) |
| 8 | Open Redirect | A5 - Broken Access Control | [View](Open_Redirect/resources/README.md) |
| 9 | HTTP Header Validation | A5 - Broken Access Control | [View](HTTP_Header_Validation/resources/README.md) |
| 10 | Path Traversal | A5 - Broken Access Control | [View](Path_Trasversal/resources/README.md) |
| 11 | Security Misconfiguration (.hidden) | A6 - Security Misconfiguration | [View](Security_Misgonfiguration/resources/README.md) |
| 12 | Sensitive Data Exposure (Admin Credentials) | A6 - Sensitive Data Exposure | [View](Admin_Credentials/resources/README.md) |
| 13 | Cross-Site Scripting (XSS) | A7 - XSS | [View](Cross-site_scripting/resources/README.md) |
| 14 | Cross-Site Scripting via Data URI | A7 - XSS | [View](Cross-site_Scripting_via_Data_URI/resources/README.md) |

---

## Repository Structure

```
Flags/
├── README.md                          ← this file
├── Admin_Credentials/
│   ├── flag
│   └── resources/README.md
├── Broken_Access_Control/
│   ├── flag
│   └── resources/README.md
├── Broken_Authentication/
│   ├── flag
│   └── resources/README.md
├── Brute_Force_Authentication/
│   ├── flag
│   └── resources/README.md
├── Cookie_Authentication/
│   ├── flag
│   └── resources/README.md
├── Cross-site_scripting/
│   ├── flag
│   └── resources/README.md
├── Cross-site_Scripting_via_Data_URI/
│   ├── flag
│   └── resources/README.md
├── HTTP_Header_Validation/
│   ├── flag
│   └── resources/README.md
├── Insecure_File_Upload/
│   ├── flag
│   └── resources/README.md
├── Open_Redirect/
│   ├── flag
│   └── resources/README.md
├── Path_Trasversal/
│   ├── flag
│   └── resources/README.md
├── Security_Misgonfiguration/
│   ├── flag
│   └── resources/
│       ├── README.md
│       ├── scraper.py          ← Playwright scraper to enumerate .hidden
│       └── requirements.txt
├── SQL_Injection/
│   ├── flag
│   └── resources/README.md
└── SQL_injection_II/
    ├── flag
    └── resources/README.md
```

---

## References

- [OWASP Top 10 (2017)](https://owasp.org/www-project-top-ten/2017/)
- [Complete Project Documentation](https://dpavon-g.github.io/Darkly/)
