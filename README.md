# Outer Core

Colección de proyectos de bajo nivel, seguridad y sistemas. Cada carpeta es un proyecto independiente con su propia documentación.

---

## Índice de proyectos

| Proyecto | Área | Descripción breve |
|---|---|---|
| [Cybersecurity_Piscine/Arachnida](#arachnida) | Ciberseguridad | Web scraper de imágenes + extractor de metadatos EXIF |
| [Darkly](#darkly) | Ciberseguridad | CTF de vulnerabilidades web (OWASP Top 10) |
| [dr-quine](#dr-quine) | Recreación teórica | Programas que imprimen su propio código fuente (quines) |
| [ft_ping](#ft_ping) | Redes / C | Reimplementación del comando `ping` con sockets raw |
| [libasm](#libasm) | Ensamblador | Reimplementación de funciones de la libc en x86-64 NASM |
| [woody-woodpacker](#woody-woodpacker) | Seguridad / ELF | Packer ELF64: cifra el segmento `.text` e inyecta un stub de autodescifrado |

---

## Cybersecurity_Piscine/Arachnida

**Ruta:** [`Cybersecurity_Piscine/Arachnida/`](Cybersecurity_Piscine/Arachnida/)
**Documentación:** [README](Cybersecurity_Piscine/Arachnida/README.md)

Toolkit de dos herramientas orientadas al análisis web y forense de imágenes:

- **Spider** (`ex00`) — scraper recursivo que descarga imágenes (`.jpg`, `.png`, `.gif`, `.bmp`) a partir de una URL, respetando dominio y profundidad configurables.
- **Scorpion** (`ex01`) — extractor de metadatos EXIF y atributos de fichero para imágenes locales.

**Tecnologías:** Python 3, `requests`, `BeautifulSoup4`, `Pillow`

---

## Darkly

**Ruta:** [`Darkly/`](Darkly/)
**Documentación:** [README](Darkly/README.md)

CTF basado en una aplicación web vulnerable intencionalmente. Se exploran y documentan 14 vulnerabilidades del **OWASP Top 10 (2017)**, incluyendo:

- SQL Injection (x2)
- Broken Authentication (reset de contraseña, manipulación de cookies, fuerza bruta)
- Subida insegura de ficheros
- Path Traversal
- Cross-Site Scripting (XSS y via Data URI)
- Open Redirect, HTTP Header Validation, Security Misconfiguration, Sensitive Data Exposure

Cada vulnerabilidad tiene su flag y su write-up en `<vuln>/resources/README.md`.

---

## dr-quine

**Ruta:** [`dr-quine/`](dr-quine/)
**Documentación:** [C](dr-quine/C/README.md) · [ASM](dr-quine/ASM/README.md) · [Python](dr-quine/Python/README.md)

Implementación de **quines** — programas que imprimen su propio código fuente exacto sin leer ningún fichero externo. El proyecto incluye tres variantes de complejidad creciente (`Colleen`, `Grace`, `Sully`), cada una implementada en **C** y en **x86-64 Assembly** (NASM).

Explora los conceptos de auto-referencia, formato posicional de `printf` y meta-programación en ensamblador.

---

## ft_ping

**Ruta:** [`ft_ping/`](ft_ping/)
**Documentación:** [README](ft_ping/README.md)

Reimplementación del comando `ping` estándar en C, usando **sockets raw ICMP**. Resuelve nombres de host vía DNS, construye y envía paquetes ICMP Echo Request, y calcula estadísticas de round-trip time (RTT).

**Tecnologías:** C, sockets raw (`SOCK_RAW`), ICMP, DNS resolution manual

---

## libasm

**Ruta:** [`libasm/`](libasm/)
**Documentación:** [README](libasm/README.md)

Reimplementación de funciones estándar de la libc (`strlen`, `strcpy`, `strcmp`, `write`, `read`, `strdup`) en **x86-64 Assembly** (NASM), siguiendo la ABI System V. Las funciones gestionan correctamente `errno` mediante `__errno_location`.

Útil para entender la convención de llamadas de bajo nivel, el uso de syscalls Linux directas y la interoperabilidad entre ensamblador y C.

---

## woody-woodpacker

**Ruta:** [`woody-woodpacker/`](woody-woodpacker/)
**Documentación:** [README](woody-woodpacker/README.md)

Packer de binarios **ELF64** que cifra el segmento ejecutable (`.text`) con XOR de 16 bytes y le inyecta un stub de autodescifrado usando la técnica de **PT_NOTE hijacking**. Al ejecutar el binario empaquetado (`woody`), éste:

1. Imprime `....WOODY....`
2. Descifra el `.text` en memoria
3. Transfiere el control al entry point original

El stub está escrito en NASM x86-64 y se inyecta en tiempo de empaquetado modificando la cabecera del programa ELF.

**Tecnologías:** C, NASM x86-64, formato ELF64, mprotect, XOR cipher
