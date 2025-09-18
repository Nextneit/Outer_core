# LibASM - Guía Básica de Assembly

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

---

¡Feliz programación en Assembly! 🚀
