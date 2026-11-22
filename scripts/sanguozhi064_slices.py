"""從卷六十四的固定見證重建正文與裴注內的傳目原句。"""
from functools import lru_cache
from pathlib import Path

try:
    from .sanguozhi063_slices import slice_volume_text
except ImportError:
    from sanguozhi063_slices import slice_volume_text


@lru_cache(maxsize=1)
def source_lines():
    source = Path(__file__).resolve().parents[1] / (
        'source-evidence/sanguozhi064-roll/ws2263487.wikitext'
    )
    return source.read_text(encoding='utf-8').splitlines()


def slice_text(fragment):
    return slice_volume_text(fragment, source_lines(), '卷64')
