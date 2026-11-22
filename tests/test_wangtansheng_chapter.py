from copy import deepcopy
import json
from pathlib import Path
import unittest
from scripts.song093_wangtansheng import song_errors, title_errors

ROOT=Path(__file__).resolve().parents[1]

class Song93Tansheng(unittest.TestCase):
    def test_preserves_explicit_actor_and_offices(self):
        ch=json.loads((ROOT/'corpus/songshu/093.json').read_text())
        titles=json.loads((ROOT/'corpus/songshu/093-titles.json').read_text())
        self.assertFalse(song_errors(ch,ROOT))
        self.assertFalse(title_errors(titles,ch,ROOT))
        bad=deepcopy(ch)
        next(p for p in bad['paragraphs'] if p['id'].endswith('line068'))['mentions'][-1]['person_id']='hx8_st4_jdd'
        self.assertTrue(song_errors(bad,ROOT))
        title=next(h for h in titles['holdings'] if h['id']=='th-songshu-093-68-30')
        title['title']='會稽太守'
        self.assertTrue(title_errors(titles,ch,ROOT))
