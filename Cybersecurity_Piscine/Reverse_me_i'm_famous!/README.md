# Reverse Me I'm Famous! 🔍

## Overview

**Objetivo**: Realizar ingeniería inversa sobre **3 binarios x86/x86-64** con dificultad progresiva. Cada ejercicio requiere analizar el código máquina, encontrar la clave de validación y reconstruir el código fuente en C.

---

## Metodología de Ingeniería Inversa

### Fase 1: Reconocimiento Estático

**Sin ejecutar el binario:**

```bash
# Tipo y arquitectura
file binary

# Cadenas de texto (pistas iniciales)
strings binary | sort -u

# Símbolos (funciones si no está stripeado)
nm binary
objdump -t binary

# Headers ELF
readelf -h binary
readelf -l binary
```

### Fase 2: Análisis Dinámico con GDB

```bash
gdb ./binary

# Dentro de GDB:
(gdb) info functions          # Listar funciones
(gdb) disas main              # Desensamblar main
(gdb) disas nombre_funcion    # Desensamblar función específica

# Breakpoints estratégicos:
(gdb) break strcmp            # Detener en comparaciones
(gdb) break atoi              # Detener en conversiones
(gdb) break printf            # Detener antes de mensajes

(gdb) run                     # Ejecutar el programa
(gdb) x/s $esp               # Ver strings en stack
(gdb) x/10x $ebp             # Ver valores en registro base
(gdb) info registers          # Estado de todos los registros
```

### Fase 3: Reconstrucción

1. **Documentar el flujo** en pseudocódigo
2. **Identificar constantes** (códigos ASCII, valores hardcodeados)
3. **Mapear estructuras de control** (loops, switches, condicionales)
4. **Escribir código C equivalente**
5. **Compilar y verificar**

---

## Ejercicios

### 📌 Level 1 — Básico (32-bit)

**Dificultad**: ⭐ Principiante  
**Arquitectura**: x86 32-bit  
**Compilador probable**: GCC sin optimizaciones

**Objetivo**: Encontrar la clave secreta en el binario `level1`

**Conceptos**:
- Stack layout en 32-bit (ESP, EBP)
- Convención de llamadas cdecl (argumentos en stack)
- Funciones básicas: `printf`, `scanf`, `strcmp`
- Hardcoding de datos en el sistema de archivos

**Archivos**:
- `binary/level1` — binario comprimido
- `level1/README.md` — análisis detallado
- `level1/source.c` — código fuente original
- `level1/password` — la clave a encontrar

**Resultado esperado**:
```
__stack_check
```

**Recursos**:
- Ver [level1/README.md](level1/README.md) para análisis completo

---

### 📌 Level 2 — Intermedio (32-bit + Algoritmo)

**Dificultad**: ⭐⭐ Intermedio  
**Arquitectura**: x86 32-bit  
**Compilador probable**: GCC con optimizaciones moderadas

**Objetivo**: Descodificar un algoritmo de transformación de entrada

**Conceptos**:
- Loops y bucles anidados
- Validación de formato (prefijo requerido: `00`)
- Decodificación decimal → ASCII
- Constantes hardcodeadas en múltiples puntos
- Técnicas de ofuscación (ruido, nombres falsos de funciones)

**Algoritmo**:
1. Input **debe empezar** con `00`
2. **Bucle**: Lee el resto de 3 en 3 dígitos
3. Convierte cada tripla a su valor ASCII (0-255)
4. Construye un buffer de 8 bytes
5. Compara con clave objetivo: `"delabere"`

**Archivos**:
- `binary/level2` — binario comprimido
- `level2/README.md` — análisis detallado
- `level2/source.c` — código fuente original
- `level2/password` — la clave a encontrar

**Clave objetivo** (decodificada):
```
delabere
```

**Clave de entrada** (codificada):
```
00100101010801110010401140908801010114
```

**Recursos**:
- Ver [level2/README.md](level2/README.md) para análisis completo

---

### 📌 Level 3 — Avanzado (64-bit + Ofuscación)

**Dificultad**: ⭐⭐⭐ Avanzado  
**Arquitectura**: x86-64  
**Compilador probable**: GCC con optimizaciones, ofuscación deliberada

**Objetivo**: Analizar código 64-bit con múltiples capas de ofuscación

