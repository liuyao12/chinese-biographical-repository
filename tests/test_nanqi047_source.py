"""True source-shaped guards; no full-catalog validation claim."""
import unittest,json,copy,tempfile,shutil,hashlib
from pathlib import Path
from scripts.fixed_nanqi047_source import errors,kinship_valid,REF,RAW
from scripts.biography_close_family import valid as close_valid
from scripts.surname_bound_ancestor import validate as surname_valid
ROOT=Path(__file__).resolve().parents[1]
def load(rel):return json.loads((ROOT/rel).read_text())
class Source047(unittest.TestCase):
 def setUp(self):
  self.cs=[load('corpus/nanqishu/'+s+'.json')for s in('047-xietiao','047-compiler-appraisal','047-qing-collation')]
  self.ch=self.cs[0];self.ps={p['id']:(c['id'],p)for c in self.cs for p in c['paragraphs']}
  self.aa=load('corpus/nanqishu/047-xietiao-assertions.json')['assertions']
 def test_all_three_complete_strata(self):
  for c in self.cs:self.assertEqual(errors(c,ROOT),[])
  self.assertEqual([len(c['paragraphs'])for c in self.cs],[12,2,1])
  self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),1229)
  self.assertEqual(sum(m['kind']=='person'for c in self.cs for p in c['paragraphs']for m in p['mentions']),109)
 def test_praise_is_separate_from_appraisal(self):
  self.assertEqual([p['text_layer']for p in self.cs[1]['paragraphs']],['received_compiler_appraisal','received_compiler_praise'])
  c=copy.deepcopy(self.cs[1]);c['paragraphs'][1]['text_layer']='received_compiler_appraisal';self.assertTrue(errors(c,ROOT))
 def test_fixed_raw_and_projection_coshift_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   r=Path(td)
   for rel in(REF,RAW):p=r/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
   (r/RAW).write_bytes((r/RAW).read_bytes().replace('謝脁'.encode(),'謝朏'.encode(),1))
   self.assertTrue(errors(self.ch,r))
   q=json.loads((r/REF).read_text());q['chapters'][0]['paragraphs'][0]['text']=q['chapters'][0]['paragraphs'][0]['text'].replace('謝脁','謝朏');(r/REF).write_text(json.dumps(q,ensure_ascii=False));self.assertTrue(errors(self.ch,r))
 def test_father_grandfather_roles(self):
  for a in self.aa[:2]:self.assertTrue(close_valid(a,self.ps,self.aa))
  a=copy.deepcopy(self.aa[0]);a['object_person_id']=self.aa[1]['object_person_id'];self.assertFalse(close_valid(a,self.ps,self.aa))
 def test_shilang_terminal_not_any_office(self):
  a=self.aa[0];self.assertTrue(close_valid(a,self.ps,self.aa))
  ps=copy.deepcopy(self.ps);cid,p=ps[a['evidence'][0]['paragraph_id']];p['text']=p['text'].replace('散騎侍郎','散騎未知');a=copy.deepcopy(a);a['evidence'][0]['quote']=p['text'];a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(close_valid(a,ps,self.aa))
 def test_three_literal_kin_roles(self):
  for a in self.aa[2:]:self.assertTrue(kinship_valid(a,self.ps))
 def test_wrong_person_wrong_kind_wrong_direction(self):
  for a in self.aa[2:]:
   for change in('person','kind','direction'):
    b=copy.deepcopy(a);ps=copy.deepcopy(self.ps)
    if change=='person':b['object_person_id']='unrelated_person'
    if change=='direction':b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id']
    if change=='kind':next(m for m in ps[b['evidence'][0]['paragraph_id']][1]['mentions']if m['id']==b['evidence'][0]['subject_person_mention_id'])['kind']='unresolved'
    self.assertFalse(kinship_valid(b,ps))
 def test_kin_rekey_all_endpoints_preserves_semantics(self):
  a=copy.deepcopy(self.aa[-1]);ps=copy.deepcopy(self.ps);old=a['subject_person_id'];new='x1a_y2b_z3c';a['subject_person_id']=new;a['qualifiers']['relative_birth_order']['younger_person_id']=new
  for cid,p in ps.values():
   for m in p['mentions']:
    if m.get('person_id')==old:m['person_id']=new
  self.assertTrue(kinship_valid(a,ps))
 def test_no_fake_common_father_mother_or_ordinals(self):
  a=copy.deepcopy(self.aa[-1]);a['qualifiers']['shared_father']=True;self.assertFalse(kinship_valid(a,self.ps))
  a=copy.deepcopy(self.aa[-1]);a['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(kinship_valid(a,self.ps))
 def test_parent_surname_source_basis(self):
  names=load('corpus/nanqishu/047-xietiao-name-components.json')['records'];chapters={c['id']:c for c in self.cs}
  for n in names:
   if n.get('surname_basis'):surname_valid(n,names,chapters,self.aa)
  n=copy.deepcopy(next(n for n in names if n.get('surname_basis')));n['surname']='王'
  with self.assertRaises(ValueError):surname_valid(n,names,chapters,self.aa)
 def test_age_and_death_no_invented_year(self):
  age=self.ch['annotation']['age_assertions'][0];self.assertEqual((age['value'],age['source_term'],age['birth_year'],age['date_expression']),(36,'時年三十六',None,None))
  ev=load('corpus/nanqishu/047-xietiao-life-events.json')['events'][0];self.assertEqual(ev['source_term'],'下獄死');self.assertIsNone(ev['date_expression']);self.assertNotIn('normalized_date',ev)
 def test_ancient_allusion_is_inside_edict(self):
  p=next(p for p in self.ch['paragraphs']if p['unit_id']=='xietiao-main:u009');m=next(m for m in p['mentions']if m['surface']=='少正');self.assertEqual(m['kind'],'person');self.assertIn('詔公等啟事如此',p['text']);self.assertNotIn('史臣曰',p['text'])
 def test_actual_family_dispatcher_and_direct_script(self):
  import runpy
  from scripts.biography_family_clause import valid as dispatched
  direct=runpy.run_path(str(ROOT/'scripts/fixed_nanqi047_source.py'))
  for a in self.aa[2:]:
   self.assertTrue(dispatched(a,self.ps,self.aa,{c['id']:c for c in self.cs}))
   self.assertTrue(direct['kinship_valid'](a,self.ps))
   b=copy.deepcopy(a);b['qualifiers']['source_clause_binding']['slot']='unknown'
   self.assertFalse(dispatched(b,self.ps,self.aa,{c['id']:c for c in self.cs}))
 def test_all_document_scopes_preserve_original_quotes(self):
  scopes=self.ch['annotation']['embedded_source_scopes'];self.assertEqual(len(scopes),6)
  for scope in scopes:
   p=self.ps[scope['paragraph_id']][1]
   self.assertEqual(p['text'][scope['start']:scope['end']],scope['quote'])
   self.assertIs(scope['human_reviewed'],False)
 def test_song052_current_roles_match_and_single_end_mutation_rejected(self):
  from scripts.fixed_nanqi047_source import predecessor_roles_match
  self.assertTrue(predecessor_roles_match(self.ch,ROOT))
  c=copy.deepcopy(self.ch);m=next(m for m in c['paragraphs'][0]['mentions']if m['id'].endswith(':m0018'));m['person_id']=next(m['person_id']for m in c['paragraphs'][0]['mentions']if m['surface']=='謝脁')
  self.assertFalse(predecessor_roles_match(c,ROOT));self.assertTrue(errors(c,ROOT))
 def test_song052_wrong_known_kind_and_raw_context_rejected(self):
  from scripts.fixed_nanqi047_source import predecessor_roles_match,PREDECESSOR_REF
  seeds=load(PREDECESSOR_REF)
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);p=r/PREDECESSOR_REF;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/PREDECESSOR_REF,p)
   foreign_path=seeds['father-wei']['path'];p=r/foreign_path;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/foreign_path,p)
   ch=json.loads(p.read_text());pa=next(p for p in ch['paragraphs']if p['id']==seeds['father-wei']['paragraph_id']);m=next(m for m in pa['mentions']if m['id']==seeds['father-wei']['mention_id']);m['kind']='unresolved';p.write_text(json.dumps(ch,ensure_ascii=False));self.assertFalse(predecessor_roles_match(self.ch,r))
   m['kind']='person';pa['text']='非'+pa['text'];p.write_text(json.dumps(ch,ensure_ascii=False));self.assertFalse(predecessor_roles_match(self.ch,r))
 def test_joint_two_source_rekey_is_not_person_id_whitelist(self):
  from scripts.fixed_nanqi047_source import predecessor_roles_match,PREDECESSOR_REF
  seeds=load(PREDECESSOR_REF);c=copy.deepcopy(self.ch)
  with tempfile.TemporaryDirectory()as td:
   r=Path(td);p=r/PREDECESSOR_REF;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/PREDECESSOR_REF,p)
   foreign_path=seeds['father-wei']['path'];foreign=load(foreign_path);mapping={}
   for key,mid in [('ancestor-shu',':m0012'),('father-wei',':m0018')]:
    mark=next(m for m in c['paragraphs'][0]['mentions']if m['id'].endswith(mid));mapping[mark['person_id']]={'ancestor-shu':'aaa_bbb_ccc_A','father-wei':'aaa_bbb_ccc_AA'}[key]
   for ch in(c,foreign):
    for pa in ch['paragraphs']:
     for m in pa['mentions']:
      if m.get('person_id')in mapping:m['person_id']=mapping[m['person_id']]
   p=r/foreign_path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(foreign,ensure_ascii=False));self.assertTrue(predecessor_roles_match(c,r))
 def test_parallel_primary_complete_units_and_scope(self):
  import re
  support=load('source-evidence/nanqi047-xietiao/near-lineage-primary-support.json')
  self.assertIs(support['human_reviewed'],False)
  self.assertEqual(len(support['primary_source_units']),2)
  for u in support['primary_source_units']:
   raw=(ROOT/u['raw_file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),u['raw_sha256'])
   selected='\n'.join(raw.decode().splitlines()[u['first_line']-1:u['last_line']]);self.assertEqual(selected,u['selected_raw_quote']);self.assertEqual(hashlib.sha256(selected.encode()).hexdigest(),u['full_unit_sha256'])
   normalized=re.sub(r'<pb:[^>]+>','',selected).replace('¶','').replace('\r','').replace('\n','');self.assertEqual(normalized,u['projected_quote']);self.assertEqual(hashlib.sha256(normalized.encode()).hexdigest(),u['projected_quote_sha256'])
  self.assertIn('不充作謝脁生母',''.join(support['limits']))
 def test_three_layers_have_native_metadata_and_progress(self):
  from scripts.work_provenance import validate
  provenance=load('registry/work-provenance.json');validate(provenance)
  works=load('registry/works.json')['works'];work=next(w for w in works if w['id']=='w-nanqishu');book=next(b for b in work['books']if b['id']=='b-nanqishu-047');progress=load('corpus/progress.json')['books']
  for c in self.cs:
   self.assertIn(c['id'],book['chapter_ids']);rows=[p for p in progress if p.get('chapter_id')==c['id']];self.assertEqual(len(rows),1);self.assertEqual(rows[0]['book_id'],c['book_id']);self.assertTrue(rows[0]['person_status'])
   base=provenance['text_bases'][c['source_id']];self.assertEqual(base['source_id'],c['source_id']);self.assertEqual(base['work_id'],c['work_id'])
   if base['status']!='documented':self.assertIsNone(base['edition_id']);self.assertIsNone(base['earliest_extant_basis_edition_id'])
 def test_non_dict_and_missing_payloads_fail_closed(self):
  for v in(None,[],1,'x'):
   self.assertFalse(kinship_valid(v,self.ps))
  for a in self.aa[2:]:
   b=copy.deepcopy(a);b['qualifiers']['source_clause_binding']['roles']={};self.assertFalse(kinship_valid(b,self.ps))
if __name__=='__main__':unittest.main()
