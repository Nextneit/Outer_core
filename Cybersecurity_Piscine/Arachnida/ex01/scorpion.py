import os
import sys
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def get_basic_info(filepath):
    stat = os.stat(filepath)
    created = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    size = stat.st_size
    return created, modified, size


def extract_exif(filepath):
    try:
        img = Image.open(filepath)
    except Exception as e:
        print(f"Error opening file: {e}")
        return
    
    created, modified, size = get_basic_info(filepath)
    print(f"  Format      : {img.format}")
    print(f"  Mode        : {img.mode}")
    print(f"  Size        : {img.size[0]}x{img.size[1]} px")
    print(f"  File size   : {size} bytes")
    print(f"  Created     : {created}")
    print(f"  Modified    : {modified}")
    
    exif_data = img._getexif() if hasattr(img, '_getexif') else None
    if exif_data:
        print("--- EXIF DATA ---")
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag:<30}: {value}")
    else:
        print("No EXIF data found")

    
def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} FILE1 [FILE2...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        print(f"\n[{filepath}]")
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            print(f"  Unsupported extension: {ext}")
            continue
        if not os.path.isfile(filepath):
            print(f"  File not found.")
            continue
        extract_exif(filepath)

if __name__ == '__main__':
    main()