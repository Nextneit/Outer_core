# ft_otp - One-Time Password Generator

A TOTP (Time-based One-Time Password) generator implemented from scratch in Python, based on the HOTP algorithm defined in [RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226).

---

## Overview

`ft_otp` generates 6-digit one-time passwords synchronized with real time. It uses HMAC-SHA1 as the underlying cryptographic function and Fernet for secure key storage.

**Core Features:**
- ✅ Implements TOTP algorithm without external crypto libraries
- ✅ Persistent Fernet key stored in `ft_otp.fernet`
- ✅ Encrypted key storage in `ft_otp.key`
- ✅ Comprehensive validation and error handling
- ✅ Full Makefile automation

---

## Installation

### Prerequisites
- Python 3.x
- `cryptography` package (for Fernet encryption)

### Setup

```bash
make install
```

This creates a virtual environment and installs dependencies.

---

## Quick Start

### Method 1: Using Make (Recommended)

```bash
# Generate random 64-char hex key and save encrypted
make

# Generate TOTP from the saved key
make run

# Start fresh (clean + rebuild)
make re
```

### Method 2: Manual Usage

```bash
# Step 1: Generate a 64-character hexadecimal key
python3 -c "import os; print(os.urandom(32).hex())" > key.hex

# Step 2: Save the key encrypted
python3 ft_otp.py -g key.hex

# Step 3: Generate a one-time password
python3 ft_otp.py -k ft_otp.key
```

---

## Flags

### `-g KEYFILE` — Generate and save encrypted key

**Usage:**
```bash
python3 ft_otp.py -g <path_to_key_file>
```

**Input Requirements:**
- File must contain at least 64 hexadecimal characters (0-9, a-f, A-F)
- Whitespace is stripped automatically
- Leading/trailing newlines are ignored

**Output:**
- Creates/overwrites `ft_otp.key` (encrypted with Fernet)
- Success message: `"Key was successfully saved in ft_otp.key"`

**Examples:**
```bash
echo "c42c3cc306414141592f772691f47fbf4d2c2263ae34e7b4b9137d128d6d2a7d" > key.hex
python3 ft_otp.py -g key.hex
```

### `-k [KEYFILE]` — Generate TOTP from encrypted key

**Usage:**
```bash
python3 ft_otp.py -k [key_file]
```

**Default:**
- If no file specified, uses `ft_otp.key`

**Output:**
- 6-digit one-time password (zero-padded)
- Changes every 30 seconds

**Examples:**
```bash
python3 ft_otp.py -k                      # Uses ft_otp.key
python3 ft_otp.py -k custom.key           # Uses custom.key
```

---

## TOTP Algorithm

The implementation follows RFC 4226 / RFC 6238:

```
1. Time Counter = floor(UNIX_TIMESTAMP / 30)
2. HMAC = HMAC-SHA1(key_bytes, counter_as_big_endian_8bytes)
3. Offset = HMAC[-1] & 0x0F (dynamically offset)
4. Code = (HMAC[offset:offset+4] & 0x7FFFFFFF) % 1_000_000
5. Output = zero-padded to 6 digits
```

**Key Properties:**
- Time-based (30-second windows)
- Independent calculation — same code within same 30s window
- Deterministic with same key and time window

---

## Makefile Targets

### Main Targets

```bash
make              # Default: generate random key and encrypt
make install      # Setup venv and install dependencies
make run          # Generate TOTP from encrypted key
make re           # Clean and rebuild from scratch
make clean        # Remove all generated files
make test         # Run full test suite
make help         # Show all available targets
```

### Test Targets

```bash
make test-gen             # Test key generation from file
make test-totp            # Test TOTP generation
make test-invalid-short   # Validate rejection of short keys
make test-invalid-hex     # Validate rejection of invalid hex
make test-help            # Display script help
```

---

## Generated Files

### On Successful `-g`:
- **`ft_otp.key`** — Encrypted TOTP secret (binary, Fernet encrypted)
- **`ft_otp.fernet`** — Persistent encryption key (binary, auto-generated on first use)

