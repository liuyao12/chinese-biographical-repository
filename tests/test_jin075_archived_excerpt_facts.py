# coding:utf-8
import unittest,json,copy,sys,tempfile,hashlib
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.archived_excerpt_facts import errors,records,valid,grammar,KIND
from scripts.person_bundle import load_catalog
CID='c-jinshu-075-xunsong-families'
class ArchivedExcerptFactsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(R);cls.rows=list(cls.catalog[1]);cls.c=next(x for x in cls.rows if x.get('id')==CID);cls.expected=records(cls.c,R)
 def changed(self,change):
  rows=copy.deepcopy(self.rows);change(rows);self.assertTrue(errors(R,rows))
 def names(self,rows):return next(x for x in rows if x.get('record_type')=='person_name_component_set'and x.get('chapter_id')==CID)['records']
 def chapter(self,rows):return next(x for x in rows if x.get('id')==CID)
 def test_all19_source_slots(self):self.assertEqual(len(self.expected),19);self.assertEqual(errors(R,self.rows),[])
 def test_lingyuan_zi_without_fabricated_person_mid(self):
  n=next(n for n in self.expected if n.get('zi')=='令遠');p=next(p for p in self.c['paragraphs']if p['id']==n['paragraph_id']);self.assertEqual(p['text'][:6],'蕤字令遠。起');self.assertEqual(n['ming'],'蕤');self.assertFalse(any(m['surface']=='令遠'for m in p['mentions']))
 def test_only_ming_ji_no_father_invention(self):
  n=next(x for x in self.expected if x.get('ming')=='籍');self.assertIsNone(n['surname']);self.assertNotIn('surname_basis',n)
 def test_wrong_name_same_paragraph_recipient_coherent_rejected(self):
  def change(rows):
   ns=self.names(rows);n=next(n for n in ns if n.get('zi')=='景猷');other=next(m for m in self.c['paragraphs'][0]['mentions']if m['surface']=='王濟');n.update(person_id=other['person_id'],person_mention_id=other['id'],surname='王',ming='濟')
  self.changed(change)
 def test_zi_cross_paragraph_rejected(self):self.changed(lambda rows:next(n for n in self.names(rows)if n.get('zi')=='令遠').update(zi='令則'))
 def test_zi_same_paragraph_bystander_rejected(self):self.changed(lambda rows:next(n for n in self.names(rows)if n.get('zi')=='景猷').update(zi='王濟'))
 def test_drop_excerpt_rejected(self):self.changed(lambda rows:self.chapter(rows)['source']['normalization']['excerpts'].pop())
 def test_rehash_candidate_quote_and_text_cannot_shift_trusted_witness(self):
  def change(rows):
   c=self.chapter(rows);p=c['paragraphs'][0];p['text']='甲'+p['text'];e=c['source']['normalization']['excerpts'][0];e['raw_quote']='甲'+e['raw_quote'];e['raw_quote_sha256']=hashlib.sha256(e['raw_quote'].encode()).hexdigest();e['selected_text_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  self.changed(change)
 def test_deleted_annotation_ref_rejected(self):self.changed(lambda rows:self.chapter(rows)['annotation'].pop('archived_excerpt_fact_slots_ref'))
 def test_no_fullraw_chapter_downgrade(self):self.changed(lambda rows:self.chapter(rows)['annotation'].update(fixed_wikisource_unit_ref='source-evidence/any-fullraw.json'))
 def test_surname_maternal_or_spouse_route_rejected(self):
  for pred in('mother','spouse','adoptive_father'):
   def change(rows):
    a=next(a for r in rows for a in r.get('assertions',[])if a['id']=='a-jinshu075-xunsong-001');a['predicate']=pred
   with self.subTest(pred=pred):self.changed(change)
 def test_agnatic_cousin_no_known_shared_father(self):
  def change(rows):
   a=next(a for r in rows for a in r.get('assertions',[])if a['id']=='a-jin075-xun-archived-kin03');a['predicate']='brother';a['qualifiers']['shared_father']=True
  self.changed(change)
 def test_collateral_not_direct_ancestor(self):
  def change(rows):
   a=next(a for r in rows for a in r.get('assertions',[])if a['id']=='a-jin075-xun-archived-kin01');a['predicate']='great_grandfather';a['qualifiers']['direct_ancestor']=True
  self.changed(change)
 def test_surname_cycle_rejected(self):
  def change(rows):
   n=next(n for n in self.names(rows)if n.get('ming')=='廞');n['surname_basis']['steps']*=2
  self.changed(change)
 def test_binding_line_or_revision_shift_rejected(self):
  for field in('revision','line'):
   def change(rows):
    c=self.chapter(rows)
    if field=='revision':c['source']['revision_id']+=1
    else:c['source']['normalization']['excerpts'][0]['source_lines']=[125,125]
   with self.subTest(field=field):self.changed(change)
 def test_five_idless_legacy_records_migrated_not_duplicated(self):
  cfg=json.loads((R/'scripts/archived_excerpt_fact_recipes.json').read_bytes())['recipes']['jin075-xun-archived-excerpts'];self.assertEqual(len(cfg['legacy_migrations']),5)
  legacy=json.loads((R/'data/corpus/profile-names.json').read_bytes())['records'];self.assertEqual(len([n for n in legacy if n.get('chapter_id')==CID]),17)
  native={n['id']:n for n in self.expected};self.assertEqual(native['nc-jin075-xun-01']['title'],'曲陵公');self.assertEqual(native['nc-jin075-xun-02']['title'],'安陵鄉侯');self.assertTrue(native['nc-jin075-xun-01']['references'])
  self.assertTrue(all(x['old_stable_id']is None and 'id'not in x['legacy_record']for x in cfg['legacy_migrations']))
  self.assertEqual(native['nc-jin075-xun-01']['migrated_source_qualification']['prior_status'],'editorial_provisional')
 def test_legacy_reintroduction_cannot_count_twice(self):
  from scripts.archived_excerpt_facts import grammar,expand
  r,marks=grammar(self.c,R);old=expand(r['legacy_migrations'][0]['legacy_record'],marks);rows=copy.deepcopy(self.rows);next(x for x in rows if x.get('record_type')=='person_name_component_set'and set(x)=={'record_type','records'})['records'].append(old);self.assertTrue(errors(R,rows))
 def test_migrated_title_and_reference_not_dropped(self):
  for key in('title','references','note'):
   def change(rows):next(n for n in self.names(rows)if n['id']=='nc-jin075-xun-01').pop(key)
   with self.subTest(key=key):self.changed(change)
 def test_native_cli_rejects_wrong_zi_without_disk_mutation(self):
  from scripts import validate_corpus
  path=R/'corpus/jinshu/075-name-components.json';before=path.read_bytes();data=json.loads(before);next(n for n in data['records']if n.get('zi')=='令遠')['zi']='令則';original=Path.read_text
  def read(p,*a,**kw):return json.dumps(data,ensure_ascii=False)if p==path else original(p,*a,**kw)
  with patch.object(Path,'read_text',read),patch.object(validate_corpus,'ROOT',R):
   # The actual main() path delegates through validate(ROOT); override its default root only.
   original_validate=validate_corpus.validate
   with patch.object(validate_corpus,'validate',lambda:original_validate(R)):
    self.assertEqual(validate_corpus.main(),1)
  self.assertEqual(path.read_bytes(),before)
if __name__=='__main__':unittest.main()
