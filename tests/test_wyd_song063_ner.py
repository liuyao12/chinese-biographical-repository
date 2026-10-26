import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
try:
 from scripts.fixed_wuyingdian_song063_wangtanshou import source_errors
 from scripts.wyd_song063_roles import source_only_projection,resolve_roles,load_contract
 from scripts.cross_chapter_references import errors as xref_errors
 from scripts.render_corpus import render
except ImportError:
 from fixed_wuyingdian_song063_wangtanshou import source_errors
 from wyd_song063_roles import source_only_projection,resolve_roles,load_contract
 from cross_chapter_references import errors as xref_errors
 from render_corpus import render
ROOT=Path(__file__).resolve().parents[1]
PATH='corpus/songshu/063-wyd1739-wangtanshou.json'
class WYD063NER(unittest.TestCase):
 def setUp(self):self.c=json.loads((ROOT/PATH).read_bytes())
 def test_full_roles_projection_and_real_xref(self):
  self.assertEqual(source_errors(self.c,ROOT),[])
  projected=source_only_projection(self.c,ROOT)
  self.assertTrue(all(p['annotation_status']=='pending'and p['mentions']==[]for p in projected['paragraphs']))
  self.assertEqual(render(self.c),(ROOT/'corpus/songshu/063-wyd1739-wangtanshou.xml').read_text())
  target=json.loads((ROOT/'corpus/songshu/071-wangsengchuo.json').read_bytes())
  self.assertEqual(xref_errors({self.c['id']:self.c,target['id']:target},ROOT),[])
  self.assertEqual(len(resolve_roles(self.c,ROOT)),21)
 def test_wrong_person_or_missing_named_slot(self):
  role=resolve_roles(self.c,ROOT)
  for change in ['person','drop']:
   c=copy.deepcopy(self.c);p=c['paragraphs'][0]
   if change=='person':next(m for m in p['mentions']if m['kind']=='person')['person_id']=role['hong']
   else:p['mentions'].pop(0)
   self.assertTrue(source_errors(c,ROOT))
 def test_no_stage_or_human_promotion(self):
  for change in ['key','human','status','raw']:
   c=copy.deepcopy(self.c)
   if change=='key':del c['annotation']['fixed_ner_role_layer']
   if change=='human':c['annotation']['fixed_ner_role_layer']['human_reviewed']=True
   if change=='status':c['paragraphs'][0]['annotation_status']='reviewed'
   if change=='raw':c['paragraphs'][0]['text']=c['paragraphs'][0]['text']+'字'
   self.assertTrue(source_errors(c,ROOT))
 def test_wrong_known_work_and_xref_target(self):
  c=copy.deepcopy(self.c);next(m for m in c['paragraphs'][-1]['mentions']if m['kind']=='work')['work_id']='w-shiji';self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.c);c['cross_chapter_references'][0]['target']['book_id']='b-songshu-070';self.assertTrue(source_errors(c,ROOT))
 def test_foreign_revision_and_reverse_refs_fail_closed(self):
  contract=load_contract(ROOT);seed=next(iter(contract['foreign_seeds'].values()));raw=Path.read_bytes
  for change in ['revision','reverse']:
   foreign=json.loads(raw(ROOT/seed['path']));reg=json.loads(raw(ROOT/'registry/persons.json'))
   if change=='revision':foreign['source']['revision_id']='wrong'
   else:
    people={p['id']:p for p in reg['persons']};p=next(p for p in self.c['paragraphs']if any(m['kind']=='person'for m in p['mentions']));m=next(m for m in p['mentions']if m['kind']=='person');people[m['person_id']]['evidence']=[e for e in people[m['person_id']]['evidence']if e.get('mention_id')!=m['id']]
   def reader(path):
    if path.resolve()==(ROOT/seed['path']).resolve():return json.dumps(foreign,ensure_ascii=False).encode()
    if path.resolve()==(ROOT/'registry/persons.json').resolve():return json.dumps(reg,ensure_ascii=False).encode()
    return raw(path)
   with patch.object(Path,'read_bytes',reader):self.assertTrue(source_errors(self.c,ROOT))
 def test_coherent_rekey_uses_mids_not_person_whitelist(self):
  roles=resolve_roles(self.c,ROOT);old=roles['tanshou'];new='a0b_c1d_e2f';raw=Path.read_bytes
  def remap(x):
   if isinstance(x,dict):return{k:remap(v)for k,v in x.items()}
   if isinstance(x,list):return[remap(v)for v in x]
   return new if x==old else x
  changed=remap(self.c)
  def reader(path):
   b=raw(path)
   if path.suffix=='.json'and path.name in ['persons.json','063-wanghua-tanshou.json','071-wangsengchuo.json']:return json.dumps(remap(json.loads(b)),ensure_ascii=False).encode()
   return b
  with patch.object(Path,'read_bytes',reader):self.assertEqual(source_errors(changed,ROOT),[])
 def test_xref_father_wrong_even_if_other_source_person(self):
  contract=load_contract(ROOT);seed=contract['xref_role_seeds']['tanshou'];roles=resolve_roles(self.c,ROOT);raw=Path.read_bytes;target=json.loads(raw(ROOT/seed['path']));reg=json.loads(raw(ROOT/'registry/persons.json'));tp=next(p for p in target['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in tp['mentions']if m['id']==seed['mention_id']);m['person_id']=roles['hong'];person=next(p for p in reg['persons']if p['id']==roles['hong']);person['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]});person['evidence'].append({'work_id':target['work_id'],'book_id':target['book_id'],'source_id':target['source_id'],'chapter_id':target['id'],'paragraph_id':tp['id'],'mention_id':m['id'],'quote':m['surface']})
  def reader(path):
   if path.resolve()==(ROOT/seed['path']).resolve():return json.dumps(target,ensure_ascii=False).encode()
   if path.resolve()==(ROOT/'registry/persons.json').resolve():return json.dumps(reg,ensure_ascii=False).encode()
   return raw(path)
  with patch.object(Path,'read_bytes',reader):self.assertTrue(source_errors(self.c,ROOT))
if __name__=='__main__':unittest.main()
