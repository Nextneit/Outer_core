# Dr-Quine - Assembly Implementation (NASM x64)

This directory contains the x64 Assembly (NASM) implementation of the **dr-quine** project from School 42. A **quine** is a program that prints its own source code without reading any external file.

## Index
- [Compilation and Execution](#compilation-and-execution)
- [Fundamental Concepts](#fundamental-concepts)
- [Colleen.s - Basic Quine](#colleens---basic-quine)
- [Grace.s - File Output Quine](#graces---file-output-quine)
- [Sully.s - Recursive Quine](#sullys---recursive-quine)
- [Technical Details](#technical-details)

---

## Compilation and Execution

### Compile all programs
```bash
make
```

### Run tests
```bash
make test              # Run all tests
make test_colleen      # Colleen individual test
make test_grace        # Grace individual test
make test_sully        # Sully individual test
```

### Clean generated files
```bash
make clean    # Clean binaries and objects
make fclean   # Complete cleanup
```

---

## Fundamental Concepts

### What is a Quine?

A quine is a program that produces its own source code as output, **without**:
- Reading files
- Using `argv[0]` or similar
- Cheating in any form

### Implementation Technique

The main technique used in these quines is **self-reference with placeholders**:

1. **Encoded string**: A string `s` is defined that contains the entire program code, but with placeholders instead of literal values.

2. **Positional format**: `printf`/`fprintf` is used with positional arguments (`%1$c`, `%2$c`, etc.) to reuse arguments.

3. **Key values**:
   - `10` = newline (`\n`)
   - `9` = tab (`\t`)
   - `34` = double quote (`"`)
   - The address of `s` itself (self-reference)

### x64 Calling Convention

The programs use the System V AMD64 calling convention:
- **First 6 arguments**: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`
- **Additional arguments**: Passed on the stack
- **Callee-saved registers**: `rbx`, `r12-r15`, `rbp`, `rsp`
- **Stack alignment**: Must be 16-byte aligned before `call`

---

## Colleen.s - Basic Quine

### Description
Prints its own source code to **stdout**.

### Code Structure

#### section .data
```nasm
s: db "; Outer comment%1$c...%1$c",0
```
- Contains the entire program code encoded
- Placeholders: `%1$c` (newline), `%2$c` (tab), `%3$c` (quote), `%4$s` (string s)

#### section .text - main
```nasm
main:
    push rbp
    mov rbp,rsp           ; Standard prologue
    
    ; Prepare printf arguments
    lea rdi,[s]           ; arg1: format (string s)
    mov rsi,10            ; arg2: %1$c = newline
    mov rdx,9             ; arg3: %2$c = tab
    mov rcx,34            ; arg4: %3$c = double quote
    lea r8,[s]            ; arg5: %4$s = address of string s
    
    xor rax,rax           ; rax=0 (no vector arguments)
    call printf           ; Print the quine
    
    xor rax,rax           ; return 0
    pop rbp
    ret
```

### Step-by-Step Execution

1. **Format loading**: `rdi` points to `s`, which contains the format with placeholders
2. **Positional arguments**: Values that will replace placeholders are loaded
3. **Self-reference**: The 5th argument (`r8`) contains the address of `s` itself
4. **Printf**: Interprets the format and substitutes:
   - `%1$c` → newline (10)
   - `%2$c` → tab (9)
   - `%3$c` → double quote (34)
   - `%4$s` → content of `s`

The result is the complete code, including comments and the definition of `s`.

### Project Requirements
- ✅ 2 comments (outer and inner)
- ✅ 1 helper function (implicit: main is called from _start)

---

## Grace.s - File Output Quine

### Description
Writes its own source code to the file **Grace_kid.s** (without executing itself).

### Code Structure

#### section .data
```nasm
s: db "; Comment%1$csection .data%1$c...",0
f: db "Grace_kid.s",0      ; Output filename
mode: db "w",0              ; Open mode: write
```

#### section .text - main
```nasm
main:
    push rbp
    mov rbp,rsp
    
    ; 1. Open Grace_kid.s file
    lea rdi,[f]           ; arg1: filename
    lea rsi,[mode]        ; arg2: mode "w"
    call fopen
    mov r12,rax           ; Save file pointer in r12 (callee-saved)
    
    ; 2. Write quine to file
    mov rdi,r12           ; arg1: file pointer
    lea rsi,[s]           ; arg2: format (string s)
    mov rdx,10            ; arg3: %1$c = newline
    mov rcx,9             ; arg4: %2$c = tab
    mov r8,34             ; arg5: %3$c = double quote
    lea r9,[s]            ; arg6: %4$s = address of string s
    xor rax,rax
    call fprintf
    
    ; 3. Close file
    mov rdi,r12
    call fclose
    
    xor rax,rax           ; return 0
    pop rbp
    ret
```

### Execution

1. **Opening**: `fopen` creates `Grace_kid.s` in write mode
2. **Writing**: `fprintf` writes the complete code to the file (same as printf in Colleen)
3. **Closing**: `fclose` closes the file
4. **Result**: The file `Grace_kid.s` is identical to `Grace.s`

### Differences with Colleen
- Uses `fprintf` instead of `printf`
- Writes to file instead of stdout
- Uses `r12` to save the file pointer (callee-saved register)

### Project Requirements
- ✅ 1 comment
- ✅ Simulated macro definition (string variables in .data)
- ✅ Does not execute itself

---

## Sully.s - Recursive Quine

### Description
Generates a chain of recursive quines that self-replicate and execute, decrementing a counter with each generation until reaching 0.

### Code Structure

#### section .data
```nasm
s: db "section .data%1$c...",0            ; Complete code
fmt: db "Sully_%d.s",0                    ; Format for filename
mode: db "w",0                            ; Write mode
cmd: db "nasm -f elf64 Sully_%d.s && gcc -no-pie Sully_%d.o -o Sully_%d && ./Sully_%d",0
```

#### section .bss
```nasm
filename: resb 32      ; Buffer para "Sully_X.s"
cmdbuf: resb 256       ; Buffer para comando de compilación
```

#### section .text - main
```nasm
main:
    push rbp
    mov rbp,rsp
    push r12              ; Guardar r12 (file pointer)
    push r15              ; Guardar r15 (contador i)
    sub rsp,32            ; Alinear stack a 16 bytes
    
    mov r15d,5            ; Inicializar contador i=5
    cmp r15d,0
    jl .end               ; If i < 0, exit
```

### Execution Phases

#### Phase 1: Generate filename
```nasm
    lea rdi,[filename]
    lea rsi,[fmt]         ; "Sully_%d.s"
    mov rdx,r15           ; i
    xor rax,rax
    call sprintf          ; filename = "Sully_5.s"
```

#### Phase 2: Write the quine with decremented counter
```nasm
    ; Open file
    lea rdi,[filename]
    lea rsi,[mode]
    call fopen
    mov r12,rax
    
    ; Write with fprintf(f, s, 10, 9, i-1, 34, s)
    mov rdi,r12           ; file pointer
    lea rsi,[s]           ; format
    mov rdx,10            ; %1$c = newline
    mov rcx,9             ; %2$c = tab
    mov r8,r15
    dec r8                ; %3$d = i-1 (DECREMENT!)
    lea r9,[s]            ; arg6: %4$s = address of string s
    xor rax,rax
    call fprintf
    add rsp,16            ; Clean stack
    
    mov rdi,r12
    call fclose
```

**Key**: The `dec r8` instruction decrements the counter before passing it as an argument. Thus:
- `Sully.s` has `i=5` and generates `Sully_5.s` with `i=4`
- `Sully_5.s` has `i=4` and generates `Sully_4.s` with `i=3`
- And so on...

#### Phase 3: Compile and Execute (if i > 0)
```nasm
    cmp r15d,0
    jle .end              ; If i <= 0, do not execute
    
    ; Build command
    lea rdi,[cmdbuf]
    lea rsi,[cmd]
    mov rdx,r15           ; i (4 times in the command)
    mov rcx,r15
    mov r8,r15
    mov r9,r15
    xor rax,rax
    call sprintf
    
    ; Execute
    lea rdi,[cmdbuf]
    call system           ; This starts the recursion
    
.end:
    xor rax,rax
    leave                 ; mov rsp,rbp; pop rbp
    ret
```

### Execution Chain

```
Sully (i=5)
  ├─> generates Sully_5.s (i=4)
  └─> compiles and executes Sully_5
        ├─> generates Sully_4.s (i=3)
        └─> compiles and executes Sully_4
              ├─> generates Sully_3.s (i=2)
              └─> compiles and executes Sully_3
                    ├─> generates Sully_2.s (i=1)
                    └─> compiles and executes Sully_2
                          ├─> generates Sully_1.s (i=0)
                          └─> compiles and executes Sully_1
                                ├─> generates Sully_0.s (i=-1)
                                └─> does NOT execute (i=0)
```

### Generated Files

A total of **11 files** (not counting .o):
- `Sully_5.s` through `Sully_0.s` → 6 .s files
- `Sully_5` through `Sully_1` → 5 executable binaries
- (`Sully_0.s` is not compiled because `i=0` triggers `jle .end`)

### Project Requirements
- ✅ Initial counter `i=5`
- ✅ Decrements in each iteration
- ✅ Stops when `i=0`
- ✅ Generates exactly 13 total files (including intermediate .o files)

---

## Technical Details

### Positional Arguments in printf/fprintf

The `%N$X` format allows:
- **N**: Argument number (1-indexed)
- **X**: Format type (`c`, `s`, `d`, etc.)

Example:
```nasm
; printf("%1$c %2$s %1$c", 10, "hello")
; Result: "\n hello \n"
```

Advantage for quines: Reuse the same argument multiple times.

### Stack Alignment

On x64, the stack must be 16-byte aligned before `call`:
```nasm
push rbp        ; rsp -= 8 (now misaligned)
mov rbp,rsp
push r12        ; rsp -= 8 (aligned)
push r15        ; rsp -= 8 (misaligned)
sub rsp,32      ; rsp -= 32 (aligned again)
```

When passing a 7th argument on the stack:
```nasm
sub rsp,8       ; Pre-align
push rax        ; Place argument
call fprintf    ; rsp is 16-byte aligned
add rsp,16      ; Clean (8+8)
```

### Registers Used

- **r12**: File pointer (callee-saved, preserved between calls)
- **r15**: Counter `i` in Sully (callee-saved)
- **rax**: Return value of functions, also nullified (`xor rax,rax`) to indicate 0 vararg arguments in vararg calls

### C Library Functions

| Function | Purpose | Arguments |
|----------|---------|-----------|
| `printf` | Print to stdout | rdi=format, rsi...=args |
| `fprintf` | Print to file | rdi=FILE*, rsi=format, rdx...=args |
| `fopen` | Open file | rdi=name, rsi=mode |
| `fclose` | Close file | rdi=FILE* |
| `sprintf` | Format to string | rdi=buffer, rsi=format, rdx...=args |
| `system` | Execute command | rdi=command |

### Placeholders in String s

The string `s` encodes:
- **Code structure**: `section .data`, `section .text`, etc.
- **Declarations**: `global main`, `extern printf`, etc.
- **Instructions**: `push rbp`, `mov rbp,rsp`, etc.
- **All separated by**: `%1$c` (newlines) and `%2$c` (tabs)

Example fragment of `s` in Colleen:
```
"section .data%1$c%2$cs: db %3$c%4$s%3$c,0%1$c%1$csection .text%1$c..."
```

When executed with arguments (10, 9, 34, s):
```nasm
section .data
	s: db "...",0

section .text
...
```

---

## Verificación de Funcionamiento

### Colleen
```bash
./Colleen > tmp_colleen
diff Colleen.s tmp_colleen
# No debería haber diferencias
```

### Grace
```bash
./Grace
diff Grace.s Grace_kid.s
# No debería haber diferencias
```

### Sully
```bash
./Sully
ls Sully_*
# Should show:
# Sully_0.s, Sully_1, Sully_1.s, Sully_2, Sully_2.s, ... Sully_5, Sully_5.s
```

---

## Key Concepts for Understanding Quines

1. **Self-reference**: The string `s` passes itself as an argument
2. **Positional formatting**: Allows using the same argument multiple times
3. **Careful encoding**: All code must be in `s`, including the definition of `s`
4. **Perfect balance**: The format and arguments must produce exactly the original code

## Additional Resources

- [x64 System V Calling Convention](https://wiki.osdev.org/System_V_ABI)
- [NASM Documentation](https://www.nasm.us/xdoc/2.15.05/html/nasmdoc0.html)
- [Printf format specifiers](https://en.cppreference.com/w/c/io/fprintf)
- [Quine (computing) - Wikipedia](https://en.wikipedia.org/wiki/Quine_(computing))

---

**Author**: dr-quine Assembly implementation  
**Fecha**: 2026  
**Assembler**: NASM 2.16+  
**Arquitectura**: x86_64 Linux
