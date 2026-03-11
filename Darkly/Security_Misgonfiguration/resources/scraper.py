import asyncio
import os
from collections import Counter, defaultdict
from urllib.parse import urljoin

from playwright.async_api import async_playwright

# URL base del directorio expuesto en el servidor vulnerable
BASE_URL = "http://10.13.250.153/.hidden/"
# Directorio local donde se guardarán los archivos con posibles flags
OUTPUT_DIR = ".hidden"
# Patrones de texto que podrían indicar que un README contiene la flag
FLAG_PATTERNS = ['flag', 'ctf', '{', '}', 'darkly', '42', 'congratulations']


async def scrape_hidden_directories(page, base_url, readme_contents, visited=None):
    """
    Recorre recursivamente el directorio expuesto siguiendo los enlaces de cada
    página. Los directorios se exploran en profundidad; los archivos README se
    descargan y almacenan en `readme_contents` como tuplas (filename, content, url).
    Se usa `visited` para evitar ciclos.
    """
    if visited is None:
        visited = set()
    if base_url in visited:
        return
    visited.add(base_url)

    try:
        print(f"[*] Visitando: {base_url}")
        await page.goto(base_url, timeout=30000)

        links = await page.query_selector_all('a')
        hrefs = []
        for link in links:
            href = await link.get_attribute('href')
            if href and href != '../':
                hrefs.append(href)

        for href in hrefs:
            full_url = urljoin(base_url, href)
            if href.endswith('/'):
                print(f"[+] Directorio encontrado: {href}")
                await scrape_hidden_directories(page, full_url, readme_contents, visited)
            elif 'README' in href:
                print(f"[+] README encontrado: {full_url}")
                await read_readme_content(page, full_url, readme_contents)

    except Exception as e:
        print(f"[!] Error al visitar {base_url}: {e}")


async def read_readme_content(page, url, readme_contents):
    """
    Descarga el contenido de un README vía HTTP sin navegar a él (usa
    `page.request.get`). Almacena la tupla (filename, content, url) en
    `readme_contents` solo si la petición es exitosa.
    """
    try:
        response = await page.request.get(url)
        if response.ok:
            content = (await response.text()).strip()
            filename = url.replace('http://', '').replace('/', '_').replace(':', '_') + '.txt'
            readme_contents.append((filename, content, url))
            print(f"[✓] Leído: {filename}")
        else:
            print(f"[!] Error HTTP {response.status} al leer {url}")
    except Exception as e:
        print(f"[!] Error al leer {url}: {e}")


def save_unique_flags(readme_contents, directory):
    """
    Analiza los contenidos recolectados y guarda solo los que son raros
    (aparecen 5 veces o menos), ya que el contenido repetido corresponde
    al README genérico del laberinto y los únicos son candidatos a flag.

    Adicionalmente busca patrones conocidos de flags en todos los contenidos
    para cubrir casos donde la flag aparezca más de 5 veces.
    """
    content_count = Counter(content for _, content, _ in readme_contents)
    content_to_files = defaultdict(list)
    for filename, content, url in readme_contents:
        content_to_files[content].append((filename, url))

    print(f"[+] Total de archivos: {len(readme_contents)}")
    print(f"[+] Contenidos únicos: {len(content_count)}\n")

    # --- Contenidos raros (posibles flags por frecuencia) ---
    rare_contents = [(content, count) for content, count in content_count.items() if count <= 5]

    if not rare_contents:
        print("[!] No se encontraron contenidos únicos o raros.")
    else:
        os.makedirs(directory, exist_ok=True)
        print("=" * 60)
        print(f"[!!!] ENCONTRADAS {len(rare_contents)} POSIBLES FLAGS:")
        print("=" * 60)

        for idx, (content, count) in enumerate(rare_contents, 1):
            files = content_to_files[content]
            filename, _ = files[0]
            filepath = os.path.join(directory, filename)

            print(f"\n[FLAG {idx}] Aparece {count} vez/veces:")
            print(f"Contenido: {content}")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[✓] Guardado en: {filepath}")
            print(f"URLs: {', '.join(url for _, url in files[:3])}")

        print("\n" + "=" * 60)
        print(f"[*] Solo se guardaron {len(rare_contents)} archivos (posibles flags)")
        print("=" * 60)

    # --- Búsqueda de patrones conocidos de flag ---
    print("\n" + "=" * 60)
    print("BÚSQUEDA DE PATRONES DE FLAG:")
    print("=" * 60)
    found_pattern = False
    for content, files in content_to_files.items():
        content_lower = content.lower()
        for pattern in FLAG_PATTERNS:
            if pattern in content_lower:
                print(f"\n[FLAG POTENTIAL] Patrón '{pattern}' encontrado en:")
                print(f"Archivo: {files[0][0]}")
                print(f"Contenido: {content}")
                found_pattern = True
                break
    if not found_pattern:
        print("[!] No se encontraron patrones conocidos de flag.")


async def main():
    readme_contents = []
    print(f"[*] Iniciando scraper en {BASE_URL}")
    print(f"[*] Recolectando todos los README en memoria...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await scrape_hidden_directories(page, BASE_URL, readme_contents)
        await browser.close()

    print("\n[*] Scraping completado!")
    print(f"[*] Analizando {len(readme_contents)} archivos...\n")
    save_unique_flags(readme_contents, OUTPUT_DIR)


if __name__ == "__main__":
    asyncio.run(main())
