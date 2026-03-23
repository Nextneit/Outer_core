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

### Usage (CLI)

General command:

```bash
python3 scorpion.py [--gui] [--strip] [--set KEY=VALUE ...] [--out OUTPUT] [FILE ...]
```

If run without arguments, Scorpion prints the help message.

Read-only extraction for one or multiple files:

```bash
python3 scorpion.py FILE1 [FILE2 ...]
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--gui` | Launch graphical interface |
| `--strip` | Remove metadata from exactly one input file (`.jpg/.jpeg/.png`) |
| `--set KEY=VALUE` | Set/modify metadata (repeatable). Requires exactly one input file |
| `--out OUTPUT` | Output path used with `--strip` or `--set` |

Examples:

```bash
# Show read-only metadata
python3 scorpion.py image.jpg

# Strip metadata
python3 scorpion.py --strip image.jpg --out cleaned.jpg

# Modify JPEG metadata (EXIF tags)
python3 scorpion.py image.jpg --set 0th.Artist="ncruz" --set Exif.UserComment="test" --out modified.jpg

# Modify PNG text metadata
python3 scorpion.py image.png --set Author="ncruz" --set Description="demo" --out modified.png

# Launch GUI explicitly
python3 scorpion.py --gui
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

To launch the GUI:

```bash
python3 scorpion.py --gui
```

**GUI Capabilities:**
- **Visual Table:** Instantly browse through image properties in an interactive and scrollable metadata tree.
- **Strip EXIF (Clean):** With the click of a button, permanently delete all tracking data (GPS, Camera Make, Software) from `.jpg` and `.png` files, exporting a 100% sanitized copy.
- **Save Modified EXIF:** Edit rows directly in the visual table and inject the manipulated metadata back into a fresh image to create decoys or bypass filters.

### Internal Architecture (Refactor)

Scorpion is split into clear layers:

- `scorpion.py`: CLI entry point and flow control.
- `gui_bonus.py`: all GUI creation, layout, and GUI interactions.
- `metadata_service.py`: shared metadata business logic (read/parse/convert/strip/modify) used by both CLI and GUI.

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
    ├── gui_bonus.py
    ├── metadata_service.py
    ├── scorpion.py
    └── requirements.txt
```
