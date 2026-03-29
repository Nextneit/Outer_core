# Level 1 — Reverse Engineering

## Objetivo

Encontrar la clave que acepta el binario `level1` y reconstruir su código fuente.

---

## 1. Reconocimiento inicial

```bash
file level1
```
- ELF 32-bit, PIE (direcciones aleatorias en cada ejecución), no stripped.

```bash
strings level1
```
- Se observan los mensajes `Please enter key:`, `Good job.` y `Nope.`
- También aparece `strcmp`, `scanf` y `printf` → el binario lee un input y lo compara con una clave.

---

## 2. Análisis con GDB

### Listar funciones
```bash
(gdb) info functions
```
La función relevante es `main` en `0x11c0`.

### Desensamblar main
```bash
(gdb) disas main
```
El flujo es:
1. Copia la clave hardcodeada desde el segmento de datos a la stack.
2. Llama a `printf` para mostrar el prompt.
3. Llama a `scanf` para leer el input del usuario.
4. Llama a `strcmp` para comparar input con la clave.
5. Salta a `Good job.` o `Nope.` según el resultado.

### Capturar la clave en runtime
```bash
(gdb) break strcmp
(gdb) run
# Introducir cualquier texto cuando pida la clave
(gdb) x/8wx $esp
```

Los punteros en el stack apuntan a los dos argumentos del `strcmp`. Inspeccionando:
```bash
(gdb) x/s 0xffffc1fc   # → input del usuario
(gdb) x/s 0xffffc1ee   # → "__stack_check"  ← la clave real
```

---

## 3. La clave

```
__stack_check
```

Un nombre que imita una función interna del sistema operativo — técnica de ofuscación para despistar al analista.

```bash
./level1
Please enter key: __stack_check
Good job.
```

---

## 4. Código fuente reconstruido

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char key[] = "__stack_check";
    char input[100];

    printf("Please enter key: ");
    scanf("%s", input);

    if (strcmp(input, key) == 0)
        printf("Good job.\n");
    else
        printf("Nope.\n");

    return 0;
}
```

### Verificación
```bash
gcc -Wall -Werror -Wextra -O0 -fPIE -pie source.c -o source_rebuilt
gdb ./source_rebuilt -ex "disas main" -ex quit
```
El flujo del disassembly reconstruido es equivalente al original:
`printf → scanf → strcmp → jne → Good job / Nope`

---

## Resumen de comandos clave

| Comando | Propósito |
|---|---|
| `file level1` | Identificar arquitectura y tipo de binario |
| `strings level1` | Buscar strings embebidos |
| `disas main` | Entender el flujo del programa |
| `break strcmp` | Parar justo antes de la comparación |
| `x/8wx $esp` | Volcar el stack para ver los punteros |
| `x/s <dirección>` | Leer un string en una dirección de memoria |