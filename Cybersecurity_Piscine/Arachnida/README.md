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

A forensic metadata extraction, manipulation, and sanitization tool for image files. It parses EXIF data and basic file attributes, allowing users to deeply analyze media.

### Usage (CLI Mode)

To extract and display read-only metadata from one or multiple files in the terminal:
```bash
python3 scorpion.py FILE1 [FILE2 ...]
```

### Supported Extensions

`.jpg` / `.jpeg` / `.png` / `.gif` / `.bmp`

### Output (CLI)

For each file, Scorpion displays:

- Image format, color mode, and dimensions
- File size in bytes
- Creation and last modification timestamps
- All available EXIF tags (or PNG info chunks) with human-readable labels

### Bonus Features (GUI Mode)

Scorpion includes a complete **Graphical User Interface (GUI)** using `tkinter` that enables advanced anti-forensic capabilities (Metadata Modification and Destruction).

To launch the GUI, run the command without any file arguments:
```bash
python3 scorpion.py
```

**GUI Capabilities:**
- **Visual Table:** Instantly browse through image properties in an interactive and scrollable metadata tree.
- **Strip EXIF (Clean):** With the click of a button, permanently delete all tracking data (GPS, Camera Make, Software) from`.jpg` and `.png` files, exporting a 100% sanitized copy.
- **Save Modified EXIF:** Edit rows directly in the visual table and inject the manipulated metadata back into a fresh image to create decoys or bypass filters.

### Dependencies

```bash
pip install Pillow piexif
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
