# coding: utf-8
import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from unittest.mock import patch
from scripts.body_note_ancestry import body_note_ancestor_parent_valid
R=Path(__file__).resolve().parents[1]
def case(root=R):
 c=json.loads((root/'corpus/sanguozhi/010.json').read_text());aa={a['id']:a for a in json.loads((root/'corpus/sanguozhi/010-phase11-xunyou-assertions.json').read_text())['assertions']};near=aa['a-xunyou11-002'];far=aa['a-xunyou11-001'];sub=near['subject_person_id'];f=near['object_person_id'];g=far['object_person_id'];ps={p['id']:p for p in c['paragraphs']};b=ps[far['evidence'][0]['paragraph_id']];n=ps[near['evidence'][0]['paragraph_id']];after=c['paragraphs'][c['paragraphs'].index(n)+1]
 rows={p:{'person_id':p,'source_person_ids':[p],'parent_person_id':None,'source_assertion_id':None}for p in [sub,f,g]};m=rows[f];m['parent_person_id']=g
 def mark(p,pid,surface=None):return next(x['id']for x in p['mentions']if x.get('person_id')==pid and x['kind']=='person'and(surface is None or x['surface']==surface))
 layer=next(x for x in n['received_text_layers']if '攸父'in x['quote']);work=next(x for x in n['mentions']if x.get('kind')=='work'and layer['start']<=x['start']<x['end']<=layer['end']);sm=next(x for x in n['mentions']if x['id']==mark(n,sub));fm=next(x for x in n['mentions']if x['id']==mark(n,f))
 refs=[]
 for a in [near,far]:refs.append({**a['evidence'][0],'assertion_id':a['id'],'scope':'同一人物正文與直接附注，父祖各原證，父之父僅編輯接合','url':c['source']['url']})
 raw='sources/witnesses/KR2a0012_010-214fcafa79894355909c9d8c2c1533089e7791c6.txt'
 m['parent_connection']={'type':'parent_between_body_and_attached_note_ancestors','interpretation_basis':'body_grandfather_attached_note_father','status':'contextual_provisional','human_reviewed':False,'rationale':'同一人物祖父正文與直接附注明父，不造原文明父。','chain_subject_person_id':sub,'nearer_ancestor_assertion_id':near['id'],'farther_ancestor_assertion_id':far['id'],'body_subject_mention_id':mark(b,sub),'body_ancestor_mention_id':mark(b,g),'note_subject_mention_id':sm['id'],'note_ancestor_mention_id':fm['id'],'references':refs,'witness_binding':{'body_paragraph_id':b['id'],'note_paragraph_id':n['id'],'following_body_paragraph_id':after['id'],'source_revision':c['source']['revision_id'],'raw_file':raw,'raw_file_sha256':hashlib.sha256((root/raw).read_bytes()).hexdigest()},'role_clause':{'kind':'attributed_genealogical_report','start':sm['start'],'end':fm['end'],'attribution_start':layer['start'],'attribution_end':layer['end'],'authority':layer['authority'],'work_mention_id':work['id'],'cited_work_id':work['work_id']}}
 return m,rows,aa,{c['id']:c}
