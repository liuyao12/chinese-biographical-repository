# -*- coding: utf-8 -*-
"""Finite full-paragraph recipient and date contracts; no identity whitelist."""
import unittest,json,copy,re,hashlib
from pathlib import Path
from scripts import attached_biography_frames as M
R=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((R/rel).read_text())
class AttachedBiographyFrames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=read('corpus/jinshu/043-shantao.json');cls.hs=read('corpus/jinshu/043-shantao-titles.json')['holdings'];cls.kin=read('corpus/jinshu/043-shantao-assertions.json')['assertions'];cls.paras={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.chapters={cls.ch['id']:cls.ch}
 def synthetic(self):
  # Build a new source, new people and new offsets from a trusted complete frame.
  frame='paragraph_frame_003';r=M.RECIPES[frame];groups={k:k for k in re.findall(r'<(r\d+)>',r['template'])}
  for g in r['same_person_groups']:
   for k in g:groups[k]=g[0]
  text='';ms=[];roles={};fields={};titles={s['field']:('秀才'if s['kind']=='unclassified'else'試任尚書')for s in r['slots'].values()}
  for part in re.split(r'(<r\d+>|\{career_\d+\})',r['template']):
   if part.startswith('<r'):
    k=part[1:-1];surface='甲'+groups[k][1:];mid='synthetic:'+k;roles[k]=mid;ms.append(dict(id=mid,kind='person',person_id='fiction-'+groups[k],surface=surface,start=len(text),end=len(text)+len(surface)));text+=surface
   elif part.startswith('{career_'):
    k=part[1:-1];v=titles[k];fields[k]=dict(paragraph_id='synthetic:p',start=len(text),end=len(text)+len(v),surface=v);text+=v
   else:text+=part
  p=dict(id='synthetic:p',text=text,mentions=ms,text_layer='received_chapter',source_position=dict(revision_id=101));ch=dict(id='synthetic',work_id='work-fiction',book_id='book-fiction',source_id='source-fiction',source=dict(revision_id=101),paragraphs=[p]);slot='career-008';s=r['slots'][slot];m=next(m for m in ms if m['id']==roles[s['recipient_role']]);a=fields[s['field']];ev=[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=text,person_mention_id=m['id'])];b=dict(kind=M.KIND,frame=frame,paragraph_id=p['id'],source_revision=101,paragraph_sha256=hashlib.sha256(text.encode()).hexdigest(),roles=roles,fields=fields,human_reviewed=False,slot=slot,recipient_role=s['recipient_role']);h=dict(id='test-office',person_id=m['person_id'],title=a['surface'],kind=s['kind'],mode=s['mode'],appointment_role=s['appointment_role'],status='source_attested',human_reviewed=False,source_career_role=b,evidence=ev,attestations=[dict(paragraph_id=p['id'],start=a['start'],end=a['end'],surface=a['surface'],person_mention_id=m['id'],usage='narrative',date_expression=None)],effective_period=dict(start=dict(status='source_event',event_type=s['mode'],date_expression=None,evidence=ev),end=dict(status='unknown',date_expression=None,evidence=[])))
  return ch,h
 def test_synthetic_new_source_and_names(self):
  ch,h=self.synthetic();self.assertTrue(M.holding_valid(h,ch))
  for mutate in [lambda c,v:v.update(person_id='other-recipient'),lambda c,v:c['paragraphs'][0]['mentions'].pop(),lambda c,v:v['source_career_role']['roles'].pop('r0'),lambda c,v:v['effective_period']['end'].update(date_expression='死年'),lambda c,v:v['evidence'][0].update(source_id='wrong-source')]:
   c,v=copy.deepcopy((ch,h));mutate(c,v);self.assertFalse(M.holding_valid(v,c))
 def test_ordinary_words_are_not_offices(self):
  for word in ['少與','高簡','不行','終身','善哉','今致錢']:
   self.assertFalse(M.nominal(word,'office','appointment'))
  self.assertTrue(M.nominal('試任尚書','office','appointment'))
 def test_every_native_holding_and_proposal(self):
  for h in self.hs:
   with self.subTest(h=h['id']):self.assertTrue(M.holding_valid(h,self.ch))
  people={m['person_id']for p in self.ch['paragraphs']for m in p['mentions']if m['kind']=='person'}
  for q in self.ch['annotation']['title_proposals']:
   self.assertEqual([],M.proposal_errors(q,self.ch,people));v=copy.deepcopy(q);v['person_id']='wrong';self.assertTrue(M.proposal_errors(v,self.ch,people));v=copy.deepcopy(q);v['outcome']='assumed';self.assertTrue(M.proposal_errors(v,self.ch,people));v=copy.deepcopy(q);v['non_assumption_anchor']['start']-=1;self.assertTrue(M.proposal_errors(v,self.ch,people))
 def test_recipients_and_complete_role_coverage(self):
  h=next(h for h in self.hs if h['title']=='黃門侍郎');v=copy.deepcopy(h);v['person_id']='other';self.assertFalse(M.holding_valid(v,self.ch))
  c=copy.deepcopy(self.ch);p=next(p for p in c['paragraphs']if p['id']==h['evidence'][0]['paragraph_id']);p['mentions'].pop();self.assertFalse(M.holding_valid(h,c))
  # Conflate the two explicitly distinct 黃門侍郎 recipients, even changing all their co-references.
  c=copy.deepcopy(self.ch);p=next(p for p in c['paragraphs']if p['id']==h['evidence'][0]['paragraph_id']);b=h['source_career_role'];r=M.RECIPES[b['frame']];a,z=r['distinct_role_groups'][0];by={m['id']:m for m in p['mentions']};old,new=by[b['roles'][z]]['person_id'],by[b['roles'][a]]['person_id']
  for m in p['mentions']:
   if m.get('person_id')==old:m['person_id']=new
  self.assertFalse(M.holding_valid(h,c))
 def test_true_regnal_validation_and_no_phase_spill(self):
  for h in self.hs:
   dates=[h['effective_period']['start']]+h['attestations']
   for n,date in enumerate(dates):
    for key in ['normalized_date','normalized_date_range']:
     if key not in date:continue
     for mutation in ['year','era','polity']:
      v=copy.deepcopy(h);d=([v['effective_period']['start']]+v['attestations'])[n][key]
      if mutation=='year':
       if key=='normalized_date':d['year']+=1
       else:d['earliest']['year']+=1
      elif mutation=='era':d.get('era_span_mapping',d.get('regnal_year_mapping'))['era_name']='不同年號'
      else:d['references'][0]['columns']['dynasty']='東晉'
      with self.subTest(h=h['id'],key=key,mutation=mutation):self.assertFalse(M.holding_valid(v,self.ch))
  h=next(h for h in self.hs if h['title']=='相國左長史');v=copy.deepcopy(h);v['effective_period']['start']['date_expression']='咸熙初';self.assertFalse(M.holding_valid(v,self.ch))
  h=next(h for h in self.hs if h['title']=='尚書左僕射');v=copy.deepcopy(h);v['effective_period']['start']['date_expression']='永嘉初';self.assertFalse(M.holding_valid(v,self.ch))
 def test_attested_era_zhi_phase_is_whole_era_not_first_year(self):
  hs=[h for h in self.hs if h['title']=='黃門侍郎'];self.assertEqual(len(hs),2)
  for h in hs:
   a=h['attestations'][0];self.assertEqual(a['date_expression'],'泰始之初');self.assertEqual(a['normalized_date_range']['earliest']['year'],265);self.assertEqual(a['normalized_date_range']['latest']['year'],274);self.assertEqual(h['effective_period']['start']['status'],'unknown')
   v=copy.deepcopy(h);v['attestations'][0]['normalized_date_range']['latest']['year']=265;self.assertFalse(M.holding_valid(v,self.ch))
 def test_posthumous_name_not_era_character(self):
  h=next(h for h in self.hs if h['title']=='康');v=copy.deepcopy(h);p=next(p for p in self.ch['paragraphs']if p['id']==h['evidence'][0]['paragraph_id']);at=p['text'].index('太康')+1;v['attestations'][0].update(start=at,end=at+1);self.assertFalse(M.holding_valid(v,self.ch))
 def test_kin_exact_roles_no_biomother_or_cousin_degree(self):
  for a in self.kin:
   self.assertTrue(M.kinship_valid(a,self.paras,self.chapters));v=copy.deepcopy(a);v['subject_person_id'],v['object_person_id']=v['object_person_id'],v['subject_person_id'];self.assertFalse(M.kinship_valid(v,self.paras,self.chapters))
  for a in self.kin:
   if a['predicate']=='maternal_role':
    v=copy.deepcopy(a);v['qualifiers']['biological_mother']=True;self.assertFalse(M.kinship_valid(v,self.paras,self.chapters))
   if a['predicate']=='agnatic_cousin':
    v=copy.deepcopy(a);v['qualifiers']['kinship_structure']['distance']=1;self.assertFalse(M.kinship_valid(v,self.paras,self.chapters))
 def test_father_rank_cross_record_validation(self):
  h=next(h for h in self.hs if 'inherited_title_binding'in h);hs={v['id']:v for v in self.hs};a=h['attestations'][0];self.assertTrue(M.inherited_surface_valid(h,a,self.ch,hs,self.kin,self.paras,self.chapters))
  v=copy.deepcopy(h);v['title']='新遝子';v['inheritance']['resolved_title']='新遝子';self.assertFalse(M.inherited_surface_valid(v,a,self.ch,hs,self.kin,self.paras,self.chapters))
  v=copy.deepcopy(h);v['inherited_title_binding']['father_assertion_id']='a-jin043-shantao-kin_007';self.assertFalse(M.inherited_surface_valid(v,a,self.ch,hs,self.kin,self.paras,self.chapters))
  v=copy.deepcopy(h);v['effective_period']['start']['date_expression']='太康四年';self.assertFalse(M.holding_valid(v,self.ch))
 def test_life_age_address_names_and_detail_values(self):
  for e in read('corpus/jinshu/043-shantao-life-events.json')['events']:
   self.assertTrue(M.life_valid(e,self.ch));v=copy.deepcopy(e);v['person_id']='wrong';self.assertFalse(M.life_valid(v,self.ch))
  for a in self.ch['annotation']['age_assertions']:
   self.assertTrue(M.age_valid(a,self.ch));v=copy.deepcopy(a);v['birth_year']=204;self.assertFalse(M.age_valid(v,self.ch))
  for a in read('corpus/jinshu/043-shantao-addresses.json')['assertions']:
   self.assertTrue(M.address_valid(a,self.ch));v=copy.deepcopy(a);v['relation']='death_place';self.assertFalse(M.address_valid(v,self.ch))
  for n in read('corpus/jinshu/043-shantao-name-components.json')['records']:
   if 'component_source_binding'not in n:continue
   self.assertTrue(M.name_valid(n,self.ch));v=copy.deepcopy(n);v['person_id']='wrong';self.assertFalse(M.name_valid(v,self.ch))
  hs={h['id']:h for h in self.hs}
  for d in read('corpus/jinshu/043-shantao-biographical-details.json')['records']:
   self.assertTrue(M.detail_valid(d,self.ch,hs,R));v=copy.deepcopy(d);v['values']['invented_duration']=283;self.assertFalse(M.detail_valid(v,self.ch,hs,R))
if __name__=='__main__':unittest.main()
