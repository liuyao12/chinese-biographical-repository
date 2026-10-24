"""Synthetic source-record contract controls, no historical-name or ID whitelist."""
import unittest,copy
from scripts.preferred_name_components import validated_readings,locator,reading_errors
class CrossSourceNameReading(unittest.TestCase):
 def setUp(self):
  self.pid='synthetic-canonical';self.chapters={};self.names=[];refs=[];evidence=[]
  for i,form in enumerate(('悦','悅')):
   cid='synthetic-chapter-'+str(i);pid=cid+':paragraph';text='某名'+form+'。';mark=dict(id=pid+':name',start=2,end=3,surface=form,kind='person',person_id=self.pid);p=dict(id=pid,text=text,mentions=[mark]);c=dict(id=cid,record_type='marked_chapter',source_id='source-'+str(i),work_id='work-'+str(i),book_id='book-'+str(i),paragraphs=[p]);self.chapters[cid]=c;n=dict(id='synthetic-record-'+str(i),person_id=self.pid,chapter_id=cid,paragraph_id=pid,surname=None,ming=form,quote=text);self.names.append(n);refs.append(dict(record=locator(n),anchor=copy.deepcopy(mark),source_id=c['source_id']));evidence.append(dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=cid,paragraph_id=pid,quote=text))
  self.decision=dict(id='synthetic-identity-decision',person_id=self.pid,scope='cross_chapter',status='contextual_provisional',chapter_ids=list(self.chapters),evidence=evidence)
  self.reading=dict(id='synthetic-reading',person_id=self.pid,field='ming',preferred_value='悅',source_values=['悦','悅'],records=refs,status='editorial_provisional',human_reviewed=False,rationale='An editorial display choice across exactly attested same-canonical records.',coverage='listed_records_only',basis=dict(kind='cross_source_attested_name_spellings',records=copy.deepcopy(refs),identity_decision_id=self.decision['id']))
 def check(self,r=None,n=None,d=None):return reading_errors(r or self.reading,n or self.names,self.chapters,[d or self.decision])
 def test_valid_cross_source_and_full_native_boundary(self):
  self.assertEqual(self.check(),[]);records=[dict(record_type='person_identity_decision_set',decisions=[self.decision]),dict(format_version='0.1',record_type='preferred_name_component_reading_set',readings=[self.reading])];self.assertEqual(validated_readings(records,self.names,self.chapters),[self.reading])
 def test_wrong_person_and_unknown_identity(self):
  for key,value in [('person_id','another-person'),('scope','within_chapter')]:
   d=copy.deepcopy(self.decision);d[key]=value;self.assertTrue(self.check(d=d))
  self.assertTrue(reading_errors(self.reading,self.names,self.chapters,[]))
 def test_wrong_record_locator_and_source_anchor(self):
  for key,value in [('id','wrong-record'),('ming','說'),('paragraph_id','wrong-paragraph')]:
   r=copy.deepcopy(self.reading);r['records'][0]['record'][key]=value;r['basis']['records']=copy.deepcopy(r['records']);self.assertTrue(self.check(r))
  r=copy.deepcopy(self.reading);r['records'][0]['anchor']['person_id']='another-person';r['basis']['records']=copy.deepcopy(r['records']);self.assertTrue(self.check(r))
 def test_cropped_quote_in_record_and_identity_evidence(self):
  r=copy.deepcopy(self.reading);r['records'][0]['record']['quote']='名悦';r['basis']['records']=copy.deepcopy(r['records']);n=copy.deepcopy(self.names);n[0]['quote']='名悦';self.assertTrue(self.check(r,n))
  d=copy.deepcopy(self.decision);d['evidence'][0]['quote']='名悦';self.assertTrue(self.check(d=d))
 def test_unattested_preferred_and_modified_source_value(self):
  r=copy.deepcopy(self.reading);r['preferred_value']='恱';self.assertTrue(self.check(r));n=copy.deepcopy(self.names);n[0]['ming']='說';self.assertTrue(self.check(n=n))
 def test_new_same_form_record_must_be_listed(self):
  n=copy.deepcopy(self.names);v=copy.deepcopy(n[0]);v['id']='new-record';n.append(v);self.assertTrue(self.check(n=n))
 def test_third_form_not_globally_normalized(self):
  n=copy.deepcopy(self.names);v=copy.deepcopy(n[0]);v.update(id='third-record',ming='恱');n.append(v);self.assertEqual(self.check(n=n),[]);self.assertFalse(any(x['record']==locator(v)for x in self.reading['records']))
 def test_old_same_paragraph_rule_not_relaxed(self):
  r=copy.deepcopy(self.reading);r['basis']=dict(kind='same_paragraph_mixed_name_spellings',source_id='source-0',chapter_id='synthetic-chapter-0',paragraph_id='synthetic-chapter-0:paragraph',quote='某名悦。',anchors=[r['records'][0]['anchor'],r['records'][1]['anchor']]);self.assertTrue(self.check(r))
if __name__=='__main__':unittest.main()
