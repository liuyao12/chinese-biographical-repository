# coding: utf-8
import json,copy,unittest,tempfile,shutil,hashlib
from pathlib import Path
from scripts.explicit_topic_gifts import explicit_topic_gift_valid
from scripts.posthumous_enfeoffments import valid as fief_valid
from scripts.biography_calendar_context import context_errors,death_subject_valid
from scripts.calendar_wiring import binding_errors
R=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
class Models(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=[read(R/f'corpus/songshu/{n}.json')for n in ['042','063-wanghua-tanshou']];cls.ps={p['id']:(c['id'],p)for c in cls.ch for p in c['paragraphs']};cls.ms={m['id']:(c['id'],p['id'],m)for c in cls.ch for p in c['paragraphs']for m in p['mentions']};cls.events={e['id']:e for n in ['042','063-wanghua-tanshou']for e in read(R/f'corpus/songshu/{n}-life-events.json')['events']};cls.hs=[h for n in ['042','063-wanghua-tanshou']for h in read(R/f'corpus/songshu/{n}-titles.json')['holdings']];cls.gifts=[h for h in cls.hs if h.get('posthumous_basis',{}).get('kind')=='explicit_topic_scoped_gift'];cls.fiefs=[h for h in cls.hs if h['mode']=='posthumous_enfeoffment'];cls.ctx=read(R/'corpus/calendar-contexts/song-wang-phase9.json')['records']
 def gv(self,h,ps=None,ms=None,events=None):return explicit_topic_gift_valid(h,ps or self.ps,ms or self.ms,events or self.events)
 def test_nonzero_topic_and_sovereign_reply_gifts(self):
  self.assertEqual(len(self.gifts),2)
  for h in self.gifts:self.assertGreater(self.ms[h['posthumous_basis']['topic_person_mention_id']][2]['start'],0);self.assertTrue(self.gv(h))
 def test_wrong_recipient_is_rejected(self):
  h=copy.deepcopy(self.gifts[0]);h['person_id']='3bh_k4m_fg4';self.assertFalse(self.gv(h))
 def test_emperor_cannot_replace_explicit_topic(self):
  h=copy.deepcopy(self.gifts[0]);b=h['posthumous_basis'];b['topic_person_mention_id']=b['sovereign_replies'][0]['person_mention_id'];self.assertFalse(self.gv(h))
 def test_unlisted_intervening_emperor_is_not_silently_ignored(self):
  h=copy.deepcopy(self.gifts[0]);h['posthumous_basis']['sovereign_replies']=[];self.assertFalse(self.gv(h))
 def test_grant_cannot_precede_death(self):
  h=copy.deepcopy(self.gifts[0]);b=h['posthumous_basis'];b['death_anchor']=copy.deepcopy(b['gift_anchor']);self.assertFalse(self.gv(h))
 def synthetic(self,topic_switch=False):
  text='先是陳甲寢疾，天子不許。九年，'+('陳乙卒'if topic_switch else'薨')+'。贈太保。';p=dict(id='p',text=text,text_layer='received_chapter',mentions=[])
  def mark(surface,pid):
   i=text.index(surface);m=dict(id='m'+str(len(p['mentions'])),kind='person',person_id=pid,start=i,end=i+len(surface),surface=surface);p['mentions'].append(m);return m
  topic=mark('陳甲','synthetic-a');em=mark('天子','synthetic-ruler')
  if topic_switch:mark('陳乙','synthetic-b')
  def a(surface):
   i=text.index(surface);return dict(paragraph_id='p',start=i,end=i+len(surface),surface=surface)
  d=a('卒'if topic_switch else'薨');g=a('贈太保');e=dict(paragraph_id='p',quote=text,person_mention_id=topic['id']);span=dict(paragraph_id='p',start=0,end=g['end'],surface=text[:g['end']]);h=dict(id='h',person_id='synthetic-a',title='太保',kind='office',mode='posthumous_grant',evidence=[e],effective_period=dict(start=dict(evidence=[e])),attestations=[dict(**a('太保'),person_mention_id=topic['id'])],posthumous_basis=dict(kind='explicit_topic_scoped_gift',source_term=span['surface'],topic_person_mention_id=topic['id'],death_event_id='d',death_anchor=d,gift_anchor=g,topic_span=span,sovereign_replies=[dict(person_mention_id=em['id'],clause_anchor=a('天子不許'))],evidence=[e]));events={'d':dict(person_id='synthetic-a',event_type='death',source_term=d['surface'],evidence=[e])};return h,{'p':('c',p)},{m['id']:('c','p',m)for m in p['mentions']},events
 def test_generic_other_name_and_prefix_work(self):self.assertTrue(self.gv(*self.synthetic()))
 def test_intervening_new_person_topic_is_rejected(self):self.assertFalse(self.gv(*self.synthetic(True)))
 def test_all_five_calendar_bindings_validate(self):
  self.assertEqual(len(self.ctx),5)
  for c in self.ctx:self.assertEqual(context_errors(c,R),[])
  self.assertEqual([c['normalized_date']['year']for c in self.ctx],[432,427,430,432,432])
 def test_wrong_topic_identity_rejected(self):
  c=copy.deepcopy(self.ctx[0]);c['timeline']['unit_subject_person_id']='3bh_k4m_fg4';self.assertTrue(context_errors(c,R))
 def test_other_biography_heading_rejected(self):
  c=copy.deepcopy(self.ctx[2]);c['timeline']['unit_heading_line']=9;self.assertTrue(context_errors(c,R))
 def test_missing_paragraph_rejected(self):
  c=copy.deepcopy(self.ctx[0]);del c['timeline']['paragraph_ids'][3];self.assertIn('傳紀年跳段／順序不符',context_errors(c,R))
 def test_reordered_paragraphs_rejected(self):
  c=copy.deepcopy(self.ctx[0]);c['timeline']['paragraph_ids'][1:3]=reversed(c['timeline']['paragraph_ids'][1:3]);self.assertTrue(context_errors(c,R))
 def test_missing_raw_line_rejected(self):
  c=copy.deepcopy(self.ctx[0]);del c['context_lines'][2];self.assertIn('傳紀年原行跳段',context_errors(c,R))
 def test_other_ruler_era_context_rejected(self):
  c=copy.deepcopy(self.ctx[0]);ep=self.ps[c['era_context']['paragraph_id']][1];c['era_context']['emperor_mention_id']=next(m['id']for m in ep['mentions']if m.get('person_id')!='3bh_k4m_fg4'and m['kind']=='person');self.assertIn('傳紀年異帝年號不得接線',context_errors(c,R))
 def test_year_arithmetic_rejected(self):
  c=copy.deepcopy(self.ctx[1]);c['normalized_date']['year']+=1;self.assertIn('傳紀年中國曆年換算不符',context_errors(c,R))
 def test_event_cannot_borrow_a_later_date_phrase(self):
  c=copy.deepcopy(self.ctx[1]);p=self.ps[c['anchor']['paragraph_id']][1];i=p['text'].index('九年');c['anchor']=dict(paragraph_id=p['id'],start=i,end=i+2,surface='九年');c['original_expression']='九年';c['basis'].update(source_number='九',regnal_year=9);c['normalized_date']['year']=432;self.assertIn('傳紀年事件不得承後出的年詞',context_errors(c,R))
 def test_wrong_antecedent_of_same_year_rejected(self):
  c=copy.deepcopy(self.ctx[0]);c['basis']['source_number']='八';c['basis']['regnal_year']=8;self.assertTrue(context_errors(c,R))
 def changed_witness(self,change_kind):
  td=tempfile.TemporaryDirectory();self.addCleanup(td.cleanup);r=Path(td.name);(r/'corpus/songshu').mkdir(parents=True);(r/'sources/calendar-context').mkdir(parents=True)
  for n in ['042','063-wanghua-tanshou']:shutil.copyfile(R/f'corpus/songshu/{n}.json',r/f'corpus/songshu/{n}.json')
  for f in (R/'sources/calendar-context').iterdir():
   if f.is_file():shutil.copyfile(f,r/'sources/calendar-context'/f.name)
  c=copy.deepcopy(self.ctx[1]);cp=r/'corpus/songshu/063-wanghua-tanshou.json';ch=read(cp);rawp=r/c['source']['file'];ls=rawp.read_text().splitlines();line=18 if change_kind=='era'else 22 if change_kind=='decedent'else 21
  if change_kind=='era':
   p=next(p for p in ch['paragraphs']if p['source_position']['first_line']==line);p['text']+='景平二年。';ls[line-1]+='景平二年。';ex=next(x for x in ch['source']['normalization']['excerpts']if x['proposed_paragraph_id']==p['id']);ex.update(raw_quote=ls[line-1],raw_quote_sha256=sha(ls[line-1].encode()),selected_text_sha256=sha(p['text'].encode()))
  elif change_kind=='decedent':
   p=next(p for p in ch['paragraphs']if p['id']==c['anchor']['paragraph_id']);at=c['event_binding']['source_term_anchor']['start'];p['text']=p['text'][:at]+'劉湛'+p['text'][at:]
   for m in p['mentions']:
    if m['start']>=at:m['start']+=2;m['end']+=2
   p['mentions'].append(dict(id='other-explicit-decedent',kind='person',surface='劉湛',person_id='h3c_ulm_pto',start=at,end=at+2));p['mentions'].sort(key=lambda m:m['start']);ls[line-1]=p['text']
   ex=next(x for x in ch['source']['normalization']['excerpts']if x['proposed_paragraph_id']==p['id']);ex.update(raw_quote=ls[line-1],raw_quote_sha256=sha(ls[line-1].encode()),selected_text_sha256=sha(p['text'].encode()));c['full_paragraph']=p['text'];c['scope']=dict(start=0,end=len(p['text']),quote=p['text'])
   for key in ['source_term_anchor','subject_death_anchor']:c['event_binding'][key]['start']+=2;c['event_binding'][key]['end']+=2
  else:ls[line-1]='==陳乙=='
  rawp.write_text('\n'.join(ls)+'\n');digest=sha(rawp.read_bytes());ch['source']['wikitext_sha256']=digest;cp.write_text(json.dumps(ch,ensure_ascii=False));c['source']['sha256']=digest;c['era_context']['source']['sha256']=digest
  for x in c['context_lines']:
   if x['line']==line:x.update(text=ls[line-1],sha256=sha(ls[line-1].encode()))
  return c,r
 def test_competing_era_even_with_self_consistent_fixed_witness_rejected(self):
  c,r=self.changed_witness('era');self.assertIn('傳紀年中途換年號',context_errors(c,r))
 def test_explicit_other_decedent_even_with_self_consistent_witness_is_rejected(self):
  c,r=self.changed_witness('decedent');self.assertEqual(context_errors(c,r),['傳紀年死亡局部主語不符，不能只憑傳題'])
 def test_generic_death_subject_and_isolated_reply_not_person_specific(self):
  text='趙乙寢疾，帝許之。七年，卒。';p=dict(text=text,mentions=[dict(kind='person',person_id='different-topic',surface='趙乙',start=0,end=2),dict(kind='person',person_id='different-ruler',surface='帝',start=5,end=6)])
  self.assertTrue(death_subject_valid(p,dict(start=text.index('卒')),'different-topic'))
 def test_missing_death_dependency_returns_validation_error(self):
  c=copy.deepcopy(self.ctx[3]);del c['event_binding']['death_event_id'];h=self.fiefs[0];d=h['effective_period']['start']['normalized_date'];contexts={x['id']:x for x in self.ctx};contexts[c['id']]=c;self.assertIn('傳紀年事件接線缺必要欄位',binding_errors(d,h,'start',contexts,{k:v[1]for k,v in self.ps.items()}))
 def test_fief_calendar_cannot_use_other_death_dependency(self):
  c=copy.deepcopy(self.ctx[3]);c['event_binding']['death_event_id']=self.ctx[2]['event_binding']['record_id'];h=self.fiefs[0];d=h['effective_period']['start']['normalized_date'];contexts={x['id']:x for x in self.ctx};contexts[c['id']]=c;ps={k:v[1]for k,v in self.ps.items()};self.assertIn('追封紀年須綁同人已驗死亡主語支持',binding_errors(d,h,'start',contexts,ps))
 def test_new_unit_heading_even_with_consistent_source_hash_rejected(self):
  c,r=self.changed_witness('topic');self.assertIn('傳紀年中途換傳／換話題',context_errors(c,r))
 def test_date_binding_cannot_point_to_other_death(self):
  c=self.ctx[0];event=copy.deepcopy(self.events[c['event_binding']['record_id']]);event['person_id']='3bh_k4m_fg4';d=event['normalized_date'];ps={k:v[1]for k,v in self.ps.items()};self.assertIn('傳紀年接線須綁同人同事件字位',binding_errors(d,event,'event',{x['id']:x for x in self.ctx},ps))
 def test_posthumous_enfeoffments_have_distinct_mode(self):
  self.assertEqual(len(self.fiefs),2)
  for h in self.fiefs:self.assertTrue(fief_valid(h,self.ps,self.ms,self.events));self.assertEqual(h['effective_period']['start']['event_type'],'posthumous_enfeoffment');self.assertEqual(h['effective_period']['start']['normalized_date']['year'],432)
 def test_lifetime_feng_not_posthumous_enfeoffment(self):
  h=copy.deepcopy(self.fiefs[0]);h['enfeoffment_basis']['source_term']='封'+h['title'];self.assertFalse(fief_valid(h,self.ps,self.ms,self.events))
 def test_office_cannot_be_posthumous_fief(self):
  h=copy.deepcopy(self.fiefs[0]);h['kind']='office';self.assertFalse(fief_valid(h,self.ps,self.ms,self.events))
 def test_other_person_death_cannot_support_fief(self):
  h=copy.deepcopy(self.fiefs[0]);h['enfeoffment_basis']['death_event_id']=next(e['id']for e in self.events.values()if e['person_id']!=h['person_id']);self.assertFalse(fief_valid(h,self.ps,self.ms,self.events))
 def test_no_age_derived_birth_or_death_endpoint(self):
  for c in self.ch:
   for age in c['annotation'].get('age_assertions',[]):self.assertIsNone(age['birth_year'])
  for h in self.gifts+self.fiefs:self.assertEqual(h['effective_period']['end']['status'],'unknown')
if __name__=='__main__':unittest.main()
