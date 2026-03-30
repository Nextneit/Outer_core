# stockholm

Ransomware simulation for educational purposes only.
Encrypts and decrypts files in `~/infection` using AES-256-GCM.

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

**Algorithm: AES-256-GCM**

- Symmetric, authenticated encryption (confidentiality + integrity)
- 256-bit key — resistant to brute force
- GCM mode detects tampering via authentication tag
- Provided by the `cryptography` library (built on OpenSSL)