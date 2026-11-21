from pathlib import Path
import copy,hashlib,json,unittest
from scripts.jin065_wangdao_main import formal_comment
from scripts.uncle_parentage import explicit_maternal_uncle_valid
from scripts.unassumed_appointments import unassumed_appointment_valid
R=Path(__file__).resolve().parents[1]
def load(path):return json.loads((R/path).read_text())
class WangDao(unittest.TestCase):
 def setUp(self):
  self.c=load('corpus/jinshu/065.json');self.p={p['id']:(self.c['id'],p) for p in self.c['paragraphs']};self.ms={m['id']:m for cid,p in self.p.values() for m in p['mentions']};self.q=load('source-evidence/jin065-wangdao-main/reading.json')
 def test_source_and_extent(self):
  for w in self.q['source_layers'].values():self.assertEqual(hashlib.sha256((R/w['raw_path']).read_bytes()).hexdigest(),w['raw_sha256'])
  for x in self.q['printed_witness']['pages']:
   self.assertEqual(x['source_url'], f"{self.q['printed_witness']['url']}#page={x['pdf_page']}")
   self.assertRegex(x['capture_sha256'],r'^[0-9a-f]{64}$')
  for x in self.q['comparisons']:
   a=x['source'];self.assertEqual(self.p[a['paragraph_id']][1]['text'][a['start']:a['end']],a['quote'])
   for s in x['witnesses']:
    raw=(R/self.q['source_layers'][s['witness']]['raw_path']).read_text();self.assertEqual(raw[s['raw_start']:s['raw_end']],s['quote'])
  ids=self.q['item_boundaries'][0]['paragraph_ids'];self.assertEqual(len(ids),26);self.assertTrue(ids[-1].endswith('line116'))
  entries=[x for x in load('data/corpus/six-dynasties-biographies.json')['biographies'] if x['book_id']==self.c['book_id']]
  original=load('source-evidence/jin065-wang-survey/survey-review.json')['entry_work']
  additions=load('source-evidence/jin065-wang-kinship/reading.json')['title_reviews']
  self.assertCountEqual([x['title'] for x in entries],[x['title'] for x in original+additions])
  self.assertTrue(all(x['item_reviewed'] for x in entries))
 def test_identity_and_reference(self):
  for s,pid in [('周圮','i1w_a4z_a3g'),('紀贍','23e_6ed_438'),('管夷吾','h1v_8ap_b9y')]:
   self.assertEqual(next(m['person_id']for m in self.ms.values()if m['surface']==s),pid)
  refs={f['id']:f for f in self.c['annotation']['person_reference_occurrences']};prefix=self.c['id']
  for suffix in ['line032:m0067','line046:m0052']:
   a=self.ms[prefix+':'+suffix];self.assertEqual((a['kind'],a['person_id']),('non_person',None))
  self.assertEqual(refs[prefix+':line032:m0082']['referent_role'],'speaker_self')
  self.assertEqual(len(self.q['comparative_mentions']),2)
  for row in self.q['comparative_mentions']:self.assertNotEqual(self.ms[row['literal_mention_id']]['person_id'],row['figurative_person_id'])
 def test_office_and_uncle(self):
  prop=next(row for row in self.c['annotation']['title_proposals']if row['id']=='tp-jin065-wangdao-mindi-libu')
  self.assertTrue(unassumed_appointment_valid(prop,self.c));b=copy.deepcopy(prop);b['role_anchor']['start']-=1;self.assertFalse(unassumed_appointment_valid(b,self.c))
  a=next(x for x in load('corpus/jinshu/065-assertions.json')['assertions']if x['id']=='a-jin065-cheng-yuliang-maternal-uncle');self.assertTrue(explicit_maternal_uncle_valid(a,self.p));self.assertFalse(explicit_maternal_uncle_valid(dict(a,subject_person_id=a['object_person_id']),self.p))
  ts=load('corpus/jinshu/065-titles.json')['holdings'];self.assertEqual(next(h['mode']for h in ts if h['id']=='th-jinshu065-wang-004'),'accession');self.assertTrue(any(h['title']=='始興郡公' for h in ts))
 def test_early_history_and_annal(self):
  ch=load('corpus/shishuoxinyu/005-wangdao-relatives.json');src,note=ch['paragraphs'];self.assertIn('而立簡文',src['text']);self.assertIn('琅邪王裒',note['text']);self.assertTrue(formal_comment(note,ch,R))
  b=copy.deepcopy(note);b['attribution']['quoted_work']='語林';self.assertFalse(formal_comment(b,ch,R))
  event=load('corpus/jinshu/007-wangdao-xiankang5-life-events.json')['events'][0];self.assertEqual(event['normalized_date']['year'],339);self.assertEqual(event['normalized_date']['precision'],'year');self.assertIn('秋七月庚申',event['evidence'][0]['quote']);self.assertEqual(self.q['historical_report_and_annal']['printed_era'],'咸和')
