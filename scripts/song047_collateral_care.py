"""Four source-bound collateral/care clauses, without fabricated parents or ages."""
import copy,hashlib,json
from pathlib import Path
KIN={'lineage','generation_difference','collateral','distance','common_ancestor_person_id','subject_relative_age'}

def valid(a, paragraphs):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];text=p['text'];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  assert set(b)=={'kind','start','end','source_revision','paragraph_sha256'}and type(b['start'])is int and type(b['end'])is int and 0<=b['start']<b['end']<=len(text)
  assert a['status']=='source_attested'and a['human_reviewed']is False and p['text_layer']=='received_chapter'and cid==e['chapter_id']and e['quote']==text
  assert b['source_revision']==p['source_position']['source_revision']and b['paragraph_sha256']==hashlib.sha256(text.encode()).hexdigest()
  assert s['kind']==o['kind']=='person'and s['person_id']==a['subject_person_id']and o['person_id']==a['object_person_id']and s['person_id']!=o['person_id']
  assert all(text[m['start']:m['end']]==m['surface']for m in(s,o))
  term=q['source_term'];assert term and term in text[b['start']:b['end']]
  if b['kind']=='biography_subject_maternal_aunt_older_cousin':
   assert a['predicate']=='maternal_cousin'and set(q)=={'source_term','kinship_structure','relative_birth_order','source_clause_binding','relative_age_interpretation'}
   k=q['kinship_structure'];assert set(k)==KIN|{'maternal_path'}and k==dict(lineage='maternal',generation_difference=0,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='older',maternal_path='mother_sister_son')
   assert b['start']==s['start']==0 and o['end']+4==b['end']and text[o['end']:b['end']]=='從母兄也'and term==o['surface']+'從母兄也'
   assert text[s['end']:o['start']].endswith('人')and s['end']<o['start']
   assert {m['id']for m in p['mentions']if m.get('kind')=='person'and m['start']<b['end']}=={s['id'],o['id']}
   assert q['relative_birth_order']==dict(operator='lt',scope='maternal_cousins',older_person_id=s['person_id'],younger_person_id=o['person_id'],older_ordinal=None,younger_ordinal=None)
   caution=q['relative_age_interpretation'];assert set(caution)=={'status','preferred_subject_relative_age','case_id','case_path','case_sha256'}and caution['status']=='chronology_unresolved'and caution['preferred_subject_relative_age']is None
  elif b['kind']=='named_person_congmu_bears_named_child':
   assert a['predicate']=='maternal_aunt'and set(q)=={'source_term','lineage','generation_difference','maternal_path','mother_person_id','source_clause_binding'}
   assert q['lineage']=='maternal'and q['generation_difference']==-1 and q['maternal_path']=='mother_sister'and q['mother_person_id']is None
   child=next(m for m in p['mentions']if m['start']==o['end']+1 and m.get('kind')=='person')
   assert o['surface']=='從母'and s['start']==b['start']and s['end']==o['start']and text[o['end']:child['start']]=='生'and child['end']==b['end']
   assert term==s['surface']+'從母生'+child['surface']==text[b['start']:b['end']]
  elif b['kind']=='congmu_weans_child_and_nurses_named_child':
   assert a['predicate']=='raised_by'and set(q)=={'source_term','care_basis','legal_adoption_status','biological_parentage_inference','source_clause_binding'}
   assert q['care_basis']=='weaned_own_child_and_nursed_named_child'and q['legal_adoption_status']=='not_stated'and q['biological_parentage_inference']=='not_inferred'
   preceding=next(m for m in p['mentions']if m['start']==b['start']and m.get('kind')=='person');own=next(m for m in p['mentions']if m['start']==o['end']+1 and m.get('kind')=='person')
   weaned=next(m for m in p['mentions']if m['start']==own['end']+4 and m.get('kind')=='person')
   assert o['surface']=='從母'and preceding['person_id']==s['person_id']and preceding['end']==o['start']and own['person_id']==weaned['person_id']and own['person_id']not in(s['person_id'],o['person_id'])
   assert text[own['end']:weaned['start']]=='未朞乃斷'and text[weaned['end']:s['start']]=='乳而自養'and s['end']==b['end']
   assert term==preceding['surface']+'從母生'+own['surface']+'未朞乃斷'+weaned['surface']+'乳而自養'+s['surface']==text[b['start']:b['end']]
  elif b['kind']=='senior_dead_then_congzi_named_junior':
   assert a['predicate']=='agnatic_senior_kin'and set(q)=={'source_term','kinship_structure','source_clause_binding'}
   assert q['kinship_structure']==dict(lineage='paternal',generation_difference=-1,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='unknown')
   assert o['start']==b['start']and s['end']==b['end']and text[o['end']:s['start']]=='既死從子'and term==o['surface']+'既死從子'+s['surface']==text[b['start']:b['end']]
  else:return False
  return True
 except (AssertionError,KeyError,ValueError,TypeError,StopIteration):return False


def chronology_caution_valid(a,root):
 try:
  q=a['qualifiers'];r=q['relative_age_interpretation'];path=Path(r['case_path']);assert not path.is_absolute()and '..'not in path.parts and path.parts[0]=='source-evidence'
  raw=(Path(root)/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['case_sha256'];case=json.loads(raw)
  assert case['id']==r['case_id']and case['status']=='unresolved'and case['preferred_interpretation']is None and case['human_reviewed']is False and case['not_stored_as_birth_year']is True
  older=next(c for c in case['source_claims']if c['kind']=='older_maternal_cousin');death=next(c for c in case['source_claims']if c['kind']=='reported_death_and_age');birth=next(c for c in case['source_claims']if c['kind']=='liuyu_explicit_birth')
  assert older['subject_person_id']==death['person_id']==a['subject_person_id']and older['object_person_id']==birth['person_id']==a['object_person_id']
  assert death['death_chinese_year']==407 and death['reported_age']==41 and birth['chinese_year']==363
  assert any(e['quote']==a['evidence'][0]['quote']and e['paragraph_id']==a['evidence'][0]['paragraph_id']for e in older['evidence'])
  return True
 except(AssertionError,KeyError,ValueError,TypeError,StopIteration,OSError):return False


def preferred_relation(a):
 result=copy.deepcopy(a)
 if a.get('qualifiers',{}).get('relative_age_interpretation',{}).get('status')=='chronology_unresolved':
  result['qualifiers'].pop('relative_birth_order',None)
  result['qualifiers']['kinship_structure']['subject_relative_age']='unknown'
 return result
