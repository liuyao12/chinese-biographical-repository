# coding:utf-8
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import contextmanager
from scripts.fixed_wikisource_units import source_errors
R=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/023-peiqian-ws2376966.json';AA='corpus/sanguozhi/023-peiqian-ws2376966-assertions.json'

@contextmanager
def current_json_views(changes):
 """Inject current source records through both real readers; captures stay byte-exact."""
 original_bytes,original_text=Path.read_bytes,Path.read_text
 payload={(R/rel).resolve():json.dumps(value,ensure_ascii=False).encode('utf8')for rel,value in changes.items()}
 def read_bytes(path,*args,**kwargs):
  return payload[path.resolve()]if path.resolve()in payload else original_bytes(path,*args,**kwargs)
 def read_text(path,*args,**kwargs):
  if path.resolve()in payload:return payload[path.resolve()].decode('utf8')
  return original_text(path,*args,**kwargs)
 with patch.object(Path,'read_bytes',read_bytes),patch.object(Path,'read_text',read_text):yield

class PeiQianFamilyOrder(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.ch=json.loads((R/CH).read_bytes());c.aa=json.loads((R/AA).read_bytes());c.by={a['id']:a for a in c.aa['assertions']}
 def test_child_is_explicit_zi_and_layers_are_kept(self):
  self.assertEqual(source_errors(self.ch,R),[]);a=self.by['a-sgz023-peiqian-xiu-father-qian'];self.assertEqual(a['predicate'],'father');self.assertEqual(a['qualifiers']['source_term'],'子');self.assertEqual(a['context']['child_term_anchor']['surface'],'子');p={p['id']:p for p in self.ch['paragraphs']};first,last=a['context']['paragraph_ids'];self.assertEqual(p[first]['text_layer'],'witness_appended_pei_songzhi_note');self.assertEqual(p[last]['text_layer'],'received_chapter');self.assertTrue(p[last]['text'].startswith('子秀嗣。'));self.assertEqual([p[first]['source_position']['first_line'],p[last]['source_position']['first_line']],[71,71]);self.assertIn('潛',p[a['context']['received_biography_subject_paragraph_id']]['text'])
 def test_eldest_is_one_and_other_ordinals_are_unknown(self):
  li=self.by['a-sgz023-peiqian-li-father-hui'];self.assertEqual(li['qualifiers']['birth_order']['ordinal'],1);self.assertEqual(li['qualifiers']['birth_order']['source_term'],'長子')
  for child in ['kang','kai','chuo']:self.assertNotIn('birth_order',self.by['a-sgz023-peiqian-'+child+'-father-hui']['qualifiers'])
  for old,new in [('li','kang'),('kang','kai'),('kai','chuo')]:
   a=self.by['a-sgz023-peiqian-'+old+'-older-than-'+new];q=a['qualifiers']['relative_birth_order'];self.assertEqual(a['predicate'],'brother');self.assertEqual(q['older_person_id'],a['subject_person_id']);self.assertEqual(q['younger_person_id'],a['object_person_id']);self.assertIsNone(q['younger_ordinal']);self.assertEqual(q['older_ordinal'],1 if old=='li'else None)
  hui=self.by['a-sgz023-peiqian-hui-brother-qian']['qualifiers']['relative_birth_order'];self.assertIsNone(hui['older_ordinal']);self.assertIsNone(hui['younger_ordinal'])
 def test_child_succession_is_not_adoption_and_wrong_parent_fails(self):
  raw=Path.read_bytes
  for kind in ['adoption','succession_only','wrong_parent','relabel_note']:
   aa=copy.deepcopy(self.aa);c=copy.deepcopy(self.ch);a=next(a for a in aa['assertions']if a['id']=='a-sgz023-peiqian-xiu-father-qian')
   if kind=='adoption':a['predicate']='adoptive_father'
   elif kind=='succession_only':a['qualifiers']['source_term']='嗣'
   elif kind=='wrong_parent':a['object_person_id']='kbq_kjc_n2f_B'
   else:next(p for p in c['paragraphs']if p['id']==a['context']['paragraph_ids'][0])['text_layer']='received_chapter'
   with current_json_views({AA:aa}):self.assertTrue(source_errors(c,R),kind)
 def test_order_and_ordinal_cannot_be_coherently_reversed_or_invented(self):
  raw=Path.read_bytes
  for kind in ['swap','invent','erase_one']:
   aa=copy.deepcopy(self.aa)
   if kind=='erase_one':next(a for a in aa['assertions']if a['id']=='a-sgz023-peiqian-li-father-hui')['qualifiers']['birth_order']['ordinal']=None
   else:
    a=next(a for a in aa['assertions']if a['id']=='a-sgz023-peiqian-kang-older-than-kai');q=a['qualifiers']['relative_birth_order']
    if kind=='invent':q['older_ordinal']=2;q['younger_ordinal']=3
    else:
     a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];q['older_person_id'],q['younger_person_id']=q['younger_person_id'],q['older_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
   with current_json_views({AA:aa}):self.assertTrue(source_errors(self.ch,R),kind)
if __name__=='__main__':unittest.main()
