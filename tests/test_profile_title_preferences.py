import unittest,copy,hashlib
from pathlib import Path
from scripts.profile_title_preferences import resolve
ROOT=Path(__file__).resolve().parents[1]
def fixture(slot='postoffice'):
 t='甲永平三年為郡守典戶口四年卒追贈太傅假節';pid='arbitrary-person';cid='synthetic-chapter';pp='synthetic-paragraph';mid='synthetic-subject'
 m=dict(id=mid,kind='person',person_id=pid,start=0,end=1,surface='甲')
 p=dict(id=pp,text=t,text_layer='commentary',mentions=[m]);c=dict(id=cid,record_type='marked_chapter',work_id='synthetic-work',book_id='synthetic-book',source_id='synthetic-source',source=dict(revision_id=1),paragraphs=[p],annotation={})
 def a(term):
  s=t.index(term);return dict(paragraph_id=pp,start=s,end=s+len(term),surface=term)
 fields={k:a(v)for k,v in dict(time='永平三年',office='郡守',duty='典戶口',deathdate='四年',postoffice='太傅',privilege='假節').items()};f=fields[slot];mode='posthumous_grant'if slot=='postoffice'else'grant';title=f['surface']
 ev=dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=cid,paragraph_id=pp,quote=t,person_mention_id=mid);at=dict(id='synthetic-holding:a',paragraph_id=pp,start=f['start'],end=f['end'],surface=title,person_mention_id=mid,date_expression=None)
 h=dict(id='synthetic-holding',person_id=pid,status='source_attested',title=title,kind='office',mode=mode,human_reviewed=False,evidence=[ev],attestations=[at],appointment_role='posthumous_office'if slot=='postoffice'else'appointment',effective_period=dict(start=dict(status='source_event',event_type=mode,date_expression=None if slot=='postoffice'else'永平三年',evidence=[ev]),end=dict(status='unknown',date_expression=None,evidence=[])),source_career_role=dict(kind='received_career_role_frame',paragraph_id=pp,rule='noted_son_career',slot=slot,recipient_role='subject',roles=dict(subject=mid),fields=fields,scope_anchor=dict(paragraph_id=pp,start=0,end=len(t),surface=t),source_revision=1,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),human_reviewed=False))
 ref={k:v for k,v in ev.items()if k not in('quote',)};ref.update(start=f['start'],end=f['end'],surface=title)
 d=dict(id='synthetic-choice',person_id=pid,selection_kind='default_profile_title',holding_id=h['id'],attestation_id=at['id'],source_ref=ref,scope='timeless_profile_heading',temporal_claim='none',status='editorial_provisional',rationale='Explicit synthetic presentation decision.',human_reviewed=False)
 rows=[c,dict(record_type='title_holding_assertion_set',holdings=[h]),dict(format_version='0.1',record_type='profile_title_preference_set',decisions=[d])];return rows,{pid:dict(id=pid)},h,d,c
class DefaultTitles(unittest.TestCase):
 def test_synthetic_posthumous_and_granted_without_dates(self):
  for slot in('postoffice','office'):
   rows,people,h,d,c=fixture(slot);v=resolve(rows,people,ROOT)[h['person_id']];self.assertEqual(v['title'],h['title']);self.assertEqual(v['mode'],h['mode']);self.assertNotIn('effective_period',v)
 def test_no_choice_no_new_field(self):
  rows,people,*_=fixture();self.assertEqual(resolve(rows[:-1],people,ROOT),{})
 def test_foreign_person_proposal_missing_attestation(self):
  for key,value in(('person_id','other'),('holding_id','proposal-id'),('attestation_id','missing')):
   rows,people,h,d,c=fixture();d[key]=value;self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_duplicate_global_choices_rejected(self):
  rows,people,h,d,c=fixture();rows.append(copy.deepcopy(rows[-1]));rows[-1]['decisions'][0]['id']='another-choice';self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_free_title_dates_lifetime_claim_rejected(self):
  for key,value in(('title','太傅郡侯'),('year',200),('temporal_claim','lifelong')):
   rows,people,h,d,c=fixture();d[key]=value;self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_offset_source_person_and_raw_title_rejected(self):
  for mode in('offset','source','person','title'):
   rows,people,h,d,c=fixture()
   if mode=='offset':d['source_ref']['start']+=1
   elif mode=='source':d['source_ref']['source_id']='other'
   elif mode=='person':c['paragraphs'][0]['mentions'][0]['person_id']='other'
   else:h['title']='太保'
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_bare_attestation_challenge_and_unresolved_subject(self):
  for mode in('bare','challenge','unresolved'):
   rows,people,h,d,c=fixture()
   if mode=='bare':h['mode']='attestation'
   elif mode=='challenge':h['source_qualification']=dict(kind='reported_office_challenged_by_commentary')
   else:c['annotation']['unresolved_identity_cases']=[dict(mention_id=d['source_ref']['person_mention_id'])]
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_same_event_unassumed_reject_other_event_same_word_does_not(self):
  rows,people,h,d,c=fixture();c['annotation']['title_proposals']=[dict(title=h['title'],outcome='not_assumed',holding_id='other-holding')];self.assertTrue(resolve(rows,people,ROOT));c['annotation']['title_proposals'][0]['holding_id']=h['id'];self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_unknown_grammar_and_source_mode_forgery(self):
  for mode in('grammar','mode'):
   rows,people,h,d,c=fixture()
   if mode=='grammar':h['source_career_role']['rule']='guessed_by_rank'
   else:h['mode']='grant';h['effective_period']['start']['event_type']='grant'
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_transaction_is_local_readonly_and_revalidates_changed_inputs(self):
  from scripts.profile_title_preferences import PreferenceCatalog,choice
  rows,people,h,d,c=fixture();tx=PreferenceCatalog(rows,people,ROOT)
  self.assertEqual(choice(tx,people,h['person_id'],ROOT)['title'],'太傅')
  self.assertRaises(TypeError,tx.append,rows[0])
  self.assertRaises(ValueError,choice,tx,people,h['person_id'],ROOT.parent/'other-tree')
  d['source_ref']['start']+=1
  self.assertRaises(ValueError,choice,tx,people,h['person_id'],ROOT)
  self.assertRaises(ValueError,PreferenceCatalog,rows,people,ROOT)
 def test_index_is_revalidated_per_transaction_not_per_person(self):
  import scripts.profile_title_preferences as module
  from unittest.mock import patch
  rows,people,h,d,c=fixture()
  with patch.object(module,'resolve',wraps=module.resolve)as spy:
   tx=module.PreferenceCatalog(rows,people,ROOT)
   for i in range(5):module.choice(tx,people,h['person_id'],ROOT);module.choice(tx,people,'other',ROOT)
   self.assertEqual(spy.call_count,1)
   module.PreferenceCatalog(rows,people,ROOT);self.assertEqual(spy.call_count,2)
 def test_alias_cannot_replace_canonical(self):
  rows,people,h,d,c=fixture();people[h['person_id']]['id_aliases']=[h['person_id']];self.assertRaises(ValueError,resolve,rows,people,ROOT)
if __name__=='__main__':unittest.main()
