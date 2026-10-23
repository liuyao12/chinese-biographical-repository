from pathlib import Path
import json,hashlib,copy,tempfile,unittest
from scripts.received_quoted_family import valid
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/sanguozhi/026-guohuai.json').read_text());CS={C['id']:C};PS={p['id']:(C['id'],p)for p in C['paragraphs']};AS=[a for a in json.loads((R/'corpus/sanguozhi/026-guohuai-assertions.json').read_text())['assertions']if a['id'].startswith('a-sgz026-guohuai-family-')]
def check(a,ps=PS,cs=CS,root=R):return valid(a,ps,cs,root)
class ReceivedFamilyTests(unittest.TestCase):
 def test_fourteen_explicit_relations(self):
  self.assertEqual(len(AS),14);self.assertTrue(all(check(a)for a in AS));self.assertEqual(sum(a['predicate']=='father_in_law'for a in AS),2)
 def test_consistent_reverse_endpoints_rejected(self):
  for orig in AS:
   a=copy.deepcopy(orig);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
   if'relative_birth_order'in a['qualifiers']:
    o=a['qualifiers']['relative_birth_order'];o['older_person_id']=a['object_person_id'];o['younger_person_id']=a['subject_person_id']
   self.assertFalse(check(a),orig['id'])
 def test_two_sons_in_law_bound_individually(self):
  pairs=[a for a in AS if a['predicate']=='father_in_law'];self.assertNotEqual(pairs[0]['subject_person_id'],pairs[1]['subject_person_id']);self.assertEqual(pairs[0]['object_person_id'],pairs[1]['object_person_id']);self.assertTrue(all(a['qualifiers']['spouse_person_id']is None for a in pairs))
 def test_consistent_wrong_father_in_law_rejected(self):
  for orig in[a for a in AS if a['predicate']=='father_in_law']:
   for offset in[5,66]:
    a=copy.deepcopy(orig);p=PS[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions']if m['start']==offset and m['kind']=='person');a['object_person_id']=m['person_id'];a['evidence'][0]['object_person_mention_id']=m['id'];a['qualifiers']['source_kinship_frame']['roles']['parent']=m['id'];self.assertFalse(check(a))
 def test_marriage_word_or_missing_binding_no_fallback(self):
  for orig in[a for a in AS if a['predicate']=='father_in_law']:
   a=copy.deepcopy(orig);a['qualifiers']['source_term']='婚';self.assertFalse(check(a));a=copy.deepcopy(orig);a['qualifiers'].pop('source_kinship_frame');self.assertFalse(check(a))
 def test_native_dispatch_rejects_missing_father_in_law_binding(self):
  from unittest.mock import patch
  from scripts.validate_corpus import validate
  path=R/'corpus/sanguozhi/026-guohuai-assertions.json';data=json.loads(path.read_text());next(a for a in data['assertions']if a['predicate']=='father_in_law')['qualifiers'].pop('source_kinship_frame');original=Path.read_text
  def read(p,*args,**kwargs):return json.dumps(data,ensure_ascii=False)if p==path else original(p,*args,**kwargs)
  with patch.object(Path,'read_text',read):errors=validate(R)
  self.assertTrue(any('收到本傳或引書親屬'in e for e in errors))
 def test_no_invented_father_or_ordinal(self):
  ids=json.loads((R/'source-evidence/sanguozhi026-guohuai/identities.json').read_text())['identities'];pairs={(a['subject_person_id'],a['object_person_id'])for a in AS if a['predicate']=='father'}
  self.assertNotIn((ids['豫']['person_id'],ids['配']['person_id']),pairs);self.assertNotIn((ids['緼']['person_id'],ids['全']['person_id']),pairs)
  for a in AS:
   self.assertNotIn('shared_father',a['qualifiers']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_grandfather_not_father(self):
  a=copy.deepcopy(next(a for a in AS if a['predicate']=='grandfather'));a['predicate']='father';a['qualifiers']['source_term']='父全';self.assertFalse(check(a))
 def test_received_glyphs_and_layers_fixed(self):
  a=AS[0];cs=copy.deepcopy(CS);p=next(p for p in cs[C['id']]['paragraphs']if p['id']==a['evidence'][0]['paragraph_id']);p['text']=p['text'].replace('緼','縕');ps={p['id']:(C['id'],p)for p in cs[C['id']]['paragraphs']};b=copy.deepcopy(a);b['evidence'][0]['quote']=p['text'];b['qualifiers']['source_kinship_frame']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(check(b,ps,cs))
 def test_co_shift_raw_and_rehash_still_rejected_by_original_receipt(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);cs=copy.deepcopy(CS);ch=cs[C['id']];raw='\n'+(R/C['source']['raw_path']).read_text();dest=root/C['source']['raw_path'];dest.parent.mkdir(parents=True);dest.write_text(raw);ch['source']['raw_file_sha256']=hashlib.sha256(raw.encode()).hexdigest()
   for p in ch['paragraphs']:
    pos=p['source_position'];pos['first_line']+=1;pos['last_line']+=1
    for f in pos['source_fragments']:f['line']+=1
   ref=AS[0]['qualifiers']['source_kinship_frame']['fixed_witness_reference']['path'];dest=root/ref;dest.parent.mkdir(parents=True);dest.write_bytes((R/ref).read_bytes());ps={p['id']:(C['id'],p)for p in ch['paragraphs']};self.assertFalse(check(AS[0],ps,cs,root))
 def test_missing_original_receipt_rejected(self):
  with tempfile.TemporaryDirectory()as tmp:self.assertFalse(check(AS[0],root=Path(tmp)))
 def test_synthetic_other_names_and_ids(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);raw='(甲子乙)';rp=root/'sources/synthetic.txt';rp.parent.mkdir();rp.write_text(raw);p={'id':'synthetic:p','text':'甲子乙','text_layer':'witness_appended_pei_songzhi_note','source_position':{'first_line':1,'last_line':1,'source_layer':'pei_annotation','source_fragments':[{'line':1,'raw_start':1,'raw_end':4,'text':'甲子乙'}]},'mentions':[{'id':'p:a','start':0,'end':1,'surface':'甲','kind':'person','person_id':'aaa_bbb_ccc'},{'id':'p:b','start':2,'end':3,'surface':'乙','kind':'person','person_id':'ddd_eee_fff'}]};ch={'id':'synthetic','work_id':'w-synthetic','book_id':'b-synthetic','source_id':'s-synthetic','source':{'raw_path':'sources/synthetic.txt','raw_file_sha256':hashlib.sha256(raw.encode()).hexdigest(),'revision_id':'fixed','source_commit':'fixed'},'paragraphs':[p]};w={'source_commit':'fixed','raw_file':'sources/synthetic.txt','raw_sha256':ch['source']['raw_file_sha256'],'chapter_id':ch['id'],'units':[{'paragraph_id':p['id'],'text':p['text'],'text_layer':p['text_layer'],'source_position':p['source_position']}]};rp=root/'source-evidence/synth.json';rp.parent.mkdir();rb=json.dumps(w).encode();rp.write_bytes(rb);e={'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':p['text'],'subject_person_mention_id':'p:b','object_person_mention_id':'p:a'};b={'kind':'received_quoted_family_frame','rule':'named_parent_child','roles':{'parent':'p:a','child':'p:b'},'fields':{},'scope_anchor':{'paragraph_id':p['id'],'start':0,'end':3,'surface':p['text']},'source_revision':'fixed','paragraph_sha256':hashlib.sha256(p['text'].encode()).hexdigest(),'source_layer':p['text_layer'],'human_reviewed':False,'fixed_witness_reference':{'path':'source-evidence/synth.json','sha256':hashlib.sha256(rb).hexdigest()}};a={'subject_person_id':'ddd_eee_fff','object_person_id':'aaa_bbb_ccc','predicate':'father','status':'source_attested','human_reviewed':False,'qualifiers':{'source_term':'子','lineage':'paternal','source_kinship_frame':b},'evidence':[e]};self.assertTrue(check(a,{p['id']:(ch['id'],p)},{ch['id']:ch},root))
if __name__=='__main__':unittest.main()
