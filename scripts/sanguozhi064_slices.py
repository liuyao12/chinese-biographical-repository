"""從《吳書》卷四十九、六十四、六十五固定見證重建正文與裴注傳目。"""
from functools import lru_cache
from pathlib import Path

try:
    from .sanguozhi063_slices import slice_volume_text
except ImportError:
    from sanguozhi063_slices import slice_volume_text


REVISIONS = {49: 2075209, 64: 2263487, 65: 2589669}


@lru_cache(maxsize=len(REVISIONS))
def source_lines(volume):
    folder = Path(__file__).resolve().parents[1] / 'source-evidence' / f'sanguozhi{volume:03}-roll'
    source = folder / f'ws{REVISIONS[volume]}.wikitext'
    return source.read_text(encoding='utf-8').splitlines()


def slice_text(fragment, volume=64):
    return slice_volume_text(fragment, source_lines(volume), f'卷{volume}')
