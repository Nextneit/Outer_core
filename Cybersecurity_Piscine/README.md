# Cybersecurity Piscine

Collection of practical cybersecurity exercises. Each project explores different areas: from web scraping and image forensics, to cryptography and authentication.

---

## Contents

| Project | Area | Description |
|---|---|---|
| [Arachnida](#arachnida) | Web Scraping & Forensics | Web scraper for images + EXIF metadata extractor |
| [ft_otp](#ft_otp) | Cryptography | TOTP (One-Time Password) generator from scratch |
| [ft_onion](#ft_onion) | Networking / Docker | Tor hidden service deployment with SSH access |
| [Stockholm](#stockholm) | Cryptography / Ransomware | Educational ransomware simulator with Fernet encryption |
| [Reverse_me_i'm_famous!](#reverse_me_im_famous) | Reverse Engineering | Binary reverse engineering with GDB (3 levels: 32-bit → 64-bit) |

---

## Arachnida

**Path:** [`Arachnida/`](Arachnida/)
**Documentation:** [README](Arachnida/README.md)

Suite of two specialized tools for web analysis and image forensics.

### Exercise 00: Spider

Recursive web scraper that downloads images from a specified URL.

**Features:**
- ✅ Downloads images in formats `.jpg`, `.png`, `.gif`, `.bmp`
- ✅ Recursive scraping with depth control (`-l`)
- ✅ Domain filtering (only downloads from specified domain)
- ✅ Respects `robots.txt`
- ✅ Configurable User-Agent
- ✅ Error handling and retries

**Flags:**
```bash
spider -r              # Enable recursive scraping
spider -l LEVEL        # Maximum depth (default: 2)
spider -p PATH         # Output directory (default: ./data/)
```

**Example:**
```bash
python3 spider.py https://example.com -r -l 2 -p ./images/
```

### Exercise 01: Scorpion

EXIF metadata and file attribute extractor for local images.

**Features:**
- ✅ EXIF metadata extraction (date, camera, GPS, etc.)
- ✅ File information (size, permissions, timestamps)
- ✅ Metadata stripping (`--strip`)
- ✅ Save cleaned images
- ✅ Support for `.jpg`, `.png`, `.gif`, `.bmp`

**Flags:**
```bash
scorpion image.jpg                    # Show metadata
scorpion image.jpg --strip            # Remove metadata
scorpion image.jpg --strip --out out/ # Save cleaned image
```

**Example:**
```bash
python3 scorpion.py photo.jpg
python3 scorpion.py photo.jpg --strip --out ./cleaned/
```

### Run Tests

```bash
cd Arachnida
make install    # Install dependencies
make test       # Run complete test suite
make clean      # Clean environment
```

**Dependencies:**
- [`requests`](https://requests.readthedocs.io/) — HTTP client
- [`BeautifulSoup4`](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [`Pillow`](https://python-pillow.org/) — Image processing
- [`piexif`](https://piexif.readthedocs.io/) — EXIF manipulation

---

## ft_otp

**Path:** [`ft_otp/`](ft_otp/)
**Documentation:** [README](ft_otp/README.md)

**TOTP** (Time-based One-Time Password) generator implemented from scratch, without using external cryptography libraries (only `hmac`, `hashlib`, `struct` from stdlib).

### Concept

TOTP is an algorithm that generates 6-digit codes that change every 30 seconds. It's used in two-factor authentication (2FA) in applications like Google, GitHub, AWS, etc.

**Theoretical Foundation:**
- **RFC 4226:** HOTP algorithm specification (counter-based)
- **RFC 6238:** Extension to TOTP (time-based)
- **HMAC-SHA1:** Underlying cryptographic hash function

### Operations

#### `-g KEYFILE` — Save encrypted key

Reads a hexadecimal key from a file and encrypts it with **Fernet** (AES-128-CBC + HMAC-SHA256).

**Requirements:**
- File must contain exactly **64+ hexadecimal characters** (0-9, a-f, A-F)
- Whitespace and newlines are ignored

**Example:**
```bash
echo "c42c3cc306414141592f772691f47fbf4d2c2263ae34e7b4b9137d128d6d2a7d" > key.hex
python3 ft_otp.py -g key.hex
```

**Output:**
```
Key was successfully saved in ft_otp.key
```

#### `-k [KEYFILE]` — Generate TOTP

Reads the encrypted key and generates a 6-digit OTP code based on the current time.

**Default:** If no file is specified, uses `ft_otp.key`

**Example:**
```bash
python3 ft_otp.py -k
# Output: 534144

# (wait 30+ seconds)
python3 ft_otp.py -k
# Output: 228629 (different)
```

### Automated Execution

The project includes a **complete Makefile** for automation:

```bash
make              # Generates random hex key and encrypts it
make run          # Generates TOTP from saved key
make test         # Complete validation suite
make re           # Clean and rebuild from scratch
make clean        # Remove all generated files
make help         # Show all available targets
```

### Key Management

#### Persistent Fernet Key

On first execution, `ft_otp.fernet` is automatically generated, which acts as the master key for encrypting/decrypting TOTP keys.

```
First execution:
  → Generates ft_otp.fernet (auto)
  → Creates ft_otp.key (encrypted)

Subsequent executions:
  → Loads existing ft_otp.fernet
  → Decrypts ft_otp.key correctly
```

⚠️ **Important:**
- Do NOT commit `ft_otp.fernet` or `ft_otp.key` to repository
- Losing `ft_otp.fernet` = losing access to all saved keys
- Keep secure backup of `ft_otp.fernet`

### File Structure

```
ft_otp/
├── ft_otp.py          # Main script
├── requirements.txt   # Dependencies (cryptography)
├── Makefile          # Complete automation
├── README.md         # Detailed documentation
├── key.hex           # Source hex key (generated by make)
├── ft_otp.key        # Encrypted key (generated by -g)
├── ft_otp.fernet     # Master key (auto-generated)
└── .venv/            # Virtual environment (created by make)
```

### Testing

```bash
cd ft_otp
make test        # Run all tests
make test-gen    # Test key generation
make test-totp   # Test OTP generation
make test-invalid-short  # Validate input rejection
make test-invalid-hex    # Validate input rejection
```

### TOTP Algorithm

Step-by-step implementation:

```
1. Counter = floor(UNIX_TIMESTAMP / 30)
2. HMAC = HMAC-SHA1(key_bytes, counter_big_endian_8bytes)
3. Offset = HMAC[-1] & 0x0F (dynamic)
4. Code = (HMAC[offset:offset+4] & 0x7FFFFFFF) % 1_000_000
5. Output = zero-padded to 6 digits
```

**Properties:**
- ✅ Deterministic: same code for same time and key
- ✅ Time-based: code changes every 30 seconds
- ✅ Synchronizable: compatible with Google Authenticator, Authy, etc.

### Verify with oathtool

Compare with standard `oathtool` tool:

```bash
# Convert hex to base32
KEY_B32=$(python3 -c "import sys; print(__import__('base64').b32encode(bytes.fromhex('$HEX_KEY')).decode().strip('='))")

# Compare outputs
oathtool --totp "$KEY_B32"    # Standard
python3 ft_otp.py -k         # Our implementation

# Should be identical within the same 30-second period
```

### Dependencies

```
cryptography >= 3.4
```

Install with:
```bash
make install
# or
pip install cryptography
```

---

## ft_onion

**Path:** [`ft_onion/`](ft_onion/)
**Documentation:** [README](ft_onion/README.md)

**Tor hidden service deployment** exposing a static web page over HTTP and accessible via SSH, fully containerized with Docker.

### Overview

Deploys three services inside a single Docker container:

| Service | Internal Port | External Port | Description |
|---------|---------------|---------------|-------------|
| **Nginx** | `80` | — | Serves static web page (Tor only) |
| **Tor** | — | — | Exposes web as `.onion` hidden service |
| **OpenSSH** | `4242` | `2222` | Remote container access |

> **Access:** Nginx is not exposed directly to the host. Web access is exclusively through Tor network via the `.onion` address.

### Quick Start

```bash
make start          # Build and start container
make check          # Get .onion address (wait 30-60s for Tor bootstrap)
make test-ssh       # Test SSH: user42 / password
make test-web       # Test web server
make stop           # Stop container
make clean          # Clean everything
```

### Technologies

- **Docker & Docker Compose** — Containerization
- **Tor** — Onion routing and hidden services
- **Nginx** — Web server
- **OpenSSH** — Secure shell access

### Learning Objectives

- ✅ Docker multi-service deployment
- ✅ Tor network fundamentals and `.onion` services
- ✅ Container networking and port mapping
- ✅ SSH configuration in containers
- ✅ Network security and anonymity concepts

---

## Stockholm

**Path:** [`Stockholm/`](Stockholm/)
**Documentation:** [README](Stockholm/README.md)

**Educational ransomware simulator** demonstrating file encryption/decryption using **Fernet symmetric encryption**. Simulates WannaCry-style file targeting (100+ file extensions) in a containerized environment.

### Overview

Stockholm encrypts files in `~/infection` with **Fernet (AES-128 + HMAC-SHA256)** and generates an encryption key saved automatically to the script directory. Decryption requires the same key.

**Targeted File Types:** 100+ extensions (documents, spreadsheets, images, archives, code, databases, media, videos)

### Quick Start

```bash
make start          # Build and start container
make create-files   # Create sample test files (.txt, .json)
make test           # Run encryption automatically
make bash           # Enter container for manual testing
```

### Usage

Inside the container:

```bash
# Encrypt files in ~/infection (auto-generates stockholm.key)
stockholm

# Decrypt files using saved key file
stockholm -r stockholm.key

# Or decrypt with key as argument
stockholm -r "CtSKTRWI0nHfQoXO1cGXWcaVyZgkrs3fX3jfPL2vZRY="

# Show help
stockholm -h

# Show version
stockholm -v
```

### Operations

| Flag | Description |
|------|-------------|
| `stockholm` | Encrypt all eligible files in `~/infection` |
| `-r KEY\|FILE` | Decrypt; accepts key string or path to `stockholm.key` |
| `-s, --silent` | Run without output |
| `-h, --help` | Show help message |
| `-v, --version` | Show version |

### Key Features

- ✅ **Fernet encryption** (symmetric, authenticated)
- ✅ **Automatic key generation** — saved to `stockholm.key` alongside script
- ✅ **100+ file extensions** — targets common document and media types
- ✅ **Recursive directory traversal** — scans all subdirectories
- ✅ **Dual-mode key loading** — accepts key file path or literal string
- ✅ **Non-destructive** — original files renamed with `.ft` extension
- ✅ **Docker Compose setup** — run in isolated, reproducible environment
- ✅ **Volume mapping to host** — encrypted files visible in `./src/`

### File Encryption Flow

```
original_file.txt → [Encrypt] → original_file.txt.ft (encrypted)
                                 stockholm.key (saved)
```

### Decryption Flow

```
original_file.txt.ft → [Decrypt using stockholm.key] → original_file.txt
```

### Makefile Targets

```bash
make help           # Show all targets
make start          # Build and start container
make stop           # Stop container (keeps volumes)
make down           # Stop and remove container
make clean          # Remove container, images, and volumes
make bash           # Open interactive shell in container
make create-files   # Generate test files in ~/infection
make test           # Create files and run encryption
make logs           # Stream container logs
```

### Docker Setup

Files are synchronized via **volume mapping**:

```yaml
volumes:
  - ./stockholm.py:/usr/local/bin/stockholm  # Script as command
  - ./src:/root/infection                     # Files visible on host
```

Result: Encrypted files appear in `./src/` directory on the host in real-time.

### Technologies

- **Python 3** — Implementation language
- **cryptography.fernet** — Encryption backend
- **Docker & Docker Compose** — Containerization

### Learning Objectives

- ✅ Symmetric encryption and key management
- ✅ File I/O and directory traversal
- ✅ Docker containerization and volume mapping
- ✅ Command-line argument parsing in Python
- ✅ Ransomware mechanics (for educational purposes)

> ⚠️ **Disclaimer:** This is an educational project demonstrating encryption concepts. Not for malicious use.

---

## Reverse_me_i'm_famous!

**Path:** [`Reverse_me_i'm_famous!/`](Reverse_me_i'm_famous!/)
**Documentation:** [README](Reverse_me_i'm_famous!/README.md)

**Reverse Engineering Challenge** consisting of 3 binary analysis exercises with increasing difficulty. Learn to use GDB for dynamic analysis, disassembly, and software reconstruction.

### Overview

Three compiled binaries to reverse engineer and find hidden keys:

| Level | Arch | Difficulty | Objective |
|-------|------|------------|-----------|
| **Level 1** | x86 32-bit | ⭐ Beginner | Find hardcoded key using `strcmp` breakpoint |
| **Level 2** | x86 32-bit | ⭐⭐ Intermediate | Decode algorithm: input validation + decimal-to-ASCII transformation |
| **Level 3** | x86-64 | ⭐⭐⭐ Advanced | 64-bit analysis with complex validation logic and control flow obfuscation |

### Quick Start

```bash
cd Reverse_me_i'm_famous!/level1

# Reconnaissance
file binary/level1
strings binary/level1 | grep -E "(Good|Nope)"

# Dynamic analysis with GDB
gdb ./binary/level1
(gdb) disas main
(gdb) break strcmp
(gdb) run
(gdb) x/s $esp    # Inspect stack memory
```

### Learning Objectives

- ✅ Binary anatomy (ELF headers, segments, symbols)
- ✅ x86 and x86-64 assembly reading
- ✅ GDB usage for dynamic debugging
- ✅ Calling conventions (cdecl on 32-bit, System V on 64-bit)
- ✅ Identifying obfuscation techniques (hardcoding, false function names, control flow complexity)
- ✅ Reconstructing source code from binary
- ✅ Understanding algorithm transformation (validation → encoding)

### Tools

```bash
gdb              # Primary debugger
strings          # Extract text from binary
objdump          # Disassemble and analyze
readelf          # Read ELF headers
strace / ltrace  # Trace syscalls and library calls
radare2          # Interactive analysis (alternative)
```

### Key Concepts

**Level 1:**
- Stack layout in 32-bit (`ESP`, `EBP`)
- cdecl calling convention (arguments on stack)
- Basic string functions: `printf`, `scanf`, `strcmp`
- Hardcoded data in executable

**Level 2:**
- Input validation (format checking with specific prefixes)
- Algorithmic transformation (decimal string → ASCII bytes)
- Loop analysis and reconstruction  
- Obfuscation: noise strings, meaningless variable names

**Level 3:**
- x86-64 registers (`RAX`, `RDI`, `RSI`, etc.)
- System V AMD64 ABI (arguments in registers)
- PIE (Position Independent Executable)
- Complex control flow (switches with multiple cases)
- Deliberate obfuscation: fake function names (`___syscall_malloc` vs `____syscall_malloc`)

---

## Key Concepts

### Cryptography in Arachnida
- **EXIF Extraction:** Analysis of digital image metadata
- **Data Security:** Importance of cleaning metadata before sharing images

### Cryptography in ft_otp
- **HMAC:** Data authentication method
- **TOTP:** Time-synchronized one-time passwords
- **Fernet Encryption:** Symmetric AES + HMAC for authenticity
- **Secret Management:** Secure storage of cryptographic keys

### Reverse Engineering in Reverse_me_i'm_famous!
- **Binary Analysis:** Understanding compiled code structure (ELF format)
- **Assembly Language:** Reading and interpreting x86/x86-64 instructions
- **Dynamic Debugging:** Using GDB to trace execution and inspect memory
- **Code Obfuscation:** Identifying and bypassing anti-analysis techniques
- **Algorithm Reconstruction:** Converting binary to high-level source code

---

## Recommended Workflow

### Arachnida

```bash
cd Arachnida
make install           # Setup (one time)

# Use Spider
python3 ex00/spider.py https://example.com -p ./images/

# Use Scorpion
python3 ex01/scorpion.py ./images/photo.jpg
python3 ex01/scorpion.py ./images/photo.jpg --strip --out ./cleaned/
```

### ft_otp

```bash
cd ft_otp
make              # Generates random key and encrypts it
make run          # Generates TOTP (6-digit code)

# Or manually
echo "c42c3cc306414141...7d2a7d" > key.hex
python3 ft_otp.py -g key.hex
python3 ft_otp.py -k
```

---

## References

### Arachnida
- [Requests Documentation](https://requests.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [EXIF Specification](https://en.wikipedia.org/wiki/Exif)
- [robots.txt Standard](https://www.robotstxt.org/)

### ft_otp
- [RFC 4226: HOTP Algorithm](https://tools.ietf.org/html/rfc4226)
- [RFC 6238: TOTP Algorithm](https://tools.ietf.org/html/rfc6238)
- [Fernet (cryptography.io)](https://cryptography.io/en/latest/fernet/)
- [HMAC Wikipedia](https://en.wikipedia.org/wiki/HMAC)

---

## Troubleshooting

### Arachnida

**Q: "ModuleNotFoundError: No module named 'requests'"**
```bash
make install
```

**Q: "SSL Certificate Error"**
- Some sites may require special headers
- Adjust User-Agent in code if necessary

### ft_otp

**Q: "error: failed to load key"**
- Delete `ft_otp.fernet` and regenerate:
```bash
rm ft_otp.fernet
python3 ft_otp.py -k
```

**Q: "key must be 64 hexadecimal characters"**
- Verify file has exactly 64 hex characters
- No spaces, newlines, or special characters

---

## Next Steps

Upcoming exercises planned for Cybersecurity Piscine:
- Inquisitor (log analysis)
- Vaccine (malware analysis)
- Iron Dome (intrusion detection)
