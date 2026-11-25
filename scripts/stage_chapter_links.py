"""Materialize canonical chapter links inside a self-contained Pages artifact."""
import argparse
from pathlib import Path
import shutil


def materialize(source, site):
    native = (source / 'corpus').resolve(strict=True)
    for link in (site / 'data/corpus').glob('*/*.json'):
        if not link.is_symlink():
            continue
        checkout_link = source / link.relative_to(site)
        if not checkout_link.is_symlink() or checkout_link.readlink() != link.readlink():
            raise ValueError(f'Unexpected staged link {link}')
        original = checkout_link.resolve(strict=True)
        relative = original.relative_to(native)
        if len(relative.parts) != 2 or original.name != link.name or not original.is_file():
            raise ValueError(f'Unexpected chapter target {original}')
        link.unlink()
        shutil.copyfile(original, link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site', type=Path)
    args = parser.parse_args()
    materialize(Path(__file__).resolve().parents[1], args.site)
