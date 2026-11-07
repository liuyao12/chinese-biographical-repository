"""One allusion primary/source-role closure, including coherent mutable endpoint rekey."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_zhou041_wangbao import proof,errors,CH,CID
from scripts.zhou041_sizong_resolution import capsule
ROOT=Path(__file__).resolve().parents[1]
class Sizong(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.c,cls.roles=proof(ROOT);cls.pid=cls.roles['$sizong'];cls.people=json.loads((ROOT/'registry/persons.json').read_bytes());cls.cap=capsule(ROOT);cls.mid=cls.cap['target_mid']
 def overlay(self,values):
  original=Path.read_bytes
  return patch.object(Path,'read_bytes',lambda p:(values[str(p.relative_to(ROOT))].encode()if isinstance(values[str(p.relative_to(ROOT))],str)else json.dumps(values[str(p.relative_to(ROOT))],ensure_ascii=False).encode())if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in values else original(p))
 def test_one_exact_marker_primary_courtesy_and_context(self):
  m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['id']==self.mid);self.assertEqual((m['surface'],m['start'],m['end'],m['kind'],m['person_id']),('嗣宗',0,2,'person',self.pid));self.assertIn('阮籍，字嗣宗',self.cap['primary']['complete_opening_paragraph']);self.assertIn('車跡所窮，輒慟哭而反',self.cap['primary']['complete_crying_paragraph'])
 def test_wrong_active_person_single_marker_rejected(self):
  ch=copy.deepcopy(self.ch);next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==self.mid)['person_id']=self.roles['$yangzhu']
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_single_seed_endpoint_rejected(self):
  rel=self.cap['catalog_seed']['path'];d=json.loads((ROOT/rel).read_bytes());next(m for p in d['paragraphs']for m in p['mentions']if m['id']==self.cap['catalog_seed']['marker']['id'])['person_id']=self.roles['$yangzhu']
  with self.overlay({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_missing_new_reverse_rejected(self):
  people=copy.deepcopy(self.people);p=next(p for p in people['persons']if p['id']==self.pid);p['evidence']=[e for e in p['evidence']if e.get('mention_id')!=self.mid]
  with self.overlay({'registry/persons.json':people}):self.assertTrue(errors(self.ch,ROOT))
 def test_missing_literal_alias_rejected(self):
  people=copy.deepcopy(self.people);p=next(p for p in people['persons']if p['id']==self.pid);a=next(a for a in p['aliases']if a['surface']=='嗣宗');a['mention_ids'].remove(self.mid)
  with self.overlay({'registry/persons.json':people}):self.assertTrue(errors(self.ch,ROOT))
 def test_coherent_current_endpoint_rekey_not_permanent_PID(self):
  new='zz8_yy7_xx6';self.assertFalse(any(p['id']==new for p in self.people['persons']))
  def replace(x):
   if isinstance(x,str):return new if x==self.pid else x
   if isinstance(x,list):return[replace(v)for v in x]
   if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
   return x
  rels=['registry/persons.json',CH,'corpus/zhoushu/041-wangbao-ws2432538-identities.json',self.cap['catalog_seed']['path']];values={rel:replace(json.loads((ROOT/rel).read_bytes()))for rel in rels};xml='corpus/zhoushu/041-wangbao-ws2432538.xml';values[xml]=(ROOT/xml).read_text().replace('ref="'+self.pid+'"','ref="'+new+'"')
  with self.overlay(values):ch,c,roles=proof(ROOT);self.assertEqual(roles['$sizong'],new)
 def test_case_counts_and_no_new_events(self):
  from collections import Counter
  from scripts.fixed_zhou041_wangbao import LETTER_REFERENCES
  from scripts.fixed_zhou041_erlu import MID as ERLU_MID
  mentions=[m for p in self.ch['paragraphs']for m in p['mentions']];self.assertEqual(len(mentions),sum(len(p['mentions'])for p in self.c['chapter_template']['paragraphs']));self.assertEqual({m['id']for m in mentions if m['kind']=='pronoun'},set(LETTER_REFERENCES))
  pending={mid for r in self.ch['annotation']['unresolved_source_reference_readings']for mid in r['unresolved_mention_ids']};self.assertEqual({m['id']for m in mentions if m['kind']=='unresolved'},pending|{ERLU_MID});self.assertFalse(any(c['id']=='d-zhou041-sizong'for c in self.ch['annotation']['unresolved_identity_cases']));self.assertIn('不是全卷或全部史實抽取',self.ch['annotation']['coverage'])
 def test_primary_qualifications_no_raw_or_print_claim(self):
  self.assertFalse(self.cap['primary']['original_wikitext_obtained']);self.assertFalse(self.cap['primary']['fixed_permalink_body_read']);self.assertIsNone(self.cap['primary']['actual_print_edition']);self.assertFalse(self.cap['image_verified'])
if __name__=='__main__':unittest.main()
