"""Finite editorial generation preference; raw 世孫 number/unused assertion stays intact."""
from pathlib import Path
import hashlib,json,copy
TYPE='ancestor_from_interpreted_generation_and_known_descendant_chain'
PROFILE='fixed_pei_kang_ziye_inclusive_eight_v1'
PIN_SHA='65a7bb28d46ca79f652519e50f18a4ecaaf2f7108238648e14592789ef285e89'
DECISION='decision-pei-kang-ziye-inclusive-eight'
REF='source-evidence/pei-kang-generation-interpretation/decision.json'
FAMILY='family-hedong-pei-mao-core'
FACTS=['a-liang030-ziye-kang-ancestor','a-nanshi033-ziye-father','a-nanshi033-zhaoming-father','a-nanshi033-yin-father','a-nanshi033-songzhi-father','a-nanshi033-songzhi-grandfather']

def _file(root,name,folder):
 p=Path(name);assert not p.is_absolute()and p.parts and p.parts[0]==folder and'..'not in p.parts
 f=root/p;assert f.resolve()==f and f.is_file();return f

def _fixed_facts(root,assertions,chapters):
 raw=_file(root,'scripts/fixed_pei_generation_pins.json','scripts').read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN_SHA
 pins=json.loads(raw);assert pins['profile']==PROFILE
 for pin in pins['chapters']:
  ch=chapters[pin['dimensions']['id']];assert {k:ch[k]for k in pin['dimensions']}==pin['dimensions']and ch['source']==pin['source']
  source=ch['source'];rb=_file(root,source['raw_path'],'sources').read_bytes();assert hashlib.sha256(rb).hexdigest()==source['raw_file_sha256']==source['raw_sha256'];text=rb.decode('utf-8')
  assert len(ch['paragraphs'])==len(pin['paragraphs'])
  for p,q in zip(ch['paragraphs'],pin['paragraphs']):
   assert {k:copy.deepcopy(p[k])for k in q if k!='mentions'}=={k:v for k,v in q.items()if k!='mentions'}
   assert [{k:m[k]for k in('id','start','end','surface','kind')}for m in p['mentions']]==q['mentions']
   sp=p['source_position'];assert sp['raw_path']==source['raw_path']and text[sp['start']:sp['end']]==sp['raw']
   assert all(p['text'][m['start']:m['end']]==m['surface']for m in p['mentions'])
 for spec in pins['facts']:
  wanted=copy.deepcopy(spec['template'])
  for key,b in spec['person_bindings'].items():
   ch=chapters[b['chapter_id']];p,=[p for p in ch['paragraphs']if p['id']==b['paragraph_id']];m,=[m for m in p['mentions']if m['id']==b['mention_id']];assert m['kind']=='person';wanted[key]=m['person_id']
  assert assertions[wanted['id']]==wanted,'Selected received assertion changed'
 return pins

