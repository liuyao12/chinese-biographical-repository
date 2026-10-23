"""Bound biographical office offers: refusal and service unreported remain separate."""
import hashlib,re

def errors(q,ch,pids):
 try:
  b=q['source_appointment_context'];a=b['clause_anchor'];p=next(x for x in ch['paragraphs']if x['id']==a['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};m=ms[q['person_mention_id']];r=q['role_anchor'];term=a['surface'];rule=b['clause_rule'];title=q['title'];e,=q['evidence']
  if(set(b)!={'kind','clause_anchor','clause_rule','source_revision','paragraph_sha256'}or b['kind']!='fixed_biography_offered_office_sequence'or b['source_revision']!=p['source_position']['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or m.get('person_id')!=q['person_id']or q['person_id']not in pids or e['quote']!=t or e['chapter_id']!=ch['id']or e['source_id']!=ch['source_id']or e['person_mention_id']!=m['id']or q['status']!='contextual_provisional'or q['human_reviewed']is not False or not q['interpretation_note']):return ['任用來源／人物不符']
  def anchor(x):return set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
  if not all(anchor(x)for x in [a,r,q['appointment_anchor']])or r['surface']!=title or not a['start']<=r['start']<r['end']<=a['end']:return ['任用錨點不符']
  outcomes={'unreported':('視事三年，徵都官尚書、中書令。','徵',None,['都官尚書','中書令']), 'longchang':('隆昌元年，復爲侍中，領新安王師。未拜，固求外出。','復爲','未拜',['侍中','新安王師']), 'jianwu':('建武四年，詔徵爲侍中、中書令，遂抗表不應召。','詔徵爲','遂抗表不應召',['侍中','中書令'])}
  if rule in outcomes:
   exact,verb,no,titles=outcomes[rule]
   if term!=exact or title not in titles:return ['任用句式不符']
   # The recipient must be the named same-paragraph biographical subject, not a ruler or brother.
   before=t[:a['start']];head=t[m['start']:m['end']]
   if m.get('person_id')!=ch['paragraphs'][0]['mentions'][0].get('person_id'):return ['任用承接主語不符']
  elif rule in ('yongyuan2','yongyuan3','accession'):
   configs={'yongyuan2':('永元二年，詔徵','爲散騎常侍、中書監，','爲散騎常侍、太常卿，並不屈。','詔徵','並不屈',['散騎常侍','中書監'],['散騎常侍','太常卿']), 'yongyuan3':('三年，又詔徵','爲侍中、太子少傅，','散騎常侍、太子詹事。時東昏皆下在所，使迫遣之，值義師已近，故並得不到。','又詔徵','並得不到',['侍中','太子少傅'],['散騎常侍','太子詹事']), 'accession':('高祖踐阼，徵','爲侍中、左光祿大夫、開府儀同三司，','散騎常侍、特進、右光祿大夫，又並不屈。','徵','並不屈',['侍中','左光祿大夫','開府儀同三司'],['散騎常侍','特進','右光祿大夫'])}
   prefix,left,right,verb,no,lt,rt=configs[rule];one=next((x for x in p['mentions']if x['start']==a['start']+len(prefix)),None)
   if not one:return ['共同任用首人缺錨']
   second_start=one['end']+len(left);two=next((x for x in p['mentions']if x['start']==second_start),None)
   if not two or term!=prefix+one['surface']+left+two['surface']+right or one.get('person_id')==two.get('person_id'):return ['共同任用雙人句式不符']
   who=one if m['id']==one['id']else two if m['id']==two['id']else None
   if who is None or title not in (lt if who is one else rt)or not who['end']<=r['start']<(two['start']if who is one else a['end']):return ['共同任用職稱錯配人物']
  elif rule=='prefecture':
   verb='加'if title=='後將軍'else'請並補';no='並不至'
   if term!='請並補臣府軍諮祭酒，朏加後將軍。」並不至。'or title not in ('軍諮祭酒','後將軍')or q['appointment_stage']!='invitation':return ['府召句式不符']
   heads=[x for x in p['mentions']if x['surface']in ('朏','胤')]
   if m not in heads or title=='後將軍'and(m['surface']!='朏'or not a['start']<m['start']<a['end']):return ['府召不明受職者']
  else:return ['未知任用句式']
  if q['appointment_anchor']['surface']!=verb:return ['任用動詞不符']
  pending=rule=='unreported'
  if q['proposal_kind']!=('appointment_service_unreported'if pending else'unassumed_appointment')or q['outcome']!=('not_reported'if pending else'not_assumed'):return ['未載與未任不得混型']
  if pending:
   if 'non_assumption_anchor'in q or 'non_assumption_kind'in q:return ['未載不得補拒絕']
  else:
   x=q['non_assumption_anchor']
   if not anchor(x)or x['surface']!=no or not a['start']<=x['start']<x['end']<=a['end']:return ['未任明文不符']
  return []
 except(KeyError,TypeError,ValueError,StopIteration):return ['任用資料不完整']
