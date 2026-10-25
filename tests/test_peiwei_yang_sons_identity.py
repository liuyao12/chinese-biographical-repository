# coding: utf-8
from pathlib import Path
import json,hashlib,copy,unittest
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1];BASE='source-evidence/peiwei-yang-sons-identity';J=lambda p:json.loads((ROOT/p).read_text());H=lambda b:hashlib.sha256(b).hexdigest()
def context_valid(main,other,current,chapters,raw):
 a,b,c=chapters;pa=a['paragraphs'][5];pb=b['paragraphs'][4];pc=c['paragraphs'][1]
 def mark(p,mid):return next(m for m in p['mentions']if m['id']==mid)
 winner=mark(pb,'c-jinshu-043-leguang:p005:m0028');old=mark(pa,'c-sanguozhi-019-yangxiu:p006:m0098');jm=mark(pc,'c-jinshu-089-jishao:p002:m0059');ref=current['jin035_fixed_unmarked_raw_reference'];unit=raw[ref['raw_start']:ref['raw_end']]
 return (winner['surface']=='裴頠'and old['surface']=='裘頠'and old['person_id']==winner['person_id']==jm['person_id']==main['person_id']==other['person_id']==current['canonical_person_id']and jm['kind']=='person'
  and pa['text'][161:163]=='裴樂'and all(s in pa['text']for s in ['準子嶠字國彦髦字士彦','頠性弘方','廣性清淳','我二兒之優劣'])and all(s in pb['text']for s in ['准之二子曰喬曰髦','頠性弘方','廣性清淳','我二兒之優劣'])
  and [e['quote']for e in main['evidence']]==[pa['text'],pb['text']]and [e['quote']for e in other['evidence']]==[pc['text'],pb['text']]
  and '尚書左僕射裴頠' in pc['text']and unit==ref['quote']and unit.startswith('頠字逸民')and '遷尚書左僕射，侍中如故。'in unit and '倫又潛懷篡逆'in unit and '頠深慮賈后亂政'in unit)
class PeiWeiIdentityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=J('corpus/sanguozhi/019-yangxiu.json');cls.b=J('corpus/jinshu/043-leguang.json');cls.c=J('corpus/jinshu/089-jishao.json');cls.d=next(d for d in J('corpus/sanguozhi/019-yangxiu-identities.json')['decisions']if d['id']=='d-sanguozhi019-peiwei-yang-sons');cls.j=next(d for d in J('corpus/jinshu/089-jishao-identities.json')['decisions']if d['id']=='d-jin089-peiwei-office-context');cls.r=J(BASE+'/current-reading.json');ref=cls.r['jin035_fixed_unmarked_raw_reference'];cls.raw=(ROOT/ref['raw_file']).read_text();cls.pid=cls.d['person_id']
 def valid(self,d=None,j=None,r=None,chapters=None):return context_valid(d or self.d,j or self.j,r or self.r,chapters or [self.a,self.b,self.c],self.raw)
 def test_full_event_and_office_context(self):self.assertTrue(self.valid());self.assertEqual(H((ROOT/self.r['jin035_fixed_unmarked_raw_reference']['raw_file']).read_bytes()),self.r['jin035_fixed_unmarked_raw_reference']['raw_file_sha256'])
 def test_wrong_current_person_rejected(self):
  wrong=next(m['person_id']for m in self.b['paragraphs'][4]['mentions']if m['surface']=='廣');j=copy.deepcopy(self.j);j['person_id']=wrong;self.assertFalse(self.valid(j=j));d=copy.deepcopy(self.d);d['person_id']=wrong;self.assertFalse(self.valid(d=d));c=copy.deepcopy(self.c);m=next(m for m in c['paragraphs'][1]['mentions']if m['id']=='c-jinshu-089-jishao:p002:m0059');m['person_id']=wrong;r=copy.deepcopy(self.r);r['canonical_person_id']=wrong;self.assertFalse(self.valid(j=j,r=r,chapters=[self.a,self.b,c]))
 def test_wrong_office_or_time_context_rejected(self):
  r=copy.deepcopy(self.r);r['jin035_fixed_unmarked_raw_reference']['quote']=r['jin035_fixed_unmarked_raw_reference']['quote'].replace('尚書左僕射','太常');self.assertFalse(self.valid(r=r));c=copy.deepcopy(self.c);c['paragraphs'][1]['text']=c['paragraphs'][1]['text'].replace('尚書左僕射裴頠','太常裴頠');self.assertFalse(self.valid(chapters=[self.a,self.b,c]));r=copy.deepcopy(self.r);r['jin035_fixed_unmarked_raw_reference']['raw_start']+=1;self.assertFalse(self.valid(r=r))
 def test_historical_unresolved_and_reuse_captures_unchanged(self):
  q=J(BASE+'/historical-qualification.json')
  for row in q['historical_files']:self.assertEqual(H((ROOT/row['path']).read_bytes()),row['sha256'])
  old=J(BASE+'/historical-reading.json')['before_unresolved_jin089'];self.assertEqual(old['kind'],'unresolved');self.assertIsNone(old['person_id']);self.assertEqual(old['candidate_person_ids'],['dc7_573_800'])
 def test_raw_source_spelling_layers_not_normalized(self):
  self.assertIn('荀綽翼州記曰',self.a['paragraphs'][5]['text']);self.assertEqual(self.a['paragraphs'][5]['text_layer'],'witness_appended_pei_songzhi_note');self.assertIn('準與裘頠樂廣',self.a['paragraphs'][5]['text']);self.assertIn('曰喬曰髦',self.b['paragraphs'][4]['text']);self.assertFalse(self.a['source']['image_verified'])
 def test_one_keeper_union_and_no_alias(self):
  people=J('registry/persons.json')['persons'];ids=[p['id']for p in people];self.assertEqual(len(ids),len(set(ids)));self.assertEqual(ids.count(self.pid),1);p=next(p for p in people if p['id']==self.pid);self.assertEqual(p['label'],'裴頠');self.assertTrue({'裘頠','裴頠','裴','頠'}<={a['surface']for a in p['aliases']});self.assertIn('秀子',p['identity_note']);self.assertIn('八裴',p['identity_note']);self.assertFalse(p.get('id_aliases'))
 def test_retirement_and_unknown_old_query(self):
  old='dc7_573_800';self.assertIn(old,retired_person_ids(ROOT));self.assertTrue(allocation_conflicts(old,retired_person_ids(ROOT)));cat=load_catalog(ROOT);self.assertNotIn(old,cat[0])
  with self.assertRaises((ValueError,KeyError)):bundle(old,root=ROOT,catalog=cat)
  for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
