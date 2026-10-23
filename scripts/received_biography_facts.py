# coding: utf-8
"""Exact received-clause roles for succession, ages and reported requests.
No person/work/chapter ID or name allowlist; no dates inferred from campaigns.
"""
import re,hashlib
TEMPLATES={
 'biography_origin':'<subject>字<style>{place}人也',
 'posthumous_named_son':'諡曰<parent>子<child>嗣',
 'office_two_heirs':'<parent>為{office}早薨子<child>嗣<child_repeat>薨子<grandchild>嗣',
 'grandson_style_office':'<source_work>曰<ancestor>孫<descendant>字<style>有才識位{office}',
 'named_enfeoffment':'封<subject>{rank}',
 'recommended_office':'<subject>出亦喜曰眞<lord>也表為{office}',
 'office_subject_prefix':'{office}<subject>',
 'death_age_after_return':'<subject>{description}<patron>曰惟<style>為能知<speaker>意年{age}自{return_place}還疾篤<patron_repeat>問疾者交錯及薨',
 'lifetime_recruitment_age':'年{age}辟{office}',
 'letter_death_age_bound':'<writer>與<recipient>書追傷<subject>曰<subject_repeat>年不滿{age}相與周旋{years}年阻險艱難皆共惟之又以其通達見世事無所疑滯欲以後事屬之何意卒爾失之',
 'requested_increase_and_total':'<subject>勲實不可忘可增邑{increase}{increase_unit}并前{total}{unit}',
 'requested_posthumous_total':'宜追增<subject>封并前{total}{unit}',
 'reported_heir_memorial_total':'今表增<subject>滿{total}{unit}',
 'campaign_service_duration':'軍祭酒<subject>自從征伐{years}年',
 'memorial_campaign_death':'<subject>{description}自在軍旅{years}餘年行同騎乘坐共幄席東禽<enemy1>西取<enemy2>斬<enemy3>之首平朔土之衆踰越險塞盪定烏九震威遼東以梟<enemy4>雖假天威易為指麾至於臨敵發揚誓命凶逆克殄勲實由<subject_repeat>方將表顯短命早終',
 'army_service_duration':'<subject>{description}自在軍旅{years}餘年',
}

def exact(p,a):
 assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'];return a

def parse(s):
 try:from scripts.biographical_appointment_sequence import integer
 except ImportError:from biographical_appointment_sequence import integer
 assert re.fullmatch('[一二三四五六七八九十百千萬有]+',s);n=integer(s.replace('有',''));assert type(n)is int and n>0;return n

