"""可攜連續本傳收養證據正負例，不讀私有封存包。"""
import unittest,json,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.chuji_parentage import chuji_parentage_valid
from scripts.person_bundle import load_catalog,bundle
J=lambda p:json.loads(p.read_text())
class NamedAgnaticAdoption(unittest.TestCase):
 def setUp(self):
  d=J(ROOT/'corpus/songshu/058-xiehongwei.json');self.ps={p['id']:(d['id'],copy.deepcopy(p)) for p in d['paragraphs']};self.rows=J(ROOT/'corpus/songshu/058-xiehongwei-assertions.json')['assertions'];self.a=copy.deepcopy(next(a for a in self.rows if a['id']=='a-song058-hw-010'));self.p=self.ps[self.a['evidence'][0]['paragraph_id']][1];self.n=self.ps[self.a['evidence'][1]['paragraph_id']][1]
 def valid(self):return chuji_parentage_valid(self.a,self.ps,self.rows)
 def replace(self,p,old,new):
  self.assertEqual(len(old),len(new));p['text']=p['text'].replace(old,new)
  for m in p['mentions']:m['surface']=p['text'][m['start']:m['end']]
  for a in self.rows+[self.a]:
   for e in a['evidence']:
    if e['paragraph_id']==p['id']:e['quote']=p['text']
 def test_positive(self):self.assertTrue(self.valid())
 def test_bundle_keeps_both_fathers(self):
  s=json.dumps(bundle(self.a['subject_person_id'],root=ROOT,catalog=load_catalog(ROOT),include_provisional=True),ensure_ascii=False);self.assertIn('a-song058-hw-001',s);self.assertIn('a-song058-hw-010',s);self.assertEqual(next(a for a in self.rows if a['id']=='a-song058-hw-001')['object_person_id'],'aa6_83c_juy_DBA')
 def test_title_alone_rejected(self):self.replace(self.n,'年十嵗出繼','年十嵗襲爵');self.a['qualifiers']['chuji_source_term']='年十嵗襲爵';self.assertFalse(self.valid())
 def test_clan_alone_rejected(self):self.replace(self.n,'年十嵗出繼','年十嵗同族');self.a['qualifiers']['chuji_source_term']='年十嵗同族';self.assertFalse(self.valid())
 def test_missing_named_heir(self):self.replace(self.p,'為嗣','襲爵');self.a['qualifiers']['source_term']=self.a['qualifiers']['source_term'].replace('為嗣','襲爵');self.assertFalse(self.valid())
 def test_missing_no_heir(self):self.replace(self.p,'無後以','有子以');self.a['qualifiers']['source_term']=self.a['qualifiers']['source_term'].replace('無後以','有子以');self.assertFalse(self.valid())
 def test_wrong_parent(self):self.a['object_person_id']='aa6_83c_juy_BAC';self.assertFalse(self.valid())
 def test_wrong_child(self):self.a['subject_person_id']='aa6_83c_juy_DBAA';self.assertFalse(self.valid())
 def test_conflicting_father(self):next(a for a in self.rows if a['id']=='a-song058-hw-001')['object_person_id']=self.a['object_person_id'];self.assertFalse(self.valid())
 def test_missing_biological_assertion(self):self.a['qualifiers']['biological_father_assertion_id']='missing';self.assertFalse(self.valid())
 def test_preservation_required(self):self.a['qualifiers']['biological_father_preserved']=False;self.assertFalse(self.valid())
 def test_cross_revision(self):self.n['source_position']['source_commit']='other';self.assertFalse(self.valid())
 def test_skipped_lines(self):self.n['source_position']['first_line']+=3;self.assertFalse(self.valid())
 def test_intervening_body(self):
  items=list(self.ps.items());fake=copy.deepcopy(self.p);fake['id']='intervening';items.insert(1,('intervening',(items[0][1][0],fake)));self.ps=dict(items);self.assertFalse(self.valid())
 def test_cross_chapter(self):self.a['evidence'][1]['chapter_id']='other';self.assertFalse(self.valid())
 def test_cross_source(self):self.a['evidence'][1]['source_id']='other';self.assertFalse(self.valid())
 def test_commentary(self):self.n['text_layer']='ancient_commentary';self.assertFalse(self.valid())
 def test_stale_quote(self):self.a['evidence'][1]['quote']+='字';self.assertFalse(self.valid())
 def test_uncle_hun_not_adoptive_father(self):self.a['evidence'][1]['object_person_mention_id']=next(m['id'] for m in self.n['mentions'] if m['surface']=='混');self.assertFalse(self.valid())
 def test_changed_topic(self):self.p['mentions'][0]['person_id']='different';self.assertFalse(self.valid())
 def test_distinct_preferred_parent_roles(self):
  d=bundle(self.a['subject_person_id'],root=ROOT,catalog=load_catalog(ROOT),include_provisional=True);rs=d['preferred_relations'];self.assertEqual([r['object_person_id'] for r in rs if r['subject_person_id']==self.a['subject_person_id'] and r['predicate']=='father'],['aa6_83c_juy_DBA']);self.assertEqual([r['object_person_id'] for r in rs if r['subject_person_id']==self.a['subject_person_id'] and r['predicate']=='adoptive_father'],['aa6_83c_juy_BAB'])
 def test_cross_biography_topic(self):
  self.n['mentions'].insert(0,{'id':'other-topic','start':0,'end':2,'surface':self.n['text'][:2],'kind':'person','person_id':'other'});self.assertFalse(self.valid())
 def test_no_birth_or_mother(self):self.assertNotIn('birth_year',self.a['qualifiers']);self.assertFalse(any(a['predicate'] in ('mother','adoptive_mother') for a in self.rows));self.assertNotIn('ordinal',self.a['qualifiers'])
if __name__=='__main__':unittest.main()
