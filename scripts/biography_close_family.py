# coding: utf-8
"""Literal close-family clauses with source-bound roles, never person-ID allowlists."""
import hashlib,re
PREFIX='close_family_'
def valid(a,paragraphs,assertions=()):
 if a.get("qualifiers",{}).get("source_clause_binding",{}).get("rule","").startswith("close_family_direct_"):
  try:
   from scripts.biography_direct_family import valid as direct_valid
  except ImportError:
   from biography_direct_family import valid as direct_valid
  return direct_valid(a,paragraphs)
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in b['roles'].items()};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if(set(b)!={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id'}or b['kind']!='biography_family_clause'or not b['rule'].startswith(PREFIX)or a['status']!='source_attested'or a['human_reviewed']is not False or e['chapter_id']!=cid or e['quote']!=t or p.get('text_layer')!='received_chapter'or p.get('source_position',{}).get('revision_id')!=b['revision_id']or hashlib.sha256(t.encode()).hexdigest()!=b['paragraph_sha256']or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or s['person_id']==o['person_id']):return False
  if any(m['kind']!='person'or type(m['start'])is not int or type(m['end'])is not int or not 0<=m['start']<m['end']<=len(t)or t[m['start']:m['end']]!=m['surface']for m in roles.values()):return False
  start,end=b['clause_start'],b['clause_end']
  if type(start)is not int or type(end)is not int or not 0<=start<end<=len(t):return False
  text=t[start:end];rule=b['rule'];allowed=[]
  def word(k):return roles[k]['surface']
  def pid(k):return roles[k]['person_id']
  def at(k,n):return roles[k]['start']==start+n
  def literal(parts):
   cursor=0;value=''
   for role,lit in parts:
    token=word(role)if role else lit
    if role and not at(role,cursor):return False
    value+=token;cursor+=len(token)
   return text==value
  if rule==PREFIX+'head_grandfather_father':
   if set(roles)!={'head','grandfather','father'}or start!=0 or len({pid(k)for k in roles})!=3:return False
   pattern=re.escape(word('head'))+r'，?字[^，。：「」]+，[^，。：「」]+人也。祖'+re.escape(word('grandfather'))+r'，[^。：「」]+。父'+re.escape(word('father'))+r'，[^。：「」]+。'
   if not re.fullmatch(pattern,text)or not at('head',0)or not t[roles['grandfather']['start']-1:roles['grandfather']['start']]=='祖'or not t[roles['father']['start']-1:roles['father']['start']]=='父'or any(x in text for x in'非未無不'):return False
   allowed=[('father','head','father'),('grandfather','head','grandfather')]
  elif rule==PREFIX+'unpunctuated_head_grandfather_father':
   if set(roles)!={'head','style','grandfather','father'}or start!=0 or pid('style')!=pid('head')or len({pid(k)for k in ('head','grandfather','father')})!=3:return False
   h=roles['head'];z=roles['style'];g=roles['grandfather'];f=roles['father']
   if not at('head',0)or z['start']!=h['end']+1 or t[h['end']:z['start']]!='字':return False
   origin=t[z['end']:g['start']];grand_office=t[g['end']:f['start']];father_office=t[f['end']:end]
   if not re.fullmatch(r'[^字祖父曰云言「」『』非未無不，。]{1,16}人也祖',origin):return False
   if not re.fullmatch(r'[^字祖父曰云言「」『』非未無不，。]{1,12}(?:卿|守|牧|將軍|尚書|侍中)父',grand_office):return False
   if not re.fullmatch(r'(?:奉朝請|[^字祖父曰云言「」『』非未無不，。]{0,12}(?:卿|守|牧|將軍|尚書|侍中))',father_office):return False
   if not h['end']<z['end']<g['start']<g['end']<f['start']<f['end']<=end:return False
   if any(m.get('kind')=='person'and start<=m['start']<end and m['id']not in b['roles'].values()for m in p['mentions']):return False
   allowed=[('father','head','father'),('grandfather','head','grandfather')]
  elif rule==PREFIX+'four_older_brothers':
   if set(roles)!={'head','first','second','third','fourth'}or len({pid(k)for k in roles})!=5:return False
   if not literal([('head',''),(None,'四兄'),('first',''),(None,'、'),('second',''),(None,'、'),('third',''),(None,'、'),('fourth','')]):return False
   allowed=[('brother',k,'head')for k in ('first','second','third','fourth')]
  elif rule==PREFIX+'father_arranged_daughter_marriage':
   if set(roles)!={'father','husband','daughter'}or word('daughter')!='女'or len({pid(k)for k in roles})!=3:return False
   if not literal([(None,'僕射'),('father',''),(None,'聞'),('husband',''),(None,'年少清正不惡，以'),('daughter',''),(None,'結婚，厚爲資送。')]):return False
   allowed=[('father','daughter','father'),('spouse','daughter','husband')]
  elif rule==PREFIX+'mother_old_care_resumed_subject':
   if set(roles)!={'head','mother','patron','prince','official','patron_resumed'}or word('mother')!='母'or pid('patron')!=pid('patron_resumed')or start!=0 or end!=len(t):return False
   if not literal([(None,'解褐車騎行參軍，遷祕書郎，司徒祭酒，丹陽丞，撫軍功曹。'),('patron',''),(None,'爲中軍，引爲記室。齊臺建，遷太子中舍人。建元初，轉'),('prince',''),(None,'友。以'),('mother',''),(None,'老須養，出爲安成內史。還爲中書郎。衞軍'),('official',''),(None,'引爲長史，雅相禮遇。除黃門郎，兼掌吏部。尋轉太子中庶子，領驍騎將軍，轉長兼侍中。'),('head',''),(None,'以晨昏有廢，固辭不受。'),('patron_resumed',''),(None,'勑令速拜，別停朝直。')]):return False
   if len({pid(k)for k in ('head','mother','patron','prince','official')})!=5:return False
   allowed=[('maternal_role','head','mother')]
  elif rule==PREFIX+'head_mother_mourning':
   if set(roles)!={'head','mother'}or word('mother')!='母'or start!=0:return False
   if not literal([('head',''),(None,'在職雖無殊能，而庶績修理。後遷光祿勳、吏部尚書，以'),('mother',''),(None,'憂去職。')]):return False
   allowed=[('maternal_role','head','mother')]
  elif rule==PREFIX+'sons_and_collateral_heir':
   if set(roles)!={'head','resumed','son','secondary_son','collateral','heir'}or word('heir')!='子'or pid('head')!=pid('resumed')or len({pid(k)for k in ('head','son','secondary_son','collateral','heir')})!=5 or start!=0 or end!=len(t):return False
   if not literal([(None,'子'),('son',''),(None,'，有美名。少而大肥，'),('head',''),(None,'令食穅，而肥愈甚。年十九卒。有庶子'),('secondary_son',''),(None,'，'),('resumed',''),(None,'所不齒。以從弟陽平太守'),('collateral',''),('heir',''),(None,'為嗣。')]):return False
   allowed=[('father','son','head'),('father','secondary_son','head'),('father','heir','collateral'),('ritual_successor_of','heir','head'),('agnatic_cousin','collateral','head')]
  elif rule==PREFIX+'head_daughter_marriage':
   if set(roles)!={'head','daughter','husband'}or word('daughter')!='女'or roles['head']['start']!=0 or not t.startswith(word('head')+'以晉室方亂，慕')or not t[:start].endswith('天下人謂之膏肓之疾。'):return False
   if not literal([('daughter',''),(None,'適'),('husband',''),(None,'，')]):return False
   allowed=[('father','daughter','head'),('spouse','daughter','husband')]
  elif rule==PREFIX+'younger_clansman_resumption':
   if set(roles)!={'head','resumed','collateral'}or roles['head']['start']!=0 or not t.startswith(word('head')+'有人倫鑒識，')or pid('head')!=pid('resumed'):return False
   if not literal([(None,'族弟'),('collateral',''),(None,'有高名，'),('resumed',''),(None,'惡之。')]):return False
   allowed=[('agnatic_cousin','collateral','head')]
  elif rule==PREFIX+'unnamed_congzi_wedding':
   if set(roles)!={'head','resumed','junior'}or word('junior')!='從子'or roles['head']['start']!=0 or not t.startswith(word('head')+'以晉室方亂，慕')or pid('head')!=pid('resumed'):return False
   if not literal([('junior',''),(None,'將婚，'),('resumed',''),(None,'遺其一單衣，婚訖而更責取。')]):return False
   allowed=[('agnatic_senior_kin','junior','head')]
  else:return False
  hit=[(pred,x,y)for pred,x,y in allowed if pred==a['predicate']and pid(x)==a['subject_person_id']and pid(y)==a['object_person_id']and roles[x]['id']==s['id']and roles[y]['id']==o['id']]
  if len(hit)!=1 or not isinstance(q.get('source_term'),str)or not q['source_term']or q['source_term']not in text:return False
  pred=hit[0][0]
  if rule in (PREFIX+'head_grandfather_father',PREFIX+'unpunctuated_head_grandfather_father'):term=('父'+word('father'))if pred=='father'else('祖'+word('grandfather'))
  elif rule==PREFIX+'four_older_brothers':term=word('head')+'四兄'+ '、'.join(word(k)for k in ('first','second','third','fourth'))
  elif rule==PREFIX+'father_arranged_daughter_marriage':term='以女結婚'
  elif rule==PREFIX+'mother_old_care_resumed_subject':term='以母老須養'
  elif rule==PREFIX+'head_mother_mourning':term='以母憂去職'
  elif rule==PREFIX+'sons_and_collateral_heir':
   if pred=='father':term='子'+word('son')if a['subject_person_id']==pid('son')else'庶子'+word('secondary_son')if a['subject_person_id']==pid('secondary_son')else word('collateral')+'子'
   elif pred=='ritual_successor_of':term='以從弟陽平太守'+word('collateral')+'子為嗣'
   else:term='從弟陽平太守'+word('collateral')
  elif rule==PREFIX+'head_daughter_marriage':term=('女適'if pred=='father'else'適')+word('husband')
  elif rule==PREFIX+'younger_clansman_resumption':term='族弟'+word('collateral')
  else:term='從子'
  if q['source_term']!=term:return False
  expected={'source_term','source_clause_binding'}
  if pred in('father','grandfather'):
   expected.add('lineage')
   if q.get('lineage')!='paternal':return False
  elif pred=='brother':
   expected.add('relative_birth_order')
   if q.get('relative_birth_order')!={'older_person_id':a['subject_person_id'],'younger_person_id':a['object_person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}:return False
  elif pred=='maternal_role':
   expected|={'role','biological_mother','father_person_id'}
   if q.get('role')!='mother_unspecified'or q.get('biological_mother')is not None or q.get('father_person_id')is not None:return False
  elif pred in('agnatic_cousin','agnatic_senior_kin'):
   expected.add('kinship_structure');structure={'lineage':'paternal','generation_difference':0 if pred=='agnatic_cousin'else -1,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'younger'if pred=='agnatic_cousin'else'unknown'}
   if q.get('kinship_structure')!=structure:return False
   if pred=='agnatic_cousin':
    expected.add('relative_birth_order')
    if q.get('relative_birth_order')!={'older_person_id':a['object_person_id'],'younger_person_id':a['subject_person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'agnatic_cousins'}:return False
  elif pred=='ritual_successor_of':
   expected|={'succession_kind','legal_adoption_status','parentage_inference'}
   if q.get('succession_kind')!='collateral_unnamed_son_weisi'or q.get('legal_adoption_status')!='not_stated'or q.get('parentage_inference')!='not_inferred':return False
   if not any(x.get('predicate')=='father'and x.get('subject_person_id')==pid('heir')and x.get('object_person_id')==pid('collateral')and valid(x,paragraphs)for x in assertions):return False
  return set(q)==expected
 except(KeyError,TypeError,ValueError,IndexError,StopIteration):return False
