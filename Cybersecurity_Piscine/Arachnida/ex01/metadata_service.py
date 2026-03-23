"""Metadata service layer for Scorpion (CLI + GUI).

This module centralizes all metadata-related operations used by both:
1) the command line interface (scorpion.py), and
2) the bonus graphical interface (gui_bonus.py).

Main responsibilities:
- Read basic file/image information.
- Extract and print metadata in console mode.
- Normalize metadata values for GUI display.
- Convert user-provided text values to EXIF-compatible binary types.
- Load metadata rows in a UI-friendly structure.
- Strip metadata from JPEG/PNG files.
- Modify metadata in JPEG/PNG files and write output files.

Design goals:
- Keep business logic out of UI layer.
- Reuse exactly the same conversion/validation rules from CLI and GUI.
- Keep behavior explicit for subject requirements and evaluation.
"""

import os
import ast
import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngInfo
import piexif

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
JPEG_IFD_NAMES = ('0th', 'Exif', 'GPS', '1st')
MODIFIABLE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def format_exif_value(value):
    """Format a raw EXIF value to a readable string for UI/console.

    Rules:
    - bytes are decoded as UTF-8 (invalid bytes ignored) and trailing NULL is removed.
    - undecodable bytes fall back to repr(value).
    - all other types are converted with str().
    """
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8', errors='ignore').rstrip('\x00')
        except Exception:
            return repr(value)
    return str(value)


def _parse_int_or_int_tuple(text):
    """Parse user text to int or tuple[int, ...].

    Accepted inputs:
    - "123"
    - "(1, 2, 3)"
    - "1,2,3"
    """
    value = text.strip()
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, int):
            return parsed
        if isinstance(parsed, (tuple, list)) and all(isinstance(x, int) for x in parsed):
            return tuple(parsed)
    except Exception:
        pass

    value = value.strip('()[]')
    if ',' in value:
        return tuple(int(part.strip()) for part in value.split(',') if part.strip())
    return int(value)


def _parse_rational(text):
    """Parse one rational value as (num, den).

    Accepted inputs:
    - "(72, 1)"
    - "72/1"
    - "72,1"
    - "72" -> (72, 1)
    """
    value = text.strip()
    try:
        parsed = ast.literal_eval(value)
        if (
            isinstance(parsed, (tuple, list))
            and len(parsed) == 2
            and all(isinstance(x, int) for x in parsed)
        ):
            return (int(parsed[0]), int(parsed[1]))
    except Exception:
        pass

    value = value.strip('()[]')
    if '/' in value:
        num, den = value.split('/', 1)
        return (int(num.strip()), int(den.strip()))
    if ',' in value:
        num, den = value.split(',', 1)
        return (int(num.strip()), int(den.strip()))
    return (int(value), 1)


def _parse_rational_or_tuple(text):
    """Parse one rational or a tuple of rationals.

    Accepted inputs:
    - single rational: "(72, 1)", "72/1", "72,1"
    - many rationals: "((1, 1), (2, 1))"
    - many rationals (alt): "1/1;2/1;3/1"
    """
    value = text.strip()
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, (tuple, list)):
            if len(parsed) == 2 and all(isinstance(x, int) for x in parsed):
                return (int(parsed[0]), int(parsed[1]))

            rationals = []
            for item in parsed:
                if (
                    isinstance(item, (tuple, list))
                    and len(item) == 2
                    and all(isinstance(x, int) for x in item)
                ):
                    rationals.append((int(item[0]), int(item[1])))
                else:
                    raise ValueError('Invalid rational tuple element')
            if rationals:
                return tuple(rationals)
    except Exception:
        pass

    if ';' in value:
        return tuple(_parse_rational(part) for part in value.split(';') if part.strip())
    return _parse_rational(value)


