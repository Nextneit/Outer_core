# Dr-Quine - Python Implementation

This directory contains the Python implementation of the **dr-quine** project from School 42. A **quine** is a program that prints its own source code without reading any external file.

## Index
- [Execution](#execution)
- [Fundamental Concepts](#fundamental-concepts)
- [Colleen.py - Basic Quine](#colleenpy---basic-quine)
- [Grace.py - File-Generating Quine](#gracepy---file-generating-quine)
- [Sully.py - Recursive Quine](#sullypy---recursive-quine)
- [Advanced Techniques](#advanced-techniques)

---

## Execution

### Run tests
```bash
make           # Run all tests
```

### Run individually
```bash
python3 Colleen.py
python3 Grace.py
python3 Sully.py
```

### Clean generated files
```bash
make clean     # Clean temporary files
make fclean    # Complete cleanup (including generated files)
```

---

## Fundamental Concepts

### What is a Quine?

A quine is a program that produces its own source code as output, **without**:
- Reading files (`open`, `read`, etc.)
- Using `sys.argv[0]` or system information
- Cheating in any form

### Project Constraints

Each program must satisfy:
- **Colleen**: Prints its own source code to stdout
- **Grace**: Writes its own source code to a file (`Grace_kid.py`)
- **Sully**: Generates a chain of 6 quines that self-replicate by decrementing a counter

### Key Technique: `%r` (repr) in Python

The fundamental technique in Python is using `%r` with `%` formatting:

```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

**Why it works**:
- `%r` applies `repr()` to the argument, automatically adding single quotes and escaping special characters
- `%%` generates a literal `%` in the output
- When substituting `s % s`, the string inserts itself completely with its quotes

### Key Values

| Technique | Usage |
|-----------|-------|
| `%r` | Inserts the string representation with quotes (self-reference) |
| `%%` | Prints a literal `%` (necessary for child to be valid) |
| `%d` | Inserts an integer (for counter in Sully) |

---

## Colleen.py - Basic Quine

### Description
Prints its own source code to **stdout**.

### Complete Code
```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

### Detailed Analysis

#### The String `s`

```python
s = 's = %r\nprint(s %% s)'
```

The string contains **almost the entire program code** with a `%r` placeholder.

#### Step-by-Step Execution

1. `s` is defined with the code template
2. `s % s` applies the format:
   - `%r` is replaced by `repr(s)` → the string with its quotes: `'s = %r\nprint(s %% s)'`
   - `%%` becomes a literal `%`
3. The result is:
   ```python
   s = 's = %r\nprint(s %% s)'
   print(s % s)
   ```

#### Why `%r` is Perfect for Quines

- `repr(s)` produces `'s = %r\nprint(s %% s)'` (note the quotes and escaped `\n`)
- Inserting that after `s = ` reproduces exactly the first line of code
- The `%%` in the template becomes `%` in the output, making the child executable

### Requirements Met
- ✅ Prints its own source code exactly
- ✅ Reads no external files

---

## Grace.py - File-Generating Quine

### Description
Writes its own source code to **Grace_kid.py**.

### Complete Code
```python
s = 's = %r\nwith open("Grace_kid.py", "w") as f:\n    f.write(s %% s)\n'
with open("Grace_kid.py", "w") as f:
    f.write(s % s)
```

### Detailed Analysis

#### The String `s`

```python
s = 's = %r\nwith open("Grace_kid.py", "w") as f:\n    f.write(s %% s)\n'
```

The string encodes the entire program, including the `with open(...)` block.

#### Step-by-Step Execution

1. `s` contains the template with the complete code (newlines escaped as `\n`)
2. `s % s`:
   - `%r` → `repr(s)` → the string with its quotes and escapes
   - `%%` → literal `%`
3. The result is written to `Grace_kid.py`
4. `Grace_kid.py` is identical to the source code of `Grace.py`

#### Verification
```bash
python3 Grace.py
diff Grace.py Grace_kid.py   # No differences
```

### Requirements Met
- ✅ `Grace_kid.py` is identical to `Grace.py`
- ✅ Reads no external files

---

## Sully.py - Recursive Quine

### Description
Generates a chain of quines that self-replicate, execute, and decrement a counter in each generation, producing 6 files in total (`Sully_5.py` through `Sully_1.py`) plus their respective executions.

### Complete Code
```python
import subprocess
s = 'import subprocess\ns = %r\ni = %d\nif i > 0:\n    fname = "Sully_" + str(i) + ".py"\n    with open(fname, "w") as f:\n        f.write(s %% (s, i - 1))\n    subprocess.run(["python3", fname])\n'
i = 5
if i > 0:
    fname = "Sully_" + str(i) + ".py"
    with open(fname, "w") as f:
        f.write(s % (s, i - 1))
    subprocess.run(["python3", fname])
```

### Line-by-Line Analysis

#### Main Variables
```python
s = 'import subprocess\n...'   # Template with all the code
i = 5                          # Initial counter
```

#### The Template with Two Placeholders
```python
s = '...s = %r\ni = %d\n...'
```
- `%r` → `repr(s)` (self-reference to the code)
- `%d` → the decremented counter

#### Phase 1: Validation
```python
if i > 0:
```
If the counter reaches 0, the program generates no more children and does nothing.

#### Phase 2: Child File Generation
```python
fname = "Sully_" + str(i) + ".py"
with open(fname, "w") as f:
    f.write(s % (s, i - 1))
```

**KEY**: `s % (s, i - 1)` uses two arguments:
- `s` → replaces `%r` (the complete code with repr)
- `i - 1` → replaces `%d` (**decremented counter**)

The child file has the same code but with `i = i-1`.

#### Phase 3: Recursive Execution
```python
subprocess.run(["python3", fname])
```
Executes the child, which in turn will generate its own child with `i-2`, and so on.

### Complete Execution Chain

```
Sully.py (i=5)
  ├─> creates Sully_5.py (with i=4)
  └─> executes python3 Sully_5.py
        ├─> creates Sully_4.py (with i=3)
        └─> executes python3 Sully_4.py
              ├─> creates Sully_3.py (with i=2)
              └─> executes python3 Sully_3.py
                    ├─> creates Sully_2.py (with i=1)
                    └─> executes python3 Sully_2.py
                          ├─> creates Sully_1.py (with i=0)
                          └─> executes python3 Sully_1.py
                                └─> i = 0, generates no more children
```

**Generated files**: `Sully_5.py`, `Sully_4.py`, `Sully_3.py`, `Sully_2.py`, `Sully_1.py` (6 in total counted with `Sully.py`)

### Requirements Met
- ✅ Generates exactly 6 scripts in the chain
- ✅ Each child is a valid quine with decremented counter
- ✅ The chain stops when `i = 0`

---

## Advanced Techniques

### Why Python is Ideal for Quines

Python facilitates writing quines thanks to:

1. **`%r` with `repr()`**: Automatically produces a string representation with quotes and escapes, avoiding the need to manually encode delimiters.

2. **Multiline strings and `\n`**: Line breaks can be encoded as `\n` within the string and `repr()` preserves them correctly.

3. **`%` formatting**: The `%` operator allows substituting multiple values (`%r`, `%d`, `%%`) in a compact way.

### Comparison with C Version

| Aspect | C | Python |
|---------|---|--------|
| Self-reference | `%4$s` with positional arguments | `%r` with repr() |
| Newlines | `%1$c` with value `10` | `\n` escaped in string |
| Quotes | `%3$c` with value `34` | Handled by `repr()` |
| Child execution (Sully) | `system()` + gcc compilation | `subprocess.run()` direct |
| Quine complexity | Medium-high | Low |
