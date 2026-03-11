# Dr-Quine - Implementación en Python

Este directorio contiene la implementación en Python del proyecto **dr-quine** de la escuela 42. Un **quine** es un programa que imprime su propio código fuente sin leer ningún archivo.

## Índice
- [Ejecución](#ejecución)
- [Conceptos Fundamentales](#conceptos-fundamentales)
- [Colleen.py - Quine Básico](#colleenpy---quine-básico)
- [Grace.py - Quine que Genera un Archivo](#gracepy---quine-que-genera-un-archivo)
- [Sully.py - Quine Recursivo](#sullypy---quine-recursivo)
- [Técnicas Avanzadas](#técnicas-avanzadas)

---

## Ejecución

### Ejecutar tests
```bash
make           # Ejecuta todos los tests
```

### Ejecutar individualmente
```bash
python3 Colleen.py
python3 Grace.py
python3 Sully.py
```

### Limpiar archivos generados
```bash
make clean     # Limpia archivos temporales
make fclean    # Limpieza completa (incluye archivos generados)
```

---

## Conceptos Fundamentales

### ¿Qué es un Quine?

Un quine es un programa que produce su propio código fuente como salida, **sin**:
- Leer archivos (`open`, `read`, etc.)
- Usar `sys.argv[0]` o información del sistema
- Hacer trampa de ninguna forma

### Restricciones del Proyecto

Cada programa debe cumplir:
- **Colleen**: Imprime su propio código fuente a stdout
- **Grace**: Escribe su propio código fuente en un archivo (`Grace_kid.py`)
- **Sully**: Genera una cadena de 6 quines que se auto-replican decrementando un contador

### Técnica Clave: `%r` (repr) en Python

La técnica fundamental en Python es usar `%r` con formato `%`:

```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

**Por qué funciona**:
- `%r` aplica `repr()` al argumento, añadiendo comillas simples y escapando caracteres especiales automáticamente
- `%%` genera un `%` literal en la salida
- Al sustituir `s % s`, el string se inserta dentro de sí mismo completo con sus comillas

### Valores Clave

| Técnica | Uso |
|---------|-----|
| `%r` | Inserta la representación del string con comillas (auto-referencia) |
| `%%` | Imprime un `%` literal (necesario para que el hijo sea válido) |
| `%d` | Inserta un entero (para el contador en Sully) |

---

## Colleen.py - Quine Básico

### Descripción
Imprime su propio código fuente a **stdout**.

### Código Completo
```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

### Análisis Detallado

#### El String `s`

```python
s = 's = %r\nprint(s %% s)'
```

El string contiene **casi todo el código del programa** con un placeholder `%r`.

#### Funcionamiento Paso a Paso

1. `s` se define con el template del código
2. `s % s` aplica el formato:
   - `%r` se reemplaza por `repr(s)` → el string con sus comillas: `'s = %r\nprint(s %% s)'`
   - `%%` se convierte en `%` literal
3. El resultado es:
   ```python
   s = 's = %r\nprint(s %% s)'
   print(s % s)
   ```

#### Por Qué `%r` es Perfecto para Quines

- `repr(s)` produce `'s = %r\nprint(s %% s)'` (nota las comillas y el `\n` escapado)
- Al insertar eso después de `s = `, reproduce exactamente la primera línea del código
- El `%%` en el template se convierte en `%` en la salida, haciendo al hijo ejecutable

### Requisitos Cumplidos
- ✅ Imprime su propio código fuente exactamente
- ✅ No lee ningún archivo

---

## Grace.py - Quine que Genera un Archivo

### Descripción
Escribe su propio código fuente en **Grace_kid.py**.

### Código Completo
```python
s = 's = %r\nwith open("Grace_kid.py", "w") as f:\n    f.write(s %% s)\n'
with open("Grace_kid.py", "w") as f:
    f.write(s % s)
```

### Análisis Detallado

#### El String `s`

```python
s = 's = %r\nwith open("Grace_kid.py", "w") as f:\n    f.write(s %% s)\n'
```

El string codifica todo el programa, incluyendo el bloque `with open(...)`.

#### Funcionamiento Paso a Paso

1. `s` contiene el template con el código completo (newlines escapados como `\n`)
2. `s % s`:
   - `%r` → `repr(s)` → el string con sus comillas y escapes
   - `%%` → `%` literal
3. El resultado se escribe en `Grace_kid.py`
4. `Grace_kid.py` es idéntico al código fuente de `Grace.py`

#### Verificación
```bash
python3 Grace.py
diff Grace.py Grace_kid.py   # Sin diferencias
```

### Requisitos Cumplidos
- ✅ `Grace_kid.py` es idéntico a `Grace.py`
- ✅ No lee ningún archivo

---

## Sully.py - Quine Recursivo

### Descripción
Genera una cadena de quines que se auto-replican, ejecutan y decrementan un contador en cada generación, produciendo 6 archivos en total (`Sully_5.py` hasta `Sully_1.py`) más sus respectivas ejecuciones.

### Código Completo
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

### Análisis Línea por Línea

#### Variables Principales
```python
s = 'import subprocess\n...'   # Template con todo el código
i = 5                          # Contador inicial
```

#### El Template con Dos Placeholders
```python
s = '...s = %r\ni = %d\n...'
```
- `%r` → `repr(s)` (auto-referencia al código)
- `%d` → el contador decrementado

#### Fase 1: Validación
```python
if i > 0:
```
Si el contador llega a 0, el programa no genera más hijos ni ejecuta nada.

#### Fase 2: Generación del Archivo Hijo
```python
fname = "Sully_" + str(i) + ".py"
with open(fname, "w") as f:
    f.write(s % (s, i - 1))
```

**¡CLAVE!**: `s % (s, i - 1)` usa dos argumentos:
- `s` → sustituye `%r` (el código completo con repr)
- `i - 1` → sustituye `%d` (**contador decrementado**)

El archivo hijo tiene el mismo código pero con `i = i-1`.

#### Fase 3: Ejecución Recursiva
```python
subprocess.run(["python3", fname])
```
Ejecuta el hijo, que a su vez generará su propio hijo con `i-2`, y así sucesivamente.

### Cadena de Ejecución Completa

```
Sully.py (i=5)
  ├─> crea Sully_5.py (con i=4)
  └─> ejecuta python3 Sully_5.py
        ├─> crea Sully_4.py (con i=3)
        └─> ejecuta python3 Sully_4.py
              ├─> crea Sully_3.py (con i=2)
              └─> ejecuta python3 Sully_3.py
                    ├─> crea Sully_2.py (con i=1)
                    └─> ejecuta python3 Sully_2.py
                          ├─> crea Sully_1.py (con i=0)
                          └─> ejecuta python3 Sully_1.py
                                └─> i = 0, no genera más hijos
```

**Archivos generados**: `Sully_5.py`, `Sully_4.py`, `Sully_3.py`, `Sully_2.py`, `Sully_1.py` (6 en total contando `Sully.py`)

### Requisitos Cumplidos
- ✅ Genera exactamente 6 scripts en la cadena
- ✅ Cada hijo es un quine válido con counter decrementado
- ✅ La cadena se detiene cuando `i = 0`

---

## Técnicas Avanzadas

### Por Qué Python es Ideal para Quines

Python facilita la escritura de quines gracias a:

1. **`%r` con `repr()`**: Produce automáticamente una representación del string con comillas y escapes, evitando la necesidad de codificar manualmente delimitadores.

2. **Strings multilínea y `\n`**: Los saltos de línea se pueden codificar como `\n` dentro del string y `repr()` los preserva correctamente.

3. **Formato `%`**: El operador `%` permite sustituir múltiples valores (`%r`, `%d`, `%%`) de forma compacta.

### Comparación con la Versión en C

| Aspecto | C | Python |
|---------|---|--------|
| Auto-referencia | `%4$s` con argumentos posicionales | `%r` con repr() |
| Newlines | `%1$c` con valor `10` | `\n` escapado en string |
| Comillas | `%3$c` con valor `34` | Manejado por `repr()` |
| Ejecución de hijos (Sully) | `system()` + compilación gcc | `subprocess.run()` directo |
| Complejidad del quine | Media-alta | Baja |
