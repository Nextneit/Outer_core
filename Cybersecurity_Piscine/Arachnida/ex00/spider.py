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
        with open(os.path.join(dest, filename), 'wb') as f:
            f.write(response.content)
    except Exception:
        pass

def scrape(url, dest, recursive, depth, visited=None):
    if visited is None:
        visited = set()
    if  url in visited or depth < 0:
        return
    visited.add(url)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        full_url = urljoin(url, src)
        ext = os.path.splitext(urlparse(full_url).path)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            download_image(full_url, dest)
    
    if recursive:
        for a in soup.find_all('a', href=True):
            link = urljoin(url, a['href'])
            if urlparse(link).netloc == urlparse(url).netloc:
                scrape(link, dest, recursive, depth - 1, visited)
      

def main():
    parser = argparse.ArgumentParser(description='Spider - image scraper')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-r', action='store_true', help='Recursive download')
    parser.add_argument('-l', type=int, default=5, help='Max depth (default: 5)')
    parser.add_argument('-p', default='./data/', help='Save path (default: ./data/)')
    args = parser.parse_args()

    os.makedirs(args.p, exist_ok=True)
    scrape(args.url, args.p, args.r, args.l)

if __name__ == '__main__':
    main()