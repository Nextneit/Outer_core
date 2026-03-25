# Dr-Quine - C Implementation

This directory contains the C implementation of the **dr-quine** project from School 42. A **quine** is a program that prints its own source code without reading any external file.

## Index
- [Compilation and Execution](#compilation-and-execution)
- [Fundamental Concepts](#fundamental-concepts)
- [Colleen.c - Basic Quine](#colleenc---basic-quine)
- [Grace.c - Quine with Macros](#gracec---quine-with-macros)
- [Sully.c - Recursive Quine](#sullyc---recursive-quine)
- [Advanced Techniques](#advanced-techniques)

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
make clean    # Clean binaries
make fclean   # Complete cleanup
```

---

## Fundamental Concepts

### What is a Quine?

A quine is a program that produces its own source code as output, **without**:
- Reading files (no `fopen`, `read`, etc.)
- Using `argv[0]` or system information
- Using compiler or debugger tricks
- Cheating in any form

### Project Constraints

Each program must satisfy:
- **Colleen**: 2 comments (one external, one internal) + 1 helper function
- **Grace**: 1 comment + exactly 3 macros (#define) + NO explicit main
- **Sully**: Create exactly 13 files (Sully + 6 .c files + 6 binaries)

### Key Technique: Printf with Positional Arguments

The fundamental technique is using `printf` with **positional arguments**:

```c
printf("%1$c %2$s %1$c", 10, "hello");
// Output: "\n hello \n"
```

**Advantages**:
- `%N$X` allows referring to the N-th argument
- You can reuse the same argument multiple times
- Essential for self-reference in quines

### Key Values

| Value | Character | Usage |
|-------|-----------|-------|
| `10` | `\n` | Newline |
| `9` | `\t` | Tab |
| `34` | `"` | Double quote |

These values allow avoiding escape characters in the encoded string.

---

## Colleen.c - Basic Quine

### Description
Prints its own source code to **stdout** using a helper function.

### Complete Code
```c
/*
	Outer comment
*/

#include <stdio.h>

void ft(){
	// Inner comment in function
	char*s="/*%1$c%2$cOuter comment%1$c*/%1$c%1$c#include <stdio.h>%1$c%1$cvoid ft(){%1$c%2$c// Inner comment in function%1$c%2$cchar*s=%3$c%4$s%3$c;%1$c%2$cprintf(s,10,9,34,s);%1$c}%1$c%1$cint main(){%1$c%2$c/* Inner comment in main */%1$c%2$cft();%1$c%2$creturn 0;%1$c}%1$c";
	printf(s,10,9,34,s);
}

int main(){
	/* Inner comment in main */
	ft();
	return 0;
}
```

### Detailed Analysis

#### Structure
- **External comment**: `/* Outer comment */`
- **Function comment**: `// Inner comment in function`
- **Main comment**: `/* Inner comment in main */`
- **Helper function**: `ft()` that performs the printing

#### The String `s`

The string `s` contains **the entire program code** encoded with placeholders:

```c
char*s="/*%1$c%2$cOuter comment%1$c*/...";
```

**Placeholders**:
- `%1$c` → argument 1 → `10` → newline (`\n`)
- `%2$c` → argument 2 → `9` → tab (`\t`)
- `%3$c` → argument 3 → `34` → double quote (`"`)
- `%4$s` → argument 4 → `s` → string s content (self-reference)

#### Step-by-Step Execution

1. **String definition**: `s` contains the code with placeholders
2. **Printf call**:
   ```c
   printf(s,10,9,34,s);
   ```
   - `s` is the format string
   - `10` replaces `%1$c` (newlines)
   - `9` replaces `%2$c` (tabs)
   - `34` replaces `%3$c` (quotes)
   - `s` replaces `%4$s` (entire string)

3. **Self-reference**: When printf sees `%4$s`, it inserts the content of `s`, which includes the definition `char*s="..."`

4. **Result**: The complete code with its original format

### Expansion Example

Simplified fragment:
```c
"char*s=%3$c%4$s%3$c;"
```

Con argumentos `(10,9,34,s)` se expande a:
```c
char*s="[contenido de s]";
```

### Requirements Met
- ✅ 2 comments (outer and inner)
- ✅ 1 helper function (`ft()`)
- ✅ Complete code reproduced exactly

## Grace.c - Quine with Macros

### Description
Writes its source code to **Grace_kid.c** using **only macros** (without visible main function).

### Complete Code
```c
/*Comment*/
#include<stdio.h>

#define S "/*Comment*/%1$c#include<stdio.h>%1$c%1$c#define S %2$c%3$s%2$c%1$c#define F {FILE*f=fopen(%2$cGrace_kid.c%2$c,%2$cw%2$c);fprintf(f,S,10,34,S);fclose(f);}%1$c#define M int main(){F return 0;}%1$cM%1$c"
#define F {FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);}
#define M int main(){F return 0;}
M
```

### Analysis of Macros

#### Macro S - Code String
```c
#define S "/*Comment*/%1$c#include<stdio.h>%1$c..."
```
- Contains the entire program code encoded
- Uses `%1$c` for newline (10) and `%2$c` for quote (34)
- `%3$s` self-references to macro S itself

#### Macro F - Functionality
```c
#define F {FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);}
```
This macro:
1. Opens the file `Grace_kid.c` in write mode
2. Writes the code using `fprintf` with string `S`
3. Closes the file

The fprintf arguments:
- `S` → format (the string with placeholders)
- `10` → `%1$c` (newline)
- `34` → `%2$c` (double quotes)
- `S` → `%3$s` (the macro S content)

#### Macro M - Implicit Main
```c
#define M int main(){F return 0;}
```
- Defines the `main` function as a macro
- Executes macro `F` (which writes the file)
- Returns 0

#### Invocation
```c
M
```
This single line:
1. Expands macro `M`
2. Which creates `int main()`
3. Which executes `F`
4. Which writes the quine to `Grace_kid.c`

### Execution Flow

```
Compiler sees: M
              ↓
Expands to: int main(){F return 0;}
              ↓
Expands F: int main(){{FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);} return 0;}
              ↓
Executes: opens Grace_kid.c
              ↓
fprintf uses S as format with args (10,34,S)
              ↓
Grace_kid.c contains the complete code
```

### Unique Technique: Hidden Main

Grace **does not have a visible `int main()`** in the source code. Everything is done through macros:
- `#define M` creates the main
- `M` at the end invokes it
- This satisfies the requirement of using only macros

### Requirements Met
- ✅ 1 comment (`/*Comment*/`)
- ✅ Exactly 3 macros (#define S, F, M)
- ✅ No visible main function (it's in a macro)
- ✅ Grace_kid.c is identical to Grace.c

---

## Sully.c - Recursive Quine

### Description
Generates a chain of quines that self-replicate, compile and execute, decrementing a counter with each generation.

### Complete Code
```c
#include<stdio.h>
#include<stdlib.h>

int main(){
	int i=5;
	char*s="#include<stdio.h>%1$c#include<stdlib.h>%1$c%1$cint main(){%1$c%2$cint i=%3$d;%1$c%2$cchar*s=%4$c%5$s%4$c;%1$c%2$cchar f[32],c[128];%1$c%1$c%2$cif(i<0)%1$c%2$c%2$creturn 0;%1$c%2$csprintf(f,%4$cSully_%%d.c%4$c,i);%1$c%2$cFILE*fp=fopen(f,%4$cw%4$c);%1$c%2$cfprintf(fp,s,10,9,i-1,34,s);%1$c%2$cfclose(fp);%1$c%2$cif(i>0){%1$c%2$c%2$csprintf(c,%4$cgcc -Wall -Wextra -Werror Sully_%%d.c -o Sully_%%d && ./Sully_%%d%4$c,i,i,i);%1$c%2$c%2$csystem(c);%1$c%2$c}%1$c%2$creturn 0;%1$c}%1$c";
	char f[32],c[128];

	if(i<0)
		return 0;
	sprintf(f,"Sully_%d.c",i);
	FILE*fp=fopen(f,"w");
	fprintf(fp,s,10,9,i-1,34,s);
	fclose(fp);
	if(i>0){
		sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
		system(c);
	}
	return 0;
}
```

### Line-by-Line Analysis

#### Main Variables
```c
int i=5;                    // Initial counter
char*s="...";               // String with all the code
char f[32],c[128];          // Buffers for filename and command
```

#### Phase 1: Validation
```c
if(i<0)
	return 0;
```
If the counter is negative, exit (although with initial `i=5` this never happens on first run).

#### Phase 2: File Generation
```c
sprintf(f,"Sully_%d.c",i);
```
Creates the filename: `Sully_5.c`, `Sully_4.c`, etc.

```c
FILE*fp=fopen(f,"w");
fprintf(fp,s,10,9,i-1,34,s);
fclose(fp);
```

**KEY**: The fprintf arguments are:
- `fp` → file pointer
- `s` → format with placeholders
- `10` → `%1$c` (newline)
- `9` → `%2$c` (tab)
- `i-1` → `%3$d` (**decremented counter**)
- `34` → `%4$c` (quotes)
- `s` → `%5$s` (the complete string)

The `i-1` is crucial: it writes the code with a reduced counter.

#### Phase 3: Compilation and Execution (Recursion)
```c
if(i>0){
	sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
	system(c);
}
```

If `i > 0`:
1. Builds the compilation command
2. Compiles `Sully_X.c` → `Sully_X`
3. Executes `./Sully_X` (which has `i` decremented)

### Complete Execution Chain

```
Sully (i=5)
  ├─> creates Sully_5.c (with i=4)
  ├─> compiles Sully_5.c → Sully_5
  └─> executes ./Sully_5
        ├─> creates Sully_4.c (with i=3)
        ├─> compiles Sully_4.c → Sully_4
        └─> executes ./Sully_4
              ├─> creates Sully_3.c (with i=2)
              ├─> compiles Sully_3.c → Sully_3
              └─> executes ./Sully_3
                    ├─> creates Sully_2.c (with i=1)
                    ├─> compiles Sully_2.c → Sully_2
                    └─> executes ./Sully_2
                          ├─> creates Sully_1.c (with i=0)
                          ├─> compiles Sully_1.c → Sully_1
                          └─> executes ./Sully_1
                                ├─> creates Sully_0.c (with i=-1)
                                └─> does NOT compile (i=0, skips if)
```

### Generated Files

Total: **13 files**

| File | Description | Counter i |
|------|-------------|-----------|
| `Sully` | Original binary | `i=5` |
| `Sully.c` | Original source code | `i=5` |
| `Sully_5.c` | Generated by Sully | `i=4` |
| `Sully_5` | Compiled binary | `i=4` |
| `Sully_4.c` | Generated by Sully_5 | `i=3` |
| `Sully_4` | Compiled binary | `i=3` |
| `Sully_3.c` | Generated by Sully_4 | `i=2` |
| `Sully_3` | Compiled binary | `i=2` |
| `Sully_2.c` | Generated by Sully_3 | `i=1` |
| `Sully_2` | Compiled binary | `i=1` |
| `Sully_1.c` | Generated by Sully_2 | `i=0` |
| `Sully_1` | Compiled binary | `i=0` |
| `Sully_0.c` | Generated by Sully_1 | `i=-1` |

**Note**: `Sully_0.c` is created but NOT compiled because the `if(i>0)` prevents it.

### Differences Between Generations

Each file `Sully_X.c` is **almost identical** to the previous one, only changes:

```c
// In Sully_5.c
int i=4;

// In Sully_4.c
int i=3;

// etc.
```

### Why It Stops

1. `Sully_1` has `i=0`
2. Executes `fprintf(fp,s,10,9,i-1,34,s)` → creates `Sully_0.c` with `i=-1`
3. The `if(i>0)` is **false** → does not compile or execute
4. Returns 0 → end of recursion

### Requirements Met
- ✅ Initial counter `i=5`
- ✅ Decrements in each generation
- ✅ Stops when `i=0` (does not execute `Sully_0`)
- ✅ Generates exactly 13 files

## Advanced Techniques

### 1. Positional Printf Formatting

The `%N$X` format allows:
```c
printf("%2$s says %1$d times", 3, "hello");
// Result: "hello says 3 times"
```

**For quines**:
```c
printf("%1$c%2$c%3$c%1$c", 10, 9, 65);
// Result: "\n\tA\n"
```

Reusing arguments is essential for self-reference.

### 2. String with Double Escaping

In string `s`, some characters need special escaping:

- `%%` → Single literal `%`
- `%1$c` → Placeholder to be substituted
- `Sully_%%d.c` → In output becomes `Sully_%d.c`

Example:
```c
char*s="sprintf(f,%4$cSully_%%d.c%4$c,i);";
```

When printed with argument `34` (quote):
```c
sprintf(f,"Sully_%d.c",i);
```

### 3. Careful Self-Reference

The trick is that `s` passes itself as an argument:

```c
printf(s, ..., s);
      ↑       ↑
   format   data
```

Inside `s`, there's a `%4$s` (or `%5$s` in Sully) that receives the content of `s`.

### 4. Buffer for System()

In Sully, the command is complex:
```c
sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
```

This builds:
```bash
gcc -Wall -Wextra -Werror Sully_5.c -o Sully_5 && ./Sully_5
```

The `&&` ensures execution only if compilation succeeds.

### 5. File Management

Common pattern:
```c
FILE*fp=fopen(filename,"w");
fprintf(fp, format, ...);
fclose(fp);
```

**Important**: Always close with `fclose()` to ensure the buffer is written to disk before `system()` tries to compile the file.

---

## Comparison with Assembly Version

| Aspect | C | Assembly |
|--------|---|----------|
| **Syntax** | More readable | More verbose |
| **Arguments** | `printf(s,10,9,34,s)` | Registers `rdi,rsi,rdx,rcx,r8` |
| **String** | Literal with escapes | `db` in `.data` section |
| **Stack** | Handled automatically | Manual with `push`/`pop` |
| **Compilation** | `gcc` | `nasm` + `gcc` |
| **Complexity** | Medium | High |

---

## Debugging Quines

### Verify Colleen
```bash
./Colleen > output.c
diff Colleen.c output.c
# No differences should exist
```

### Verify Grace
```bash
./Grace
diff Grace.c Grace_kid.c
# No differences should exist
```

### Verify Sully
```bash
./Sully
ls -1 Sully*
# Should list 13 files

# Verify content
diff <(cat Sully.c | sed 's/int i=5/int i=4/') Sully_5.c
# No differences except the counter
```

### Common Errors

1. **Whitespace differences**:
   - Check tabs vs spaces
   - Check newlines at end of file

2. **Quote issues**:
   - Use `%3$c` with argument `34`
   - Don't try to escape with `\"`

3. **Positional arguments**:
   - Verify `%N$X` uses correct index
   - Remember they are 1-indexed (not 0-indexed)

4. **Buffer overflow in Sully**:
   - `char f[32]` must be sufficient for `Sully_X.c`
   - `char c[128]` must be sufficient for the complete command

---

## Theoretical Concepts

### Kleene's Recursion Theorem

Quines are possible because of **Kleene's recursion theorem**, which states:
> For any computable function f, there exists a program p such that p produces f(p) as output.

In a quine, f is the identity function, so p produces p.

### The Quine Paradox

How can a program describe itself without reading itself?

**Answer**: By using a data structure that describes itself on two levels:
1. **Code**: "Print X in quotes, then X"
2. **Data X**: "Print X in quotes, then X"

### Applications

Quines are not just theoretical exercises:
- **Computer viruses**: Self-replicating viruses are quine variants
- **Bootstrapping compilers**: Compiler that compiles itself
- **Computation theory**: Demonstration of Turing-completeness properties

---

## Additional Resources

- [Printf format specifiers (C Reference)](https://en.cppreference.com/w/c/io/fprintf)
- [Quine (computing) - Wikipedia](https://en.wikipedia.org/wiki/Quine_(computing))
- [The Quine Page](http://www.nyx.net/~gthompso/quine.htm)
- [42 Project Guide](https://github.com/agavrel/42_CheatSheet)

---

## Tips for Creating Quines

1. **Start with the basic structure**:
   ```c
   char*s="...";
   printf(s, args...);
   ```

2. **Identify what you need to print**:
   - All code before `s`
   - The declaration of `s` with quotes
   - All code after `s`

3. **Encode with placeholders**:
   - `%1$c` for newlines
   - `%2$c` for tabs
   - `%3$c` for quotes
   - `%N$s` for self-reference

4. **Verify step by step**:
   - Print only one part first
   - Verify that spacing is correct
   - Add the rest gradually
   - Asegúrate de que cada `%N$X` tenga su argumento correspondiente
   - No olvides el argumento de auto-referencia al final

---

**Autor**: dr-quine C implementation  
**Fecha**: 2026  
**Compilador**: gcc 11+ con flags -Wall -Wextra -Werror  
**Standard**: C99+
