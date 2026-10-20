import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.table_person_profiles import build
ROOT=Path(__file__).resolve().parents[1]
class ProfileBundleNameComponents(unittest.TestCase):
 def fixture(self,directory,names):
  root=Path(directory);pid='abc_def_123'
  def put(path,data):
   p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False))
  put('data/corpus/index.json',{'chapters':[]});put('data/corpus/profile-names.json',{'records':[{'person_id':pid,'surname':'甲','ming':'乙','quote':'中央原記錄'}]});put('data/historical-tables/person-candidates.json',{'persons':[]});put('registry/persons.json',{'persons':[{'id':pid,'label':'甲乙','aliases':[]}]});put('exports/persons/index.json',{'persons':[{'person_id':pid}]})
  b={'canonical_person_id':pid,'person_ids':[pid],'passages':[],'most_mentioned_source_ids':[],'source_mention_summary':[],'table_occurrences':[],'mentions':[],'title_holdings':[],'address_assertions':[],'persons':[{'id':pid,'label':'甲乙','aliases':[]}],'sources':[],'relations':[],'date_normalizations':[]}
  if names is not None:b['name_components']=names
  put('exports/persons/'+pid+'.json',b);return root,pid,b
 def test_profile_preserves_all_central_and_corpus_name_records_exactly_as_bundle(self):
  names=[{'person_id':'abc_def_123','surname':'甲','ming':'乙','quote':'中央原記錄','work_id':'central-work','source_id':'central-source'},{'person_id':'abc_def_123','surname':'甲','ming':'乙','zi':'丙','quote':'甲乙字丙','work_id':'corpus-work','source_id':'corpus-source','references':[{'quote':'另一來源'}]}]
  with tempfile.TemporaryDirectory()as directory:
   root,pid,b=self.fixture(directory,names);build(root);p=json.loads((root/'data/corpus/profiles'/f'{pid}.json').read_text());self.assertEqual(p['name_components'],b['name_components'])
 def test_missing_bundle_names_do_not_resurrect_stale_central_record(self):
  with tempfile.TemporaryDirectory()as directory:
   root,pid,b=self.fixture(directory,None);build(root);p=json.loads((root/'data/corpus/profiles'/f'{pid}.json').read_text());self.assertEqual(p['name_components'],[])
 def test_actual_wangyi_brother_and_cao_profiles_follow_complete_bundle_sources(self):
  ids={'qsd_v11_ya1_AA':('懿','仲德',None),'lrq_cdc_wxj':('叡','元德',None),'30k_jzz_tpd_A':('真','子丹',None),'30k_jzz_tpd_AA':('爽','昭伯','黙')};captured={};prefix=str(ROOT/'data/corpus/profiles');original_read=Path.read_text
  def read(path,*a,**kw):return captured[str(path)]if str(path)in captured else original_read(path,*a,**kw)
  def write(path,text,*a,**kw):
   self.assertTrue(str(path).startswith(prefix+'/'));captured[str(path)]=text;return len(text)
  def mkdir(path,*a,**kw):self.assertEqual(str(path),prefix)
  with patch.object(Path,'read_text',read),patch.object(Path,'write_text',write),patch.object(Path,'mkdir',mkdir):build(ROOT,person_ids=set(ids))
  for pid,(ming,zi,xiaozhi)in ids.items():
   b=json.loads((ROOT/'exports/persons'/f'{pid}.json').read_text());p=json.loads(captured[str(ROOT/'data/corpus/profiles'/f'{pid}.json')]);self.assertEqual(p['name_components'],b.get('name_components',[]));self.assertTrue(any(r.get('ming')==ming and r.get('zi')==zi for r in p['name_components']))
   if xiaozhi:self.assertTrue(any(r.get('xiaozhi')==xiaozhi for r in p['name_components']))
if __name__=='__main__':unittest.main()