def analyse(rec,ch,root):
 try:from scripts.fixed_kanripo_projection import errors
 except ImportError:from fixed_kanripo_projection import errors
 assert not errors(ch,root)
 b=rec['source_fact_frame'];assert set(b)in({'kind','rule','slot','paragraph_id','scope_anchor','roles','fields','source_revision','paragraph_sha256','source_layer'},{'kind','rule','slot','paragraph_id','scope_anchor','roles','fields','source_revision','paragraph_sha256','source_layer','prior_subject_reference'})and b['kind']=='received_biographical_fact_frame'
 p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];ms={m['id']:m for m in p['mentions']};rs={k:ms[v]for k,v in b['roles'].items()};fs=b['fields'];a=exact(p,b['scope_anchor']);rule=b['rule']
 assert b['source_revision']==ch['source']['revision_id']and b['source_layer']==p['text_layer']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
 assert a['start']==0 or t[a['start']-1]not in'未不非無'
 assert not any(c in t[:a['start']]for c in'「『')or(t[:a['start']].count('「')==t[:a['start']].count('」')and t[:a['start']].count('『')==t[:a['start']].count('』'))
 pos=a['start'];usedr=set();usedf=set()
 for tok in re.split(r'(<[^>]+>|\{[^}]+\})',TEMPLATES[rule]):
  if not tok:continue
  if tok.startswith('<'):
   k=tok[1:-1];m=rs[k];assert m['kind']==('work'if k=='source_work'else'person')and m['start']==pos and t[m['start']:m['end']]==m['surface'];pos=m['end'];usedr.add(k)
  elif tok.startswith('{'):
   k=tok[1:-1];f=exact(p,fs[k]);assert f['start']==pos and not any(c in f['surface']for c in'「」『』');pos=f['end'];usedf.add(k)
  else:assert t.startswith(tok,pos);pos+=len(tok)
 assert pos==a['end']and set(rs)==usedr and set(fs)==usedf
 if rule in('posthumous_named_son','office_two_heirs','grandson_style_office'):assert a['start']==0 and a['end']==len(t)
 if rule in('named_enfeoffment','recommended_office','lifetime_recruitment_age'):assert a['end']==len(t)
 if 'rank'in fs:assert re.fullmatch(r'[^曰云未非無不]{1,15}[公侯伯子男王]',fs['rank']['surface'])
 for k in('unit','increase_unit'):
  if k in fs:assert fs[k]['surface']in('尸','戶','户','戸')
 if rule=='office_two_heirs':assert len({rs[k]['person_id']for k in('parent','child','grandchild')})==3
 if rule in('posthumous_named_son','grandson_style_office','death_age_after_return'):
  role={'posthumous_named_son':'parent','grandson_style_office':'ancestor','death_age_after_return':'subject'}[rule];head=ch['paragraphs'][0]['mentions'][0];assert head['kind']=='person'and head['start']==0 and ch['paragraphs'][0]['text'][head['end']:].startswith('字')and head['person_id']==rs[role]['person_id']
 assert all(m['id']in b['roles'].values()for m in p['mentions']if m['kind']=='person'and a['start']<=m['start']<a['end'])
 for k in ('description',):
  if k in fs:assert len(fs[k]['surface'])<=80 and not any(x in fs[k]['surface']for x in('曰','云','詔','謂','未','非'))
 for k in ('office','rank'):
  if k in fs:assert 1<=len(fs[k]['surface'])<=16 and not any(x in fs[k]['surface']for x in'曰云未非無不')
 if 'child_repeat'in rs:assert rs['child_repeat']['person_id']==rs['child']['person_id']
 if 'patron_repeat'in rs:assert rs['patron_repeat']['person_id']==rs['patron']['person_id']==rs['speaker']['person_id']!=rs['subject']['person_id']==rs['style']['person_id']
 if 'subject_repeat'in rs:
  assert rs['subject_repeat']['person_id']==rs['subject']['person_id']
  if 'writer'in rs:assert rs['writer']['person_id']!=rs['subject']['person_id']
 if 'style'in rs and 'descendant'in rs:assert rs['style']['person_id']==rs['descendant']['person_id']!=rs['ancestor']['person_id']
 prior=None
 if 'prior_subject_reference'in b:
  ref=b['prior_subject_reference'];assert set(ref)=={'paragraph_id','person_mention_id'}and ref['paragraph_id']==p['id'];prior=ms[ref['person_mention_id']];assert prior['kind']=='person'and prior['end']<=a['start']
  between=t[prior['end']:a['start']];assert not any(x in between for x in('曰','云','詔','謂','言','「','」','『','』'))and not any(m['kind']=='person'and prior['end']<=m['start']<a['start']for m in p['mentions'])
 e,=rec['evidence'];assert all(e[k]==ch[k]for k in('work_id','book_id','source_id'))and e['chapter_id']==ch['id']and e['paragraph_id']==p['id']and e['quote']==t
 assert rec['status']=='source_attested'and rec['human_reviewed']is False and rec['model']is None
 return b,p,rs,fs,prior

