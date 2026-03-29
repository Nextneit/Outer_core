# Level 3 — Reverse Engineering

## Objetivo

Encontrar la clave que acepta el binario `level3` y reconstruir su código fuente.

---

## 1. Reconocimiento inicial

```bash
file level3
```
- ELF **64-bit**, PIE, no stripped. Primera vez en 64-bit → convención de llamada distinta (argumentos en registros `rdi`, `rsi`, `rdx`... en lugar del stack).

```bash
strings level3
```
Pistas relevantes:
- `********` → 8 asteriscos, posible clave objetivo (`0x2a = 42` en decimal)
- `nice`, `this`, `not.`, `that.`, `easy.` → mensajes o nombres de funciones
- `%23s` → scanf con límite de 35 chars
- `atoi`, `strlen`, `memset`, `strcmp` → misma maquinaria que level2
- `___syscall_malloc` y `____syscall_malloc` → nombres falsos para ocultar las ramas ok/no

```bash
(gdb) info functions
```
Funciones con nombres de palabras: `wt`, `nice`, `try`, `but`, `this`, `it`, `not`, `that`, `easy` → ruido. Las relevantes son `___syscall_malloc` (Nope + exit) y `____syscall_malloc` (Good job).

---

## 2. Análisis con GDB

### Desensamblar main

```bash
(gdb) disas main
```

El flujo se divide en tres bloques:

---

### Bloque 1 — Validación del prefijo

```asm
cmp $0x34, -0x40(%rbp)   → input[0] == '4'  (0x34 = ASCII '4')
cmp $0x32, -0x3f(%rbp)   → input[1] == '2'  (0x32 = ASCII '2')
```

El input debe empezar obligatoriamente con `42`.

---

### Bloque 2 — Bucle de decodificación decimal → ASCII

Idéntico al de level2:

```asm
movb $0x2a, -0x21(%rbp)   → buffer[0] = '*' (0x2a = 42, hardcodeado)
movq $0x2,  -0x18(%rbp)   → i = 2  (salta el prefijo "42")
movl $0x1,  -0xc(%rbp)    → j = 1

; Condición: strlen(buffer) < 8 → continuar

; Cuerpo:
input[i..i+2]   → 3 dígitos consecutivos
atoi(input+i)   → convierte a byte
buffer[j] = resultado
i += 3
j += 1
```

El primer byte `'*'` (`0x2a = 42`) está hardcodeado. Los 7 restantes se decodifican del input de 3 en 3 dígitos.

---

### Bloque 3 — strcmp + switch ofuscado

```asm
strcmp(buffer, "********")   → compara con 8 asteriscos
resultado → -0x54(%rbp)

switch (resultado):
  -2  → ___syscall_malloc   (Nope)
  -1  → ___syscall_malloc   (Nope)
   0  → ____syscall_malloc  (Good job) ← único caso de éxito
   1  → ___syscall_malloc   (Nope)
   2  → ___syscall_malloc   (Nope)
   3  → ___syscall_malloc   (Nope)
   4  → ___syscall_malloc   (Nope)
   5  → ___syscall_malloc   (Nope)
 115  → ___syscall_malloc   (Nope)
```

En lugar de un simple `if/else`, el resultado del `strcmp` pasa por un switch con 9 casos. Solo `resultado == 0` llama a `____syscall_malloc` (4 guiones bajos = "Good job"). Todos los demás llaman a `___syscall_malloc` (3 guiones bajos = "Nope" + exit).

---

## 3. Construcción de la clave

El buffer debe ser `"********"` (8 asteriscos):

| Origen | Decimal | ASCII |
|--------|---------|-------|
| Hardcodeado `0x2a` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |
| `atoi("042")` | 42 | `*` |

El prefijo `42` también es el valor decimal de `*` — todo coherente.

**La clave es:**
```
42042042042042042042042
```

```bash
./level3
Please enter key: 42042042042042042042042
Good job.
```

---

## 4. Código fuente reconstruido

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void    ___syscall_malloc(void)
{
    puts("Nope.");
    exit(1);
}

void    ____syscall_malloc(void)
{
    puts("Good job.");
}

int     main(void)
{
    char    input[36];
    char    buffer[9];
    char    tmp[4];
    int     result;
    int     j;
    long    i;

    printf("Please enter key: ");
    if (scanf("%35s", input) != 1)
        ___syscall_malloc();

    if (input[0] != '4' || input[1] != '2')
        ___syscall_malloc();

    memset(buffer, 0, 9);
    buffer[0] = '*';
    tmp[3] = '\0';

    i = 2;
    j = 1;
    while (strlen(buffer) < 8)
    {
        tmp[0] = input[i];
        tmp[1] = input[i + 1];
        tmp[2] = input[i + 2];
        buffer[j] = (char)atoi(tmp);
        i += 3;
        j += 1;
    }
    buffer[j] = '\0';

    result = strcmp(buffer, "********");
    switch (result)
    {
        case -2:    ___syscall_malloc(); break;
        case -1:    ___syscall_malloc(); break;
        case  0:    ____syscall_malloc(); break;
        case  1:    ___syscall_malloc(); break;
        case  2:    ___syscall_malloc(); break;
        case  3:    ___syscall_malloc(); break;
        case  4:    ___syscall_malloc(); break;
        case  5:    ___syscall_malloc(); break;
        case  115:  ___syscall_malloc(); break;
        default:    ___syscall_malloc(); break;
    }
    return (0);
}
```

---

## 5. Diferencias respecto a level2

| Aspecto | Level 2 | Level 3 |
|---------|---------|---------|
| Arquitectura | 32-bit (x86) | 64-bit (x86-64) |
| Convención de llamada | Argumentos en stack | Argumentos en registros |
| Prefijo obligatorio | `00` | `42` |
| Primer byte hardcodeado | `'d'` (0x64) | `'*'` (0x2a) |
| Clave objetivo | `"delabere"` | `"********"` |
| Rama de éxito | `ok()` / `no()` | Switch con 9 casos, solo `case 0` llama a "Good job" |
| Ofuscación extra | Nombres sin sentido | Nombres de funciones sistema falsos con distinto número de `_` |