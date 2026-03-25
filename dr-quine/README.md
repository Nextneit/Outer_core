# Dr-Quine - Quine Programs in Multiple Languages

This project demonstrates **quines** - programs that print their own source code without reading any external files. Implementations are provided in **C**, **Assembly (NASM x64)**, and **Python**.

## What is a Quine?

A quine is a program that outputs its own source code as its only output, without:
- Reading files
- Using external program information (like `argv[0]`)
- Using compiler or system tricks
- Cheating in any way

## Project Structure

```
dr-quine/
├── README.md              ← This file
├── C/                     # C implementation
│   ├── Colleen.c
│   ├── Grace.c
│   ├── Sully.c
│   ├── Makefile
│   └── README.md          # Detailed C documentation
├── ASM/                   # x64 Assembly (NASM) implementation
│   ├── Colleen.s
│   ├── Grace.s
│   ├── Sully.s
│   ├── Makefile
│   └── README.md          # Detailed Assembly documentation
└── Python/                # Python implementation
    ├── Colleen.py
    ├── Grace.py
    ├── Sully.py
    ├── Makefile
    └── README.md          # Detailed Python documentation
```

## Three Implementations per Language

Each implementation (C, Assembly, Python) includes three progressively complex quines:

### Colleen - Basic Quine
Prints its own source code to **stdout**.

**Techniques:**
- String encoding with placeholders
- Positional format arguments (`%1$c`, `%2$c`, etc.)
- Self-reference through a single string variable

### Grace - File-Generating Quine
Writes its own source code to a file WITHOUT executing itself.

**Additional Challenges:**
- File I/O operations
- Macro usage (C version)
- No main execution (remains generation-only)

### Sully - Recursive Quine
Generates a chain of self-replicating quines that execute and compile, with a decremented counter.

**Most Complex:**
- Generates 6 quines in total (Sully_5 through Sully_0)
- Each generation compiles itself
- Counter decrements with each generation
- Recursion stops when counter reaches 0

## Key Techniques

### Placeholder-Based Encoding

All implementations use a core technique of encoding the program in a string with placeholders:

**C/Assembly:**
```c
printf("%1$c %2$c %3$c", 10, 9, 34);
// Result: "\n \t "
```

**Python:**
```python
s = 's = %r\nprint(s %% s)'
print(s % s)  # Prints the quine
```

### Language-Specific Features

| Feature | C | Assembly | Python |
|---------|---|----------|--------|
| **Self-reference** | `%4$s` with address | `lea r8,[s]` and `%4$s` | `%r` with repr() |
| **Newlines** | `%1$c` → 10 | `%1$c` → 10 | `\n` in string |
| **Complexity** | Medium-High | High | Low |
| **Recursion** | system() + gcc | system() + nasm/gcc | subprocess.run() |

## Quick Start

### Build and Test All Implementations
```bash
cd C && make test
cd ../ASM && make test
cd ../Python && make test
```

### Run Individual Programs
```bash
# C
./C/Colleen           # Prints to stdout
./C/Grace             # Creates Grace_kid.c
./C/Sully             # Generates 13 files

# Python
python3 Python/Colleen.py
python3 Python/Grace.py
python3 Python/Sully.py

# Assembly (requires NASM and gcc)
./ASM/Colleen
./ASM/Grace
./ASM/Sully
```

## Detailed Documentation

For in-depth explanations of each implementation:
- [C Implementation](C/README.md) - Detailed C quine techniques
- [Assembly Implementation](ASM/README.md) - x64 assembly quine programming
- [Python Implementation](Python/README.md) - Python string formatting quines

## References

- **RFC 6238**: TOTP (Time-based One-Time Password) standard
- **Quine concepts**: Programs that generate their own source code
- **System V AMD64 ABI**: Calling convention for assembly implementations

## Compilation Requirements

- **C**: gcc, make
- **Assembly**: nasm (Netwide Assembler), gcc, make
- **Python**: Python 3.x

## Learning Outcomes

After studying these quines, you'll understand:
1. String manipulation and self-reference in code
2. Printf-style format string arguments (positional formatting)
3. Low-level assembly programming (x86-64)
4. Memory addressing and calling conventions
5. Recursive program generation and execution
6. Python string formatting with repr()
7. File I/O and process spawning

## Challenge Progression

1. **Colleen** establishes the basic quine pattern
2. **Grace** adds file generation (meta-programming)
3. **Sully** combines recursion with compilation
4. Each language showcases idioms different from the others

This progression demonstrates that the quine concept transcends any single language while requiring different techniques in each context.
