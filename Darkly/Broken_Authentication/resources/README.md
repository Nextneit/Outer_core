# A2 - Broken Authentication (Reset Password)

Vulnerabilidad del OWASP Top 10 (2017). En la pantalla de reset de contraseña, el email destino viaja en un campo oculto del formulario que el servidor acepta sin validación, permitiendo redirigir el reset a cualquier cuenta.

---

## Pasos para obtener la flag

### 1. Identificar el vector

En el formulario de recuperación, el email destino está en un campo `hidden`:
```html
<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">
```
Aunque no es editable visualmente, puede modificarse desde las DevTools del navegador o interceptando la petición.

### 2. Explotar

1. Abrir las herramientas de desarrollador (F12) e inspeccionar el formulario.
2. Localizar el campo `mail`.
3. Cambiar su valor a:
   ```
   root@borntosec.co
   ```
4. Enviar el formulario → la aplicación procesa el reset para ese email y devuelve la **flag**.

### 3. Por qué funciona

- La restricción estaba solo en el cliente (HTML/UI).
- El backend no verifica la identidad ni la autorización del email recibido.
- Acepta el parámetro manipulado sin comprobar su origen.

---

## Impacto

- **Account Takeover:** reset sobre cuentas privilegiadas sin autorización.
- **Escalada de privilegios:** si se compromete un usuario administrador.
- **Pérdida de confidencialidad:** acceso a cuentas con datos sensibles.

---

## Mitigación

1. **No confiar en campos del cliente para identidad sensible:** el email objetivo debe determinarse en servidor (ej. desde la sesión), nunca desde parámetros manipulables.
2. **Tokens robustos:** aleatorios, de un solo uso, con expiración corta y ligados a una cuenta específica.
3. **No usar campos `hidden` para datos sensibles:** son totalmente modificables por el usuario.
4. **Rate limiting y logging** de intentos anómalos de reset.
5. **Mensajes genéricos:** no revelar si un correo existe o no en el sistema.
