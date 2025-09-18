# LibASM - Assembly Library Implementation

![Assembly](https://img.shields.io/badge/Assembly-x86_64-blue)
![NASM](https://img.shields.io/badge/Assembler-NASM-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)
![Status](https://img.shields.io/badge/Status-Complete-success)

## 📋 Project Overview

LibASM is a complete implementation of standard C library functions written entirely in x86_64 assembly language using NASM. This project recreates essential string manipulation and I/O functions, providing a deep understanding of low-level programming and system calls.

### 🎯 Implemented Functions

| Function | Description | Status |
|----------|-------------|--------|
| `ft_strlen` | Calculate string length | ✅ Complete |
| `ft_strcpy` | Copy string from source to destination | ✅ Complete |
| `ft_strcmp` | Compare two strings lexicographically | ✅ Complete |
| `ft_write` | Write data to file descriptor | ✅ Complete |
| `ft_read` | Read data from file descriptor | ✅ Complete |
| `ft_strdup` | Duplicate string (with malloc) | ✅ Complete |

### 🔧 Technical Specifications

- **Architecture**: x86_64
- **Assembler**: NASM (Netwide Assembler)
- **Format**: ELF64
- **Calling Convention**: System V ABI
- **Platform**: Linux
- **External Dependencies**: malloc (for ft_strdup), __errno_location (for syscalls)

## 🚀 Quick Start

### Prerequisites

```bash
# Install required tools on Ubuntu/Debian
sudo apt update
sudo apt install nasm build-essential

# Verify installation
nasm --version
gcc --version
```

### Build & Test

```bash
# Clone the repository
git clone <repository-url>
cd libasm

# Build the library
make

# Test individual functions
gcc -Wall -Wextra -Werror -no-pie main_strlen.c libasm.a -o test_strlen && ./test_strlen
gcc -Wall -Wextra -Werror -no-pie main_strcpy.c libasm.a -o test_strcpy && ./test_strcpy
gcc -Wall -Wextra -Werror -no-pie main_strcmp.c libasm.a -o test_strcmp && ./test_strcmp
gcc -Wall -Wextra -Werror -no-pie main_write.c libasm.a -o test_write && ./test_write
gcc -Wall -Wextra -Werror -no-pie main_read.c libasm.a -o test_read && ./test_read
gcc -Wall -Wextra -Werror -no-pie main_strdup.c libasm.a -o test_strdup && ./test_strdup

# Clean build files
make clean      # Remove object files
make fclean     # Remove everything
make re         # Rebuild from scratch
```

## 📁 Project Structure

```
libasm/
├── ft_strlen.s        # String length calculation
├── ft_strcpy.s        # String copy operation  
├── ft_strcmp.s        # String comparison
├── ft_write.s         # Write syscall wrapper
├── ft_read.s          # Read syscall wrapper
├── ft_strdup.s        # String duplication with malloc
├── main_*.c           # Test files for each function
├── Makefile           # Build configuration
└── README.md          # This file
```

## 🔍 Function Details

### ft_strlen
Calculates the length of a null-terminated string.
```c
size_t ft_strlen(const char *s);
```

### ft_strcpy  
Copies string from source to destination including null terminator.
```c
char *ft_strcpy(char *dest, const char *src);
```

### ft_strcmp
Compares two strings lexicographically. Returns negative, zero, or positive value.
```c
int ft_strcmp(const char *s1, const char *s2);
```

### ft_write
Writes up to count bytes from buffer to file descriptor.
```c
ssize_t ft_write(int fd, const void *buf, size_t count);
```

### ft_read
Reads up to count bytes from file descriptor into buffer.
```c
ssize_t ft_read(int fd, void *buf, size_t count);
```

### ft_strdup
Creates a duplicate of the string with dynamically allocated memory.
```c
char *ft_strdup(const char *s);
```

---

# LibASM - Implementación de Biblioteca en Assembly (Español)

![Assembly](https://img.shields.io/badge/Assembly-x86_64-blue)
![NASM](https://img.shields.io/badge/Assembler-NASM-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)
![Status](https://img.shields.io/badge/Status-Completo-success)

## 📋 Resumen del Proyecto

LibASM es una implementación completa de funciones de la biblioteca estándar de C escrita enteramente en lenguaje ensamblador x86_64 usando NASM. Este proyecto recrea funciones esenciales de manipulación de strings y E/S, proporcionando una comprensión profunda de la programación de bajo nivel y llamadas al sistema.

### 🎯 Funciones Implementadas

| Función | Descripción | Estado |
|---------|-------------|--------|
| `ft_strlen` | Calcular longitud de string | ✅ Completo |
| `ft_strcpy` | Copiar string de origen a destino | ✅ Completo |
| `ft_strcmp` | Comparar dos strings lexicográficamente | ✅ Completo |
| `ft_write` | Escribir datos a descriptor de archivo | ✅ Completo |
| `ft_read` | Leer datos de descriptor de archivo | ✅ Completo |
| `ft_strdup` | Duplicar string (con malloc) | ✅ Completo |

### 🔧 Especificaciones Técnicas

- **Arquitectura**: x86_64
- **Ensamblador**: NASM (Netwide Assembler)
- **Formato**: ELF64
- **Convención de Llamada**: System V ABI
- **Plataforma**: Linux
- **Dependencias Externas**: malloc (para ft_strdup), __errno_location (para syscalls)

## 🚀 Inicio Rápido

### Requisitos Previos

```bash
# Instalar herramientas necesarias en Ubuntu/Debian
sudo apt update
sudo apt install nasm build-essential

# Verificar instalación
nasm --version
gcc --version
```

### Compilar y Probar

```bash
# Clonar el repositorio
git clone <repository-url>
cd libasm

# Compilar la biblioteca
make

# Probar funciones individuales
gcc -Wall -Wextra -Werror -no-pie main_strlen.c libasm.a -o test_strlen && ./test_strlen
gcc -Wall -Wextra -Werror -no-pie main_strcpy.c libasm.a -o test_strcpy && ./test_strcpy
gcc -Wall -Wextra -Werror -no-pie main_strcmp.c libasm.a -o test_strcmp && ./test_strcmp
gcc -Wall -Wextra -Werror -no-pie main_write.c libasm.a -o test_write && ./test_write
gcc -Wall -Wextra -Werror -no-pie main_read.c libasm.a -o test_read && ./test_read
gcc -Wall -Wextra -Werror -no-pie main_strdup.c libasm.a -o test_strdup && ./test_strdup

# Limpiar archivos de compilación
make clean      # Eliminar archivos objeto
make fclean     # Eliminar todo
make re         # Recompilar desde cero
```

## 📁 Estructura del Proyecto

```
libasm/
├── ft_strlen.s        # Cálculo de longitud de string
├── ft_strcpy.s        # Operación de copia de string  
├── ft_strcmp.s        # Comparación de strings
├── ft_write.s         # Wrapper de syscall write
├── ft_read.s          # Wrapper de syscall read
├── ft_strdup.s        # Duplicación de string con malloc
├── main_*.c           # Archivos de prueba para cada función
├── Makefile           # Configuración de compilación
└── README.md          # Este archivo
```

## 🔍 Detalles de las Funciones

### ft_strlen
Calcula la longitud de una string terminada en null.
```c
size_t ft_strlen(const char *s);
```

### ft_strcpy  
Copia string desde origen a destino incluyendo el terminador null.
```c
char *ft_strcpy(char *dest, const char *src);
```

### ft_strcmp
Compara dos strings lexicográficamente. Retorna valor negativo, cero o positivo.
```c
int ft_strcmp(const char *s1, const char *s2);
```

### ft_write
Escribe hasta count bytes desde buffer al descriptor de archivo.
```c
ssize_t ft_write(int fd, const void *buf, size_t count);
```

### ft_read
Lee hasta count bytes desde descriptor de archivo al buffer.
```c
ssize_t ft_read(int fd, void *buf, size_t count);
```

### ft_strdup
Crea un duplicado de la string con memoria asignada dinámicamente.
```c
char *ft_strdup(const char *s);
```

## 📖 Introducción

Assembly es un lenguaje de programación de bajo nivel que permite comunicarse directamente con el procesador. Esta guía te ayudará a empezar desde cero con Assembly en sistemas Linux (Ubuntu).

## 🛠️ Instalación de Herramientas

### Instalar herramientas necesarias en Ubuntu:

```bash
# Actualizar el sistema
sudo apt update

# Instalar NASM (Netwide Assembler)
sudo apt install nasm

# Instalar herramientas de desarrollo
sudo apt install build-essential

# Instalar GDB para depuración (opcional)
sudo apt install gdb

# Verificar instalación
nasm --version
```

## 🏗️ Conceptos Básicos

### Registros de Propósito General (x86_64)
- **RAX** - Acumulador (resultados de operaciones)
- **RBX** - Base (datos)
- **RCX** - Contador (bucles)
- **RDX** - Datos
- **RSI** - Índice fuente
- **RDI** - Índice destino
- **RSP** - Puntero de pila (stack pointer)
- **RBP** - Puntero base de marco (frame pointer)

### Tamaños de Registros
- **64 bits**: RAX, RBX, RCX, etc.
- **32 bits**: EAX, EBX, ECX, etc. (parte baja de 64 bits)
- **16 bits**: AX, BX, CX, etc.
- **8 bits**: AL, BL, CL, etc. (parte baja) / AH, BH, CH, etc. (parte alta)

### Instrucciones Básicas
- `mov dest, src` - Mover datos
- `add dest, src` - Sumar
- `sub dest, src` - Restar
- `mul src` - Multiplicar
- `div src` - Dividir
- `cmp op1, op2` - Comparar
- `jmp label` - Salto incondicional
- `je label` - Salto si es igual
- `jne label` - Salto si no es igual
- `call function` - Llamar función
- `ret` - Retornar de función

## 🔧 Compilación y Ejecución

### Método 1: Solo Assembly
```bash
# Ensamblar
nasm -f elf64 archivo.s -o archivo.o

# Enlazar
ld archivo.o -o archivo

# Ejecutar
./archivo
```

### Método 2: Con GCC (recomendado para funciones)
```bash
# Ensamblar
nasm -f elf64 archivo.s -o archivo.o

# Enlazar con GCC
gcc archivo.o -o archivo

# Ejecutar
./archivo
```

### Método 3: Makefile básico
```makefile
NAME = libasm.a
NASM = nasm
NASMFLAGS = -f elf64
CC = gcc
CFLAGS = -Wall -Wextra -Werror

SRCDIR = .
OBJDIR = obj

SRCS = ft_strlen.s ft_strcpy.s ft_strcmp.s
OBJS = $(SRCS:%.s=$(OBJDIR)/%.o)

all: $(NAME)

$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

$(OBJDIR)/%.o: $(SRCDIR)/%.s
	@mkdir -p $(OBJDIR)
	$(NASM) $(NASMFLAGS) $< -o $@

clean:
	rm -rf $(OBJDIR)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
```

## 📝 Estructura Básica de un Programa

### Programa Standalone
```assembly
section .data
    ; Variables inicializadas
    msg db 'Hola Mundo', 0

section .bss
    ; Variables no inicializadas
    buffer resb 256

section .text
    global _start

_start:
    ; Tu código aquí
    
    ; Salir del programa
    mov rax, 60      ; syscall: sys_exit
    mov rdi, 0       ; status: 0 (éxito)
    syscall
```

### Función para uso con C
```assembly
section .text
    global nombre_funcion

nombre_funcion:
    ; Tu código aquí
    ret
```

## 🔄 Convenciones de Llamada (System V ABI)

### Parámetros de entrada (primeros 6):
1. **RDI** - Primer parámetro
2. **RSI** - Segundo parámetro
3. **RDX** - Tercer parámetro
4. **RCX** - Cuarto parámetro
5. **R8** - Quinto parámetro
6. **R9** - Sexto parámetro

### Valor de retorno:
- **RAX** - Valor de retorno

### Registros que debes preservar:
- RBX, RSP, RBP, R12, R13, R14, R15

## 📋 Syscalls Útiles en Linux

| Número | Nombre | RAX | RDI | RSI | RDX |
|--------|--------|-----|-----|-----|-----|
| 0 | sys_read | 0 | fd | buffer | count |
| 1 | sys_write | 1 | fd | buffer | count |
| 60 | sys_exit | 60 | status | - | - |

## 🐛 Depuración

### Usar GDB:
```bash
# Compilar con símbolos de depuración
nasm -f elf64 -g -F dwarf archivo.s -o archivo.o
gcc -g archivo.o -o archivo

# Ejecutar con GDB
gdb ./archivo

# Comandos útiles en GDB:
# (gdb) break _start     - Poner breakpoint
# (gdb) run              - Ejecutar
# (gdb) step             - Paso a paso
# (gdb) info registers   - Ver registros
# (gdb) x/10i $rip       - Ver próximas instrucciones
```

## 📊 Ejemplo: ft_strlen

```assembly
section .text
    global ft_strlen

ft_strlen:
    mov rax, 0          ; Contador = 0
    
.loop:
    cmp byte [rdi + rax], 0  ; Comparar con '\0'
    je .done                 ; Si es '\0', terminar
    inc rax                  ; Incrementar contador
    jmp .loop               ; Repetir
    
.done:
    ret                     ; Retornar (resultado en RAX)
```

## ⚠️ Errores Comunes

1. **Olvido de `ret`** - Las funciones deben terminar con `ret`
2. **No preservar registros** - Algunos registros deben guardarse
3. **Acceso a memoria inválida** - Verificar punteros antes de usar
4. **Confundir tamaños** - `byte`, `word`, `dword`, `qword`
5. **Sintaxis incorrecta** - NASM usa sintaxis Intel, no AT&T

## 📚 Recursos Adicionales

- [NASM Documentation](https://www.nasm.us/docs.php)
- [System V ABI](https://wiki.osdev.org/System_V_ABI)
- [Linux Syscall Table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
- [Intel x86_64 Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

## 🎯 Ejercicios Recomendados

1. `ft_strlen` - Calcular longitud de string
2. `ft_strcpy` - Copiar string
3. `ft_strcmp` - Comparar strings
4. `ft_write` - Wrapper de syscall write
5. `ft_read` - Wrapper de syscall read
6. `ft_strdup` - Duplicar string con asignación dinámica

## 💡 Consejos de Optimización

### Técnicas Avanzadas:
- **Desenrollado de bucles** - Reducir overhead de iteraciones
- **Alineación de memoria** - Mejorar rendimiento de acceso
- **Uso de registros SIMD** - Para operaciones paralelas
- **Predicción de saltos** - Organizar código para mejor branch prediction

### Ejemplo de Optimización:
```assembly
; Versión básica
.loop:
    cmp byte [rdi + rax], 0
    je .done
    inc rax
    jmp .loop

; Versión optimizada (desenrollado)
.loop:
    cmp byte [rdi + rax], 0
    je .done
    cmp byte [rdi + rax + 1], 0
    je .done_plus_one
    cmp byte [rdi + rax + 2], 0
    je .done_plus_two
    cmp byte [rdi + rax + 3], 0
    je .done_plus_three
    add rax, 4
    jmp .loop
```

## 🧪 Testing y Validación

### Estrategias de Testing:
1. **Tests unitarios** - Cada función individualmente
2. **Tests de edge cases** - NULL pointers, strings vacías
3. **Tests de memoria** - Verificar leaks con valgrind
4. **Tests de rendimiento** - Comparar con implementaciones estándar
5. **Tests de integración** - Usar múltiples funciones juntas

### Herramientas Útiles:
```bash
# Verificar memory leaks
valgrind --leak-check=full ./test_program

# Análisis de rendimiento
perf record ./test_program
perf report

# Verificar comportamiento con diferentes inputs
echo "test string" | ./test_program
```

---

¡Feliz programación en Assembly! 🚀

## 📄 License

This project is part of the 42 School curriculum and follows their academic guidelines.

## 👨‍💻 Author

**Project**: LibASM  
**Version**: 1.0.0  
**Last Updated**: September 2025  
**42 School Project**

---

*Made with ❤️ and lots of caffeine ☕*
