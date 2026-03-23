import os
import argparse
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
REQUEST_TIMEOUT = 10
MIME_TO_EXTENSION = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/bmp': '.bmp',
    'image/x-ms-bmp': '.bmp',
}

def download_image(url, dest):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        save_image_response(url, response, dest)
    except Exception as e:
        print(f"[ERROR] No se pudo descargar {url} - {e}")


def process_image_url(url, dest, seen_images):
    if url in seen_images:
        return False
    seen_images.add(url)
    download_image(url, dest)
    return True


def process_image_response(url, response, dest, seen_images):
    if url in seen_images:
        return False
    seen_images.add(url)
    save_image_response(url, response, dest)
    return True

def infer_extension_from_content_type(content_type):
    if not content_type:
        return None
    mime = content_type.split(';', 1)[0].strip().lower()
    return MIME_TO_EXTENSION.get(mime)


def is_html_content_type(content_type):
    value = (content_type or '').lower()
    return 'text/html' in value or 'application/xhtml+xml' in value


def build_unique_filename(url, ext, fallback_base='image'):
    path = urlparse(url).path
    base_name = os.path.basename(path)
    stem = os.path.splitext(base_name)[0] or fallback_base
    # Hash corto y estable para evitar colisiones entre URLs distintas.
    short_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()[:10]
    return f"{stem}_{short_hash}{ext}"


def save_image_response(url, response, dest):
    content_type = response.headers.get('Content-Type', '')
    path = urlparse(url).path
    filename = os.path.basename(path) or 'image'
    ext = os.path.splitext(filename)[1].lower()
    inferred_ext = infer_extension_from_content_type(content_type)

    # Criterio 1: extension permitida en la URL.
    # Criterio 2: URL sin extension (o extension no valida) pero MIME permitido.
    if ext in ALLOWED_EXTENSIONS:
        final_ext = ext
    elif inferred_ext in ALLOWED_EXTENSIONS:
        final_ext = inferred_ext
    else:
        print(f"[SKIP] Formato no permitido: {url} (Content-Type: {content_type or 'desconocido'})")
        return

    # Generar un nombre unico y estable para evitar colisiones entre rutas.
    filename = build_unique_filename(url, final_ext)
    file_path = os.path.join(dest, filename)

    if os.path.exists(file_path):
        print(f"[SKIP] Ya existe: {filename}")
        return

    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"[OK] Descargada: {filename} -> {dest}")


def scrape(url, dest, recursive, depth, visited=None, seen_images=None):
    if visited is None:
        visited = set()
    if seen_images is None:
        seen_images = set()
    if  url in visited or depth < 0:
        return
    visited.add(url)
    
    print(f"\n[*] Analizando URL (Profundidad restante: {depth}): {url}")
    
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo acceder a {url} - {e}")
        return

    content_type = response.headers.get('Content-Type', '').lower()
    if infer_extension_from_content_type(content_type) in ALLOWED_EXTENSIONS:
        process_image_response(url, response, dest, seen_images)
        print(f"[INFO] Saltando parseo HTML en {url} (Content-Type: {content_type or 'desconocido'})")
        return

    if not is_html_content_type(content_type):
        print(f"[INFO] Saltando parseo HTML en {url} (Content-Type: {content_type or 'desconocido'})")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    images_found = soup.find_all('img')
    print(f"[INFO] Encontradas {len(images_found)} etiquetas <img> en esta página.")
    
    for img in images_found:
        src = img.get('src')
        if not src:
            continue
        if src.startswith('data:'):
            print("[SKIP] Imagen embebida en data URI.")
            continue
        full_url = urljoin(url, src)
        process_image_url(full_url, dest, seen_images)

    links_found = soup.find_all('a', href=True)
    linked_images = 0
    for a in links_found:
        link = urljoin(url, a['href'])
        ext = os.path.splitext(urlparse(link).path)[1].lower()
        if ext in ALLOWED_EXTENSIONS and process_image_url(link, dest, seen_images):
            linked_images += 1

    if linked_images:
        print(f"[INFO] Descargadas {linked_images} imágenes desde enlaces <a>.")
    
    if recursive:
        pending_links = []
        for a in links_found:
            link = urljoin(url, a['href'])
            # Asegurarse de que el enlace sea del mismo dominio y no se haya visitado ya
            if urlparse(link).netloc == urlparse(url).netloc and link not in visited:
                pending_links.append(link)

        if depth > 0:
            print(f"[INFO] Buscando enlaces para recursividad... ({len(links_found)} enlaces evaluados)")
            for link in pending_links:
                scrape(link, dest, recursive, depth - 1, visited, seen_images)
        elif pending_links:
            print(
                f"[INFO] Límite de profundidad alcanzado en {url}. "
                f"Quedan {len(pending_links)} enlaces pendientes sin visitar."
            )
      

def main():
    parser = argparse.ArgumentParser(description='Spider - image scraper')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-r', action='store_true', help='Recursive download')
    parser.add_argument('-l', type=int, default=5, help='Max depth (default: 5)')
    parser.add_argument('-p', default='./data/', help='Save path (default: ./data/)')
    args = parser.parse_args()

    print(f"--- Iniciando Spider ---")
    print(f"URL: {args.url}")
    print(f"Ruta: {args.p}")
    print(f"Recursividad: {'ON' if args.r else 'OFF'} (Prof: {args.l})")
    print(f"------------------------\n")

    os.makedirs(args.p, exist_ok=True)
    scrape(args.url, args.p, args.r, args.l)
    print("\n[+] Extracción finalizada.")

if __name__ == '__main__':
    main()