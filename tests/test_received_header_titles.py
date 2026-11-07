"""Received heading choices exercise the public resolver and real filesystem proof."""
import copy,json,os,pathlib,tempfile,unittest
from scripts.profile_title_preferences import resolve,PreferenceCatalog,choice
BASE=pathlib.Path(os.environ.get('HEADER_TEST_SOURCE',pathlib.Path(__file__).resolve().parents[1]))
PAYLOAD=pathlib.Path(os.environ.get('HEADER_TEST_PAYLOAD',BASE))
PREF='corpus/editorial/xun-support-profile-title-preferences.json'
def load(p):return json.loads(p.read_bytes())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False)+'\n')
class ReceivedHeaderTitles(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name)
  pref=load(PAYLOAD/PREF);self.pref=pref;self.records=[];self.paths={}
  ids={d['person_id']for d in pref['decisions']}
  people=load(BASE/'registry/persons.json');people['persons']=[x for x in people['persons']if x['id']in ids];write(self.root/'registry/persons.json',people)
  write(self.root/'registry/works.json',load(BASE/'registry/works.json'))
  for d in pref['decisions']:
   found=[]
   for p in (PAYLOAD/'corpus').glob('*/*-titles.json'):
    doc=load(p)
    if any(h['id']==d['holding_id']for h in doc.get('holdings',[])):found.append((p,doc))
   p,doc=found[0];h=next(h for h in doc['holdings']if h['id']==d['holding_id']);b=h['received_header_attestation'];ch=load(BASE/b['chapter_path'])
   write(self.root/b['chapter_path'],ch);write(self.root/b['holding_path'],doc)
   self.records.extend([ch,doc]);self.paths[ch['id']]=(b['chapter_path'],b['holding_path'])
  self.records.append(pref);self.people={x['id']:x for x in people['persons']}
 def result(self):return resolve(self.records,self.people,self.root)
 def first(self):
  d=self.pref['decisions'][0];ch=next(x for x in self.records if x.get('id')==d['source_ref']['chapter_id']);doc=next(x for x in self.records if x.get('record_type')=='title_holding_assertion_set'and any(h['id']==d['holding_id']for h in x['holdings']));h=next(h for h in doc['holdings']if h['id']==d['holding_id']);return d,ch,doc,h
 def sync(self):
  for ch in [x for x in self.records if x.get('record_type')=='marked_chapter']:
   cp,hp=self.paths[ch['id']];write(self.root/cp,ch)
   doc=next(x for x in self.records if x.get('record_type')=='title_holding_assertion_set'and x['chapter_id']==ch['id']);write(self.root/hp,doc)
  d=load(self.root/'registry/persons.json');d['persons']=list(self.people.values());write(self.root/'registry/persons.json',d)
 def rejects(self):
  with self.assertRaises(ValueError):self.result()
 def test_four_real_headers(self):
  self.assertEqual(set(x['title']for x in self.result().values()),{'廬陵威王','世祖文皇帝','高祖文皇帝','秦孝王'})
 def test_wrong_recipient(self):
  d,ch,doc,h=self.first();h['person_id']=self.pref['decisions'][1]['person_id'];self.sync();self.rejects()
 def test_literal_title_change(self):
  d,ch,doc,h=self.first();h['title']='廬陵王';self.sync();self.rejects()
 def test_original_text_change(self):
  d,ch,doc,h=self.first();ch['paragraphs'][0]['text']+='。';self.sync();self.rejects()
 def test_caller_unknown_field(self):
  d,*_=self.first();self.people[d['person_id']]['unknown_test_field']=False;self.rejects()
 def test_physical_reverse_loss(self):
  d,ch,doc,h=self.first();p=self.people[d['person_id']];p['evidence']=[e for e in p['evidence']if e.get('mention_id')!=d['source_ref']['person_mention_id']];self.sync();self.rejects()
 def test_physical_alias_loss(self):
  d,ch,doc,h=self.first();m=d['source_ref']['person_mention_id'];p=self.people[d['person_id']];p['aliases']=[a for a in p['aliases']if m not in a.get('mention_ids',[])];self.sync();self.rejects()
 def test_metadata_mismatch(self):
  d,ch,doc,h=self.first();h['received_header_attestation']['source_metadata']['edition']='unproved';self.sync();self.rejects()
 def test_image_qualification_upgrade(self):
  d,ch,doc,h=self.first();ch['source']['image_verified']=True;h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.rejects()
 def test_unknown_print_upgrade(self):
  d,ch,doc,h=self.first();ch['source']['actual_print_edition']='unverified-print';h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.rejects()
 def test_unknown_registered_chapter(self):
  works=load(self.root/'registry/works.json');cid=self.pref['decisions'][0]['source_ref']['chapter_id']
  for w in works['works']:
   for b in w['books']:b['chapter_ids']=[x for x in b['chapter_ids']if x!=cid]
  write(self.root/'registry/works.json',works);self.rejects()
 def test_no_grant_date(self):
  d,ch,doc,h=self.first();h['effective_period']['start']={'status':'source_event','event_type':'grant','date_expression':'某年','evidence':h['evidence']};self.sync();self.rejects()
 def test_boolean_anchor(self):
  d,ch,doc,h=self.first();h['attestations'][0]['start']=False;d['source_ref']['start']=False;self.sync();self.rejects()
 def test_coherent_rekey_conserves_text_and_opaque_mids(self):
  old=self.pref['decisions'][0]['person_id'];new='zzz_abc_123_A';before=[(x['paragraphs'][0]['text'],[m['id']for m in x['paragraphs'][0]['mentions']])for x in self.records if x.get('record_type')=='marked_chapter']
  def rekey(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if k=='person_id'and v==old:x[k]=new
     else:rekey(v)
   elif isinstance(x,list):
    for v in x:rekey(v)
  rekey(self.records);p=self.people.pop(old);p['id']=new;self.people[new]=p;self.sync();self.assertIn(new,self.result())
  self.assertEqual(before,[(x['paragraphs'][0]['text'],[m['id']for m in x['paragraphs'][0]['mentions']])for x in self.records if x.get('record_type')=='marked_chapter'])
  self.people[new]['evidence']=[];self.sync();self.rejects()
 def test_single_endpoint_rekey(self):
  d,ch,doc,h=self.first();ch['paragraphs'][0]['mentions'][0]['person_id']='zzz_abc_123_A';self.sync();self.rejects()
 def test_transaction_cannot_reuse_after_raw_or_caller_change(self):
  pc=PreferenceCatalog(self.records,self.people,self.root);d=self.pref['decisions'][0];self.assertEqual(choice(pc,self.people,d['person_id'],self.root)['title'],'廬陵威王')
  self.people[d['person_id']]['unknownfield']=True
  with self.assertRaises(ValueError):choice(pc,self.people,d['person_id'],self.root)
 def test_transaction_raw_registry_invalidation(self):
  pc=PreferenceCatalog(self.records,self.people,self.root);d=self.pref['decisions'][0];p=self.root/'registry/persons.json';p.write_bytes(p.read_bytes()+b' ')
  with self.assertRaises(ValueError):choice(pc,self.people,d['person_id'],self.root)
 def test_transaction_replacement_caller(self):
  pc=PreferenceCatalog(self.records,self.people,self.root);d=self.pref['decisions'][0];other=copy.deepcopy(self.people);other[d['person_id']]['newfield']=True
  with self.assertRaises(ValueError):choice(pc,other,d['person_id'],self.root)
 def test_legal_physical_metadata_enrichment(self):
  d,*_=self.first();self.people[d['person_id']]['future_metadata']={'a':[True,1,None]};self.sync();self.assertIn(d['person_id'],self.result())
 def test_missing_physical_holding(self):
  d,ch,doc,h=self.first();(self.root/h['received_header_attestation']['holding_path']).unlink();self.rejects()
 def test_caller_holding_metadata_theft(self):
  d,ch,doc,h=self.first();h['unproved']=True;self.rejects()
 def test_other_owner_reverse_theft(self):
  d,ch,doc,h=self.first();other=next(x for k,x in self.people.items()if k!=d['person_id']);ev=next(e for e in self.people[d['person_id']]['evidence']if e.get('mention_id')==d['source_ref']['person_mention_id']);other['evidence'].append(copy.deepcopy(ev));self.sync();self.rejects()
 def test_other_owner_alias_theft(self):
  d,ch,doc,h=self.first();other=next(x for k,x in self.people.items()if k!=d['person_id']);a=next(a for a in self.people[d['person_id']]['aliases']if d['source_ref']['person_mention_id']in a.get('mention_ids',[]));other['aliases'].append(copy.deepcopy(a));self.sync();self.rejects()
 def test_duplicate_mid_in_same_alias(self):
  d,ch,doc,h=self.first();mid=d['source_ref']['person_mention_id'];a=next(a for a in self.people[d['person_id']]['aliases']if mid in a.get('mention_ids',[]));a['mention_ids'].append(mid);self.sync();self.rejects()
 def test_duplicate_reverse(self):
  d,ch,doc,h=self.first();p=self.people[d['person_id']];e=next(e for e in p['evidence']if e.get('mention_id')==d['source_ref']['person_mention_id']);p['evidence'].append(copy.deepcopy(e));self.sync();self.rejects()
 def test_consistent_but_false_acquisition_upgrade(self):
  for flag in('original_wikitext_obtained','raw_wikitext_obtained','fixed_permalink_body_read'):
   with self.subTest(flag=flag):
    d,ch,doc,h=self.first();ch['source'][flag]=True;h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.rejects();ch['source'].pop(flag);h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync()
 def test_consistent_edition_claim_upgrade(self):
  d,ch,doc,h=self.first();ch['source']['edition']='unverified Wuyingdian edition claim';h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.rejects()
 def test_consistent_print_identifier_upgrade(self):
  for field in('actual_print_edition_id','printed_base_edition_id','printed_edition','printed_edition_id','print_edition','print_edition_id'):
   with self.subTest(field=field):
    d,ch,doc,h=self.first();ch['source'][field]='unverified-print';h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.rejects();ch['source'].pop(field);h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync()
 def test_unknown_edition_qualification_enrichment(self):
  d,ch,doc,h=self.first();ch['source']['edition']='普通數位轉錄；印本未知；書影未核。附錄取得說明，不提升底本資格。';ch['source']['editorial_note']='metadata enrichment';h['received_header_attestation']['source_metadata']=copy.deepcopy(ch['source']);self.sync();self.assertIn(d['person_id'],self.result())
if __name__=='__main__':unittest.main()