def valid(rec,ch,root):
 try:
  b,p,r,f,prior=analyse(rec,ch,root);rule=b['rule'];slot=b['slot'];ev=rec['evidence'][0]
  word=lambda k:r[k]['surface'];pid=lambda k:r[k]['person_id'];value=lambda k:f[k]['surface']
  if 'predicate'in rec:
   if rule=='posthumous_named_son':child,parent='child','parent';term='子'+word(child);pred='father'
   elif rule=='office_two_heirs':
    child,parent={'first_son':('child','parent'),'second_son':('grandchild','child_repeat')}[slot];term='子'+word(child);pred='father'
   elif rule=='grandson_style_office':child,parent='descendant','ancestor';term='孫'+word(child);pred='grandfather'
   else:return False
   assert rec['predicate']==pred and rec['subject_person_id']==pid(child)!=pid(parent)==rec['object_person_id']and ev['subject_person_mention_id']==r[child]['id']and ev['object_person_mention_id']==r[parent]['id']and rec['qualifiers']['source_term']==term and rec['qualifiers']['lineage']=='paternal'
   if pred=='grandfather':assert rec['qualifiers']==dict(source_term=term,lineage='paternal',generation_distance=2,parent_person_id=None,intermediate_person_ids=[None])
   else:assert rec['qualifiers']==dict(source_term=term,lineage='paternal')
   return True
  if 'relation'in rec:
   assert rule=='biography_origin'and rec['relation']=='biographical_origin'and rec['person_id']==pid('subject')==pid('style')and ev['person_mention_id']==r['subject']['id']and rec['place']==dict(source_name=value('place'),place_id=None,modern_identification=None)and rec['source_term']==value('place')+'人也'and rec['date_expression']is None
   return True
  if 'event_type'in rec:
   assert rec['date_expression']is None and not any(k.startswith('normalized_date')for k in rec)
   if rec['event_type']=='death':
    who,term={('death_age_after_return','death'):('subject','及薨'),('memorial_campaign_death','death'):('subject','短命早終'),('letter_death_age_bound','death'):('subject','何意卒爾失之'),('office_two_heirs','parent_death'):('parent','早薨'),('office_two_heirs','child_death'):('child_repeat','薨')}[(rule,slot)]
    assert rec['person_id']==pid(who)and ev['person_mention_id']==r[who]['id']and rec['source_term']==term
   elif rec['event_type']=='recruitment':assert rule=='lifetime_recruitment_age'and slot=='recruitment'and prior and rec['person_id']==prior['person_id']and ev['person_mention_id']==prior['id']and rec['source_term']=='辟'+value('office')and rec['recruiting_organ_source_name']==value('office')and rec['office_title']is None and rec['service_attested']is False
   elif rec['event_type']=='noble_title_succession':
    who,parent={('posthumous_named_son','succession'):('child','parent'),('office_two_heirs','first_succession'):('child','parent'),('office_two_heirs','second_succession'):('grandchild','child_repeat')}[(rule,slot)];term='子'+word(who)+'嗣'
    assert rec['person_id']==pid(who)and rec['predecessor_person_id']==pid(parent)and rec['source_term']==term and ev['person_mention_id']==r[who]['id']and rec['title']is None and rec['holding_id']is None and rec['mode']=='accession'
   else:return False
   return True
  if 'age_context'in rec:
   who=prior if rule=='lifetime_recruitment_age'else r['subject'];assert who and rec['person_id']==who['person_id']and ev['person_mention_id']==who['id']and rec['source_number']==value('age')and rec['birth_year']is None and rec['counting']=='unspecified_source_age'and rec['unit']=='source_age_years'
   assert rec['age_context']['kind']==('during_life'if rule=='lifetime_recruitment_age'else'at_death')
   if rule=='letter_death_age_bound':assert rec['source_term']=='年不滿'+value('age')and rec['value']is None and rec['bounds']==dict(lower=None,lower_inclusive=None,upper=parse(value('age')),upper_inclusive=False)and rec['reporting_status']=='upper_bound_report'
   else:assert rec['source_term']=='年'+value('age')and rec['value']==parse(value('age'))and'bounds'not in rec
   return True
  if 'title'in rec:
   who,key,kind,mode={('posthumous_named_son','posthumous'):('parent','parent','honorific','posthumous_naming'),('office_two_heirs','office'):('parent','office','office','attestation'),('grandson_style_office','office'):('descendant','office','office','attestation'),('named_enfeoffment','rank'):('subject','rank','noble_rank','grant'),('office_subject_prefix','office'):('subject','office','office','attestation')}[(rule,slot)];title=word(key)if key in r else value(key)
   assert rec['person_id']==pid(who)and rec['title']==title and rec['kind']==kind and rec['mode']==mode and ev['person_mention_id']==r[who]['id']
   if mode=='posthumous_naming':
    basis=rec['naming_basis'];assert set(basis)=={'kind','source_term','death_event_id','evidence'}and basis['kind']=='received_unit_naming_after_death'and basis['source_term']=='諡曰'+title and basis['evidence']==rec['evidence']
    from pathlib import Path
    import json
    events=[e for path in(Path(root)/'corpus').glob('*/*-life-events.json')for e in json.loads(path.read_bytes())['events']if e['id']==basis['death_event_id']]
    death,=events;assert death['person_id']==rec['person_id']and death['event_type']=='death'and ch['paragraphs'].index(next(p for p in ch['paragraphs']if p['id']==death['evidence'][0]['paragraph_id']))<ch['paragraphs'].index(p)
    assert valid(death,ch,root)
   a,=rec['attestations'];assert a['person_mention_id']==r[who]['id']and a['surface']==title and p['text'][a['start']:a['end']]==title
   assert rec['effective_period']['end']==dict(status='unknown',date_expression=None,evidence=[])
   start=rec['effective_period']['start'];assert start==(dict(status='source_event',event_type=mode,date_expression=None,evidence=rec['evidence'])if mode in('grant','posthumous_naming')else dict(status='unknown',date_expression=None,evidence=[]))
   return True
  if 'values'in rec:
   v=rec['values'];a=exact(p,rec['source_anchor']);assert rec['source_term']==a['surface']and rec['source_revision']==b['source_revision']and rec['paragraph_sha256']==b['paragraph_sha256']and rec['date_expression']is None and b['scope_anchor']['start']<=a['start']<a['end']<=b['scope_anchor']['end']
   if rule=='recommended_office':expected=dict(office_source_name=value('office'),appointment_stage='memorial_nomination',assumption_attested_by_this_clause=False);who='subject';kind='office_nomination';term='表為'+value('office')
   elif rule in('requested_increase_and_total','requested_posthumous_total','reported_heir_memorial_total'):
    expected=dict(increase=parse(value('increase'))if'increase'in f else None,increase_source_number=value('increase')if'increase'in f else None,increase_unit_source_name=value('increase_unit')if'increase_unit'in f else None,total=parse(value('total')),total_source_number=value('total'),unit_source_name=value('unit'),enactment_status='memorial_report_not_independent_confirmation',actual_revenue=None,request_kind={'requested_increase_and_total':'memorial_request','requested_posthumous_total':'memorial_request','reported_heir_memorial_total':'reported_memorial_submission'}[rule]);who='subject';kind='fief_household_count';term=('可增邑'+value('increase')+value('increase_unit')+'并前'+value('total')+value('unit'))if rule=='requested_increase_and_total'else('宜追增'+word('subject')+'封并前'+value('total')+value('unit'))if rule=='requested_posthumous_total'else'今表增'+word('subject')+'滿'+value('total')+value('unit')
   elif rule in('campaign_service_duration','army_service_duration','letter_death_age_bound'):
    who='subject';kind='reported_service_duration';num=value('years');expected=dict(value=None if rule=='army_service_duration'else parse(num),source_number=num,lower_exclusive=parse(num)if rule=='army_service_duration'else None,unit='source_years',counting='unspecified_source_years',activity_code={'campaign_service_duration':'campaign_service','army_service_duration':'military_service','letter_death_age_bound':'association_with_letter_writer'}[rule],office_tenure=False);term={'campaign_service_duration':'自從征伐'+num+'年','army_service_duration':'自在軍旅'+num+'餘年','letter_death_age_bound':'相與周旋'+num+'年'}[rule]
   else:return False
   assert rec['person_id']==pid(who)and ev['person_mention_id']==r[who]['id']and rec['kind']==kind and rec['source_term']==term and v==expected
   return True
  return False
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError,OSError):return False

