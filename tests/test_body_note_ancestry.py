import unittest,json,copy
from pathlib import Path
from scripts.body_note_ancestry import body_note_ancestor_parent_valid
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text())
class BodyNoteAncestry(unittest.TestCase):
 def setUp(self):
  c=J('corpus/sanguozhi/009-caoxiu.json');aa=J('corpus/sanguozhi/009-caoxiu-assertions.json')['assertions'];self.a={a['id']:a for a in aa};self.near=self.a['a-sgz009-caoxiu54a-006'];self.far=self.a['a-sgz009-caoxiu54a-005'];sub=self.near['subject_person_id'];father=self.near['object_person_id'];grand=self.far['object_person_id'];self.rows={p:{'person_id':p,'source_person_ids':[p],'parent_person_id':None,'source_assertion_id':None}for p in[sub,father,grand]};self.member=self.rows[father];self.member['parent_person_id']=grand;self.chapters={c['id']:c};b,n=c['paragraphs'][:2]
  def m(p,pid,surf):return next(m['id']for m in p['mentions']if m['person_id']==pid and m['surface']==surf)
  refs=[{**{k:a['evidence'][0][k]for k in['chapter_id','paragraph_id','source_id','quote']},'assertion_id':a['id'],'scope':'完整來源段','url':c['source']['url']}for a in[self.near,self.far]]
  self.member['parent_connection']={'type':'parent_between_body_and_attached_note_ancestors','status':'contextual_provisional','human_reviewed':False,'rationale':'兩條不同層原文的連續祖先編輯推導，非直接父之父原句。','chain_subject_person_id':sub,'nearer_ancestor_assertion_id':self.near['id'],'farther_ancestor_assertion_id':self.far['id'],'source_revision':c['source']['revision_id'],'nearer_subject_mention_id':m(b,sub,'曹休'),'farther_subject_mention_id':m(n,sub,'休'),'nearer_ancestor_mention_id':m(b,father,'父'),'farther_ancestor_mention_id':m(n,grand,'祖父'),'references':refs}
 def valid(self):return body_note_ancestor_parent_valid(self.member,self.rows,self.a,self.chapters,R)
 def note(self):return next(iter(self.chapters.values()))['paragraphs'][1]
 def test_complete_body_and_attached_note(self):self.assertTrue(self.valid());self.assertIsNone(self.member['source_assertion_id'])
 def test_wrong_subject(self):self.far['subject_person_id']=self.far['object_person_id'];self.assertFalse(self.valid())
 def test_wrong_father(self):self.near['object_person_id']=self.far['object_person_id'];self.assertFalse(self.valid())
 def test_nonpaternal_grandfather(self):self.far['qualifiers']['lineage']='maternal';self.assertFalse(self.valid())
 def test_ambiguous_father_word(self):self.near['qualifiers']['source_term']='族父';self.assertFalse(self.valid())
 def test_identity_unresolved(self):m=next(m for m in self.note()['mentions']if m['id']==self.member['parent_connection']['farther_subject_mention_id']);m['kind']='unresolved';m['person_id']=None;self.assertFalse(self.valid())
 def test_multiple_identity_candidates(self):m=next(m for m in self.note()['mentions']if m['id']==self.member['parent_connection']['farther_subject_mention_id']);m['candidate_person_ids']=[m['person_id'],self.far['object_person_id']];self.assertFalse(self.valid())
 def test_different_biography_unit(self):self.note()['source_position']['source_unit_id']='other-biography';self.assertFalse(self.valid())
 def test_adjacent_note_about_another_person(self):self.note()['source_position']['biography_subject_person_id']=self.far['object_person_id'];self.assertFalse(self.valid())
 def test_wrong_attachment(self):self.note()['source_position']['attached_note_to_paragraph_id']='another-body';self.assertFalse(self.valid())
 def test_skipped_body(self):c=next(iter(self.chapters.values()));c['paragraphs'].insert(1,{'id':'skipped-body','text':'另一正文','mentions':[],'text_layer':'received_chapter'});self.assertFalse(self.valid())
 def test_revision_change(self):self.note()['source_position']['revision_id']='different-fixed-revision';self.assertFalse(self.valid())
 def test_wrong_note_layer(self):self.note()['text_layer']='witness_appended_li_xian_note';self.assertFalse(self.valid())
 def test_raw_projection_cannot_shift(self):self.note()['source_position']['projected_start']+=1;self.assertFalse(self.valid())
 def test_reference_must_be_complete(self):self.member['parent_connection']['references'][1]['quote']='休祖父';self.assertFalse(self.valid())
 def test_conflicting_direct_father(self):self.a['test-conflict']={'predicate':'father','subject_person_id':self.near['object_person_id'],'object_person_id':self.near['subject_person_id']};self.assertFalse(self.valid())
 def test_cycle(self):self.rows[self.far['object_person_id']]['parent_person_id']=self.near['object_person_id'];self.assertFalse(self.valid())
 def test_no_fake_direct_source_assertion(self):self.member['source_assertion_id']=self.near['id'];self.assertFalse(self.valid())
 def test_human_review_not_inferred_from_ai(self):self.member['parent_connection']['human_reviewed']=True;self.assertFalse(self.valid())
 def test_cross_chapter(self):
  c=copy.deepcopy(next(iter(self.chapters.values())));old=c['id'];c['id']='test-other';self.chapters[c['id']]=c;self.member['parent_connection']['references'][1]['chapter_id']=c['id'];self.far['evidence'][0]['chapter_id']=c['id'];self.assertFalse(self.valid())