def convert_user_value_for_exif(value_type, user_text):
    """Convert editable text from UI/CLI to a value compatible with piexif.

    Args:
    - value_type: one of piexif.TYPES.*
    - user_text: user-provided text input

    Returns:
    - value in the exact Python shape expected by piexif for that type.
    """
    text = user_text.strip()
    if value_type == piexif.TYPES.Ascii:
        return text.encode('utf-8', errors='ignore') + b'\x00'
    if value_type in (piexif.TYPES.Byte, piexif.TYPES.Short, piexif.TYPES.Long, piexif.TYPES.SLong):
        return _parse_int_or_int_tuple(text)
    if value_type in (piexif.TYPES.Rational, piexif.TYPES.SRational):
        return _parse_rational_or_tuple(text)
    if value_type == piexif.TYPES.Undefined:
        return text.encode('utf-8', errors='ignore')
    return text


def get_basic_info(filepath):
    """Return (created, modified, size_bytes) for a file path."""
    stat = os.stat(filepath)
    created = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    size = stat.st_size
    return created, modified, size


def extract_exif(filepath):
    """Print image basic info + metadata to stdout.

    This is the read-only console path used when user passes file arguments
    without --strip / --set.
    """
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
    png_info = img.info if img.format == 'PNG' and img.info else None

    if exif_data:
        print('--- EXIF DATA ---')
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag:<30}: {value}")
    elif png_info:
        print('--- PNG INFO/METADATA ---')
        for key, value in png_info.items():
            if key not in ['dpi', 'icc_profile', 'vpi']:
                print(f"{key:<30}: {value}")
    else:
        print('No EXIF/Metadata found')


def load_metadata_rows(filepath):
    """Load metadata rows in a structure directly consumable by GUI treeview.

    Returns:
    - exif_dict: raw piexif dict for JPEG (or None)
    - rows: list of dicts with shape:
        {
            'tag': '<display tag>',
            'value': '<display value>',
            'meta': {'ifd': str, 'tag_id': int, 'type': int} or None
        }

    Notes:
    - For JPEG + piexif data, rows include machine metadata in 'meta' so GUI
      can write modified values back to correct EXIF tag/type.
    - For PNG/other fallback rows, 'meta' is None (display-oriented).
    """
    rows = []
    try:
        exif_dict = piexif.load(filepath)
    except Exception:
        exif_dict = None

    img = Image.open(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    exif_data = img._getexif() if hasattr(img, '_getexif') else None

    if ext in {'.jpg', '.jpeg'} and exif_dict:
        for ifd_name in JPEG_IFD_NAMES:
            ifd_data = exif_dict.get(ifd_name) or {}
            for tag_id, value in ifd_data.items():
                tag_info = piexif.TAGS[ifd_name].get(tag_id, {})
                tag_name = tag_info.get('name', str(tag_id))
                value_type = tag_info.get('type')
                rows.append({
                    'tag': f'{ifd_name}.{tag_name}',
                    'value': format_exif_value(value),
                    'meta': {'ifd': ifd_name, 'tag_id': tag_id, 'type': value_type},
                })
    elif exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8', errors='ignore')
                except Exception:
                    value = '<Binary Data>'
            rows.append({'tag': str(tag_name), 'value': str(value), 'meta': None})
    elif img.format == 'PNG' and img.info:
        for key, value in img.info.items():
            if key not in ['dpi', 'icc_profile', 'vpi']:
                rows.append({'tag': str(key), 'value': str(value), 'meta': None})
    else:
        rows.append({'tag': 'No EXIF data', 'value': 'found', 'meta': None})

    return exif_dict, rows


def _default_output_path(filepath, prefix):
    """Build default output path as '<prefix>_<original_name>' in same folder."""
    directory = os.path.dirname(filepath)
    base = os.path.basename(filepath)
    return os.path.join(directory, f'{prefix}_{base}')


def parse_set_items(items):
    """Parse repeated --set KEY=VALUE arguments into a dict.

    Raises ValueError on malformed entries.
    """
    updates = {}
    for item in items:
        if '=' not in item:
            raise ValueError(f"Invalid --set value '{item}'. Expected KEY=VALUE")
        key, value = item.split('=', 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --set key in '{item}'")
        updates[key] = value
    return updates


def _find_jpeg_tag(tag_key):
    """Resolve a user-facing JPEG tag name to (ifd_name, tag_id, value_type).

    Supported key formats:
    - explicit: "Exif.UserComment"
    - simple: "UserComment" (must be unique across known IFDs)

    Raises KeyError when tag is unknown or ambiguous.
    """
    key = tag_key.strip()

    if '.' in key:
        ifd_part, tag_part = key.split('.', 1)
        ifd_name = ifd_part.strip()
        tag_name = tag_part.strip().lower()
        if ifd_name not in JPEG_IFD_NAMES:
            raise KeyError(f"Unknown IFD '{ifd_name}'")

        for tag_id, info in piexif.TAGS[ifd_name].items():
            if info.get('name', '').lower() == tag_name:
                return ifd_name, tag_id, info.get('type')
        raise KeyError(f"Unknown JPEG tag '{tag_key}'")

    matches = []
    tag_name = key.lower()
    for ifd_name in JPEG_IFD_NAMES:
        for tag_id, info in piexif.TAGS[ifd_name].items():
            if info.get('name', '').lower() == tag_name:
                matches.append((ifd_name, tag_id, info.get('type')))

    if not matches:
        raise KeyError(f"Unknown JPEG tag '{tag_key}'")
    if len(matches) > 1:
        sample_ifd, sample_tag_id, _ = matches[0]
        sample_name = piexif.TAGS[sample_ifd][sample_tag_id].get('name', str(sample_tag_id))
        raise KeyError(
            f"Ambiguous JPEG tag '{tag_key}'. Use IFD.TagName format, e.g. {sample_ifd}.{sample_name}"
        )
    return matches[0]


def strip_metadata(filepath, out_path=None):
    """Remove metadata from JPEG/PNG and save output file.

    JPEG: uses piexif.remove.
    PNG: rewrites pixel data into a new image to drop text chunks/metadata.

    Returns output path.
    """
    ext = os.path.splitext(filepath)[1].lower()
    output = out_path or _default_output_path(filepath, 'cleaned')

    if ext in {'.jpg', '.jpeg'}:
        piexif.remove(filepath, output)
    elif ext in MODIFIABLE_EXTENSIONS:
        img = Image.open(filepath)
        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)
        clean_img.save(output, 'PNG')
    else:
        raise ValueError('Strip operation is only supported for JPEG and PNG files')

    print(f'[OK] Metadata stripped: {output}')
    return output


def write_jpeg_exif(source_path, exif_dict, output_path):
    """Serialize exif_dict and write it into a JPEG output file."""
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, source_path, output_path)


