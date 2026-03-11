# A6 - Security Misconfiguration

Vulnerabilidad del OWASP Top 10 (2017). El servidor expone públicamente el directorio `.hidden` en la raíz web, que contiene más de 35.000 archivos README distribuidos en una estructura laberíntica de subdirectorios. La flag está enterrada entre ellos.

---

## Pasos para obtener la flag

### 1. Descubrir el directorio expuesto

Durante el reconocimiento (nmap, enumeración web) se detecta:
```
http://<IP>/.hidden/
```
El servidor lista el contenido en lugar de denegar el acceso.

### 2. Automatizar la búsqueda

La profundidad y el volumen hacen inviable la búsqueda manual. Se usa el script `scraper.py` (playwright) para recorrer recursivamente todos los subdirectorios, recolectar el contenido de cada README en memoria y filtrar los que aparecen pocas veces (posibles flags).

```bash
python3 scraper.py
```

El script guarda en `.hidden/` únicamente los archivos con contenido único o raro (≤5 apariciones), que son los candidatos a flag.

### 3. Por qué funciona

- El servidor no restringe el acceso a dotfiles (archivos/carpetas que empiezan por `.`).
- El listado de directorios (`autoindex`) está habilitado, permitiendo navegar toda la estructura.
- La "seguridad por oscuridad" (esconder la flag entre miles de archivos) no es una medida de control real: un atacante con herramientas básicas de scraping la encuentra.

---

## Impacto

- **Information Leakage:** exposición de archivos que deberían ser inaccesibles.
- **Reconocimiento facilitado:** revela la estructura interna del servidor, facilitando buscar `.git`, `.env`, `.htaccess` u otros archivos críticos.
- **Superficie de ataque ampliada:** cualquier dato sensible depositado bajo la premisa de "nadie lo encontrará" queda expuesto.

---

## Mitigación

1. **Denegar acceso a dotfiles en Nginx:**
   ```nginx
   location ~ /\.(.*) {
       deny all;
   }
   ```
   **En Apache (.htaccess):**
   ```apache
   RedirectMatch 404 /\..*$
   ```

2. **Deshabilitar el listado de directorios:**
   - Nginx: `autoindex off;`
   - Apache: `Options -Indexes`

3. **Política de lista blanca:** el servidor solo debe servir los assets necesarios (HTML, JS, CSS, imágenes). Cualquier otra ruta devuelve `403` o `404`.

4. **Eliminar contenido no esencial antes de producción:** aplicar el principio de superficie de ataque mínima; borrar directorios de prueba, temporales y estructuras no funcionales.
