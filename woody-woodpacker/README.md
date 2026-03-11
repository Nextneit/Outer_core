# woody-woodpacker

A 64-bit ELF binary packer that encrypts the executable segment and injects a self-decrypting stub into the binary.

## Overview

`woody_woodpacker` takes any 64-bit ELF executable, encrypts its `.text` segment with a randomly generated XOR key, and injects a small decryption stub into the binary using the **PT_NOTE hijacking** technique. The resulting binary (`woody`) decrypts itself at runtime, prints `....WOODY....` to stdout, and then transfers control to the original entry point transparently.

### How it works

```
[Input ELF] ──► encrypt .text (XOR, 16-byte key) ──► inject stub ──► [woody]
                                                            │
                                    At runtime:             ▼
                                    1. Print "....WOODY...."
                                    2. mprotect(.text, RWX)
                                    3. XOR-decrypt .text in memory
                                    4. mprotect(.text, RX)
                                    5. jmp → original entry point
```

#### PT_NOTE Hijacking

The stub is placed at the end of the file (page-aligned) and a `PT_NOTE` segment header is repurposed as a new `PT_LOAD` executable segment pointing to it. The ELF entry point (`e_entry`) is redirected to the stub's virtual address. This technique works because the kernel ignores `PT_NOTE` segments at load time, so they can be freely reused.

---

## Requirements

- Linux x86-64
- GCC
- NASM (`nasm`)
- GNU Make

---

## Build

```bash
make
```

This compiles the project and produces the `woody_woodpacker` binary.

| Target       | Description                             |
|--------------|-----------------------------------------|
| `make`       | Build `woody_woodpacker`                |
| `make clean` | Remove compiled object files            |
| `make fclean`| Remove objects and the binary           |
| `make re`    | Full rebuild (`fclean` + `all`)         |
| `make test`  | Build, create a test binary, and run it |

---

## Usage

```bash
./woody_woodpacker <elf_file>
```

- `<elf_file>` — Path to a 64-bit ELF executable to pack.

The tool will:
1. Validate that the file is a 64-bit ELF.
2. Generate a random 16-byte XOR key.
3. Print the key to stdout in hex.
4. Encrypt the executable segment in memory.
5. Inject the decryption stub using PT_NOTE hijacking.
6. Write the packed binary to a file named **`woody`** in the current directory.

### Example

```bash
# Compile a target binary
gcc -o hello hello.c

# Pack it
./woody_woodpacker hello
# Output:
# [KEY] a3 f1 0c ... (16 bytes)
# [+] Archivo 'woody' escrito (XXXX bytes)

# Run the packed binary
./woody
# Output:
# ....WOODY....
# Hello, World!
```

---

## Project Structure

```
woody-woodpacker/
├── Makefile
├── include/
│   └── woody-woodpacker.h   # Global header (types, structs, constants)
├── libft/                   # Custom C library
└── src/
    ├── main.c               # Entry point and orchestration
    ├── elf_parser.c         # ELF64 header validation
    ├── crypto.c             # Key generation and XOR encryption
    ├── inject_stub.c        # PT_NOTE hijacking and stub injection
    ├── write_woody.c        # Write packed binary to disk
    ├── stub.s               # x86-64 NASM decryption stub (source)
    ├── stub.c               # Compiled stub bytes (generated)
    └── stub_bytes.h         # Stub bytecode array declaration
```

### Key constants (`woody-woodpacker.h`)

| Constant    | Value | Description                        |
|-------------|-------|------------------------------------|
| `KEY_SIZE`  | 16    | XOR key length in bytes            |
| `STUB_SIZE` | 240   | Decryption stub size in bytes      |

---

## Technical Details

### Encryption

The `.text` segment (first `PT_LOAD` with the executable flag `PF_X`) is encrypted byte-by-byte using a cyclic 16-byte XOR key:

```
ciphertext[i] = plaintext[i] XOR key[i % 16]
```

The key is generated from `/dev/random` (falls back to `rand()` if unavailable).

### Stub layout (patched at inject time)

| Offset | Size     | Field        | Description                         |
|--------|----------|--------------|-------------------------------------|
| +0x6A  | 16 bytes | `key`        | XOR decryption key                  |
| +0x7A  | 8 bytes  | `seg_addr`   | Virtual address of encrypted segment|
| +0x82  | 8 bytes  | `seg_size`   | Size of encrypted segment           |
| +0x8A  | 8 bytes  | `orig_entry` | Original ELF entry point            |

### Limitations

- Only supports **64-bit ELF** binaries (`ET_EXEC` and `ET_DYN`/PIE).
- The target binary must have a `PT_NOTE` segment (most Linux ELFs do).
- The target binary must have an executable `PT_LOAD` segment.
- Output is always written to `./woody` in the current working directory.
