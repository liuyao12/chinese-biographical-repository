from pathlib import Path
import copy,unittest
ROOT=Path(__file__).resolve().parents[1]
class SGZ015FullPending(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts import fixed_wyd_sgz015_jia_opening as h
  cls.h=h;cls.st=h.state(ROOT);cls.ch=cls.st['chapter'];cls.records=[cls.ch]+[h.read(ROOT,h.CH.removesuffix('.json')+'-'+key+'.json')for key in cls.st['contract']['sidecar_templates']]
  if 'ner_contract'in cls.st:
   n=cls.st['ner_contract'];cls.records += [h.read(ROOT,p)for p in n['sidecar_templates']]+[h.read(ROOT,p)for p in sorted(set(s['path']for s in n['known_seeds'].values()))]
  if 'ner_contract'in cls.st:cls.records += h.caozhang_catalog_support(ROOT)
 def test_exact_full_text_keeps78_and_pending_rest(self):
  self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),3980);self.assertEqual(len(self.ch['paragraphs']),28);self.assertEqual([len(p['text'])for p in self.ch['paragraphs'][:2]],[40,38]);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),369 if 'ner_contract'in self.st else 11)
  for p in self.ch['paragraphs'][2:]:
   if 'ner_contract'in self.st:self.assertEqual(p['annotation_status'],'in_progress');self.assertTrue(p['mentions'])
   else:self.assertEqual(p['annotation_status'],'pending');self.assertEqual(p['mentions'],[])
 def test_unknown8_stays_editorial_null(self):
  xs=self.st['full_contract']['unknown_doc']['readings'];self.assertEqual(len(xs),8)
  for u in xs:self.assertIsNone(u['accepted']);self.assertTrue(u['editorial_placeholder']);self.assertFalse(u['original_printed_character_claimed'])
 def test_full_added_text_and_old_boundary_drift_rejected(self):
  for index in(0,2,27):
   c=copy.deepcopy(self.ch);c['paragraphs'][index]['text']='錯'+c['paragraphs'][index]['text'][1:]
   with self.assertRaises(ValueError):self.h.state(ROOT,c)
  c=copy.deepcopy(self.ch);c['paragraphs'][2]['mentions']=[{'id':'fake','kind':'person','surface':c['paragraphs'][2]['text'][0],'start':0,'end':1,'person_id':self.st['roles']['kui']}]
  with self.assertRaises(ValueError):self.h.state(ROOT,c)
 def test_actual_full_catalog_source_membership(self):
  self.h.guard_bundle(ROOT,self.st['roles']['kui'],self.st['people'],self.records)
  for rows in(self.records[1:],self.records[:-1],self.records+[{'record_type':'person_assertion_set','chapter_id':self.h.CID,'assertions':[]}]):
   with self.assertRaises(ValueError):self.h.guard_bundle(ROOT,self.st['roles']['kui'],self.st['people'],rows)
if __name__=='__main__':unittest.main()
