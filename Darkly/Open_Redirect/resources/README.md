# A5 - Open Redirect

Vulnerabilidad del OWASP Top 10 (2017), clasificada dentro de A5: Broken Access Control. Los enlaces a redes sociales de la página pasan por un endpoint interno donde el parámetro `site` controla el destino final de la redirección sin validación en servidor.

---

## Pasos para obtener la flag

### 1. Identificar el vector

Los enlaces a redes sociales tienen esta estructura:
```
index.php?page=redirect&site=facebook
```

El parámetro `site` determina el destino. El backend ejecuta algo como:
```php
header("Location: " . $site);
```

### 2. Explotar

Cambiar el valor del parámetro `site` por cualquier valor no esperado:
```
index.php?page=redirect&site=test
```
La aplicación procesa el valor sin validarlo y devuelve la **flag**.

Para un ataque de phishing real, el valor podría ser una URL externa:
```
index.php?page=redirect&site=https://attacker.example/phishing
```

---

## Impacto

- **Phishing:** el usuario confía en el dominio legítimo y es redirigido a una web maliciosa.
- **Robo de sesión:** combinable con XSS o ingeniería social.
- **Bypass del flujo de navegación:** se altera el comportamiento esperado de la aplicación.

---

## Mitigación

1. **Lista blanca estricta en servidor:** aceptar solo identificadores internos y resolver el destino en backend:
   ```php
   $allowed = [
       'facebook'  => 'https://facebook.com',
       'twitter'   => 'https://twitter.com',
       'instagram' => 'https://instagram.com',
   ];
   $site = $_GET['site'] ?? '';
   if (!array_key_exists($site, $allowed)) {
       http_response_code(400);
       exit('Invalid redirect target');
   }
   header('Location: ' . $allowed[$site]);
   ```
2. **No redirigir a URLs directas del usuario:** solo aceptar claves internas, nunca URLs crudas.
3. **Validar esquema y dominio:** permitir solo `https` y dominios aprobados.
4. **Logging:** registrar valores inesperados en `site` para detectar abusos.
