"""A qualified 從父弟 path plus a verified two-father chain; no unnamed person is created."""
from pathlib import Path
import json,hashlib
TYPE='ancestor_from_qualified_first_cousin_and_known_paternal_chain'
BASIS='fixed_kanripo_congfudi_erya_named_two_generation_chain'
LEXICAL_CONTEXT_SHA256='5fc153af37f1c102c5b43ec609cdcb9bec59fd8f12d35ee73dac708ccd25bb98'
LEXICAL_RULE='兄之子弟之子相謂爲從父晜弟{{雙行註文|從父|而别}}'

def _safe_file(root,relative):
 p=Path(relative);assert not p.is_absolute()and p.parts and p.parts[0]=='source-evidence'and'..'not in p.parts
 f=root/p;assert f.resolve()==f and f.is_file();return f

def lexical_path_valid(root,relative):
 try:
  root=Path(root).resolve();raw=_safe_file(root,relative).read_bytes();assert hashlib.sha256(raw).hexdigest()==LEXICAL_CONTEXT_SHA256
  d=json.loads(raw);assert d['parent_revision']==2652958 and d['literal_lexical_rule']==LEXICAL_RULE and d['image_verified']is False
  expected=[(1138113,'9a0b0e509b4e40510bcdbb6d0269b556983c9e0f84fc1d0b66cd5a75fb2653e8'),(1138114,'60c3c7ca503421ef2c833fc658da724ff59fb0be74f60e453c1ecba252891156'),(1138115,'906d51545ac7acced75980c780543ec63d406b4faf9de5f55bb4fa08f0b9162c')]
  assert [(x['revision'],x['sha256'])for x in d['pages']]==expected;parts=[]
  for p in d['pages']:
   b=_safe_file(root,p['raw_file']).read_bytes();assert hashlib.sha256(b).hexdigest()==p['sha256']and len(b)==p['bytes'];text=b.decode('utf-8');s=p['unit_slice'];assert type(s['start'])is int and type(s['end'])is int and text[s['start']:s['end']]==s['literal'];parts.append(s['literal']);assert p['image_verified']is False and str(p['revision'])in p['url']
  assert ''.join(parts)==d['complete_unit_transcription_wikitext']and ''.join(parts).count(LEXICAL_RULE)==1
  i=d['interpretation'];assert i['reported_kinship_path']==['father','brother','son']and i['direction']=='from_named_reference_to_named_junior'and i['status']=='editorial_provisional'and i['human_reviewed']is False
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,AttributeError,OSError):return False

