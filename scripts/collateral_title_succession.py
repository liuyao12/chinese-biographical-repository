# coding: utf-8
"""A named collateral successor is not automatically a son or adopted son."""
import hashlib

def valid(h, holdings, paragraphs, relations):
 try:
  i=h['inheritance'];b=i['source_chain_binding'];e,=i['evidence']
  prior=holdings[i['predecessor_holding_id']];cid,p=paragraphs[e['paragraph_id']];text=p['text'];ms={m['id']:m for m in p['mentions']}
  assert set(i)=={'predecessor_person_id','predecessor_holding_id','resolved_title','source_term','status','evidence','rationale','human_reviewed','predecessor_relation','source_chain_binding'}
  assert i['predecessor_relation']=='named_collateral_succession'and i['status']=='contextual_provisional'and i['human_reviewed']is False and i['rationale']
  assert h['kind']==prior['kind']=='noble_rank'and h['mode']=='accession'and h['status']=='source_attested'and prior['mode']=='grant'and 'inheritance'not in prior
  assert i['predecessor_person_id']==prior['person_id']!=h['person_id']and i['resolved_title']==prior['title']
  assert set(b)=={'kind','predecessor_person_mention_id','father_person_mention_id','successor_person_mention_id','brother_assertion_id','father_assertion_id','clause_anchor','antecedent_title_anchor','source_revision','paragraph_sha256'}
  assert b['kind']=='no_son_brother_supplies_named_son'and e['chapter_id']==cid and e['quote']==text and p['text_layer']=='received_chapter'
  assert b['source_revision']==p['source_position']['source_revision']and b['paragraph_sha256']==hashlib.sha256(text.encode()).hexdigest()
  predecessor,father,successor=[ms[b[key]]for key in('predecessor_person_mention_id','father_person_mention_id','successor_person_mention_id')]
  assert all(m['kind']=='person'and text[m['start']:m['end']]==m['surface']for m in(predecessor,father,successor))
  assert predecessor['person_id']==prior['person_id']and successor['person_id']==h['person_id']and len({m['person_id']for m in(predecessor,father,successor)})==3
  def anchored(a):
   return(set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['surface'])
  clause,antecedent=b['clause_anchor'],b['antecedent_title_anchor'];assert anchored(clause)and anchored(antecedent)
  assert clause['surface']==i['source_term']=='無子弟'+father['surface']+'以子'+successor['surface']+'嗣封'
  assert father['start']==clause['start']+3 and successor['start']==father['end']+2 and successor['end']+2==clause['end']
  assert antecedent['surface']==prior['title']and any(all(a.get(k)==v for k,v in antecedent.items())for a in prior['attestations'])
  assert antecedent['end']<predecessor['start']<predecessor['end']<=clause['start']
  assert text[predecessor['end']:clause['start']]=='官三年卒時年四十一追贈左將軍'
  assert any(a['person_mention_id']in ms and ms[a['person_mention_id']]['person_id']==predecessor['person_id']for a in prior['attestations'])
  family={r['id']:r for r in relations};bro=family[b['brother_assertion_id']];fa=family[b['father_assertion_id']]
  assert bro['predicate']=='brother'and bro['subject_person_id']==father['person_id']and bro['object_person_id']==predecessor['person_id']
  assert fa['predicate']=='father'and fa['subject_person_id']==successor['person_id']and fa['object_person_id']==father['person_id']
  assert all(r['status']=='source_attested'and any(x['paragraph_id']==p['id']and x['quote']==text for x in r['evidence'])for r in(bro,fa))
  assert h['title']=='嗣封'and e['person_mention_id']==successor['id']and h['evidence']==i['evidence']==h['effective_period']['start']['evidence']
  start=h['effective_period']['start'];assert start=={'status':'source_event','event_type':'accession','date_expression':None,'evidence':h['evidence']}
  assert h['effective_period']['end']=={'status':'unknown','date_expression':None,'evidence':[]}
  assert any(a.get('person_mention_id')==successor['id']and a.get('paragraph_id')==p['id']and a.get('surface')=='嗣封'and a.get('start')==successor['end']and a.get('end')==clause['end']and a.get('date_expression')is None for a in h['attestations'])
  return True
 except(AssertionError,KeyError,TypeError,ValueError):return False
