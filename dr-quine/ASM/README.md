# Dr-Quine - Implementación en Assembly (NASM x64)

Este directorio contiene la implementación en Assembly x64 (NASM) del proyecto **dr-quine** de la escuela 42. Un **quine** es un programa que imprime su propio código fuente sin leer ningún archivo.

## Índice
- [Compilación y Ejecución](#compilación-y-ejecución)
- [Conceptos Fundamentales](#conceptos-fundamentales)
- [Colleen.s - Quine Básico](#colleens---quine-básico)
- [Grace.s - Quine a Archivo](#graces---quine-a-archivo)
- [Sully.s - Quine Recursivo](#sullys---quine-recursivo)
- [Detalles Técnicos](#detalles-técnicos)

---

## Compilación y Ejecución

### Compilar todos los programas
```bash
make
```

### Ejecutar tests
```bash
make test              # Ejecuta todos los tests
make test_colleen      # Test individual de Colleen
make test_grace        # Test individual de Grace
make test_sully        # Test individual de Sully
```

### Limpiar archivos generados
```bash
make clean    # Limpia binarios y objetos
make fclean   # Limpieza completa
```

---

## Conceptos Fundamentales

### ¿Qué es un Quine?

Un quine es un programa que produce su propio código fuente como salida, **sin**:
- Leer archivos
- Usar `argv[0]` o similares
- Hacer trampa de ninguna forma

### Técnica de Implementación

La técnica principal utilizada en estos quines es la **auto-referencia con placeholders**:

1. **String codificado**: Se define una cadena `s` que contiene todo el código del programa, pero con placeholders en lugar de valores literales.

2. **Formato posicional**: Se usa `printf`/`fprintf` con argumentos posicionales (`%1$c`, `%2$c`, etc.) para poder reutilizar argumentos.

3. **Valores clave**:
   - `10` = newline (`\n`)
   - `9` = tab (`\t`)
   - `34` = comillas dobles (`"`)
   - La dirección de `s` misma (auto-referencia)

### Convención de Llamada x64

Los programas utilizan la convención de llamada System V AMD64:
- **Primeros 6 argumentos**: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`
- **Argumentos adicionales**: Se pasan por el stack
- **Registros callee-saved**: `rbx`, `r12-r15`, `rbp`, `rsp`
- **Alineación del stack**: Debe estar alineado a 16 bytes antes de `call`

---

## Colleen.s - Quine Básico

### Descripción
Imprime su propio código fuente a **stdout**.

### Estructura del Código

#### section .data
```nasm
s: db "; Outer comment%1$c...%1$c",0
```
- Contiene todo el código del programa codificado
- Placeholders: `%1$c` (newline), `%2$c` (tab), `%3$c` (quote), `%4$s` (string s)

#### section .text - main
```nasm
main:
    push rbp
    mov rbp,rsp           ; Prólogo estándar
    
    ; Preparar argumentos para printf
    lea rdi,[s]           ; arg1: formato (string s)
    mov rsi,10            ; arg2: %1$c = newline
    mov rdx,9             ; arg3: %2$c = tab
    mov rcx,34            ; arg4: %3$c = comillas dobles
    lea r8,[s]            ; arg5: %4$s = dirección de string s
    
    xor rax,rax           ; rax=0 (no hay args vectoriales)
    call printf           ; Imprimir el quine
    
    xor rax,rax           ; return 0
    pop rbp
    ret
```

### Funcionamiento Paso a Paso

1. **Carga del formato**: `rdi` apunta a `s`, que contiene el formato con placeholders
2. **Argumentos posicionales**: Se cargan los valores que sustituirán los placeholders
3. **Auto-referencia**: El 5º argumento (`r8`) contiene la dirección de `s` misma
4. **Printf**: Interpreta el formato y sustituye:
   - `%1$c` → newline (10)
   - `%2$c` → tab (9)
   - `%3$c` → comilla doble (34)
   - `%4$s` → contenido de `s`

El resultado es el código completo, incluyendo los comentarios y la definición de `s`.

### Requisitos del proyecto
- ✅ 2 comentarios (outer e inner)
- ✅ 1 función auxiliar (implícita: la función main es llamada desde _start)

---

## Grace.s - Quine a Archivo

### Descripción
Escribe su propio código fuente en el archivo **Grace_kid.s** (sin ejecutarse a sí mismo).

### Estructura del Código

#### section .data
```nasm
s: db "; Comment%1$csection .data%1$c...",0
f: db "Grace_kid.s",0      ; Nombre del archivo de salida
mode: db "w",0              ; Modo de apertura: escritura
```

#### section .text - main
```nasm
main:
    push rbp
    mov rbp,rsp
    
    ; 1. Abrir archivo Grace_kid.s
    lea rdi,[f]           ; arg1: nombre de archivo
    lea rsi,[mode]        ; arg2: modo "w"
    call fopen
    mov r12,rax           ; Guardar file pointer en r12 (callee-saved)
    
    ; 2. Escribir el quine al archivo
    mov rdi,r12           ; arg1: file pointer
    lea rsi,[s]           ; arg2: formato (string s)
    mov rdx,10            ; arg3: %1$c = newline
    mov rcx,9             ; arg4: %2$c = tab
    mov r8,34             ; arg5: %3$c = comillas dobles
    lea r9,[s]            ; arg6: %4$s = dirección de string s
    xor rax,rax
    call fprintf
    
    ; 3. Cerrar archivo
    mov rdi,r12
    call fclose
    
    xor rax,rax           ; return 0
    pop rbp
    ret
```

### Funcionamiento

1. **Apertura**: `fopen` crea `Grace_kid.s` en modo escritura
2. **Escritura**: `fprintf` escribe el código completo al archivo (igual que printf en Colleen)
3. **Cierre**: `fclose` cierra el archivo
4. **Resultado**: El archivo `Grace_kid.s` es idéntico a `Grace.s`

### Diferencias con Colleen
- Usa `fprintf` en lugar de `printf`
- Escribe a archivo en lugar de stdout
- Usa `r12` para guardar el file pointer (registro callee-saved)

### Requisitos del proyecto
- ✅ 1 comentario
- ✅ Definición de macros simulada (variables de string en .data)
- ✅ No se ejecuta a sí mismo

---

## Sully.s - Quine Recursivo

### Descripción
Genera una cadena de quines recursivos que se auto-replican y ejecutan, decrementando un contador en cada generación hasta llegar a 0.

### Estructura del Código

#### section .data
```nasm
s: db "section .data%1$c...",0            ; Código completo
fmt: db "Sully_%d.s",0                    ; Formato para nombre de archivo
mode: db "w",0                            ; Modo de escritura
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
    jl .end               ; Si i < 0, terminar
```

### Fases de Ejecución

#### Fase 1: Generar nombre de archivo
```nasm
    lea rdi,[filename]
    lea rsi,[fmt]         ; "Sully_%d.s"
    mov rdx,r15           ; i
    xor rax,rax
    call sprintf          ; filename = "Sully_5.s"
```

#### Fase 2: Escribir el quine con contador decrementado
```nasm
    ; Abrir archivo
    lea rdi,[filename]
    lea rsi,[mode]
    call fopen
    mov r12,rax
    
    ; Escribir con fprintf(f, s, 10, 9, i-1, 34, s)
    mov rdi,r12           ; file pointer
    lea rsi,[s]           ; formato
    mov rdx,10            ; %1$c = newline
    mov rcx,9             ; %2$c = tab
    mov r8,r15
    dec r8                ; %3$d = i-1 (¡DECREMENTAR!)
    mov r9,34             ; %4$c = comillas
    
    ; 7º argumento al stack (dirección de s)
    lea rax,[s]
    sub rsp,8             ; Alinear stack
    push rax              ; %5$s = string s
    xor rax,rax
    call fprintf
    add rsp,16            ; Limpiar stack
    
    mov rdi,r12
    call fclose
```

**Clave**: El `dec r8` decrementa el contador antes de pasarlo como argumento. Así:
- `Sully.s` tiene `i=5` y genera `Sully_5.s` con `i=4`
- `Sully_5.s` tiene `i=4` y genera `Sully_4.s` con `i=3`
- Y así sucesivamente...

#### Fase 3: Compilar y ejecutar (si i > 0)
```nasm
    cmp r15d,0
    jle .end              ; Si i <= 0, no ejecutar
    
    ; Construir comando
    lea rdi,[cmdbuf]
    lea rsi,[cmd]
    mov rdx,r15           ; i (4 veces en el comando)
    mov rcx,r15
    mov r8,r15
    mov r9,r15
    xor rax,rax
    call sprintf
    
    ; Ejecutar
    lea rdi,[cmdbuf]
    call system           ; Esto inicia la recursión
    
.end:
    xor rax,rax
    leave                 ; mov rsp,rbp; pop rbp
    ret
```

### Cadena de Ejecución

```
Sully (i=5)
  ├─> genera Sully_5.s (i=4)
  └─> compila y ejecuta Sully_5
        ├─> genera Sully_4.s (i=3)
        └─> compila y ejecuta Sully_4
              ├─> genera Sully_3.s (i=2)
              └─> compila y ejecuta Sully_3
                    ├─> genera Sully_2.s (i=1)
                    └─> compila y ejecuta Sully_2
                          ├─> genera Sully_1.s (i=0)
                          └─> compila y ejecuta Sully_1
                                ├─> genera Sully_0.s (i=-1)
                                └─> NO ejecuta (i=0)
```

### Archivos Generados

Un total de **11 archivos** (sin contar .o):
- `Sully_5.s` a `Sully_0.s` → 6 archivos .s
- `Sully_5` a `Sully_1` → 5 binarios ejecutables
- (`Sully_0.s` no se compila porque `i=0` activa `jle .end`)

### Requisitos del proyecto
- ✅ Contador inicial `i=5`
- ✅ Decrementa en cada iteración
- ✅ Se detiene cuando `i=0`
- ✅ Genera exactamente 13 archivos totales (incluyendo .o intermedios)

---

## Detalles Técnicos

### Argumentos Posicionales en printf/fprintf

El formato `%N$X` permite:
- **N**: Número de argumento (1-indexed)
- **X**: Tipo de formato (`c`, `s`, `d`, etc.)

Ejemplo:
```nasm
; printf("%1$c %2$s %1$c", 10, "hello")
; Resultado: "\n hello \n"
```

Ventaja para quines: Reutilizar el mismo argumento múltiples veces.

### Alineación del Stack

En x64, el stack debe estar alineado a 16 bytes antes de `call`:
```nasm
push rbp        ; rsp -= 8 (ahora desalineado)
mov rbp,rsp
push r12        ; rsp -= 8 (alineado)
push r15        ; rsp -= 8 (desalineado)
sub rsp,32      ; rsp -= 32 (alineado de nuevo)
```

Cuando se pasa un 7º argumento por stack:
```nasm
sub rsp,8       ; Pre-alinear
push rax        ; Poner argumento
call fprintf    ; rsp está alineado a 16 bytes
add rsp,16      ; Limpiar (8+8)
```

### Registros Utilizados

- **r12**: File pointer (callee-saved, se preserva entre llamadas)
- **r15**: Contador `i` en Sully (callee-saved)
- **rax**: Valor de retorno de funciones, también se anula (`xor rax,rax`) para indicar 0 argumentos vectoriales en llamadas vararg

### Funciones de la Biblioteca C

| Función | Propósito | Argumentos |
|---------|-----------|------------|
| `printf` | Imprimir a stdout | rdi=formato, rsi...=args |
| `fprintf` | Imprimir a archivo | rdi=FILE*, rsi=formato, rdx...=args |
| `fopen` | Abrir archivo | rdi=nombre, rsi=modo |
| `fclose` | Cerrar archivo | rdi=FILE* |
| `sprintf` | Formatear a string | rdi=buffer, rsi=formato, rdx...=args |
| `system` | Ejecutar comando | rdi=comando |

### Placeholders en el String s

El string `s` codifica:
- **Estructura del código**: `section .data`, `section .text`, etc.
- **Declaraciones**: `global main`, `extern printf`, etc.
- **Instrucciones**: `push rbp`, `mov rbp,rsp`, etc.
- **Todo separado por**: `%1$c` (newlines) y `%2$c` (tabs)

Ejemplo fragmento de `s` en Colleen:
```
"section .data%1$c%2$cs: db %3$c%4$s%3$c,0%1$c%1$csection .text%1$c..."
```

Cuando se ejecuta con argumentos (10, 9, 34, s):
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
# Debería mostrar:
# Sully_0.s, Sully_1, Sully_1.s, Sully_2, Sully_2.s, ... Sully_5, Sully_5.s
```

---

## Conceptos Clave para Entender los Quines

1. **Auto-referencia**: El string `s` se pasa a sí mismo como argumento
2. **Formato posicional**: Permite usar el mismo argumento múltiples veces
3. **Codificación cuidadosa**: Todo el código debe estar en `s`, incluyendo la definición de `s`
4. **Balance perfecto**: El formato y los argumentos deben producir exactamente el código original

## Recursos Adicionales

- [Convención de llamada x64 System V](https://wiki.osdev.org/System_V_ABI)
- [NASM Documentation](https://www.nasm.us/xdoc/2.15.05/html/nasmdoc0.html)
- [Printf format specifiers](https://en.cppreference.com/w/c/io/fprintf)
- [Quine (computing) - Wikipedia](https://en.wikipedia.org/wiki/Quine_(computing))

---

**Autor**: dr-quine ASM implementation  
**Fecha**: 2026  
**Assembler**: NASM 2.16+  
**Arquitectura**: x86_64 Linux
