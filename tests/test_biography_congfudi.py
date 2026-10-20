# coding: utf-8
import unittest,copy,json,sys,pathlib
V=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(V))
from scripts.biography_congfudi import biography_congfudi_valid as valid
from scripts.historical_family_clauses import explicit_congdi_valid as dispatch
A=json.loads((V/'corpus/jinshu/061-congfudi-assertions.json').read_bytes())['assertions'][0]
C=json.loads((V/'corpus/jinshu/061-zhou-family.json').read_bytes())
P=next(p for p in C['paragraphs']if p['id'].endswith(':p020'))
class Congfudi(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(A);self.p=copy.deepcopy(P)
 def check(self,want=False):self.assertEqual(valid(self.a,{self.p['id']:(C['id'],self.p)}),want)
 def text(self,head):
  tail=P['text'][11:];self.p['text']=head+tail
  self.a['evidence'][0]['quote']=self.p['text']
  self.a['qualifiers']['source_term']=head
  self.a['qualifiers']['source_clause_binding']['end']=len(head)
  s,o=self.p['mentions'][0],self.p['mentions'][2]
  o['start']=head.index('浚');o['end']=o['start']+1
 def test_actual(self):self.check(True);self.assertTrue(dispatch(self.a,{P['id']:(C['id'],P)}))
 def test_review_true(self):self.a['human_reviewed']=True;self.check(True)
 def test_review_shape(self):
  for v in [None,'false',0,1]:self.a['human_reviewed']=v;self.check()
 def test_missing_fu(self):self.text('馥字祖宣，浚從弟也。');self.check()
 def test_congzu(self):self.text('馥字祖宣，浚從祖弟也。');self.check()
 def test_congmu(self):self.text('馥字祖宣，浚從母弟也。');self.check()
 def test_negation(self):self.text('馥字祖宣，非浚從父弟也。');self.check()
 def test_alternative(self):self.text('馥字祖宣，或云浚從父弟也。');self.check()
 def test_quoted(self):self.text('馥字祖宣，曰浚從父弟也。');self.check()
 def test_wrong_subject(self):self.a['subject_person_id']='3xx_gdy_or6_AA';self.check()
 def test_reversed(self):
  a=self.a;a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id'];self.check()
 def test_wrong_age(self):self.a['qualifiers']['kinship_structure']['subject_relative_age']='older';self.check()
 def test_cross_paragraph(self):self.a['evidence'][0]['paragraph_id']='missing';self.check()
 def test_truncated_quote(self):self.a['evidence'][0]['quote']=self.p['text'][:11];self.check()
 def test_truncated_term(self):self.a['qualifiers']['source_term']=self.p['text'][:10];self.check()
 def test_common_ancestor_id(self):self.a['qualifiers']['kinship_structure']['common_ancestor_person_id']='made_up';self.check()
 def test_common_ancestor_name(self):self.a['qualifiers']['kinship_structure']['common_ancestor_name']='某';self.check()
 def test_father_age(self):self.a['qualifiers']['kinship_structure']['father_relative_age']='older';self.check()
 def test_metric_integer(self):self.a['qualifiers']['kinship_structure']['distance']=2;self.check()
 def test_metric_wrong_kind(self):self.a['qualifiers']['kinship_structure']['distance']['kind']='cousins';self.check()
 def test_metric_wrong_depth(self):self.a['qualifiers']['kinship_structure']['distance']['common_ancestor_depth']['subject']=3;self.check()
 def test_metric_bool(self):self.a['qualifiers']['kinship_structure']['generation_difference']=False;self.check()
 def test_parent_brother_edge(self):self.a['predicate']='elder_brother';self.check()
 def test_collateral_bool(self):self.a['qualifiers']['kinship_structure']['collateral']=1;self.check()
 def test_paragraph_commentary(self):self.p['source_layer']='ancient_commentary';self.check()
 def test_evidence_commentary(self):self.a['evidence'][0]['source_layer']='ancient_commentary';self.check()
 def test_wrong_source_layer(self):self.a['qualifiers']['source_clause_binding']['source_layer']='ancient_commentary';self.check()
 def test_literature_wrong_layer(self):self.a['qualifiers']['literary_usage']['citations'][1]['layer']='received_text';self.check()
 def test_literature_wrong_quote(self):self.a['qualifiers']['literary_usage']['citations'][0]['quote']='搜尋摘要';self.check()
 def test_exact_term(self):self.a['qualifiers']['source_term']='從父弟';self.check()
 def test_anonymous(self):self.p['mentions'][0]['kind']='anonymous_person';self.check()
 def test_mismatched_anchor(self):self.p['mentions'][2]['surface']='顗';self.check()
 def test_wrong_clause_offset(self):self.a['qualifiers']['source_clause_binding']['start']=1;self.check()
 def test_head_only(self):
  self.p['text']='或曰'+self.p['text'];self.a['evidence'][0]['quote']=self.p['text'];self.check()
 def test_source_position_layer(self):
  for layer in ['pei_annotation','ancient_commentary','received_annal']:
   self.p['source_position']['source_layer']=layer;self.check()
 def test_received_position_layers(self):
  for layer in ['received_body','received_biography','received_text']:
   self.p['source_position']['source_layer']=layer;self.check(True)
 def test_annotator_without_layer(self):
  self.p['source_position']['annotator']='裴松之';self.check()
 def test_attached_note_without_layer(self):
  self.p['source_position']['attached_note_to_paragraph_id']='other';self.check()
 def test_real_pei_metadata_without_top_layer(self):
  c=json.loads((V/'corpus/sanguozhi/009-caoxiu.json').read_bytes())
  note=next(p for p in c['paragraphs']if p.get('text_layer')=='witness_appended_pei_songzhi_note')
  self.p['source_position']=copy.deepcopy(note['source_position']);self.p['text_layer']=note['text_layer'];self.check()
 def test_note_text_layer_alone(self):self.p['text_layer']='witness_appended_pei_songzhi_note';self.check()
 def test_wrong_layer_review_status_independent(self):
  for reviewed in [True,False]:
   self.a['human_reviewed']=reviewed;self.p['source_position']['annotator']='裴松之';self.check()
 def test_record_id_not_allowlist(self):self.a['id']='different-history-record';self.check(True)
 def test_absent_parent_assertions(self):self.check(True)
 def test_generic_069(self):
  c=json.loads((V/'corpus/jinshu/069-zhouyi.json').read_bytes());p=c['paragraphs'][0];t=p['text'];at=t.index('顗從弟穆');s=next(m for m in p['mentions']if m['start']==at+3);o=next(m for m in p['mentions']if m['start']==at)
  a=copy.deepcopy(A);a.update(subject_person_id=s['person_id'],object_person_id=o['person_id']);q=a['qualifiers'];q.pop('literary_usage');q['source_term']='顗從弟穆';q['kinship_structure']['distance']=None;q['source_clause_binding']={'kind':'named_object_congdi_subject','start':at,'end':at+4}
  a['evidence']=[dict(chapter_id=c['id'],paragraph_id=p['id'],quote=t,subject_person_mention_id=s['id'],object_person_mention_id=o['id'])];ps={p['id']:(c['id'],p)}
  self.assertTrue(dispatch(a,ps));q['kinship_structure']['distance']=copy.deepcopy(A['qualifiers']['kinship_structure']['distance']);self.assertFalse(dispatch(a,ps));self.assertFalse(valid(a,ps))
if __name__=='__main__':unittest.main(verbosity=2)
