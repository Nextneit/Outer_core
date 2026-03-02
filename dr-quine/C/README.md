# Dr-Quine - Implementación en C

Este directorio contiene la implementación en C del proyecto **dr-quine** de la escuela 42. Un **quine** es un programa que imprime su propio código fuente sin leer ningún archivo.

## Índice
- [Compilación y Ejecución](#compilación-y-ejecución)
- [Conceptos Fundamentales](#conceptos-fundamentales)
- [Colleen.c - Quine Básico](#colleenc---quine-básico)
- [Grace.c - Quine con Macros](#gracec---quine-con-macros)
- [Sully.c - Quine Recursivo](#sullyc---quine-recursivo)
- [Técnicas Avanzadas](#técnicas-avanzadas)

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
make clean    # Limpia binarios
make fclean   # Limpieza completa
```

---

## Conceptos Fundamentales

### ¿Qué es un Quine?

Un quine es un programa que produce su propio código fuente como salida, **sin**:
- Leer archivos (no `fopen`, `read`, etc.)
- Usar `argv[0]` o información del sistema
- Usar trucos del compilador o depurador
- Hacer trampa de ninguna forma

### Restricciones del Proyecto

Cada programa debe cumplir:
- **Colleen**: 2 comentarios (uno externo, uno interno) + 1 función auxiliar
- **Grace**: 1 comentario + exactamente 3 macros (#define) + NO main explícito
- **Sully**: Crear exactamente 13 archivos (Sully + 6 archivos .c + 6 binarios)

### Técnica Clave: Printf con Argumentos Posicionales

La técnica fundamental es usar `printf` con **argumentos posicionales**:

```c
printf("%1$c %2$s %1$c", 10, "hello");
// Resultado: "\n hello \n"
```

**Ventajas**:
- `%N$X` permite referirse al argumento N-ésimo
- Puedes reutilizar el mismo argumento múltiples veces
- Esencial para la auto-referencia en quines

### Valores Clave

| Valor | Carácter | Uso |
|-------|----------|-----|
| `10` | `\n` | Newline (salto de línea) |
| `9` | `\t` | Tab (tabulación) |
| `34` | `"` | Comillas dobles |

Estos valores permiten evitar caracteres de escape en el string codificado.

---

## Colleen.c - Quine Básico

### Descripción
Imprime su propio código fuente a **stdout** usando una función auxiliar.

### Código Completo
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

### Análisis Detallado

#### Estructura
- **Comentario externo**: `/* Outer comment */`
- **Comentario en función**: `// Inner comment in function`
- **Comentario en main**: `/* Inner comment in main */`
- **Función auxiliar**: `ft()` que realiza la impresión

#### El String `s`

El string `s` contiene **todo el código del programa** codificado con placeholders:

```c
char*s="/*%1$c%2$cOuter comment%1$c*/...";
```

**Placeholders**:
- `%1$c` → argumento 1 → `10` → newline (`\n`)
- `%2$c` → argumento 2 → `9` → tab (`\t`)
- `%3$c` → argumento 3 → `34` → comilla doble (`"`)
- `%4$s` → argumento 4 → `s` → el contenido del string s (auto-referencia)

#### Funcionamiento Paso a Paso

1. **Definición del string**: `s` contiene el código con placeholders
2. **Llamada a printf**:
   ```c
   printf(s,10,9,34,s);
   ```
   - `s` es el formato
   - `10` sustituye `%1$c` (newlines)
   - `9` sustituye `%2$c` (tabs)
   - `34` sustituye `%3$c` (comillas)
   - `s` sustituye `%4$s` (el string completo)

3. **Auto-referencia**: Cuando printf ve `%4$s`, inserta el contenido de `s`, que incluye la definición `char*s="..."`

4. **Resultado**: El código completo con su formato original

### Ejemplo de Expansión

Fragmento simplificado:
```c
"char*s=%3$c%4$s%3$c;"
```

Con argumentos `(10,9,34,s)` se expande a:
```c
char*s="[contenido de s]";
```

### Requisitos Cumplidos
- ✅ 2 comentarios (outer e inner)
- ✅ 1 función auxiliar (`ft()`)
- ✅ Código completo reproducido exactamente

---

## Grace.c - Quine con Macros

### Descripción
Escribe su código fuente en **Grace_kid.c** usando **solo macros** (sin función main visible).

### Código Completo
```c
/*Comment*/
#include<stdio.h>

#define S "/*Comment*/%1$c#include<stdio.h>%1$c%1$c#define S %2$c%3$s%2$c%1$c#define F {FILE*f=fopen(%2$cGrace_kid.c%2$c,%2$cw%2$c);fprintf(f,S,10,34,S);fclose(f);}%1$c#define M int main(){F return 0;}%1$cM%1$c"
#define F {FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);}
#define M int main(){F return 0;}
M
```

### Análisis de las Macros

#### Macro S - String del Código
```c
#define S "/*Comment*/%1$c#include<stdio.h>%1$c..."
```
- Contiene todo el código del programa codificado
- Usa `%1$c` para newline (10) y `%2$c` para comilla (34)
- `%3$s` se auto-referencia al macro S mismo

#### Macro F - Funcionalidad
```c
#define F {FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);}
```
Esta macro:
1. Abre el archivo `Grace_kid.c` en modo escritura
2. Escribe el código usando `fprintf` con el string `S`
3. Cierra el archivo

Los argumentos de fprintf:
- `S` → formato (el string con placeholders)
- `10` → `%1$c` (newline)
- `34` → `%2$c` (comillas dobles)
- `S` → `%3$s` (el contenido del macro S)

#### Macro M - Main Implícito
```c
#define M int main(){F return 0;}
```
- Define la función `main` como macro
- Ejecuta el macro `F` (que escribe el archivo)
- Retorna 0

#### Invocación
```c
M
```
Esta única línea:
1. Expande el macro `M`
2. Que crea `int main()`
3. Que ejecuta `F`
4. Que escribe el quine en `Grace_kid.c`

### Flujo de Ejecución

```
Compilador ve: M
              ↓
Expande a: int main(){F return 0;}
              ↓
Expande F: int main(){{FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);} return 0;}
              ↓
Ejecuta: abre Grace_kid.c
              ↓
fprintf usa S como formato con args (10,34,S)
              ↓
Grace_kid.c contiene el código completo
```

### Técnica Única: Main Oculto

Grace **no tiene un `int main()` visible** en el código fuente. Todo se hace mediante macros:
- `#define M` crea el main
- `M` al final lo invoca
- Esto cumple con el requisito de usar solo macros

### Requisitos Cumplidos
- ✅ 1 comentario (`/*Comment*/`)
- ✅ Exactamente 3 macros (#define S, F, M)
- ✅ No hay función main visible (está en un macro)
- ✅ Grace_kid.c es idéntico a Grace.c

---

## Sully.c - Quine Recursivo

### Descripción
Genera una cadena de quines que se auto-replican, compilan y ejecutan, decrementando un contador en cada generación.

### Código Completo
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

### Análisis Línea por Línea

#### Variables Principales
```c
int i=5;                    // Contador inicial
char*s="...";               // String con todo el código
char f[32],c[128];          // Buffers para filename y comando
```

#### Fase 1: Validación
```c
if(i<0)
	return 0;
```
Si el contador es negativo, terminar (aunque con `i=5` inicial esto nunca pasa en la primera ejecución).

#### Fase 2: Generación del Archivo
```c
sprintf(f,"Sully_%d.c",i);
```
Crea el nombre del archivo: `Sully_5.c`, `Sully_4.c`, etc.

```c
FILE*fp=fopen(f,"w");
fprintf(fp,s,10,9,i-1,34,s);
fclose(fp);
```

**¡CLAVE!**: Los argumentos de fprintf son:
- `fp` → file pointer
- `s` → formato con placeholders
- `10` → `%1$c` (newline)
- `9` → `%2$c` (tab)
- `i-1` → `%3$d` (**contador decrementado**)
- `34` → `%4$c` (comillas)
- `s` → `%5$s` (el string completo)

El `i-1` es crucial: escribe el código con el contador reducido.

#### Fase 3: Compilación y Ejecución (Recursión)
```c
if(i>0){
	sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
	system(c);
}
```

Si `i > 0`:
1. Construye el comando de compilación
2. Compila `Sully_X.c` → `Sully_X`
3. Ejecuta `./Sully_X` (que tiene `i` decrementado)

### Cadena de Ejecución Completa

```
Sully (i=5)
  ├─> crea Sully_5.c (con i=4)
  ├─> compila Sully_5.c → Sully_5
  └─> ejecuta ./Sully_5
        ├─> crea Sully_4.c (con i=3)
        ├─> compila Sully_4.c → Sully_4
        └─> ejecuta ./Sully_4
              ├─> crea Sully_3.c (con i=2)
              ├─> compila Sully_3.c → Sully_3
              └─> ejecuta ./Sully_3
                    ├─> crea Sully_2.c (con i=1)
                    ├─> compila Sully_2.c → Sully_2
                    └─> ejecuta ./Sully_2
                          ├─> crea Sully_1.c (con i=0)
                          ├─> compila Sully_1.c → Sully_1
                          └─> ejecuta ./Sully_1
                                ├─> crea Sully_0.c (con i=-1)
                                └─> NO compila (i=0, salta el if)
```

### Archivos Generados

Total: **13 archivos**

| Archivo | Descripción | Contador i |
|---------|-------------|------------|
| `Sully` | Binario original | `i=5` |
| `Sully.c` | Código fuente original | `i=5` |
| `Sully_5.c` | Generado por Sully | `i=4` |
| `Sully_5` | Binario compilado | `i=4` |
| `Sully_4.c` | Generado por Sully_5 | `i=3` |
| `Sully_4` | Binario compilado | `i=3` |
| `Sully_3.c` | Generado por Sully_4 | `i=2` |
| `Sully_3` | Binario compilado | `i=2` |
| `Sully_2.c` | Generado por Sully_3 | `i=1` |
| `Sully_2` | Binario compilado | `i=1` |
| `Sully_1.c` | Generado por Sully_2 | `i=0` |
| `Sully_1` | Binario compilado | `i=0` |
| `Sully_0.c` | Generado por Sully_1 | `i=-1` |

**Nota**: `Sully_0.c` se crea pero NO se compila porque el `if(i>0)` lo impide.

### Diferencias Entre Generaciones

Cada archivo `Sully_X.c` es **casi idéntico** al anterior, solo cambia:

```c
// En Sully_5.c
int i=4;

// En Sully_4.c
int i=3;

// etc.
```

### Por Qué se Detiene

1. `Sully_1` tiene `i=0`
2. Ejecuta `fprintf(fp,s,10,9,i-1,34,s)` → crea `Sully_0.c` con `i=-1`
3. El `if(i>0)` es **false** → no compila ni ejecuta
4. Retorna 0 → fin de la recursión

### Requisitos Cumplidos
- ✅ Contador inicial `i=5`
- ✅ Decrementa en cada generación
- ✅ Se detiene cuando `i=0` (no ejecuta `Sully_0`)
- ✅ Genera exactamente 13 archivos

---

## Técnicas Avanzadas

### 1. Formato Posicional de Printf

El formato `%N$X` permite:
```c
printf("%2$s dice %1$d veces", 3, "hola");
// Resultado: "hola dice 3 veces"
```

**Para quines**:
```c
printf("%1$c%2$c%3$c%1$c", 10, 9, 65);
// Resultado: "\n\tA\n"
```

Reutilizar argumentos es esencial para la auto-referencia.

### 2. String con Doble Escape

En el string `s`, algunos caracteres necesitan escape especial:

- `%%` → Un solo `%` literal
- `%1$c` → Placeholder que será sustituido
- `Sully_%%d.c` → En la salida será `Sully_%d.c`

Ejemplo:
```c
char*s="sprintf(f,%4$cSully_%%d.c%4$c,i);";
```

Cuando se imprime con argumento `34` (comilla):
```c
sprintf(f,"Sully_%d.c",i);
```

### 3. Auto-referencia Cuidadosa

El truco está en que `s` se pasa a sí mismo como argumento:

```c
printf(s, ..., s);
      ↑       ↑
   formato  dato
```

Dentro de `s`, hay un `%4$s` (o `%5$s` en Sully) que recibe el contenido de `s`.

### 4. Buffer para System()

En Sully, el comando es complejo:
```c
sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
```

Esto construye:
```bash
gcc -Wall -Wextra -Werror Sully_5.c -o Sully_5 && ./Sully_5
```

El `&&` asegura que solo se ejecute si la compilación tiene éxito.

### 5. Gestión de Archivos

Patrón común:
```c
FILE*fp=fopen(filename,"w");
fprintf(fp, format, ...);
fclose(fp);
```

**Importante**: Siempre cerrar con `fclose()` para garantizar que el buffer se escriba al disco antes de que `system()` intente compilar el archivo.

---

## Comparación con la Versión ASM

| Aspecto | C | Assembly |
|---------|---|----------|
| **Sintaxis** | Más legible | Más verbosa |
| **Argumentos** | `printf(s,10,9,34,s)` | Registros `rdi,rsi,rdx,rcx,r8` |
| **String** | Literal con escapes | `db` en `.data` section |
| **Stack** | Manejado automáticamente | Manual con `push`/`pop` |
| **Compilación** | `gcc` | `nasm` + `gcc` |
| **Complejidad** | Media | Alta |

---

## Debugging de Quines

### Verificar Colleen
```bash
./Colleen > output.c
diff Colleen.c output.c
# No debe haber diferencias
```

### Verificar Grace
```bash
./Grace
diff Grace.c Grace_kid.c
# No debe haber diferencias
```

### Verificar Sully
```bash
./Sully
ls -1 Sully*
# Debe listar 13 archivos

# Verificar contenido
diff <(cat Sully.c | sed 's/int i=5/int i=4/') Sully_5.c
# No debe haber diferencias excepto el contador
```

### Errores Comunes

1. **Diferencias en whitespace**:
   - Verificar tabs vs espacios
   - Verificar newlines al final del archivo

2. **Problemas con comillas**:
   - Usar `%3$c` con argumento `34`
   - No intentar escapar con `\"`

3. **Argumentos posicionales**:
   - Verificar que `%N$X` usa el índice correcto
   - Recordar que son 1-indexed (no 0-indexed)

4. **Buffer overflow en Sully**:
   - `char f[32]` debe ser suficiente para `Sully_X.c`
   - `char c[128]` debe ser suficiente para el comando completo

---

## Conceptos Teóricos

### Teorema de Recursión de Kleene

Los quines son posibles gracias al **teorema de recursión de Kleene**, que dice:
> Para cualquier función computable f, existe un programa p tal que p produce f(p) como salida.

En un quine, f es la función identidad, por lo que p produce p.

### La Paradoja del Quine

¿Cómo puede un programa describirse a sí mismo sin leerse?

**Respuesta**: Usando una estructura de datos que se describe a sí misma en dos niveles:
1. **Código**: "Imprime X entre comillas, luego X"
2. **Dato X**: "Imprime X entre comillas, luego X"

### Aplicaciones

Los quines no son solo ejercicios teóricos:
- **Virus informáticos**: Los virus auto-replicantes son variantes de quines
- **Compiladores bootstrapping**: Compilador que se compila a sí mismo
- **Teoría de la computación**: Demostración de propiedades de Turing-completeness

---

## Recursos Adicionales

- [Printf format specifiers (C Reference)](https://en.cppreference.com/w/c/io/fprintf)
- [Quine (computing) - Wikipedia](https://en.wikipedia.org/wiki/Quine_(computing))
- [The Quine Page](http://www.nyx.net/~gthompso/quine.htm)
- [42 Project Guide](https://github.com/agavrel/42_CheatSheet)

---

## Tips para Crear Quines

1. **Empieza con la estructura básica**:
   ```c
   char*s="...";
   printf(s, args...);
   ```

2. **Identifica qué necesitas imprimir**:
   - Todo el código antes de `s`
   - La declaración de `s` con comillas
   - Todo el código después de `s`

3. **Codifica con placeholders**:
   - `%1$c` para newlines
   - `%2$c` para tabs
   - `%3$c` para comillas
   - `%N$s` para la auto-referencia

4. **Verifica paso a paso**:
   - Imprime solo una parte primero
   - Verifica que los espacios sean correctos
   - Añade el resto gradualmente

5. **Cuenta los argumentos**:
   - Asegúrate de que cada `%N$X` tenga su argumento correspondiente
   - No olvides el argumento de auto-referencia al final

---

**Autor**: dr-quine C implementation  
**Fecha**: 2026  
**Compilador**: gcc 11+ con flags -Wall -Wextra -Werror  
**Standard**: C99+
