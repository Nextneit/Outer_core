# A6 - Sensitive Data Exposure (Admin Credentials)

Vulnerabilidad del OWASP Top 10 (2017). Las credenciales de administrador están expuestas en un archivo accesible públicamente, descubierto a través del `robots.txt` del servidor.

---

## Pasos para obtener la flag

### 1. Reconocimiento

El escaneo con nmap revela dos rutas en `robots.txt`:
```
/whatever
/.hidden
```

Estas rutas intentan ocultarse de motores de búsqueda, pero son accesibles sin autenticación.

### 2. Acceder a `/whatever`

```
http://<IP>/whatever/
```

El directorio contiene un archivo con credenciales en texto plano:
```
root:437394baff5aa33daa618be47b75cb49
```

### 3. Descifrar la contraseña

El hash `437394baff5aa33daa618be47b75cb49` es MD5 → descifra a `qwerty123@`.

> Herramienta: [md5decrypt.net](https://md5decrypt.net/en/)

### 4. Acceder al panel de administración

1. Navegar a `http://<IP>/admin`
2. Introducir las credenciales:
   - **Usuario:** `root`
   - **Contraseña:** `qwerty123@`
3. Acceso concedido → se muestra la **flag**.

---

## Flujo del ataque

```
Nmap → robots.txt → /whatever → credenciales → /admin → flag
```

---

## Impacto

- **Exposición de credenciales:** contraseñas almacenadas en archivos públicos.
- **Cifrado débil:** MD5 es trivialmente reversible con rainbow tables.
- **robots.txt como pista:** listar rutas sensibles en `robots.txt` las hace más obvias para atacantes.
- **Compromiso total:** acceso completo al panel administrativo.

---

## Mitigación

1. **Nunca almacenar credenciales en archivos dentro del webroot.**
2. **Usar hashing fuerte:** `password_hash($pass, PASSWORD_ARGON2ID)` en lugar de MD5.
3. **No listar recursos sensibles en `robots.txt`:** protegerlos con autenticación real, no intentar ocultarlos.
4. **Usar variables de entorno** para secretos en lugar de hardcodearlos.
5. **Auditorías regulares:** buscar archivos `.txt`, `.bak`, `.old` expuestos en el webroot.
   ```bash
   find /var/www/html -name "*.txt" -o -name "*.bak" -o -name "*.old"
   ```
