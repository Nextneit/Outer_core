import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def download_image(url, dest):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(dest, filename)
        
        if os.path.exists(file_path):
            print(f"[SKIP] Ya existe: {filename}")
            return
            
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"[OK] Descargada: {filename} -> {dest}")
    except Exception as e:
        print(f"[ERROR] No se pudo descargar {url} - {e}")

def scrape(url, dest, recursive, depth, visited=None):
    if visited is None:
        visited = set()
    if  url in visited or depth < 0:
        return
    visited.add(url)
    
    print(f"\n[*] Analizando URL (Profundidad restante: {depth}): {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo acceder a {url} - {e}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    images_found = soup.find_all('img')
    print(f"[INFO] Encontradas {len(images_found)} etiquetas <img> en esta página.")
    
    for img in images_found:
        src = img.get('src')
        if not src:
            continue
        full_url = urljoin(url, src)
        ext = os.path.splitext(urlparse(full_url).path)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            download_image(full_url, dest)
    
    if recursive and depth > 0:
        links_found = soup.find_all('a', href=True)
        print(f"[INFO] Buscando enlaces para recursividad... ({len(links_found)} enlaces evaluados)")
        for a in links_found:
            link = urljoin(url, a['href'])
            # Asegurarse de que el enlace sea del mismo dominio y no se haya visitado ya
            if urlparse(link).netloc == urlparse(url).netloc and link not in visited:
                scrape(link, dest, recursive, depth - 1, visited)
      

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