class FramedBodyNoteAncestry(unittest.TestCase):
 def setUp(self):self.member,self.rows,self.aa,self.chapters=case();self.c=next(iter(self.chapters.values()));self.conn=self.member['parent_connection'];self.near=self.aa[self.conn['nearer_ancestor_assertion_id']];self.far=self.aa[self.conn['farther_ancestor_assertion_id']]
 def para(self,key):return next(p for p in self.c['paragraphs']if p['id']==self.conn['witness_binding'][key])
 def valid(self,root=R):return body_note_ancestor_parent_valid(self.member,self.rows,self.aa,self.chapters,root)
 def test_real_positive_editorial_only(self):self.assertTrue(self.valid());self.assertIsNone(self.member['source_assertion_id'])
 def test_co_shift_all_raw_positions_retaining_fragments(self):
  for key in ['body_paragraph_id','note_paragraph_id','following_body_paragraph_id']:
   for f in self.para(key)['witness_fragments']:f['raw_line_start']+=1;f['raw_line_end']+=1
  self.assertFalse(self.valid())
 def test_note_layer_erased(self):self.para('note_paragraph_id')['text_layer']='received_chapter';self.assertFalse(self.valid())
 def test_body_annotator_cannot_masquerade_as_body(self):self.para('body_paragraph_id')['source_position']['annotator']='裴松之';self.assertFalse(self.valid())
 def test_body_nested_text_layer_is_checked(self):self.para('body_paragraph_id')['source_position']['text_layer']='witness_appended_pei_songzhi_note';self.assertFalse(self.valid())
 def test_other_subject(self):self.far['subject_person_id']=self.far['object_person_id'];self.assertFalse(self.valid())
 def test_maternal(self):self.far['qualifiers']['lineage']='maternal';self.assertFalse(self.valid())
 def test_generation_gap(self):self.far['predicate']='great_grandfather';self.assertFalse(self.valid())
 def test_named_marker_wrong_person_even_same_quote(self):
  p=self.para('note_paragraph_id');m=next(m for m in p['mentions']if m['id']==self.conn['note_ancestor_mention_id']);m['person_id']=self.near['subject_person_id'];self.assertFalse(self.valid())
 def test_role_crosses_attributed_source_scope(self):self.conn['role_clause']['attribution_end']=self.conn['role_clause']['end']-1;self.assertFalse(self.valid())
 def test_wrong_cited_work(self):self.conn['role_clause']['cited_work_id']='w-unrelated';self.assertFalse(self.valid())
 def test_injected_dialogue_is_not_a_genealogy(self):
  p=self.para('note_paragraph_id');p['text']=p['text'][:44]+'曰「'+p['text'][44:]+'」';self.near['evidence'][0]['quote']=p['text'];self.conn['references'][0]['quote']=p['text'];self.assertFalse(self.valid())
 def test_conflicting_direct_father(self):self.aa['other']={'predicate':'father','subject_person_id':self.near['object_person_id'],'object_person_id':self.near['subject_person_id']};self.assertFalse(self.valid())
 def test_raw_actual_read_hash(self):
  original=Path.read_bytes;target=(R/self.conn['witness_binding']['raw_file']).resolve()
  with patch.object(Path,'read_bytes',lambda p:original(p)+b' 'if p.resolve()==target else original(p)):self.assertFalse(self.valid())
 def test_source_response_hash_mismatch(self):self.c['source']['response_sha256']='0'*64;self.assertFalse(self.valid())
 def test_revision_mismatch(self):self.conn['witness_binding']['source_revision']='different';self.assertFalse(self.valid())
 def test_attachment_offset_gap(self):self.conn['witness_binding']['following_body_paragraph_id']=self.conn['witness_binding']['body_paragraph_id'];self.assertFalse(self.valid())
 def test_outside_symlink_raw_rejected(self):
  with tempfile.TemporaryDirectory()as a,tempfile.TemporaryDirectory()as b:
   root=Path(a);(root/'sources').mkdir();outside=Path(b)/'raw.txt';outside.write_bytes((R/self.conn['witness_binding']['raw_file']).read_bytes());(root/'sources/link.txt').symlink_to(outside);self.conn['witness_binding']['raw_file']='sources/link.txt';self.assertFalse(self.valid(root))
 def test_cycle(self):self.rows[self.far['object_person_id']]['parent_person_id']=self.member['person_id'];self.assertFalse(self.valid())
 def test_fake_source_father(self):self.member['source_assertion_id']=self.near['id'];self.assertFalse(self.valid())
 def test_human_review_cannot_be_invented(self):self.conn['human_reviewed']=True;self.assertFalse(self.valid())
 def test_missing_full_reference(self):self.conn['references'][0]['quote']='攸父彞';self.assertFalse(self.valid())

 def test_body_courtesy_marker_cannot_switch_subject(self):
  p=self.para('body_paragraph_id');m=next(m for m in p['mentions']if m['start']==3);m['person_id']=self.far['object_person_id'];self.assertFalse(self.valid())

 def test_body_courtesy_role_unresolved(self):
  p=self.para('body_paragraph_id');next(m for m in p['mentions']if m['start']==3)['status']='unresolved';self.assertFalse(self.valid())
 def test_duplicate_revision_fields_must_agree(self):
  self.para('note_paragraph_id')['source_position']['revision_id']='wrong';self.assertFalse(self.valid())
