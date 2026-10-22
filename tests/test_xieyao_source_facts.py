# coding:utf-8
import unittest,json,copy,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'corpus').exists():ROOT=Path(__file__).resolve().parent/'fixture'
sys.path.insert(0,str(ROOT))
from scripts.biography_family_clause import valid
from scripts.noble_state_abolition import valid as abolition_valid
class XieyaoFactsTests(unittest.TestCase):
 def setUp(self):
  c=json.loads((ROOT/'corpus/jinshu/079.json').read_text());self.paragraphs={p['id']:(c['id'],p)for p in c['paragraphs']};self.rels=[a for a in json.loads((ROOT/'corpus/jinshu/079-assertions.json').read_text())['assertions']if a['id'].startswith('a-jin079-xieyao-')];self.event=next(e for e in json.loads((ROOT/'corpus/jinshu/079-events.json').read_text())['events']if e['id']=='ev-jin079-xieyao-chengbo-guochu')
 def test_seven_source_relations(self):
  self.assertEqual(len(self.rels),7)
  for a in self.rels:self.assertTrue(valid(a,self.paragraphs,self.rels),a['id'])
  self.assertFalse(any(a['predicate']=='adoptive_father'for a in self.rels))
 def test_reversed_and_mixed_parentage_rejected(self):
  for original in self.rels:
   a=copy.deepcopy(original);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,self.paragraphs,self.rels))
  a=copy.deepcopy(next(a for a in self.rels if a['predicate']=='ritual_successor_of'));a['predicate']='adoptive_father';self.assertFalse(valid(a,self.paragraphs,self.rels))
 def test_ritual_requires_separate_literal_biological_father(self):
  a=next(a for a in self.rels if a['predicate']=='ritual_successor_of');self.assertFalse(valid(a,self.paragraphs,[]));bad=copy.deepcopy(self.rels)
  for r in bad:
   if r['id'].endswith('mo-chengbo'):r['object_person_id']=a['object_person_id']
  self.assertFalse(valid(a,self.paragraphs,bad))
 def test_negation_and_omitted_role_fail_closed(self):
  a=copy.deepcopy(next(a for a in self.rels if a['id'].endswith('yao-gai')));a['qualifiers']['source_clause_binding']['roles'].pop('heir');self.assertFalse(valid(a,self.paragraphs,self.rels))
  a=copy.deepcopy(next(a for a in self.rels if a['id'].endswith('yao-gai')));ps=copy.deepcopy(self.paragraphs);p=ps[a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('以子承伯嗣','非子承伯嗣');a['evidence'][0]['quote']=p['text'];a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(valid(a,ps,self.rels))
 def test_unranked_children_and_relative_brothers(self):
  self.assertTrue(all('birth_order'not in a['qualifiers']for a in self.rels))
  for a in self.rels:
   if a['predicate']=='brother':self.assertIsNone(a['qualifiers']['relative_birth_order']['younger_ordinal'])
 def test_noble_abolition_binding(self):
  self.assertTrue(abolition_valid(self.event,self.paragraphs));a=copy.deepcopy(self.event);a['person_id']=next(a for a in self.rels if a['id'].endswith('yao-gai'))['subject_person_id'];self.assertFalse(abolition_valid(a,self.paragraphs))
 def test_abolition_no_date_title_or_death(self):
  for key,value in [('date_expression','元熙中'),('title','建昌縣公'),('holding_id','invented'),('event_type','death')]:
   a=copy.deepcopy(self.event);a[key]=value;self.assertFalse(abolition_valid(a,self.paragraphs))
  for key in ['title','holding_id','date_expression']:
   a=copy.deepcopy(self.event);a.pop(key);self.assertFalse(abolition_valid(a,self.paragraphs))
 def test_unnamed_succession_is_event_not_fake_title(self):
  es=json.loads((ROOT/'corpus/jinshu/079-events.json').read_text())['events'];a=next(e for e in es if e['id']=='ev-jin079-xieyao-yao-succession');self.assertTrue(abolition_valid(a,self.paragraphs));self.assertIsNone(a['title']);self.assertIsNone(a['predecessor_person_id'])
  for key,value in [('title','爵'),('predecessor_person_id','aa6_83c_juy_B'),('mode','grant')]:
   bad=copy.deepcopy(a);bad[key]=value;self.assertFalse(abolition_valid(bad,self.paragraphs))
 def test_date_and_location_boundaries(self):
  h=json.loads((ROOT/'corpus/jinshu/079-titles.json').read_text())['holdings'];ours=[x for x in h if x['id'].startswith('th-jin079-xieyao-')];self.assertEqual(len(ours),8)
  for x in ours:
   self.assertEqual(x['effective_period']['end']['status'],'unknown')
   for a in x['attestations']:
    if a['date_expression']=='元熙中':self.assertEqual((a['normalized_date_range']['earliest']['year'],a['normalized_date_range']['latest']['year']),(419,420))
  addresses=[a for a in json.loads((ROOT/'corpus/jinshu/079-addresses.json').read_text())['assertions']if a['id'].startswith('pa-jin079-xieyao-')];self.assertEqual([a['place']['source_name']for a in addresses if a['relation']=='biographical_origin'],['太山']);self.assertFalse(any(a['relation']in ['death_place','burial_place']for a in addresses))
if __name__=='__main__':unittest.main()
