# coding: utf-8
"""Native fixed-witness named-recipient gift regression; no private dependencies."""
from pathlib import Path
import copy,json,sys,unittest,hashlib
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT)not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.posthumous_gifts import posthumous_gift_valid
from scripts.validate_corpus import normalized_date_errors
FX=json.loads((Path(__file__).parent/'fixtures/jin039-named-gift39.json').read_text(encoding='utf-8'))
def maps(f):
 c=f['chapter'];return ({p['id']:(c['id'],p)for p in c['paragraphs']},{m['id']:(c['id'],p['id'],m)for p in c['paragraphs']for m in p['mentions']},{f['death']['id']:f['death']})
def valid(f):return posthumous_gift_valid(f['holding'],*maps(f))
class NamedRecipientPosthumousGiftTests(unittest.TestCase):
 def setUp(self):self.f=copy.deepcopy(FX)
 def bad(self,path,value):
  o=self.f
  for k in path[:-1]:o=o[k]
  o[path[-1]]=value;self.assertFalse(valid(self.f))
 def test_actual_named_recipient_267(self):
  self.assertTrue(valid(self.f));h=self.f['holding'];d=h['effective_period']['start']['normalized_date'];self.assertEqual(d['year'],267);self.assertEqual(normalized_date_errors(d,{self.f['chapter']['id']:self.f['chapter']}),[])
 def test_original_word_and_not_lifetime_office(self):
  h=self.f['holding'];self.assertEqual(h['posthumous_basis']['source_clause_anchor']['surface'],'其贈沈司空公');self.assertEqual(h['mode'],'posthumous_grant');self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_not_empire_at_paragraph_start(self):
  p=self.f['chapter']['paragraphs'][0];self.assertTrue(p['text'].startswith('及帝'));self.assertTrue(valid(self.f));self.assertEqual(self.f['holding']['person_id'],self.f['death']['person_id'])
 def test_wrong_recipient(self):self.bad(['holding','person_id'],'hgm_jvn_hle')
 def test_other_person_death(self):self.bad(['death','person_id'],'hgm_jvn_hle')
 def test_death_not_death(self):self.bad(['death','event_type'],'birth')
 def test_missing_death(self):self.bad(['holding','posthumous_basis','death_event_id'],'missing')
 def test_lifetime_mode_rejected(self):self.bad(['holding','mode'],'grant')
 def test_wrong_office(self):self.bad(['holding','title'],'司徒')
 def test_wrong_mention(self):self.bad(['holding','posthumous_basis','recipient_person_mention_id'],FX['chapter']['paragraphs'][0]['mentions'][0]['id'])
 def test_wrong_revision(self):self.bad(['holding','posthumous_basis','source_revision'],123)
 def test_wrong_paragraph_hash(self):self.bad(['holding','posthumous_basis','paragraph_sha256'],'0'*64)
 def test_wrong_grant_anchor(self):self.bad(['holding','posthumous_basis','grant_anchor','start'],0)
 def test_wrong_death_anchor(self):self.bad(['holding','posthumous_basis','death_anchor','surface'],'荀氏卒')
 def test_wrong_relative_anchor(self):self.bad(['holding','posthumous_basis','relative_date_anchor','start'],0)
 def test_267_cannot_be266(self):self.bad(['holding','effective_period','start','normalized_date','year'],266)
 def test_267_cannot_be268(self):self.bad(['holding','effective_period','start','normalized_date','year'],268)
 def test_original_relative_word_not_fabricated_full_year(self):self.bad(['holding','effective_period','start','date_expression'],'泰始三年')
 def test_bad_relative_mapping(self):self.bad(['holding','effective_period','start','normalized_date','regnal_year_mapping','year_offset'],0)
 def test_other_antecedent(self):self.bad(['holding','effective_period','start','normalized_date','relative_year_reference','antecedent_expression'],'咸寧二年')
 def test_attestation_not_posthumous_usage(self):self.bad(['holding','attestations',0,'usage'],'narrative')
 def test_source_full_paragraph_required(self):self.bad(['holding','posthumous_basis','source_term'],'其贈沈司空公')
 def test_same_source_scope_required(self):self.bad(['death','evidence',0,'paragraph_id'],'other')
 def test_other_source_death(self):self.bad(['death','evidence',0,'source_id'],'other')
 def test_synthetic_other_named_recipient(self):
  old=FX['holding']['person_id'];new='synthetic-person'
  def change(x):
   if isinstance(x,dict):return {k:change(v)for k,v in x.items()}
   if isinstance(x,list):return [change(v)for v in x]
   if isinstance(x,str):return new if x==old else x.replace('沈','甲')
   return x
  f=change(self.f);f['holding']['posthumous_basis']['paragraph_sha256']=hashlib.sha256(f['chapter']['paragraphs'][0]['text'].encode()).hexdigest();self.assertTrue(valid(f))
if __name__=='__main__':unittest.main()
