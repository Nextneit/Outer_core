# A7 - Cross-Site Scripting (XSS)

Vulnerabilidad del OWASP Top 10 (2017). El formulario de feedback valida la entrada solo en el cliente (JavaScript). El servidor no sanitiza la entrada, permitiendo inyectar código JavaScript que se ejecuta en el navegador.

---

## Pasos para obtener la flag

### 1. Identificar el vector

El formulario de feedback tiene una validación en cliente con `validate_form()`. Esta validación es trivialmente eludible sin tocar el servidor.

### 2. Explotar

**Opción A – Anular la validación desde la consola (F12):**
```js
function validate_form(thisform) {
    with (thisform) {
        if (validate_required(txtName,"Name can not be empty.")==false)
        {txtName.focus();return true;}
        if (validate_required(mtxMessage,"Message can not be empty.")==false)
        {mtxtMessage.focus();return true;}
    }
}
```
Tras redefinir la función, enviar el formulario con cualquier payload (ej. `<script>alert("XSS")</script>`) → el servidor devuelve la **flag**.

**Opción B – Burp Suite:**
Interceptar el POST y enviar directamente:
```
txtName=<script>alert("XSS")</script>&mtxtMessage=test
```

### 3. Por qué funciona

La validación cliente es fácilmente eludible. El servidor no aplica ningún `htmlspecialchars`, escape ni filtrado sobre los datos recibidos, por lo que el payload se procesa y la flag se muestra.

> **Nota:** El código HTML usa `mtxtMessage` como nombre del textarea, pero el JS referencia `mtxMessage` (sin la `t`). Este bug hace que la validación falle internamente, lo que en la práctica también permite bypassearla sin modificar nada.

---

## Impacto

- **Robo de cookies/sesión:** `document.cookie` expuesto a atacantes.
- **Phishing:** inyección de formularios falsos para capturar credenciales.
- **Redirección maliciosa:** enviar usuarios a sitios de phishing.
- **Acciones en nombre del usuario:** peticiones autenticadas sin conocimiento del usuario.

---

## Mitigación

1. **Sanitizar en servidor:**
   ```php
   $feedback = htmlspecialchars($_POST['feedback'], ENT_QUOTES, 'UTF-8');
   ```
2. **Usar librerías de sanitización** (ej. HTML Purifier) para contenido enriquecido.
3. **Content Security Policy (CSP):**
   ```html
   <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
   ```
4. **Nunca confiar en validaciones del cliente** para seguridad; son solo para UX.
5. **Frameworks modernos:** usar templating engines que escapen automáticamente el output.