def errors(root):
 from pathlib import Path
 import json
 root=Path(root).resolve();records=[json.loads(p.read_bytes())for p in(root/'corpus').glob('*/*.json')];chapters={d['id']:d for d in records if d.get('record_type')=='marked_chapter'};out=[]
 for d in records:
  ch=chapters.get(d.get('chapter_id')or d.get('id'))
  if not ch:continue
  rows=[x for k in('assertions','holdings','events','records')for x in d.get(k,[])]+d.get('annotation',{}).get('age_assertions',[])
  for x in rows:
   if 'source_fact_frame'in x and not valid(x,ch,root):out.append('收到傳文生命親屬與奏請框架不符:'+str(x.get('id')))
 return out

def validate_surname(n,names,chapters,assertions,root):
 try:
  b=n['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','source_full_quote','assertion_ids'}and b['kind']=='contextual_surname_from_received_fact_chain'and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale']and n['status']=='contextual_provisional'and n['human_reviewed']is False
  seed,=[x for x in names if x.get('id')==b['source_name_record_id']];ch=chapters[n['chapter_id']];assert seed['chapter_id']==ch['id']and not seed.get('surname_basis')and seed['surname']==n['surname']and seed['ming']and seed['surname']
  ps={p['id']:p for p in ch['paragraphs']};p=ps[seed['paragraph_id']];sm=next(m for m in p['mentions']if m['id']==seed['person_mention_id']);assert seed['quote']==b['source_full_quote']==p['text']and sm['person_id']==seed['person_id']and sm['start']==0 and sm['surface']==seed['surname']+seed['ming']and p['text'].startswith(sm['surface']+'字')
  p=ps[n['paragraph_id']];tm=next(m for m in p['mentions']if m['id']==n['person_mention_id']);assert tm['person_id']==n['person_id']and tm['surface']==n['ming']and n['quote']==p['text']
  if 'zi'in n:assert p['text'][tm['end']:tm['end']+len(n['zi'])+1]=='字'+n['zi']
  ids=b['assertion_ids'];assert 1<=len(ids)<=3 and len(set(ids))==len(ids);current=seed['person_id'];seen={current}
  for aid in ids:
   x,=[x for x in assertions if x['id']==aid];assert x['predicate']in('father','grandfather')and x['object_person_id']==current and x['qualifiers']['lineage']=='paternal'and valid(x,ch,root)and x['subject_person_id']not in seen
   if x['predicate']=='grandfather':assert x['qualifiers']['parent_person_id']is None and x['qualifiers']['intermediate_person_ids']==[None]
   current=x['subject_person_id'];seen.add(current)
  assert current==n['person_id']
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,OSError):raise ValueError('收到姓名須由同源明姓種子沿最多三條已綁父祖原證，不用ID、配偶或未名中間父親補姓')
