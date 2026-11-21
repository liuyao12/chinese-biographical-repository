"""三方原誌的日期、親屬、拒官與省文。"""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from scripts import xiangshan_m9_epitaphs as study

ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text())
def doc(slug,kind=None):
    base='corpus/epitaph-'+slug+'/full'
    return read(base+('-'+kind if kind else '')+'.json')

class XiangshanM9(unittest.TestCase):
    def test_year_and_leap_month(self):
        for slug in ('wangjianzhi','liumeizi-stone','liumeizi-brick'):
            chapter=doc(slug)
            chapters={chapter['id']:chapter}
            for e in doc(slug,'life-events')['events']:
                if 'normalized_date' not in e:
                    continue
                self.assertTrue(study.inscribed_year_valid(e['normalized_date'],e,'life_event',chapters,ROOT))
                changed=deepcopy(e)
                changed['inscribed_date_components']['day']+=1
                self.assertFalse(study.inscribed_year_valid(changed['normalized_date'],changed,'life_event',chapters,ROOT))
        death=doc('wangjianzhi','life-events')['events'][0]
        date=death['inscribed_date_components']
        self.assertTrue(date['is_leap_month'])
        self.assertIsNone(date['month'])
        self.assertEqual((date['day'],date['day_sexagenary']),(12,'丁丑'))
        husband=doc('wangjianzhi')
        self.assertFalse(any(p['title'] in ('西曹','州別駕') for p in doc('wangjianzhi','titles')['holdings']))
        for proposal in husband['annotation']['title_proposals']:
            self.assertTrue(study.proposal_valid(proposal,husband))

    def test_two_separate_epitaphs_of_liumeizi(self):
        stone=doc('liumeizi-stone')
        brick=doc('liumeizi-brick')
        self.assertEqual(stone['annotation']['status'],'reviewed')
        self.assertEqual(brick['annotation']['status'],'in_progress')
        text=brick['paragraphs'][0]['text']
        self.assertIn('二女並二歲亡',text)
        for word in ('玉龜','道末','脩武令乂','戊戌朔'):
            self.assertNotIn(word,text)
        mother=next(r for r in doc('liumeizi-stone','assertions')['assertions'] if r['id'].endswith('-child-張願'))
        self.assertEqual(mother['predicate'],'mother')
        changed=deepcopy(mother)
        changed['predicate']='father'
        self.assertFalse(study.kin_valid(changed,stone,ROOT))
        self.assertFalse(study.kin_valid(mother,brick,ROOT))
        for n,d in (('wangjianzhi',275),('liumeizi-stone',171),('liumeizi-brick',143)):
            self.assertEqual(len(doc(n)['paragraphs'][0]['text']),d)
