# stockholm

Ransomware simulation for educational purposes only.
Encrypts and decrypts files in `~/infection` using Fernet (AES-128-CBC + HMAC-SHA256).

## Dependencies

- Python 3.x
- `cryptography` library

## Installation

```bash
make
```

> This installs the required Python dependencies automatically.

## Usage

```bash
./stockholm [OPTIONS]
```

| Option | Description |
|---|---|
| `-h`, `--help` | Show help message |
| `-v`, `--version` | Show program version |
| `-s`, `--silent` | Run without output |
| `-r <key>`, `--reverse <key>` | Decrypt files using the provided key |

## Examples

```bash
# Encrypt files in ~/infection
./stockholm

# Encrypt silently / decrypt with key
./stockholm -s
./stockholm -r <your-key>
```

## Encryption

**Algorithm: Fernet (AES-128-CBC + HMAC-SHA256)**

- Symmetric, authenticated encryption (confidentiality + integrity)
- HMAC-SHA256 detects any tampering before decryption
- Key generated via `Fernet.generate_key()` — 32 bytes (base64), well above 16 char minimum
- Provided by the `cryptography` library (built on OpenSSL)