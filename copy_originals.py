import os
import re
import shutil
import argparse
import sys

VARIANT_PATTERN = re.compile(
    r'^(.+)-(\d+x\d+|scaled|rotated)(\.[^.]+)$',
    re.IGNORECASE
)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff', '.tif', '.avif'}


def is_variant(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower() not in IMAGE_EXTENSIONS:
        return False
    return bool(VARIANT_PATTERN.match(filename))


def copy_originals(src, dst, dry_run=False):
    copied = 0
    skipped = 0

    for root, _, files in os.walk(src):
        for filename in files:
            if is_variant(filename):
                skipped += 1
                print(f"  SKIP  {os.path.relpath(os.path.join(root, filename), src)}")
                continue

            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, src)
            dst_path = os.path.join(dst, rel_path)

            print(f"  COPY  {rel_path}")

            if not dry_run:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

            copied += 1

    print(f"\nDone: {copied} copied, {skipped} skipped (variants)")
    if dry_run:
        print("(dry run — no files were actually copied)")


class HelpOnErrorParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}\n", file=sys.stderr)
        self.print_help(sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    parser = HelpOnErrorParser(
        prog='copy_originals',
        description='Copy all original WordPress files (images, zips, etc.), skipping resized image variants.',
        epilog=(
            'WordPress generates variants like image-300x200.jpg, image-scaled.jpg,\n'
            'image-rotated.jpg alongside originals. This tool copies only the originals.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('src', help='Source folder (e.g. wp-content/uploads)')
    parser.add_argument('dst', help='Destination folder for originals')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview which files would be copied without writing anything'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.src):
        parser.error(f"source folder not found: {args.src}")

    copy_originals(args.src, args.dst, dry_run=args.dry_run)
