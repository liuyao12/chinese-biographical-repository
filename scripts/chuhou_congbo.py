"""One received 出後從伯 clause: adopter, natal father and age rank stay separate.
No person-ID whitelist; received text and stable source roles are pinned instead.
The enclosing native fixed-witness validator independently verifies the raw witness.
"""
import hashlib
BASIS='fixed_received_chuhou_named_congbo'
PARAGRAPH_SHA='94e37a418e1ef099ce75d0633046b78c7f0481eb44210265b11e5c16abbd2021'
RAW_SHA='b27aa9fc386b5f40990822d615febffcb8b8cd6df3fe6f74585274ff733c12be'

def chuhou_congbo_valid(a, paragraphs, assertions):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
  assert a['predicate']=='adoptive_father'and a['status']=='source_attested'and a['human_reviewed']is False
  assert cid==e['chapter_id']=='c-jinshu-035-peiwei'and e['work_id']=='w-jinshu'and e['book_id']=='b-jinshu-035'and e['source_id']=='s-jinshu-035-ws2506399-peiwei'
  assert e['quote']==t and hashlib.sha256(t.encode()).hexdigest()==PARAGRAPH_SHA
  assert p['text_layer']=='received_chapter'and p['source_position']['source_layer']=='received_biography'and p['source_position']['revision_id']==2506399
  assert set(q)=={'source_term','source_interpretation_status','adoption_basis','biological_father_assertion_id','collateral_source_term','modern_legal_status','actual_upbringing','exact_distance','common_ancestor_person_id','connecting_person_ids','source_clause_binding'}
  assert q['adoption_basis']==BASIS and q['source_term']=='該出後從伯凱'and q['collateral_source_term']=='從伯'and q['source_interpretation_status']=='explicit_source_wording'
  assert q['modern_legal_status']==q['actual_upbringing']=='not_inferred'and all(q[k]is None for k in ('exact_distance','common_ancestor_person_id','connecting_person_ids'))
  assert set(b)=={'kind','revision_id','paragraph_sha256','raw_sha256','clause_anchor','roles'}and b['kind']==BASIS and b['revision_id']==2506399 and b['paragraph_sha256']==PARAGRAPH_SHA and b['raw_sha256']==RAW_SHA
  start=t.index('該出後從伯凱');assert b['clause_anchor']==dict(paragraph_id=p['id'],start=start,end=start+6,surface='該出後從伯凱')
  roles=b['roles'];assert set(roles)=={'child','adopter','biological_child','biological_father'}
  expected={'child':(151,152,'該'),'adopter':(156,157,'凱'),'biological_child':(71,72,'該'),'biological_father':(10,11,'頠')}
  for role,(lo,hi,surface)in expected.items():
   m=ms[roles[role]];assert m['id']==p['id']+':m%04d'%lo and m['kind']=='person'and(m['start'],m['end'],m['surface'])==(lo,hi,surface)and t[lo:hi]==surface
  child,parent,natal,fa=(ms[roles[r]]for r in ('child','adopter','biological_child','biological_father'))
  assert child['person_id']==natal['person_id']==a['subject_person_id']and parent['person_id']==a['object_person_id']
  assert len({child['person_id'],parent['person_id'],fa['person_id']})==3
  assert e['subject_person_mention_id']==child['id']and e['object_person_mention_id']==parent['id']
  fathers=[x for x in assertions if x['id']==q['biological_father_assertion_id']];f,=fathers
  assert f['predicate']=='father'and f['status']=='source_attested'and f['subject_person_id']==child['person_id']and f['object_person_id']==fa['person_id']and f['qualifiers']['source_term']=='二子嵩、該'and f['qualifiers']['lineage']=='paternal'
  fe,=f['evidence'];assert fe==dict(work_id=e['work_id'],book_id=e['book_id'],source_id=e['source_id'],chapter_id=cid,paragraph_id=p['id'],quote=t,subject_person_mention_id=natal['id'],object_person_mention_id=fa['id'])
  assert t[67:72]=='二子嵩、該'and t[start:start+6]=='該出後從伯凱'
  return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,AttributeError,IndexError):return False
