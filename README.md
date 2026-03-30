# Outer Core

Collection of low-level, security, and systems projects. Each folder is an independent project with its own documentation.

---

## Project Index

| Project | Area | Brief Description |
|---|---|---|
| [Cybersecurity_Piscine/Arachnida](#cybersecurity_piscinearachnida) | Cybersecurity | Web scraper for images + EXIF metadata extractor |
| [Cybersecurity_Piscine/ft_otp](#cybersecurity_piscineft_otp) | Cybersecurity | TOTP (One-Time Password) generator from scratch |
| [Cybersecurity_Piscine/ft_onion](#cybersecurity_piscineft_onion) | Cybersecurity | Tor hidden service with SSH access (Docker) |
| [Cybersecurity_Piscine/Stockholm](#cybersecurity_piscinestockholm) | Cybersecurity | Educational ransomware simulator with Fernet encryption |
| [Cybersecurity_Piscine/Reverse_me_i'm_famous!](#cybersecurity_piscinereverse_me_im_famous) | Cybersecurity | Reverse engineering binaries with GDB (3 levels: 32-bit → 64-bit) |
| [Darkly](#darkly) | Cybersecurity | CTF with web vulnerabilities (OWASP Top 10) |
| [dr-quine](#dr-quine) | Theoretical Recreation | Programs that print their own source code (quines) |
| [ft_ping](#ft_ping) | Networking / C | Reimplementation of `ping` command with raw sockets |
| [libasm](#libasm) | Assembly | Reimplementation of libc functions in x86-64 NASM |
| [woody-woodpacker](#woody-woodpacker) | Security / ELF | ELF64 packer: encrypts `.text` segment and injects unpacker stub |

---

## Cybersecurity_Piscine/Arachnida

**Path:** [`Cybersecurity_Piscine/Arachnida/`](Cybersecurity_Piscine/Arachnida/)
**Documentation:** [README](Cybersecurity_Piscine/Arachnida/README.md)

Two-tool toolkit focused on web analysis and image forensics:

- **Spider** (`ex00`) — recursive scraper that downloads images (`.jpg`, `.png`, `.gif`, `.bmp`) from a URL, respecting domain and configurable depth.
- **Scorpion** (`ex01`) — EXIF metadata and file attribute extractor for local images.

**Technologies:** Python 3, `requests`, `BeautifulSoup4`, `Pillow`

---

## Cybersecurity_Piscine/ft_otp

**Path:** [`Cybersecurity_Piscine/ft_otp/`](Cybersecurity_Piscine/ft_otp/)
**Documentation:** [README](Cybersecurity_Piscine/ft_otp/README.md)

**TOTP** (Time-based One-Time Password) generator implemented from scratch, based on the HOTP algorithm defined in **RFC 4226** and **RFC 6238**.

**Operations:**
- **`-g KEYFILE`** — Reads a hexadecimal key (64+ characters) from a file and saves it encrypted in `ft_otp.key`
- **`-k [KEYFILE]`** — Generates a 6-digit OTP code from the encrypted key

**Features:**
- ✅ Implementation from scratch without external TOTP libraries
- ✅ Uses `hmac-sha1`, `struct`, `time` (only standard library for computation)
- ✅ Persistent encryption with **Fernet** (AES-128-CBC + HMAC-SHA256)
- ✅ Secure key management with Fernet key persistence
- ✅ Complete Makefile with testing and automation targets

**Quick Start:**
```bash
make              # Generates random hex key and encrypts it
make run          # Generates TOTP from saved key
make test         # Complete validation suite
```

**Technologies:** Python 3, `cryptography` (Fernet)

---

## Cybersecurity_Piscine/ft_onion

**Path:** [`Cybersecurity_Piscine/ft_onion/`](Cybersecurity_Piscine/ft_onion/)
**Documentation:** [README](Cybersecurity_Piscine/ft_onion/README.md)

**Tor hidden service deployment** with SSH access, fully containerized with Docker.

- Deploys **3 services**: Nginx (web server), Tor (hidden service), OpenSSH (remote access)
- Exposes a static web page exclusively via `.onion` address
- SSH access available on port `2222` (credentials: `user42` / `password`)
- Multi-service Docker Compose setup with automatic Tor bootstrap

**Quick Start:**
```bash
make start          # Build and start
make check          # Get .onion address
make test-ssh       # Test SSH access
make test-web       # Test web server
make stop           # Stop container
```

**Technologies:** Docker, Docker Compose, Tor, Nginx, OpenSSH

---

## Cybersecurity_Piscine/Stockholm

**Path:** [`Cybersecurity_Piscine/Stockholm/`](Cybersecurity_Piscine/Stockholm/)
**Documentation:** [README](Cybersecurity_Piscine/Stockholm/README.md)

**Educational ransomware simulator** demonstrating file encryption/decryption with **Fernet symmetric encryption**. Targets 100+ file extensions (WannaCry-style targeting) in a fully containerized environment with Docker Compose.

**Operations:**
- **Encryption** — Encrypts files in `~/infection` with auto-generated `stockholm.key`
- **Decryption** — Restores encrypted files using the saved key file or key string

**Features:**
- ✅ Fernet encryption (AES-128 + HMAC-SHA256)
- ✅ Automatic key generation and persistence
- ✅ 100+ file type targeting
- ✅ Recursive directory traversal
- ✅ Dual-mode key loading (file or string)
- ✅ Docker Compose setup with volume mapping to `./src/`

**Quick Start:**
```bash
cd Cybersecurity_Piscine/Stockholm
make start          # Build and start container
make create-files   # Generate test files
make test           # Run encryption
make bash           # Enter container
stockholm -r stockholm.key  # Decrypt (inside container)
```

**Technologies:** Python 3, cryptography (Fernet), Docker, Docker Compose

---

## Cybersecurity_Piscine/Reverse_me_i'm_famous!

**Path:** [`Cybersecurity_Piscine/Reverse_me_i'm_famous!/`](Cybersecurity_Piscine/Reverse_me_i'm_famous!/)
**Documentation:** [README](Cybersecurity_Piscine/Reverse_me_i'm_famous!/README.md)

**Reverse Engineering Challenge** with 3 binary analysis exercises:

- **Level 1** (x86 32-bit, ⭐ Beginner) — Find hardcoded key inside executable using GDB
- **Level 2** (x86 32-bit, ⭐⭐ Intermediate) — Reverse decode algorithm: input format validation + decimal-to-ASCII transformation
- **Level 3** (x86-64, ⭐⭐⭐ Advanced) — Analyze 64-bit code with obfuscated control flow and fake function names

**Concepts:** Binary anatomy (ELF), x86/x86-64 assembly, GDB debugging, calling conventions, code obfuscation, source reconstruction

**Quick Start:**
```bash
cd Cybersecurity_Piscine/Reverse_me_i\'m_famous\!/level1
file binary/level1
gdb ./binary/level1
(gdb) disas main
(gdb) break strcmp
(gdb) run
```

**Technologies:** GDB, x86/x86-64 assembly, ELF format analysis

---

## Darkly

**Path:** [`Darkly/`](Darkly/)
**Documentation:** [README](Darkly/README.md)

CTF based on an intentionally vulnerable web application. 14 vulnerabilities from **OWASP Top 10 (2017)** are explored and documented, including:

- SQL Injection (x2)
- Broken Authentication (password reset, cookie manipulation, brute force)
- Insecure file upload
- Path Traversal
- Cross-Site Scripting (XSS and via Data URI)
- Open Redirect, HTTP Header Validation, Security Misconfiguration, Sensitive Data Exposure

Each vulnerability has its flag and write-up in `<vuln>/resources/README.md`.

---

## dr-quine

**Path:** [`dr-quine/`](dr-quine/)
**Documentation:** [C](dr-quine/C/README.md) · [ASM](dr-quine/ASM/README.md) · [Python](dr-quine/Python/README.md)

Implementation of **quines** — programs that print their own source code exactly without reading any external file. The project includes three variants of increasing complexity (`Colleen`, `Grace`, `Sully`), each implemented in **C** and in **x86-64 Assembly** (NASM).

Explores the concepts of self-reference, positional formatting in `printf`, and meta-programming in assembly.

---

## ft_ping

**Path:** [`ft_ping/`](ft_ping/)
**Documentation:** [README](ft_ping/README.md)

Reimplementation of the standard `ping` command in C, using **raw ICMP sockets**. Resolves hostnames via DNS, constructs and sends ICMP Echo Request packets, and calculates round-trip time (RTT) statistics.

**Technologies:** C, raw sockets (`SOCK_RAW`), ICMP, manual DNS resolution

---

## libasm

**Path:** [`libasm/`](libasm/)
**Documentation:** [README](libasm/README.md)

Reimplementation of standard libc functions (`strlen`, `strcpy`, `strcmp`, `write`, `read`, `strdup`) in **x86-64 Assembly** (NASM), following System V ABI. Functions correctly handle `errno` using `__errno_location`.

Useful for understanding low-level calling conventions, direct Linux syscalls, and assembly-C interoperability.

---

## woody-woodpacker

**Path:** [`woody-woodpacker/`](woody-woodpacker/)
**Documentation:** [README](woody-woodpacker/README.md)

**ELF64** binary packer that encrypts the executable segment (`.text`) with 16-byte XOR and injects an unpacker stub using the **PT_NOTE hijacking** technique. When executing the packed binary (`woody`), it:

1. Prints `....WOODY....`
2. Decrypts the `.text` in memory
3. Transfers control to the original entry point

The stub is written in NASM x86-64 and injected at packing time by modifying the ELF program header.

**Technologies:** C, NASM x86-64, ELF64 format, mprotect, XOR cipher
