import json,tempfile,unittest
from pathlib import Path
from scripts.table_person_profiles import build
class ProfileAuthority(unittest.TestCase):
 def test_stale_reader_index_cannot_hide_current_identity_caveat(self):
  with tempfile.TemporaryDirectory()as directory:
   r=Path(directory);pid='abc_def_123'
   def put(path,data):
    p=r/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False))
   put('data/corpus/index.json',{'chapters':[]});put('data/corpus/profile-names.json',{'records':[]});put('data/historical-tables/person-candidates.json',{'persons':[]})
   put('data/corpus/persons.json',{pid:{'id':pid,'label':'舊稱','identity_note':None}})
   put('registry/persons.json',{'persons':[{'id':pid,'label':'新稱','identity_note':'同人暫定；不能排除更替。','historicity':'legendary_tradition'}]})
   put('exports/persons/index.json',{'persons':[{'person_id':pid}]})
   put('exports/persons/'+pid+'.json',{'canonical_person_id':pid,'person_ids':[pid],'passages':[],'most_mentioned_source_ids':[],'source_mention_summary':[],'table_occurrences':[],'mentions':[],'title_holdings':[],'address_assertions':[],'persons':[{'id':pid,'label':'新稱','aliases':[]}],'sources':[],'relations':[],'date_normalizations':[]})
   build(r);p=json.loads((r/'data/corpus/profiles'/f'{pid}.json').read_text());self.assertEqual(p['label'],'新稱');self.assertEqual(p['identity_note'],'同人暫定；不能排除更替。');self.assertEqual(p['historicity'],'legendary_tradition')
if __name__=='__main__':unittest.main()