**Conceptos**:
- Registros x86-64 (RAX, RBX, RCX, RDX, RSI, RDI)
- Convención de llamadas System V AMD64 (argumentos en registros)
- Validación de prefijo (requerido: `42`)
- Mismo algoritmo decodificador que Level2 pero con cambios sutiles
- Switch con múltiples casos falsos (ofuscación)
- Nombres de funciones falsos (`___syscall_malloc` vs `____syscall_malloc`)

**Algoritmo**:
1. Input **debe empezar** con `42`
2. **Bucle**: Lee el resto de 3 en 3 dígitos
3. Byte inicial hardcodeado: `'*'` (0x2a = 42 en decimal)
4. Decodifica 7 bytes adicionales
5. Compara con clave objetivo: `"********"` (8 asteriscos)
6. Switch ofuscado: 9 casos, solo uno válido

**Archivos**:
- `binary/level3` — binario comprimido
- `level3/README.md` — análisis detallado
- `level3/source.c` — código fuente original
- `level3/password` — la clave a encontrar

**Clave objetivo** (decodificada):
```
********  (8 asteriscos)
```

**Recursos**:
- Ver [level3/README.md](level3/README.md) para análisis completo

---

## Guía Rápida de Uso

### Comenzar con Level 1

```bash
cd level1

# 1. Reconocimiento
file binary/level1
strings binary/level1 | grep -E "(Good|Nope|key|password)"

# 2. Análisis con GDB
gdb ./binary/level1
(gdb) disas main
(gdb) break strcmp
(gdb) run
(gdb) x/s $esp

# 3. Verificar resultado
cat password
./binary/level1
# Introducir la clave
```

### Progresión Recomendada

```
Level 1 (32-bit básico)
    ↓
Level 2 (32-bit + algoritmo)
    ↓
Level 3 (64-bit + ofuscación)
```

---

## Herramientas Recomendadas

| Herramienta | Propósito |
|---|---|
| `gdb` | Debugger principal, ejecución paso a paso |
| `strings` | Extrae cadenas de texto del binario |
| `objdump` | Desensambla y analiza estructura ELF |
| `readelf` | Lee headers ELF |
| `strace` | Traza llamadas al sistema |
| `ltrace` | Traza llamadas a librería |
| `radare2` | Análisis interactivo alternativo |
| `Ghidra` | Decompilador gráfico (NSA) |
| `IDA Free` | Disassembler profesional (versión gratuita) |

---

## Consejos de Ofuscación y Defensa

Los binarios pueden usar técnicas para dificultar el análisis:

**Técnicas encontradas en estos ejercicios**:
1. ✅ **Hardcoding de valores** — constantes en memoria
2. ✅ **Nombres falsos de funciones** — `___syscall_malloc` vs `____syscall_malloc`
3. ✅ **Ruido en strings** — texto en latín sin uso
4. ✅ **Ofuscación de control de flujo** — switches complejos
5. ✅ **Validación de prefijo** — formato rígido de entrada
6. ✅ **PIE (Position Independent Executable)** — direcciones aleatorias
7. ✅ **Bucles de transformación** — decodificadores inline

---

## Checklist de Análisis

```
☐ Ejecutar: file, strings, nm, objdump
☐ Identificar main() y punto de entrada
☐ Listar todas las funciones
☐ Desensamblar main y funciones relevantes
☐ Identificar strings y constantes
☐ Mapear loops y condicionales
☐ Encontrar comparaciones (strcmp, memcmp)
☐ Setear breakpoints en puntos críticos
☐ Ejecutar paso a paso
☐ Inspeccionar stack y registros en tiempo real
☐ Reconstruir pseudocódigo
☐ Escribir código C equivalente
☐ Compilar y verificar funcionamiento
```

---

## Referencias

- **GDB Manual**: https://sourceware.org/gdb/documentation/
- **x86 Assembly**: https://en.wikibooks.org/wiki/X86_Assembly
- **x86-64 ABI**: https://en.wikipedia.org/wiki/X86_calling_conventions
- **ELF Format**: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format

---

## Estructura de Carpetas

```
Reverse_me_i'm_famous!/
├── README.md           ← Este archivo
├── binary/
│   ├── level1
│   ├── level2
│   └── level3
├── level1/
│   ├── README.md       → Análisis detallado
│   ├── source.c        → Código original
│   └── password        → Solución
├── level2/
│   ├── README.md
│   ├── source.c
│   └── password
└── level3/
    ├── README.md
    ├── source.c
    └── password
```

---

**Última actualización**: Marzo 2026  
**Estado**: Completado (3/3 levels)