def save_png_text_metadata(source_path, metadata_map, output_path):
    """Save PNG with provided text metadata map (key/value text pairs)."""
    img = Image.open(source_path)
    meta = PngInfo()
    for key, value in metadata_map.items():
        meta.add_text(str(key), str(value))
    img.save(output_path, 'PNG', pnginfo=meta)


def modify_metadata(filepath, updates, out_path=None):
    """Modify metadata in JPEG/PNG and save output file.

    JPEG flow:
    - load exif dict
    - resolve each update key to concrete EXIF tag
    - convert each text value to expected EXIF binary type
    - write updated EXIF

    PNG flow:
    - preserve existing textual metadata from img.info
    - merge with updates
    - save PNG with merged text chunks

    Returns output path.
    """
    ext = os.path.splitext(filepath)[1].lower()
    output = out_path or _default_output_path(filepath, 'modified')

    if ext in {'.jpg', '.jpeg'}:
        exif_dict = piexif.load(filepath)
        for key, raw_value in updates.items():
            ifd_name, tag_id, value_type = _find_jpeg_tag(key)
            converted = convert_user_value_for_exif(value_type, raw_value)
            exif_dict[ifd_name][tag_id] = converted
        write_jpeg_exif(filepath, exif_dict, output)
    elif ext in MODIFIABLE_EXTENSIONS:
        img = Image.open(filepath)
        merged = {}
        for key, value in img.info.items():
            if isinstance(value, str):
                merged[str(key)] = value
        for key, value in updates.items():
            merged[str(key)] = str(value)
        save_png_text_metadata(filepath, merged, output)
    else:
        raise ValueError('Modify operation is only supported for JPEG and PNG files')

    print(f'[OK] Metadata modified: {output}')
    return output
