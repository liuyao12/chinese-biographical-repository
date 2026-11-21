import copy
import hashlib
import json
import unittest
from pathlib import Path
from scripts.jin065_children import gift_valid, succession_valid
from scripts.liuxiaobiao_layers import valid as comment_valid
from scripts.lexical_annotations import non_person_errors

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class WangChildren(unittest.TestCase):
    def setUp(self):
        self.ch=read('corpus/jinshu/065.json')
        self.paras={p['id']:(self.ch['id'],p) for p in self.ch['paragraphs']}
        self.byline={p['source_position']['first_line']:p for _,p in self.paras.values()}
        self.ms={m['id']:(self.ch['id'],p['id'],m) for _,p in self.paras.values() for m in p['mentions']}
        self.proof=read('source-evidence/jin065-wang-children/reading.json')

    def test_ranges_raw_images_and_stage(self):
        for w in self.proof['external_witnesses'].values():
            self.assertEqual(hashlib.sha256((ROOT/w['raw_path']).read_bytes()).hexdigest(),w['raw_sha256'])
        for comp in self.proof['comparisons']:
            a=comp['anchor'];self.assertEqual(self.paras[a['paragraph_id']][1]['text'][a['start']:a['end']],a['quote'])
            for s in comp['sources']:
                raw=(ROOT/self.proof['external_witnesses'][s['witness']]['raw_path']).read_text()
                self.assertEqual(raw[s['raw_start']:s['raw_end']],s['quote'])
        for p in self.proof['printed_witness']['pages']:
            self.assertEqual(hashlib.sha256((ROOT/p['local_path']).read_bytes()).hexdigest(),p['sha256'])
        for a in self.proof['item_boundaries']:
            self.assertEqual(a['paragraph_ids'],[self.byline[i]['id'] for i in range(a['first_line'],a['last_line']+1,2)])
            row=next(v for v in read('data/corpus/six-dynasties-biographies.json')['biographies'] if v['book_id']==self.ch['book_id'] and v['title']==a['title'])
            self.assertTrue(row['item_reviewed'])

    def test_limited_liu_layer(self):
        ch=read('corpus/shishuoxinyu/001-wangdao-source.json')
        for p in ch['paragraphs'][1:]:
            self.assertTrue(comment_valid(p,ch,ROOT))
            q=copy.deepcopy(p);q['source_quote']['raw_start']+=1
            self.assertFalse(comment_valid(q,ch,ROOT))
            q=copy.deepcopy(p);q['attribution']['quoted_work']='魏書'
            self.assertFalse(comment_valid(q,ch,ROOT))
        self.assertFalse(comment_valid(ch['paragraphs'][0],ch,ROOT))

    def test_ages_and_relationships(self):
        self.assertEqual([(x['reports'][0]['age'],x['reports'][1]['age']) for x in self.proof['source_age_readings']],[(36,26),(38,28)])
        self.assertEqual([x['source_ordinal'] for x in self.proof['ranked_sons']],[1,2,3])
        expected=[('001','father','3da_7da_fe2','peq_fze_t0g'),('035','mother','7r6_k52_qji_ABAAC','wv1_vsj_6xy')]
        for n,predicate,subject,obj in expected:
            rows=read('corpus/shishuoxinyu/'+n+'-wangdao-source-assertions.json')['assertions']
            self.assertIn((subject,predicate,obj),[(r['subject_person_id'],r['predicate'],r['object_person_id']) for r in rows])
        shu=read('corpus/shishuoxinyu/025-wangdao-source.json')['paragraphs'][0]
        self.assertEqual({m['person_id'] for m in shu['mentions'] if m['surface'] in ('奉正','混')},{'7r6_k52_qji_ABAACA'})

    def test_role_succession_and_awards(self):
        for start in (87,):
            m=next(m for m in self.byline[64]['mentions'] if m['start']==start)
            self.assertFalse(non_person_errors(m,self.byline[64]['text']))
            changed=dict(m,kind='person');self.assertTrue(non_person_errors(changed,self.byline[64]['text']))
        rows=[e for e in read('corpus/jinshu/065-events.json')['events'] if e['id'].startswith('ev-jin065-yuesi-')]
        self.assertEqual(len(rows),3)
        for e in rows:
            self.assertTrue(succession_valid(e,self.paras))
            self.assertFalse(succession_valid(dict(e,title='丹陽尹'),self.paras))
            self.assertFalse(succession_valid(dict(e,predecessor_person_id=e['person_id']),self.paras))
        deaths={x['id']:x for x in read('corpus/jinshu/065-life-events.json')['events']}
        awards=[a for a in read('corpus/jinshu/065-titles.json')['holdings'] if a['id'].startswith('th-wang065-family-gift-')]
        self.assertEqual(len(awards),2)
        for a in awards:
            self.assertTrue(gift_valid(a,self.paras,self.ms,deaths))
            self.assertFalse(gift_valid(dict(a,mode='accession'),self.paras,self.ms,deaths))
