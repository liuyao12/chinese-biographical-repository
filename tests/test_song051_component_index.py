"""Compact exact-name lookup must follow both complete source proofs."""
from pathlib import Path
import copy,json,tempfile,unittest
from unittest.mock import patch
from scripts import wyd_song051_yixin as y
from scripts import fixed_wuyingdian_song051_family_phase as core
from scripts import validation_context as context
ROOT=Path(__file__).resolve().parents[1]

class ProvenComponentIndexTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with context.scope(ROOT):
   cls.chapter,cls.roles,cls.contract,cls.docs=y.state(ROOT)
   cls.names=[n for d in cls.docs.values()for n in d.get('records',[])]
  cls.name=cls.names[0]
 def test_all_163_exact_current_rows_and_complete_chapter(self):
  self.assertEqual(len(self.names),163)
  with context.scope(ROOT):
   self.assertTrue(all(y.component_valid(n,self.chapter,ROOT)for n in self.names))
   self.assertFalse(y.component_valid(self.name,None,ROOT));self.assertFalse(y.component_valid(self.name,{},ROOT))
 def test_record_unknown_fields_types_and_nested_metadata_do_not_reuse_proof(self):
  changes=[]
  for key,value in [('unknown_metadata',{'review':[False]}),('human_reviewed',0),('person_id','abc_def_123')]:
   row=copy.deepcopy(self.name);row[key]=value;changes.append(row)
  row=copy.deepcopy(self.name);row['component_source_binding']['unlisted_key']='wrong';changes.append(row)
  row=copy.deepcopy(self.name);row['quote']='bad'+row['quote'];changes.append(row)
  row=copy.deepcopy(self.name);row['component_source_binding']=tuple(row['component_source_binding']);changes.append(row)
  row=copy.deepcopy(self.name);row[1]='integer key';changes.append(row)
  class NotPlainDict(dict):pass
  changes.extend([NotPlainDict(self.name),None,[],{'float':float('nan')}])
  with context.scope(ROOT):
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   for row in changes:self.assertFalse(y.component_valid(row,self.chapter,ROOT),repr(row)[:80])
 def test_complete_chapter_unknown_metadata_original_mark_and_text_rejected(self):
  with context.scope(ROOT):
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   for mode in ['unknown','mark','text','type']:
    chapter=copy.deepcopy(self.chapter)
    if mode=='unknown':chapter['annotation']['unknown_metadata']={'extra':1}
    elif mode=='mark':next(m for p in chapter['paragraphs']for m in p['mentions']if m.get('kind')=='person')['person_id']='abc_def_123'
    elif mode=='text':chapter['paragraphs'][0]['text']='wrong'
    else:chapter['paragraphs']=tuple(chapter['paragraphs'])
    self.assertFalse(y.component_valid(self.name,chapter,ROOT),mode)
 def test_compact_return_cannot_poison_later_lookup_or_full_state(self):
  with context.scope(ROOT):
   index=y._proven_component_index(ROOT);index['records'].clear();index['chapter']='wrong'
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   actual,roles,contract,docs=y.state(ROOT);actual['annotation'].clear();docs.clear();contract.clear();roles.clear()
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   self.assertEqual(y.state(ROOT)[0],self.chapter)
 def test_one_full_index_build_per_scope_and_outside_is_fresh(self):
  with patch.object(core,'context',wraps=core.context)as proof:
   with context.scope(ROOT):
    self.assertTrue(y.component_valid(self.names[0],self.chapter,ROOT));self.assertTrue(y.component_valid(self.names[1],self.chapter,ROOT))
   self.assertEqual(proof.call_count,1)
   self.assertTrue(y.component_valid(self.names[0],self.chapter,ROOT));self.assertTrue(y.component_valid(self.names[1],self.chapter,ROOT));self.assertEqual(proof.call_count,3)
   with context.scope(ROOT):self.assertTrue(y.component_valid(self.names[0],self.chapter,ROOT))
   self.assertEqual(proof.call_count,4)
 def test_different_root_missing_proof_never_uses_current_root_index(self):
  with tempfile.TemporaryDirectory()as other,context.scope(ROOT):
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT));self.assertFalse(y.component_valid(self.name,self.chapter,Path(other)))
 def test_nested_disabled_and_exception_do_not_export_private_memo(self):
  with context.scope(ROOT)as outer:
   self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   with context.scope(ROOT)as inner:self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
   self.assertTrue(inner['closed']);self.assertEqual(inner['memo'],{})
   with context.scope(ROOT,enabled=False),patch.object(core,'context',side_effect=ValueError('missing proof')):self.assertFalse(y.component_valid(self.name,self.chapter,ROOT))
   self.assertIs(context._ACTIVE.get(),outer);self.assertTrue(y.component_valid(self.name,self.chapter,ROOT))
  self.assertTrue(outer['closed']);self.assertEqual(outer['memo'],{});self.assertIsNone(context._ACTIVE.get())
 def test_real_contract_sidecar_and_registry_proof_fail_closed(self):
  original=Path.read_bytes
  for mode in ['contract','sidecar','registry']:
   with self.subTest(mode=mode):
    relative=y.REF if mode=='contract'else next(iter(self.docs))if mode=='sidecar'else 'registry/persons.json';target=(ROOT/relative).resolve();data=json.loads(original(target))
    if mode=='registry':
     person=next(p for p in data['persons']if p['id']==self.name['person_id']);person['evidence']=[e for e in person['evidence']if e.get('chapter_id')!=y.CID]
    else:data['unknown_metadata']={'unreviewed':True}
    altered=json.dumps(data,ensure_ascii=False).encode()
    def read(path,*args,**kwargs):return altered if path.resolve()==target else original(path,*args,**kwargs)
    with patch.object(Path,'read_bytes',read),context.scope(ROOT):self.assertFalse(y.component_valid(self.name,self.chapter,ROOT))
 def test_missing_caller_name_seed_and_assertions_still_rejected(self):
  name=next(n for n in self.names if n.get('surname_basis'))
  names=self.names+json.loads((ROOT/'corpus/songshu/051-wyd1739-name-components.json').read_bytes())['records'];assertions=[a for d in self.docs.values()for a in d.get('assertions',[])]
  with context.scope(ROOT):
   self.assertTrue(y.validate_surname(name,names,{y.CID:self.chapter},assertions,ROOT))
   for short_names,chapters,short_assertions in [([],{y.CID:self.chapter},assertions),(names,{},assertions),(names,{y.CID:self.chapter},[])]:
    with self.assertRaises(ValueError):y.validate_surname(name,short_names,chapters,short_assertions,ROOT)
 def test_real_raw_witness_change_fails_complete_proof(self):
  original=Path.read_bytes;target=(ROOT/self.chapter['source']['raw_file']).resolve();changed=original(target)+b'\nwrong source bytes\n'
  def read(path,*args,**kwargs):return changed if path.resolve()==target else original(path,*args,**kwargs)
  with patch.object(Path,'read_bytes',read),context.scope(ROOT):self.assertFalse(y.component_valid(self.name,self.chapter,ROOT))
 def test_end_fingerprint_still_rejects_new_source_dependency(self):
  from scripts import validate_corpus
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp);(root/'source-evidence').mkdir()
   def mutate(root):
    # End-guard mechanism itself remains unmodified; no source is supplied here.
    (root/'source-evidence/new-file.json').write_text('{}');return []
   with patch.object(validate_corpus,'_validate_uncached',mutate):self.assertIn(context.DRIFT_ERROR,validate_corpus.validate(root))
