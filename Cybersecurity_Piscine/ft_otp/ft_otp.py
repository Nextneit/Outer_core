import sys
import os
import argparse
import time
import struct
import hmac
import hashlib
from cryptography.fernet import Fernet

FERNET_KEY_FILE = 'ft_otp.fernet'

def get_fernet_key() -> bytes:
    """Load existing Fernet key or generate and save a new one."""
    if os.path.exists(FERNET_KEY_FILE):
        with open(FERNET_KEY_FILE, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(FERNET_KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def validate_hex_key(hex_key: str) -> bool:
    """Validate that the key is at least 64 hexadecimal characters."""
    if len(hex_key) < 64:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in hex_key)

def generate_totp(hex_key: str) -> str:
    """Generate a 6-digit TOTP based on current time and hex key."""
    key_bytes = bytes.fromhex(hex_key)
    counter = struct.pack('>Q', int(time.time()) // 30)
    h = hmac.new(key_bytes, counter, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = (h[offset] & 0x7F) << 24 | h[offset + 1] << 16 | h[offset + 2] << 8 | h[offset + 3]
    return str(code % 1_000_000).zfill(6)

def save_key(key_file_input: str, key_file: str = 'ft_otp.key') -> None:
    """Read hex key from a file, validate and encrypt it."""
    try:
        with open(key_file_input, 'r') as f:
            hex_key = f.read().strip()
    except FileNotFoundError:
        print(f"error: file '{key_file_input}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"error: failed to read file '{key_file_input}': {e}")
        sys.exit(1)

    if not validate_hex_key(hex_key):
        print(f"error: key must be 64 hexadecimal characters.")
        sys.exit(1)

    try:
        fernet = Fernet(get_fernet_key())
        encrypted = fernet.encrypt(hex_key.encode())
        with open(key_file, 'wb') as f:
            f.write(encrypted)
        print(f"Key was successfully saved in {key_file}")
    except Exception as e:
        print(f"error: failed to save key: {e}")
        sys.exit(1)

def load_key(key_file: str) -> str:
    """Load and decrypt a hex key from a file."""
    try:
        if not os.path.exists(key_file):
            print(f"error: key file '{key_file}' not found.")
            sys.exit(1)
        
        with open(key_file, 'rb') as f:
            encrypted = f.read()
        
        fernet = Fernet(get_fernet_key())
        hex_key = fernet.decrypt(encrypted).decode()
        return hex_key
    except Exception as e:
        print(f"error: failed to load key: {e}")
        sys.exit(1)

def main():
    """Parse arguments and execute the appropriate action."""
    parser = argparse.ArgumentParser(
        prog='ft_otp',
        description='TOTP (Time-based One-Time Password) generator',
        usage='%(prog)s (-g KEYFILE | -k [KEYFILE])',
        epilog='Examples:\n  python3 ft_otp.py -g key.hex\n  python3 ft_otp.py -k\n  python3 ft_otp.py -k custom.key',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create mutually exclusive group for -g and -k flags
    group = parser.add_mutually_exclusive_group(required=True)
    
    # Flag: -g to generate and save a key
    group.add_argument(
        '-g',
        metavar='KEYFILE',
        dest='generate_key',
        help='Read hex key from file and save encrypted to ft_otp.key'
    )
    
    # Flag: -k to generate TOTP from saved key
    group.add_argument(
        '-k',
        nargs='?',
        const='ft_otp.key',
        metavar='KEYFILE',
        dest='keyfile',
        help='Generate TOTP from a saved key file (default: ft_otp.key)'
    )
    
    args = parser.parse_args()
    
    # Execute appropriate action
    if args.generate_key:
        save_key(args.generate_key)
    elif args.keyfile is not None:
        hex_key = load_key(args.keyfile)
        print(generate_totp(hex_key))

if __name__ == "__main__":
    main()