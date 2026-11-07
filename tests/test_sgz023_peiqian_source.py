# coding: utf-8
"""Fixed complete text, bounded accepted roles, and source/metadata preservation."""
import copy,json,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
from contextlib import contextmanager
from collections import Counter
from scripts.fixed_sgz023_peiqian import CID,REF,errors,project,load
from scripts.fixed_wikisource_units import source_errors
from scripts.render_corpus import render
R=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/023-peiqian-ws2376966.json'

@contextmanager
def current_json_views(changes):
 """Inject current source records through both real readers; captures stay byte-exact."""
 original_bytes,original_text=Path.read_bytes,Path.read_text
 payload={(R/rel).resolve():json.dumps(value,ensure_ascii=False).encode('utf8')for rel,value in changes.items()}
 def read_bytes(path,*args,**kwargs):
  return payload[path.resolve()]if path.resolve()in payload else original_bytes(path,*args,**kwargs)
 def read_text(path,*args,**kwargs):
  if path.resolve()in payload:return payload[path.resolve()].decode('utf8')
  return original_text(path,*args,**kwargs)
 with patch.object(Path,'read_bytes',read_bytes),patch.object(Path,'read_text',read_text):yield

class PeiQianSource(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.ch=json.loads((R/CH).read_bytes());c.contract=load(R)
 def test_normal_source_and_xml(self):
  self.assertEqual(source_errors(self.ch,R),[]);self.assertEqual(render(self.ch),(R/CH).with_suffix('.xml').read_text());self.assertEqual((len(self.ch['paragraphs']),sum(len(p['text'])for p in self.ch['paragraphs'])),(14,3403))
 def test_complete_body_notes_four_biographies_and_fish_comment(self):
  raw=(R/self.ch['source']['raw_path']).read_text();units,_=project(raw);self.assertEqual([p['text']for p in self.ch['paragraphs']],[u['text']for u in units]);text=''.join(p['text']for p in self.ch['paragraphs']);self.assertIn('◎嚴幹字公仲',text);self.assertIn('◎韓宣字景然',text);self.assertIn('◎黃朗字文達',text);self.assertTrue(text.endswith('至於檢己，老而益明，亦難能也。'));self.assertNotIn('評曰：和洽',text);self.assertNotIn('244年',text);self.assertIn('正始五年',text)
 def test_unknown_print_and_current_named_pass_remain_provisional(self):
  self.assertIsNone(self.ch['source']['edition']);self.assertFalse(self.ch['source']['image_verified']);self.assertFalse(self.ch['annotation']['human_reviewed']);self.assertEqual(self.ch['annotation']['status'],'in_progress')
  self.assertTrue(all(p['annotation_status']=='in_progress'for p in self.ch['paragraphs']))
  self.assertEqual(Counter(m['kind']for p in self.ch['paragraphs']for m in p['mentions']),{'person':225,'work':26,'unresolved':12})
  self.assertEqual(self.ch['annotation']['four_biographies_ner_ref'],'source-evidence/sgz023-peiqian-ws2376966/four-biographies-ner-contract.json')
  self.assertEqual(self.ch['annotation']['typed_work_author_ref'],'source-evidence/sgz023-peiqian-ws2376966/work-author-contract.json')
 def test_source_changes_note_laundering_promotions_and_false_names_refused(self):
  for case in ['drop','glyph','note_layer','human','edition','revision','drop_contract','wrong_person','name_as_pronoun','work_name_as_person']:
   c=copy.deepcopy(self.ch)
   if case=='drop':c['paragraphs'].pop()
   elif case=='glyph':c['paragraphs'][0]['text']=c['paragraphs'][0]['text'].replace('潛','潜')
   elif case=='note_layer':c['paragraphs'][1]['text_layer']='received_chapter'
   elif case=='human':c['annotation']['human_reviewed']=True
   elif case=='edition':c['source']['edition']='武英殿本'
   elif case=='revision':c['source']['revision_id']=1
   elif case=='drop_contract':del c['annotation']['fixed_sgz023_peiqian_ref']
   elif case=='wrong_person':c['paragraphs'][0]['mentions'][0]['person_id']='kbq_kjc_n2f_B'
   elif case=='name_as_pronoun':c['paragraphs'][0]['mentions'][0]['kind']='pronoun'
   else:c['paragraphs'][1]['mentions'].insert(0,{'id':CID+':wrong','start':1,'end':3,'surface':'魏略','kind':'person','person_id':'kbq_kjc_n2f'})
   self.assertTrue(source_errors(c,R),case)
 def test_reverse_and_exact_kin_direction_reject_coherent_local_spoofs(self):
  raw=Path.read_bytes;rel='corpus/sanguozhi/023-peiqian-ws2376966-assertions.json'
  for case in ['reverse','alias','direction','relative_order']:
   reg=json.loads(raw(R/'registry/persons.json'));side=json.loads(raw(R/rel))
   if case in ('reverse','alias'):
    mid=self.ch['paragraphs'][0]['mentions'][0]['id'];pid=self.ch['paragraphs'][0]['mentions'][0]['person_id'];p=next(p for p in reg['persons']if p['id']==pid)
    if case=='reverse':p['evidence']=[e for e in p['evidence']if e.get('mention_id')!=mid]
    else:
     for a in p['aliases']:a['mention_ids']=[x for x in a['mention_ids']if x!=mid]
   else:
    a=side['assertions'][0 if case=='direction'else 3]
    if case=='direction':a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
    else:a=next(a for a in side['assertions']if a['predicate']=='brother');q=a['qualifiers']['relative_birth_order'];q['older_person_id'],q['younger_person_id']=q['younger_person_id'],q['older_person_id']
   with current_json_views({'registry/persons.json':reg,rel:side}):self.assertTrue(source_errors(self.ch,R),case)
 def test_actual_raw_mutation_and_unrecognized_wrappers_rejected(self):
  b=(R/self.ch['source']['raw_path']).read_bytes();reader=Path.read_bytes
  def altered(p):return b.replace('裴潛'.encode(),'裴潜'.encode(),1)if p.resolve()==(R/self.ch['source']['raw_path']).resolve()else reader(p)
  with patch.object(Path,'read_bytes',altered):self.assertTrue(source_errors(self.ch,R))
  with self.assertRaises(AssertionError):project(b.decode().replace('裴潛字文行','{{不明|裴潛}}字文行',1))
 def test_coherent_rekey_uses_fixed_source_mids(self):
  # A simulated current endpoint move changes current records, never immutable
  # contracts/projections/captures or opaque MID/assertion IDs.
  old=self.ch['paragraphs'][0]['mentions'][0]['person_id'];new='abc_def_987'
  registry=json.loads((R/'registry/persons.json').read_bytes());self.assertNotIn(new,{p['id']for p in registry['persons']})
  def endpoints(x):
   if isinstance(x,list):return[endpoints(v)for v in x]
   if not isinstance(x,dict):return x
   out={}
   for key,value in x.items():
    if key.endswith('_person_id')or key=='person_id':out[key]=new if value==old else value
    elif key.endswith('_person_ids')and isinstance(value,list):out[key]=[new if v==old else v for v in value]
    else:out[key]=endpoints(value)
   return out
  registry=endpoints(registry)
  for person in registry['persons']:
   if person['id']==old:person['id']=new
  changes={'registry/persons.json':registry}
  for path in sorted((R/'corpus').glob('*/*.json')):
   value=json.loads(path.read_bytes());moved=endpoints(value)
   if moved!=value:changes[str(path.relative_to(R))]=moved
  moved=changes[CH];before={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']};after={m['id']:m for p in moved['paragraphs']for m in p['mentions']}
  self.assertEqual(set(before),set(after))
  for mid,mark in before.items():self.assertEqual({k:v for k,v in mark.items()if k!='person_id'},{k:v for k,v in after[mid].items()if k!='person_id'})
  self.assertTrue(all(path=='registry/persons.json'or path.startswith('corpus/')for path in changes))
  captures={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in(R/'source-evidence/sgz023-peiqian-ws2376966').glob('*.json')}
  with current_json_views(changes):
   self.assertEqual(source_errors(moved,R),[])
   for rel,want in captures.items():self.assertEqual(hashlib.sha256((R/rel).read_bytes()).hexdigest(),want)
   broken=copy.deepcopy(moved);broken['paragraphs'][0]['mentions'][0]['person_id']=old
   self.assertTrue(source_errors(broken,R))
 def test_two_hui_and_he_shao_remain_unmerged_and_no_foster_father(self):
  cases=self.ch['annotation']['unresolved_identity_cases'];self.assertFalse(any(x['id']=='case-sgz023-two-hui-deferred'for x in cases));self.assertTrue(any(x['id']=='case-sgz023-two-hui-deferred'and x['identity_decision_id']=='d-sgz023-hui-explicit-xuncan-reference'for x in self.ch['annotation']['resolved_identity_reviews']));p=next(p for p in self.ch['paragraphs']if '潛少弟徽' in p['text']);self.assertTrue(all(m['kind']=='unresolved'and m['person_id']is None for m in p['mentions']if m['surface']=='郃'));aa=json.loads((R/'corpus/sanguozhi/023-peiqian-ws2376966-assertions.json').read_bytes())['assertions'];self.assertFalse(any(a['predicate']=='adoptive_father'for a in aa));self.assertTrue(all(a['human_reviewed']is False for a in aa))
if __name__=='__main__':unittest.main()
