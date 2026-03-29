# Level 2 — Reverse Engineering

## Objetivo

Encontrar la clave que acepta el binario `level2` y reconstruir su código fuente.

---

## 1. Reconocimiento inicial

```bash
file level2
```
- ELF 32-bit, PIE, no stripped. Misma arquitectura que level1.

```bash
strings level2
```
Pistas relevantes extraídas:
- `delabere` → string sospechoso, posible clave objetivo
- `%23s` → formato scanf con límite de 35 chars (`0x23 = 35`)
- `atoi`, `strlen`, `memset` → manipulación y conversión de strings
- Texto en latín extenso → ruido para despistar
- Funciones con nombres sin sentido: `no`, `xd`, `ok`, `xxd`, `n`, `xxxd`, `ww`, `xyxxd`

```bash
(gdb) info functions
```
Funciones relevantes: `main`, `ok` (rama "Good job"), `no` (rama "Nope" + exit).

---

## 2. Análisis con GDB

### Desensamblar main

```bash
(gdb) disas main
```

El flujo de `main` se divide en tres bloques:

---

### Bloque 1 — Validación del formato del input

```asm
scanf(...)              → guarda nº de items leídos en -0xc(%ebp)
cmp $0x1, -0xc(%ebp)   → ¿scanf leyó exactamente 1 item?
jne → no()             → si no, termina

cmp $0x30, -0x34(%ebp) → ¿primer char == '0'?
jne → no()

cmp $0x30, -0x35(%ebp) → ¿segundo char == '0'?
jne → no()
```

**Conclusión**: el input debe empezar obligatoriamente con `00`.

---

### Bloque 2 — Bucle de decodificación decimal → ASCII

```asm
movb $0x64, -0x1d(%ebp)   → buffer[0] = 'd' (hardcodeado)
movl $0x2,  -0x14(%ebp)   → i = 2  (salta el prefijo "00")
movl $0x1,  -0x10(%ebp)   → j = 1  (posición en buffer, empieza en 1)

; Condición del bucle:
strlen(buffer) < 8  → continuar

; Cuerpo:
input[i..i+2]  → 3 dígitos consecutivos del input
atoi(input+i)  → convierte esos 3 dígitos a un entero
buffer[j] = resultado  → guarda el byte en el buffer
i += 3
j += 1
```

El bucle lee el input de **3 en 3 dígitos** y convierte cada grupo a su valor ASCII, construyendo el buffer byte a byte.

---

### Bloque 3 — Comparación final

```asm
strcmp(buffer, "delabere")
jne → no()
je  → ok()
```

El buffer construido debe ser igual a `"delabere"`.

---

## 3. Construcción de la clave

El buffer se forma así:

| Origen | Valor | Char |
|--------|-------|------|
| Hardcodeado | `0x64` | `d` |
| `atoi("101")` | 101 | `e` |
| `atoi("108")` | 108 | `l` |
| `atoi("097")` | 97 | `a` |
| `atoi("098")` | 98 | `b` |
| `atoi("101")` | 101 | `e` |
| `atoi("114")` | 114 | `r` |
| `atoi("101")` | 101 | `e` |

**La clave es:**
```
00101108097098101114101
```

```bash
./level2
Please enter key: 00101108097098101114101
Good job.
```

---

## 4. Código fuente reconstruido

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void no(void)
{
    puts("Nope.");
    exit(1);
}

void ok(void)
{
    puts("Good job.");
}

int main(void)
{
    char    input[36];
    char    buffer[9];
    char    tmp[4];
    int     i;
    int     j;

    printf("Please enter key: ");
    if (scanf("%35s", input) != 1)
        no();

    if (input[0] != '0' || input[1] != '0')
        no();

    memset(buffer, 0, 9);
    buffer[0] = 'd';
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

    if (strcmp(buffer, "delabere") != 0)
        no();
    ok();
    return (0);
}
```

---

## 5. Técnicas de ofuscación usadas

| Técnica | Descripción |
|---------|-------------|
| Nombres de funciones sin sentido | `xd`, `ww`, `xyxxd`, `xxxd`... para dificultar la lectura del CFG |
| Texto en latín extenso | Relleno en el segmento de datos para confundir `strings` |
| Codificación decimal | La clave no es legible directamente, requiere decodificar grupos de 3 dígitos |
| Primer byte hardcodeado | `'d'` se inserta directamente en el buffer, no viene del input |
| Prefijo obligatorio `00` | Validación extra que filtra inputs sin formato correcto |