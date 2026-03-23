import os
import sys
import argparse
from metadata_service import (
    ALLOWED_EXTENSIONS,
    extract_exif,
    parse_set_items,
    strip_metadata,
    modify_metadata,
)


def _validate_single_existing_file(files, action_name):
    if len(files) != 1:
        print(f'Error: {action_name} requires exactly one input file.')
        raise SystemExit(2)

    filepath = files[0]
    if not os.path.isfile(filepath):
        print('Error: file not found.')
        raise SystemExit(1)
    return filepath


def launch_gui_mode():
    from gui_bonus import launch_gui
    launch_gui()


def main():
    parser = argparse.ArgumentParser(description='Scorpion - metadata forensics and management')
    parser.add_argument('files', nargs='*', help='Image file(s) to inspect')
    parser.add_argument('--gui', action='store_true', help='Launch graphical interface')
    parser.add_argument('--strip', action='store_true', help='Strip metadata from a file (JPEG/PNG)')
    parser.add_argument('--set', action='append', default=[], metavar='KEY=VALUE', help='Set metadata value (repeatable)')
    parser.add_argument('--out', help='Output file path for --strip/--set operations')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.gui:
        launch_gui_mode()
        return

    if args.strip and args.set:
        print('Error: use either --strip or --set, not both at the same time.')
        raise SystemExit(2)

    if args.strip:
        filepath = _validate_single_existing_file(args.files, '--strip')
        strip_metadata(filepath, args.out)
        return

    if args.set:
        filepath = _validate_single_existing_file(args.files, '--set')
        updates = parse_set_items(args.set)
        modify_metadata(filepath, updates, args.out)
        return

    for filepath in args.files:
        print(f"\n[{filepath}]")
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            print(f"  Unsupported extension: {ext}")
            continue
        if not os.path.isfile(filepath):
            print('  File not found.')
            continue
        extract_exif(filepath)


if __name__ == '__main__':
    main()
