# Arachnida

A two-part web scraping toolkit focused on image extraction and metadata analysis.

---

## Exercise 00 — Spider

A recursive web scraper that downloads images from a target URL.

### Usage

```bash
python3 spider.py [-r] [-l DEPTH] [-p PATH] URL
```

| Flag | Description | Default |
|------|-------------|---------|
| `-r` | Enable recursive crawling | Disabled |
| `-l DEPTH` | Maximum recursion depth | `5` |
| `-p PATH` | Directory to save downloaded images | `./data/` |

### Supported Extensions

`.jpg` / `.jpeg` / `.png` / `.gif` / `.bmp`

### Examples

```bash
# Download images from a single page
python3 spider.py https://example.com

# Recursive crawl with default depth (5)
python3 spider.py -r https://example.com

# Recursive crawl, custom depth and output directory
python3 spider.py -r -l 3 -p ./images/ https://example.com
```

### Notes

- Crawling is restricted to the same domain as the target URL to prevent unintended traversal.
- Visited URLs are tracked to avoid infinite loops in cyclic link structures.

### Dependencies

```bash
pip install requests beautifulsoup4
```

---

## Exercise 01 — Scorpion

A metadata extraction tool for image files. Parses EXIF data and basic file attributes and displays them in a structured format.

### Usage

```bash
python3 scorpion.py FILE1 [FILE2 ...]
```

### Supported Extensions

`.jpg` / `.jpeg` / `.png` / `.gif` / `.bmp`

### Output

For each file, Scorpion displays:

- Image format, color mode, and dimensions
- File size in bytes
- Creation and last modification timestamps
- All available EXIF tags with human-readable labels

### Examples

```bash
python3 scorpion.py photo.jpg
python3 scorpion.py img1.png img2.jpg img3.bmp
```

### Dependencies

```bash
pip install Pillow
```

---

## Project Structure

```
Arachnida/
├── ex00/
│   ├── spider.py
│   └── requirements.txt
└── ex01/
    ├── scorpion.py
    └── requirements.txt
```
