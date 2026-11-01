"""Fixed complete Jin037 units and current-role/unknown-kinship conservation."""
import copy,json,hashlib,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_jin037_gaomi_nanyang as source
from scripts.validation_context import scope
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
ROOT=Path(__file__).resolve().parents[1]
class Jin037NearFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with scope(ROOT):
   cls.chapter,cls.roles=source.proof(ROOT);cls.people,cls.records=load_catalog(ROOT);cls.family,_=load_assemblies(ROOT,(cls.people,cls.records))
 def overlay(self,path,value):
  original=Path.read_bytes;payload=value if isinstance(value,bytes)else(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
  return patch.object(Path,'read_bytes',lambda p:payload if p==ROOT/path else original(p))
 def test_complete_units_and_source_qualification(self):
  ch=self.chapter;self.assertEqual(len(ch['paragraphs']),18);self.assertEqual(len(ch['annotation']['modern_collation_reports']),5);self.assertIsNone(ch['source']['edition']);self.assertIs(ch['source']['image_verified'],False)
  self.assertIn('虓字武會',ch['paragraphs'][11]['text']);self.assertIn('又乙太宰',ch['paragraphs'][13]['text']);self.assertIn('四祖之業',ch['paragraphs'][15]['text'])
  for p in ch['paragraphs']:
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
    if m['kind']=='person':self.assertNotIn(m['surface'],('之','其','公','臣','陛下'))
  p=ch['paragraphs'][14];self.assertEqual(next(m for m in p['mentions']if m['surface']=='周禮')['kind'],'work')
 def test_local_roles_and_non_name_boundaries(self):
  self.assertNotEqual(self.roles['$fufeng_jun'],self.roles['$yangjun']);self.assertNotEqual(self.roles['$shijian'],self.roles['$cong'])
  p=self.chapter['paragraphs'][3];start=p['text'].index('攻略')+1;self.assertFalse(any(m['start']==start for m in p['mentions']))
  p=self.chapter['paragraphs'][0];self.assertFalse(any(m['surface']=='魏陽亭侯'for m in p['mentions']))
  self.assertEqual(next(m['person_id']for p in self.chapter['paragraphs']for m in p['mentions']if m['surface']=='司徒戎'),self.roles['$wangrong'])
  p=self.chapter['paragraphs'][14]
  for term,offset in [('一方事重',1),('王室',0)]:
   start=p['text'].index(term)+offset;self.assertFalse(any(m['start']<=start<m['end']and m['kind']=='person'for m in p['mentions']))
  p=self.chapter['paragraphs'][16];start=p['text'].index('王之身');m,=[m for m in p['mentions']if m['start']==start];self.assertEqual((m['surface'],m['person_id']),('王',self.roles['$ying']))
 def test_direct_biological_adoptive_and_ritual_roles_remain_separate(self):
  a=json.loads((ROOT/'corpus/jinshu/037-gaomi-nanyang-assertions.json').read_bytes())['assertions'];rels={(x['subject_person_id'],x['predicate'],x['object_person_id'])for x in a}
  self.assertIn((self.roles['$li'],'father',self.roles['$mo']),rels);self.assertIn((self.roles['$li'],'adoptive_father',self.roles['$xiao']),rels);self.assertIn((self.roles['$jun'],'father',self.roles['$hong']),rels)
  self.assertNotIn((self.roles['$jun'],'father',self.roles['$ju']),rels);self.assertFalse(any(x['predicate']=='mother'for x in a))
  r=self.chapter['annotation']['unresolved_kinship_references'][0];self.assertEqual(r['reference_person_candidates'],[]);self.assertIsNone(r['adoptive_father_person_id']);self.assertEqual(r['biological_father_person_id'],self.roles['$tai'])
  for role in ('tai','sui'):
   m=self.family[self.roles['$'+role]];self.assertIsNone(m['source_assertion_id']);self.assertEqual(m['parent_connection']['type'],'shared_father_through_sibling');self.assertIs(m['parent_connection']['same_father_independently_attested'],False)
 def test_secondary_deaths_ages_and_burial_are_source_specific(self):
  events=json.loads((ROOT/'corpus/jinshu/037-gaomi-nanyang-life-events.json').read_bytes())['events'];self.assertEqual(len(events),13)
  for role in ('caoshu','ju','jiapi','peibao','zhangfang','bao','li'):
   e=next(e for e in events if e['person_id']==self.roles['$'+role]);self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
  self.assertEqual({a['value']for a in self.chapter['annotation']['age_assertions']},{27,37})
  addresses=json.loads((ROOT/'corpus/jinshu/037-gaomi-nanyang-addresses.json').read_bytes())['assertions'];self.assertTrue(any(a['person_id']==self.roles['$bao']and a['relation']=='burial_place'and a['place']['source_name']=='上邽'for a in addresses))
 def test_unassumed_offices_keep_appointments_without_actual_arrival(self):
  from scripts.unassumed_appointments import unassumed_appointment_valid
  items=self.chapter['annotation']['title_proposals'];self.assertEqual(len(items),5)
  for item in items:
   self.assertTrue(unassumed_appointment_valid(item,self.chapter));bad=copy.deepcopy(item);bad['person_id']=self.roles['$can'];self.assertFalse(unassumed_appointment_valid(bad,self.chapter))
  titles=json.loads((ROOT/'corpus/jinshu/037-gaomi-nanyang-titles.json').read_bytes())['holdings'];self.assertFalse(any(h['person_id']==self.roles['$mo']and h['title']=='司空'for h in titles));self.assertTrue(any(h['person_id']==self.roles['$bao']and h['title']=='晉王'and h['mode']=='self_proclamation'for h in titles))
 def test_caller_single_endpoint_and_missing_sidecar_or_reverse_refused(self):
  records=copy.deepcopy(self.records);ch=next(r for r in records if r.get('id')==source.CID);m=next(m for p in ch['paragraphs']for m in p['mentions']if m.get('source_identity_role')=='mo');m['person_id']=self.roles['$can']
  with self.assertRaises(AssertionError):source.guard_bundle(ROOT,self.roles['$can'],self.people,records)
  records=[r for r in self.records if not(r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==source.CID)]
  with self.assertRaises(AssertionError):source.guard_bundle(ROOT,self.roles['$kui'],self.people,records)
  people=copy.deepcopy(self.people);people[self.roles['$mo']]['evidence'].pop()
  with self.assertRaises(AssertionError):source.guard_bundle(ROOT,self.roles['$mo'],people,self.records)
 def test_physical_one_endpoint_or_unknown_owner_or_raw_change_refused(self):
  for change in ('endpoint','owner'):
   ch=copy.deepcopy(self.chapter)
   if change=='endpoint':ch['paragraphs'][0]['mentions'][0]['person_id']=self.roles['$can']
   else:ch['source_id']='foreign-source'
   with self.overlay(source.CH,ch),self.assertRaises(AssertionError):source.proof(ROOT)
  with self.overlay(self.chapter['source']['raw_path'],b'wrong raw'),self.assertRaises(AssertionError):source.proof(ROOT)
 def test_normal_bundle_exposes_names_family_ages_and_no_redirect(self):
  with scope(ROOT):
   item=bundle(self.roles['$bao'],ROOT,True,(self.people,self.records));self.assertEqual(item['canonical_person_id'],self.roles['$bao']);self.assertTrue(item.get('age_assertions'));self.assertTrue(item.get('life_events'));self.assertTrue(item.get('title_holdings'))
  with scope(ROOT):
   cao=bundle(self.roles['$caoshu'],ROOT,True,(self.people,self.records));self.assertTrue(any(n.get('surname')=='曹'and n.get('ming')=='攄'for n in cao['name_components']));self.assertTrue(any(n.get('zi')=='顏遠'and n.get('chapter_id')=='c-jinshu-090-caoshu'for n in cao['name_components']))
  from scripts.retired_person_ids import retired_person_ids
  retired=retired_person_ids(ROOT);receipt=json.loads((ROOT/'source-evidence/jin037-gaomi-nanyang/retirement-mo.json').read_bytes());self.assertTrue(set(receipt['retired_person_ids'])<=retired);self.assertFalse(set(receipt['retired_person_ids'])&set(self.people))
 def test_own_bao_coherent_rekey_preserves_captures_and_rejects_reverse_theft(self):
  from contextlib import ExitStack
  from scripts.render_corpus import render
  old=self.roles['$bao'];new=old+'Z';self.assertNotIn(new,self.people)
  endpoint_fields={'person_id','subject_person_id','object_person_id','representative_source_person_id','source_person_ids','retained_person_id','canonical_person_id','current_person_id'}
  def project(x,key=None,person_registry=False):
   if isinstance(x,str):return new if x==old and key in endpoint_fields else x
   if isinstance(x,list):return[project(v,key,person_registry)for v in x]
   if isinstance(x,dict):
    out={k:project(v,k,person_registry)for k,v in x.items()}
    if person_registry and x.get('id')==old and 'aliases'in x and 'evidence'in x:out['id']=new
    return out
   return x
  changes={};capture_hashes={};original_read=Path.read_bytes;original_text=Path.read_text
  for folder in ('registry','corpus','source-evidence'):
   for file in (ROOT/folder).rglob('*.json'):
    rel=str(file.relative_to(ROOT));before=original_read(file);data=json.loads(before);after=project(data,person_registry=rel=='registry/persons.json')
    if after!=data:
     changes[rel]=(json.dumps(after,ensure_ascii=False,indent=2)+'\n').encode()
     if isinstance(data,dict)and data.get('record_type')=='marked_chapter':
      self.assertEqual([(p['text'],[(m['id'],m['surface'],m['start'],m['end'],m['kind'])for m in p['mentions']])for p in data['paragraphs']],[(p['text'],[(m['id'],m['surface'],m['start'],m['end'],m['kind'])for m in p['mentions']])for p in after['paragraphs']]);changes[str(file.with_suffix('.xml').relative_to(ROOT))]=render(after).encode()
    if '/historical-before/'in rel:capture_hashes[rel]=hashlib.sha256(before).hexdigest()
  self.assertNotIn(source.REF,changes)
  def get(file):return changes.get(str(file.relative_to(ROOT)))if file.is_relative_to(ROOT)else None
  with ExitStack()as stack:
   stack.enter_context(patch.object(Path,'read_bytes',lambda f:get(f)if get(f)is not None else original_read(f)))
   stack.enter_context(patch.object(Path,'read_text',lambda f,*a,**k:get(f).decode()if get(f)is not None else original_text(f,*a,**k)))
   with scope(ROOT):
    chapter,roles=source.proof(ROOT);self.assertEqual(roles['$bao'],new);people,records=load_catalog(ROOT);item=bundle(new,ROOT,True,(people,records));self.assertEqual(item['canonical_person_id'],new)
    self.assertEqual(capture_hashes,{rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()for rel in capture_hashes})
    missing=copy.deepcopy(people);missing[new]['evidence']=[]
    with self.assertRaises(AssertionError):source.guard_bundle(ROOT,new,missing,records)
if __name__=='__main__':unittest.main()