def valid(member,rows,assertions,chapters,root):
 try:
  assert root is not None;root=Path(root).resolve();c=member['ancestor_connection']
  assert c['type']==TYPE and c['interpretation_basis']==BASIS and c['status']=='contextual_provisional'and c['human_reviewed']is False and c['rationale']
  assert member['parent_person_id']is None and member['source_assertion_id']is None and member['connection']=='grandfather'and member['generation_distance']==2 and member['intermediate_person_ids']==[None]
  ref=rows[c['reference_person_id']];rf=rows[c['reference_father_person_id']];grand=rows[member['ancestor_person_id']]
  groups=[set(v['source_person_ids'])for v in (member,ref,rf,grand)];assert all(groups)and all(not a&b for i,a in enumerate(groups)for b in groups[i+1:])
  k=assertions[c['qualified_cousin_assertion_id']];f=assertions[c['reference_father_assertion_id']];g=assertions[c['reference_father_father_assertion_id']];q=k['qualifiers']
  assert k['predicate']=='agnatic_cousin'and k['subject_person_id']in groups[0]and k['object_person_id']in groups[1]
  assert q['kinship_structure']==dict(lineage='paternal',generation_difference=0,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='younger')
  assert q['source_paternal_path_term']=='從父弟'and q['reported_kinship_path']==['father','brother','son']and q['reported_kinship_path_direction']=='object_to_subject'
  assert q['reported_kinship_path_from_person_id']==k['object_person_id']and q['reported_kinship_path_to_person_id']==k['subject_person_id']
  qi=q['reported_kinship_path_interpretation'];assert qi['status']=='editorial_provisional'and qi['human_reviewed']is False and qi['source_term']=='從父弟'and qi['rationale']
  assert c['lexical_source_ref']==qi['lexical_source_ref']and lexical_path_valid(root,c['lexical_source_ref'])
  order=q['relative_birth_order'];assert order['older_person_id']in groups[1]and order['younger_person_id']in groups[0]and order['operator']=='lt'and order['scope']=='agnatic_cousins'and order['older_ordinal']is None and order['younger_ordinal']is None
  assert f['predicate']==g['predicate']=='father'and f['subject_person_id']in groups[1]and f['object_person_id']==g['subject_person_id']in groups[2]and g['object_person_id']in groups[3]
  assert f['qualifiers']['lineage']==g['qualifiers']['lineage']=='paternal'
  assert ref['parent_person_id']==rf['person_id']and ref['source_assertion_id']==f['id']and rf['parent_person_id']==grand['person_id']and rf['source_assertion_id']==g['id']
  # A newly named father replaces this missing-father construction, even if otherwise compatible.
  assert not any(a.get('predicate')=='father'and a.get('subject_person_id')in groups[0]for a in assertions.values())
  assert not any(a.get('predicate')=='father'and((a.get('subject_person_id')in groups[1]and a.get('object_person_id')not in groups[2])or(a.get('subject_person_id')in groups[2]and a.get('object_person_id')not in groups[3]))for a in assertions.values())
  assert not any(a.get('predicate')in('adoptive_father','ritual_successor_of')and a.get('subject_person_id')in(groups[0]|groups[1]|groups[2])for a in assertions.values())
  assert not any(a.get('predicate')=='grandfather'and a.get('subject_person_id')in groups[0]for a in assertions.values())
  proof=[k,f,g];cid=None;recipe_key=None
  try:from scripts.fixed_kanripo_fact_slots import valid as source_valid
  except ImportError:from fixed_kanripo_fact_slots import valid as source_valid
  for a in proof:
   assert a['status']=='source_attested'and a['human_reviewed']is False;b=a['fixed_source_fact_binding'];assert b['kind']=='fixed_kanripo_person_fact_slots'
   aq=a['qualifiers'];assert aq.get('adopted_for_family_tree')is not False and aq.get('shared_father')is not False and aq.get('lineage')not in('maternal','non_paternal')and not any(aq.get(x)for x in('adoptive','sworn','same_mother_only'))
   acs={e['chapter_id']for e in a['evidence']};assert len(acs)==1;ac=next(iter(acs));cid=ac if cid is None else cid;recipe_key=b['key']if recipe_key is None else recipe_key;assert ac==cid and b['key']==recipe_key and source_valid(a,chapters[ac],root)
   ch=chapters[ac]
   for e in a['evidence']:
    assert all(e[x]==ch[x]for x in('work_id','book_id','source_id'));p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];assert e['quote']==p['text']
  ch=chapters[cid];e,=k['evidence'];p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];marks={m['id']:m for m in p['mentions']};anchor=c['relation_clause'];local_ref=marks[anchor['reference_person_mention_id']];local_child=marks[anchor['descendant_person_mention_id']]
  assert local_ref['kind']==local_child['kind']=='person'and local_ref['person_id']in groups[1]and local_child['person_id']in groups[0]
  assert anchor==dict(paragraph_id=p['id'],start=local_ref['start'],end=local_child['end'],surface=q['source_term'],reference_person_mention_id=local_ref['id'],descendant_person_mention_id=local_child['id'])
  assert p['text'][local_ref['end']:local_child['start']]=='從父弟'and p['text'][anchor['start']:anchor['end']]==anchor['surface']
  assert e['subject_person_mention_id']==local_child['id']and marks[e['object_person_mention_id']]['person_id']in groups[1]
  refs=c['references'];expected={(a['id'],e['chapter_id'],e['paragraph_id'],e['source_id'],e['quote'])for a in proof for e in a['evidence']};actual=[(v['assertion_id'],v['chapter_id'],v['paragraph_id'],v['source_id'],v['quote'])for v in refs];assert len(actual)==len(set(actual))==len(expected)and set(actual)==expected
  for v in refs:
   assert v['scope']and v['url']in(ch['source'].get('url'),ch['source'].get('permalink'))and v['work_id']==ch['work_id']and v['book_id']==ch['book_id']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
