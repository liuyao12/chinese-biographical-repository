import copy,json,unittest
from pathlib import Path
from scripts.wife_father_clause import wife_father_clause_valid
ROOT=Path(__file__).resolve().parents[1]
class WifeFatherClause(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  c=json.loads((ROOT/'corpus/jinshu/079.json').read_text());cls.ps={p['id']:(c['id'],p)for p in c['paragraphs']};r=json.loads((ROOT/'corpus/jinshu/079-assertions.json').read_text());cls.rows=[a for a in r['assertions']if a.get('qualifiers',{}).get('relationship_basis')=='named_wifes_father']
 def test_three_literal_roles(self):self.assertEqual(len(self.rows),2);self.assertTrue(all(wife_father_clause_valid(a,self.ps)for a in self.rows))
 def test_wrong_parent_or_subject(self):
  for field,value in [('predicate','mother'),('subject_person_id',self.rows[1]['object_person_id']),('object_person_id',self.rows[1]['object_person_id'])]:
   a=copy.deepcopy(self.rows[0]);a[field]=value;self.assertFalse(wife_father_clause_valid(a,self.ps))
 def test_outer_quote_even_after_sentence_boundary(self):
  a=copy.deepcopy(self.rows[0]);ps=copy.deepcopy(self.ps);p=ps[a['evidence'][0]['paragraph_id']][1];p['text']='「'+p['text']+'」';a['evidence'][0]['quote']=p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  for key in ['clause_anchor','locality_prefix_anchor']:
   x=a['qualifiers']['wife_father_context'][key];x['start']+=1;x['end']+=1
  self.assertFalse(wife_father_clause_valid(a,ps))
 def test_not_commentary_or_attached_note(self):
  for changes in [{'text_layer':'witness_appended_bangu_note'},{'annotator':'someone'},{'attached_note_to_paragraph_id':'other'}]:
   a=copy.deepcopy(self.rows[0]);ps=copy.deepcopy(self.ps);ps[a['evidence'][0]['paragraph_id']][1].update(changes);self.assertFalse(wife_father_clause_valid(a,ps))
if __name__=='__main__':unittest.main()
