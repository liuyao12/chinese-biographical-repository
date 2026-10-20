"""Synthetic grammar fixtures, not historical claims."""
import copy
import unittest
from scripts.historical_family_clauses import explicit_shouyang_valid,named_zusun_fenghou_valid,explicit_congdi_valid

def fixture(i):
    texts=['乙哀甲少孤収養與諸子同使與丙共止','乙為司空時納甲母并収養甲其時丙另居','封乙族孫甲為新昌亭侯邑三百戸以奉乙後','乙從弟甲'];t=texts[i];s=t.rfind('甲')if i==1 else t.index('甲');o=t.rfind('乙')if i==2 else t.index('乙');ms=[dict(id='child',surface='甲',start=s,end=s+1,person_id='synthetic-child',kind='person'),dict(id='other',surface='乙',start=o,end=o+1,person_id='synthetic-other',kind='person')]
    if i==1:ms.append(dict(id='embedded',surface='甲',start=t.index('甲'),end=t.index('甲')+1,person_id='synthetic-child',kind='person'))
    if i==2:ms.append(dict(id='ante',surface='乙',start=1,end=2,person_id='synthetic-other',kind='person'))
    term=t[:t.index('養')+1]if i==0 else ('以奉乙後'if i==2 else(t[:t.index('其時')]if i==1 else t));start=t.index(term);b=dict(kind=['named_orphan_shouyang','named_mother_received_child_shouyang','feng_named_zusun_yifenghou','named_object_congdi_subject'][i],start=start,end=start+len(term));q=dict(source_term=term,source_clause_binding=b)
    if i<2:q.update(adoption_basis='explicit_shouyang',adoption_kind='historical_shouyang',modern_legal_status='not_inferred',parentage_inference='not_inferred')
    elif i==2:b['antecedent_mention_id']='ante';q.update(succession_kind='named_zusun_feng_hou',legal_adoption_status='not_stated',parentage_inference='not_inferred')
    else:q['kinship_structure']=dict(lineage='paternal',generation_difference=0,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='younger')
    a=dict(predicate=['adoptive_father','adoptive_father','ritual_successor_of','agnatic_cousin'][i],subject_person_id='synthetic-child',object_person_id='synthetic-other',status='source_attested',human_reviewed=False,qualifiers=q,evidence=[dict(chapter_id='synthetic-c',paragraph_id='synthetic-p',quote=t,subject_person_mention_id='child',object_person_mention_id='other')]);return a,{'synthetic-p':('synthetic-c',dict(text=t,mentions=ms))}
def valid(a,p):return {'adoptive_father':explicit_shouyang_valid,'ritual_successor_of':named_zusun_fenghou_valid,'agnatic_cousin':explicit_congdi_valid}[a['predicate']](a,p)
class HistoricalFamilyClauses(unittest.TestCase):
 def test_four_positive_clauses(self):
  for i in range(4):self.assertTrue(valid(*fixture(i)))
 def test_swapped_roles(self):
  for i in range(4):
   a,p=fixture(i);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id'];self.assertFalse(valid(a,p))
 def test_nested_or_antecedent_occurrence_not_recipient(self):
  for i,role,mid in [(1,'subject','embedded'),(2,'object','ante')]:
   a,p=fixture(i);a['evidence'][0][role+'_person_mention_id']=mid;self.assertFalse(valid(a,p))
 def test_crop_and_bad_offset_rejected(self):
  for i in range(4):
   a,p=fixture(i);a['evidence'][0]['quote']=a['evidence'][0]['quote'][:-1];self.assertFalse(valid(a,p));a,p=fixture(i);a['qualifiers']['source_clause_binding']['start']+=1;self.assertFalse(valid(a,p))
 def test_invented_legal_or_biological_or_ancestor_information_rejected(self):
  for i in range(4):
   a,p=fixture(i);a['qualifiers']['father_person_id']='synthetic';self.assertFalse(valid(a,p))
  a,p=fixture(3);a['qualifiers']['kinship_structure']['common_ancestor_person_id']='synthetic';self.assertFalse(valid(a,p))
 def test_plural_negation_and_nested_insertions(self):
  for i,word in [(0,'及某'),(0,'不'),(1,'弟'),(2,'未'),(3,'非')]:
   a,ps=fixture(i);p=ps['synthetic-p'][1];b=a['qualifiers']['source_clause_binding'];s=next(m for m in p['mentions']if m['id']=='child');at=s['end']if i<2 else b['start']+1;p['text']=p['text'][:at]+word+p['text'][at:]
   for m in p['mentions']:
    if m['start']>=at:m['start']+=len(word);m['end']+=len(word)
   b['end']+=len(word);a['qualifiers']['source_term']=p['text'][b['start']:b['end']];a['evidence'][0]['quote']=p['text'];self.assertFalse(valid(a,ps))

 def test_unbound_plural_after_single_child_clause_rejected(self):
  a,ps=fixture(1);p=ps['synthetic-p'][1];at=a['qualifiers']['source_clause_binding']['end'];p['text']=p['text'][:at]+'及某'+p['text'][at:];a['evidence'][0]['quote']=p['text'];self.assertFalse(valid(a,ps))
