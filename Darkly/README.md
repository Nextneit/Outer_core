# Darkly — Flags & Write-ups

Documentación de las vulnerabilidades encontradas y explotadas en el reto **Darkly**, basado en el OWASP Top 10 (2017).

---

## Índice

| # | Vulnerabilidad | Categoría OWASP | Write-up |
|---|---|---|---|
| 1 | SQL Injection (I) | A1 - Injection | [Ver](SQL_Injection/resources/README.md) |
| 2 | SQL Injection (II) | A1 - Injection | [Ver](SQL_injection_II/resources/README.md) |
| 3 | Broken Authentication (Reset Password) | A2 - Broken Authentication | [Ver](Broken_Authentication/resources/README.md) |
| 4 | Broken Authentication (Cookie Manipulation) | A2 - Broken Authentication | [Ver](Cookie_Authentication/resources/README.md) |
| 5 | Broken Authentication (Brute Force) | A2 - Broken Authentication | [Ver](Brute_Force_Authentication/resources/README.md) |
| 6 | Insecure File Upload | A4 - Insecure Direct Object References | [Ver](Insecure_File_Upload/resources/README.md) |
| 7 | Broken Access Control (Survey) | A5 - Broken Access Control | [Ver](Broken_Access_Control/resources/README.md) |
| 8 | Open Redirect | A5 - Broken Access Control | [Ver](Open_Redirect/resources/README.md) |
| 9 | HTTP Header Validation | A5 - Broken Access Control | [Ver](HTTP_Header_Validation/resources/README.md) |
| 10 | Path Traversal | A5 - Broken Access Control | [Ver](Path_Trasversal/resources/README.md) |
| 11 | Security Misconfiguration (.hidden) | A6 - Security Misconfiguration | [Ver](Security_Misgonfiguration/resources/README.md) |
| 12 | Sensitive Data Exposure (Admin Credentials) | A6 - Sensitive Data Exposure | [Ver](Admin_Credentials/resources/README.md) |
| 13 | Cross-Site Scripting (XSS) | A7 - XSS | [Ver](Cross-site_scripting/resources/README.md) |
| 14 | Cross-Site Scripting via Data URI | A7 - XSS | [Ver](Cross-site_Scripting_via_Data_URI/resources/README.md) |

---

## Estructura del repositorio

```
Flags/
├── README.md                          ← este archivo
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
│       ├── scraper.py          ← scraper playwright para enumerar .hidden
│       └── requirements.txt
├── SQL_Injection/
│   ├── flag
│   └── resources/README.md
└── SQL_injection_II/
    ├── flag
    └── resources/README.md
```

---

## Referencias

- [OWASP Top 10 (2017)](https://owasp.org/www-project-top-ten/2017/)
- [Documentación completa del proyecto](https://dpavon-g.github.io/Darkly/)