def valid(member,rows,assertions,chapters,root,assembly):
 try:
  root=Path(root).resolve();c=member['ancestor_connection'];pins=_fixed_facts(root,assertions,chapters)
  assert assembly['id']==FAMILY and assembly['human_reviewed']is False
  assert c['type']==TYPE and c['interpretation_basis']==PROFILE and c['status']=='contextual_provisional'and c['human_reviewed']is False and c['rationale']
  assert member['parent_person_id']is None and member['source_assertion_id']is None and member['connection']=='grandfather'and member['generation_distance']==2 and member['intermediate_person_ids']==[None]
  assert c['generation_decision_ref']==REF and c['generation_decision_id']==DECISION
  d=json.loads(_file(root,REF,'source-evidence').read_bytes())
  assert d['record_type']=='editorial_generation_interpretation'and d['id']==DECISION and d['profile']==PROFILE and d['status']=='contextual_preferred'and d['human_reviewed']is False and d['reviewer']
  assert d['source_assertion_id']==FACTS[0]and d['reported_source_term']=='康八世孫'and type(d['reported_generation_number'])is int and d['reported_generation_number']==8
  assert type(d['preferred_generation_distance'])is int and d['preferred_generation_distance']==7 and d['confidence']=='moderate'and d['counting_interpretation']and d['our_inference']
  assert d['modern_reference']==pins['modern_reference']and d['modern_reference']['opinion_independently_validated']is False and d['modern_reference']['not_exhaustive_or_latest_claim']is True
  assert len(d['alternatives'])==1 and d['alternatives'][0]['generation_distance']==8 and d['alternatives'][0]['status']=='retained_alternative'and d['alternatives'][0]['interpretation']
  raw=assertions[FACTS[0]];q=raw['qualifiers'];assert raw['predicate']=='ancestor'and raw['status']=='source_attested'and raw['human_reviewed']is False
  assert q==dict(source_term='康八世孫',source_number='八',reported_generation_number=8,generation_distance=None,adopted_for_family_tree=False)
  assert d['subject_person_id']==raw['subject_person_id']and d['ancestor_person_id']==raw['object_person_id']
  assert d['supersedes']==dict(kind='source_assertion_assembly_interpretation_only',assertion_id=raw['id'],preserved_source_qualifiers=q,effective_assembly_interpretation=dict(adopted_for_family_tree=True,generation_distance=7),original_assertion_remains_unchanged=True,not_a_global_shisun_conversion_rule=True)
  chain=c['known_chain_person_ids'];assert isinstance(chain,list)and len(chain)==6 and len(set(chain))==6 and chain[0]==c['reported_descendant_person_id']and chain[-1]==member['person_id']
  selected=[rows[pid]for pid in chain];ancestor=rows[member['ancestor_person_id']];groups=[set(r['source_person_ids'])for r in selected]+[set(ancestor['source_person_ids'])]
  assert all(len(g)==1 for g in groups)and len(set.union(*groups))==7 and raw['subject_person_id']in groups[0]and raw['object_person_id']in groups[-1]
  assert d['scope']==dict(kind='family_assembly_ancestor_connection_only',family_id=FAMILY,descendant_person_id=next(iter(groups[5])),connection='grandfather',generation_distance=2,intermediate_person_ids=[None])
  assert d['known_close_chain']==dict(person_ids=[next(iter(g))for g in groups[:6]],distance=5,last_edge_kind='editorial_parent_between_consecutive_ancestors',last_edge_not_source_father_assertion=True)
  assert d['preferred_generation_distance']-d['known_close_chain']['distance']==member['generation_distance']
  assert c['generation_interpretation']==dict(decision_id=d['id'],source_assertion_id=d['source_assertion_id'],reported_generation_number=8,preferred_generation_distance=7,alternative_generation_distances=[8],known_descendant_chain_distance=5,effective_assembly_generation_distance=2,supersedes_scope='this_family_ancestor_connection_only',raw_source_qualifiers_unchanged=True,preserves_editorial_gui_mei_parent=True,modern_opinion_independently_validated=False,modern_reference_url=d['modern_reference']['url'],human_reviewed=False)
  wanted_steps=[dict(kind='source_assertion',assertion_id=k)for k in FACTS[1:5]]+[dict(kind='editorial_parent_between_consecutive_ancestors',nearer_ancestor_assertion_id=FACTS[4],farther_ancestor_assertion_id=FACTS[5])]
  assert c['steps']==wanted_steps
  for i,aid in enumerate(FACTS[1:5]):
   a=assertions[aid];assert a['predicate']=='father'and a['subject_person_id']in groups[i]and a['object_person_id']in groups[i+1]and a['qualifiers']['lineage']=='paternal'
   assert selected[i]['parent_person_id']==chain[i+1]and selected[i]['source_assertion_id']==aid
  gui=selected[4];pc=gui['parent_connection'];assert gui['parent_person_id']==member['person_id']and gui['source_assertion_id']is None
  assert pc['type']=='parent_between_consecutive_ancestors'and pc['chain_subject_person_id']==chain[3]and pc['nearer_ancestor_assertion_id']==FACTS[4]and pc['farther_ancestor_assertion_id']==FACTS[5]and pc['human_reviewed']is False
  try:from scripts.ancestry_chain import consecutive_ancestor_parent_valid
  except ImportError:from ancestry_chain import consecutive_ancestor_parent_valid
  assert consecutive_ancestor_parent_valid(gui,rows,assertions,chapters,root)
  # New explicit ancestry supersedes this unnamed slot and requires a reviewed successor.
  assert not any(a.get('predicate')in('father','grandfather')and a.get('subject_person_id')in groups[5]for a in assertions.values())
  assert not any(a.get('predicate')in('adoptive_father','ritual_successor_of')and a.get('subject_person_id')in set.union(*groups[:6])for a in assertions.values())
  for i in range(5):
   assert not any(a.get('predicate')=='father'and a.get('subject_person_id')in groups[i]and a.get('object_person_id')not in groups[i+1]for a in assertions.values())
  expected={(a['id'],e['chapter_id'],e['paragraph_id'],e['source_id'],e['quote'])for aid in FACTS for a in[assertions[aid]]for e in a['evidence']}
  refs=c['references'];actual=[(r['assertion_id'],r['chapter_id'],r['paragraph_id'],r['source_id'],r['quote'])for r in refs];assert len(actual)==len(expected)and set(actual)==expected
  for r in refs:
   ch=chapters[r['chapter_id']];assert r['scope']and r['url']in(ch['source']['url'],ch['source']['permalink'])and r['work_id']==ch['work_id']and r['book_id']==ch['book_id']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