### Temporary:
- **`key.hex`** — Source key file (created by `make`)
- **`.venv/`** — Python virtual environment

---

## Key Management

### Fernet Key Persistence

The first run generates and saves `ft_otp.fernet`, which is used for all subsequent encryptions/decryptions. This allows:

✅ Saving multiple keys with the same encryption master
✅ Reading previously saved keys across different sessions
✅ Losing the ability to decrypt if `ft_otp.fernet` is deleted

### Security Implications

- ⚠️ **Do NOT commit** `ft_otp.fernet` or `ft_otp.key` to version control
- Keep `ft_otp.fernet` safe — losing it means losing access to all saved keys
- The `.gitignore` should exclude these files

---

## Example Workflow

```bash
# 1. Setup (one time)
$ make
[→] Creating virtual environment...
[✓] Installation complete!
[✓] Random key file generated: key.hex
Key was successfully saved in ft_otp.key

# 2. Generate TOTP (repeatable)
$ make run
[TEST 2] Generating TOTP from key file...
→ Current TOTP:
534144

# 3. Wait 30+ seconds (code changes)
$ sleep 35 && make run
534144    # (different code after 30 seconds)

# 4. Clean up
$ make clean
[→] Cleaning up...
[✓] Clean complete!

# 5. Start fresh
$ make re
[✓] Rebuild complete!
```

---

## Testing

Run comprehensive tests:

```bash
make test
```

This validates:
- ✅ Valid key generation and encryption
- ✅ Proper TOTP generation from stored keys
- ✅ Rejection of keys shorter than 64 characters
- ✅ Rejection of non-hexadecimal characters
- ✅ Help message display

---

## Verification Against `oathtool`

Compare with the standard `oathtool`:

```bash
# Convert hex key to base32 (oathtool requirement)
KEY_B32=$(python3 -c "import sys; print(__import__('base64').b32encode(bytes.fromhex('$KEY')).decode().strip('='))")

# Compare outputs
oathtool --totp "$KEY_B32"
python3 ft_otp.py -k
```

Both should return the same 6-digit code within the same 30-second window.

---

## Dependencies

```
cryptography >= 3.4
```

Install with:
```bash
pip install cryptography
```

Or via Makefile:
```bash
make install
```

---

## Security Notes

- **Key File:** Never stored in plaintext. Encrypted with Fernet (AES-128-CBC + HMAC-SHA256)
- **Fernet Key:** Auto-generated, persistent, never committed
- **Input Validation:** Strict — rejects any non-64-char-hex input
- **Time-based:** No dependency on counter files or state — purely time-based
- **Error Handling:** Clear error messages for all failure scenarios

---

## Project Structure

```
ft_otp/
├── ft_otp.py          # Main script
├── requirements.txt   # Dependencies (cryptography)
├── Makefile          # Automation
├── README.md         # This file
├── key.hex           # Source key (generated by make)
├── ft_otp.key        # Encrypted key (generated by -g)
├── ft_otp.fernet     # Fernet master key (auto-generated)
└── .venv/            # Virtual environment (created by make install)
```

---

## Troubleshooting

**Q: "file 'key.hex' not found"**
- Run `make` first to generate a key file

**Q: "error: failed to load key"**
- Delete `ft_otp.fernet` and retry (forces new encryption key)
- Or restore backup of `ft_otp.fernet`

**Q: Generated code differs from oathtool**
- Ensure you're comparing within the same 30-second window
- Check that the hex key is identical

**Q: "key must be 64 hexadecimal characters"**
- Ensure input has exactly 64 chars of 0-9, a-f (or A-F)
- No spaces, newlines, or extra characters

---

## References

- [RFC 4226: HOTP Algorithm](https://tools.ietf.org/html/rfc4226)
- [RFC 6238: TOTP Algorithm](https://tools.ietf.org/html/rfc6238)
- [Fernet Encryption (cryptography.io)](https://cryptography.io/en/latest/fernet/)

