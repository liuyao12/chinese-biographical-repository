# coding: utf-8
"""Finite, position-bound received biographical kinship; no identity allowlists."""
import hashlib,re
KIND='punctuated_received_family_frame'
# Slots are actual person mentions; repeated roles must retain one identity.
FRAMES={
 'wife_named':('{husband}婦{title}{wife}，性妒忌。',[('spouse','wife','husband')]),
 'wife_children':('初，{husband}前妻{wife}淑美有才行，生二女{daughter1}、{daughter2}，{repeat1}一名{alias1}，{repeat2}一名{alias2}。父{father}誅，{repeatwife}坐流徙。後娶{office}{newfather}女，即{newwife}也。',[('spouse','wife','husband'),('mother','daughter1','wife'),('mother','daughter2','wife'),('father','daughter1','husband'),('father','daughter2','husband'),('father','wife','father'),('father','newwife','newfather')]),
 'named_parentage_head':('{child}字{zi}。母{mother}，{grandfather}少女也。父{father}，字{fatherzi}，{origin}人，{office}{ancestor}曾孫。',[('mother','child','mother'),('father','child','father'),('father','mother','grandfather'),('great_grandfather','father','ancestor')]),
 'named_daughter_marriage':('{father}秘之，遂以{daughter}妻{husband}。',[('spouse','daughter','husband'),('father','daughter','father')]),
 'named_external_grandson_heir':('及薨，{grandmother}輒以外孫{child}爲{heirfather}子，奉{ancestor}後。',[('grandmother','child','grandmother'),('adoptive_father','child','heirfather'),('ritual_successor_of','child','ancestor')]),
 'brother_courtesy':('{older}弟{younger}，字{zi}，',[('brother','younger','older')]),
 'collateral_two_nephews':('{senior}從子{junior1}、{junior2}並有鑒裁，俱爲黃門郎。',[('kinship_unspecified','junior1','senior'),('kinship_unspecified','junior2','senior')]),
 'brother_named':('{older}弟{younger}最知名。',[('brother','younger','older')]),
 'maternal_collateral_head':('{head}，字{headzi}，{origin}人，{niece}從舅也。',[('kinship_unspecified','niece','head')]),
 'collateral_grandson_heir_offer':('欲以{senior}從孫散騎侍郎{junior}爲嗣，{repeatjunior}陽狂自免。',[('kinship_unspecified','junior','senior')]),
 'collateral_greatgrandson_heir':('永興中，立{senior}從曾孫{junior}爲魯公，奉{repeatsenior}後，遭亂死，國除。',[('kinship_unspecified','junior','senior'),('ritual_successor_of','junior','senior')]),
}
FRAMES.update({
 'collateral_head_named_father_brother':('{child}，字{zi}，{senior}之從父弟也。父{father}，官至{office}。兄{brother}，{brotheroffice}。',[('father','child','father'),('brother','child','brother')]),
 'head_named_father':('{child}，字{zi}，{origin}人也。父{father}，{office}。',[('father','child','father')]),
 'named_mother_recalled':('初，{child}母{mother}見古今重節義，',[('maternal_role','child','mother')]),
 'named_daughter_princess':('而{wife}爲{husband}妃，',[('spouse','wife','husband')]),
 'named_mother_daughter_princess':('既而{mother}女爲{daughter}，',[('mother','daughter','mother')]),
 'queen_mother_title':('{emperor}即位，{daughter}擅權，加{other}廟備六佾之樂，母{mother}爲宜城君。',[('mother','daughter','mother')]),
 'heir_offer_then_named_son':('欲以{senior}從孫散騎侍郎{junior}爲嗣，{repeatjunior}陽狂自免。以子{child}後{repeatsenior}，封魯公，又病死。',[('father','child','repeatjunior'),('ritual_successor_of','child','repeatsenior')]),
 'biography_death_then_son':('{father}不得志，憂憤成疾。卒，追贈車騎將軍、開府儀同三司，諡曰成。子{child}字{zi}嗣，',[('father','child','father')]),
 'four_named_siblings_execution':('{head}少弟{younger1}有器望，及{repeathead}兄鞏令{older}、弟散騎侍郎{younger2}、呉王友{younger3}、{child}母{mother}皆伏誅。',[('brother','younger1','head'),('brother','head','older'),('brother','younger2','head'),('brother','younger3','head'),('mother','child','mother')]),
})
FRAMES.update({
 'named_elder_younger_office':('騎督{older}弟太子舍人{younger}謂',[('brother','younger','older')]),
 'named_emperor_maternal_uncle':('{child}舅{uncle}嘗毀',[('maternal_uncle','child','uncle')]),
 'two_granddaughters_marital_context':('時沛國{son}{mother}，及{emperor}舅羽林監{husband}{wife}，皆{grandfather}孫女。',[('maternal_role','son','mother'),('spouse','wife','husband'),('grandfather','mother','grandfather'),('grandfather','wife','grandfather'),('maternal_uncle','emperor','husband')]),
 'collateral_fiefs_named_list':('{emperor}遣侍中{envoy}犒勞，賜{senior}帛八千匹，增邑八千戸；分封從孫{junior1}新城亭侯，{junior2}安陽亭侯；弟陽裏亭侯{brother}、從孫關內侯{junior3}增戸邑。',[('kinship_unspecified','junior1','senior'),('kinship_unspecified','junior2','senior'),('kinship_unspecified','junior3','senior'),('brother','brother','senior')]),
})
FRAMES.update({
 'named_posthumous_son':('追贈{parent}子{child}爲魯殤公。',[('father','child','parent')]),
 'named_daughter_recommendation':('{reporter}因言{parent}{child}才質令淑，宜配{prince}。',[('father','child','parent')]),
 'named_daughter_as_princess':('又以{parent}{child}爲{repeatchild}，懼後益盛。',[('father','child','parent')]),
})
LITERALS={'title':r'[^，。；：「」]{1,12}','office':r'[^，。；：「」]{1,12}','brotheroffice':r'[^，。；：「」]{1,12}','origin':r'[^，。；：「」]{1,12}'}

def valid(a,paragraphs,chapters=None,root=None):
 try:
  q=a['qualifiers'];b=q['received_family_frame'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
  assert b['kind']==KIND and b['rule']in FRAMES and a['status']=='source_attested'and a['human_reviewed']is False
  assert set(b)=={'kind','rule','roles','clause_start','clause_end','paragraph_sha256','revision_id'}
  assert e['chapter_id']==cid and e['quote']==t and p['text_layer']=='received_chapter'
  assert p['source_position']['revision_id']==b['revision_id'] and hashlib.sha256(t.encode()).hexdigest()==b['paragraph_sha256']
  if chapters is not None and root is not None:
   try:from scripts.fixed_wikisource_units import source_errors
   except ImportError:from fixed_wikisource_units import source_errors
   ch=chapters[cid];assert ch.get('annotation',{}).get('fixed_wikisource_unit_ref')and ch['source']['revision_id']==b['revision_id']
   assert next(x for x in ch['paragraphs']if x['id']==p['id'])==p and p['source_position']['source_layer']=='received_biography'
   assert not source_errors(ch,root)
  start,end=b['clause_start'],b['clause_end'];assert type(start)is int and type(end)is int and 0<=start<end<=len(t)
  assert not start or t[start-1]in'。；，'
  assert t[:start].count('「')==t[:start].count('」')
  pattern,allowed=FRAMES[b['rule']];keys=re.findall(r'{(\w+)}',pattern);roles=b['roles'];assert set(roles)==set(keys)-set(LITERALS)
  parts=[];offsets={};cursor=0
  for token in re.finditer(r'{(\w+)}',pattern):
   parts.append(re.escape(pattern[cursor:token.start()]));key=token[1]
   if key in LITERALS:parts.append('(?P<'+key+'>'+LITERALS[key]+')')
   else:
    m=ms[roles[key]];assert m['kind']=='person'and m.get('person_id')and t[m['start']:m['end']]==m['surface'];parts.append('(?P<'+key+'>'+re.escape(m['surface'])+')')
   cursor=token.end()
  parts.append(re.escape(pattern[cursor:]));match=re.fullmatch(''.join(parts),t[start:end]);assert match
  for key,mid in roles.items():assert (ms[mid]['start'],ms[mid]['end'])==(start+match.start(key),start+match.end(key))
  def pid(k):return ms[roles[k]]['person_id']
  for key,other in [('repeat1','daughter1'),('alias1','daughter1'),('repeat2','daughter2'),('alias2','daughter2'),('repeatwife','wife'),('zi','child'),('fatherzi','father'),('repeatjunior','junior'),('repeatsenior','senior'),('repeathead','head'),('repeatchild','child')]:
   if key in roles and other in roles:assert pid(key)==pid(other)
  if b['rule']=='collateral_head_named_father_brother':assert len({pid(k)for k in ('child','senior','father','brother')})==4
  if b['rule']=='wife_children':assert len({pid(k)for k in ('husband','wife','daughter1','daughter2','father','newfather','newwife')})==7
  if b['rule']=='four_named_siblings_execution':assert len({pid(k)for k in ('head','younger1','older','younger2','younger3')})==5
  if b['rule']=='brother_courtesy':assert pid('zi')==pid('younger')
  if b['rule']=='maternal_collateral_head':assert pid('headzi')==pid('head')
  if b['rule']in('head_named_father','biography_death_then_son','collateral_head_named_father_brother'):assert pid('zi')==pid('child')
  s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  assert s['person_id']==a['subject_person_id']and o['person_id']==a['object_person_id']and s['person_id']!=o['person_id']
  hits=[x for x in allowed if (x[0],roles[x[1]],roles[x[2]])==(a['predicate'],s['id'],o['id'])];assert len(hits)==1
  rule=b['rule'];pred=a['predicate'];extra={}
  if pred=='kinship_unspecified':
   term,gen,lineage={'collateral_two_nephews':('從子',-1,'paternal'),'collateral_grandson_heir_offer':('從孫',-2,'paternal'),'collateral_greatgrandson_heir':('從曾孫',-3,'paternal'),'maternal_collateral_head':('從舅',-1,'maternal'),'collateral_fiefs_named_list':('從孫',-2,'paternal')}[rule]
   extra={'kinship_basis':'bound_collateral_generation_term','source_term':term,'lineage':lineage,'generation_difference':gen,'collateral':True,'exact_distance':None,'common_ancestor_person_id':None,'connecting_person_ids':None}
  elif pred=='brother':extra={'source_term':('兄'if (rule=='four_named_siblings_execution'and hits[0][1]=='head')or rule=='collateral_head_named_father_brother'else'弟'),'relative_age':'younger','relative_birth_order':{'older_person_id':o['person_id'],'younger_person_id':s['person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}}
  elif pred=='maternal_uncle':extra={'source_term':'舅','lineage':'maternal','generation_difference':-1}
  elif pred=='grandfather'and rule=='two_granddaughters_marital_context':extra={'source_term':'孫女','generation_difference':-2,'lineage':'paternal','connecting_person_ids':None}
  elif pred=='adoptive_father':extra={'source_term':'爲'+o['surface']+'子','adoption_basis':'named_external_grandson_posthumous_heir','modern_legal_status':'not_inferred','actual_upbringing':'not_inferred','biological_parentage':'retained_separately'}
  elif pred=='ritual_successor_of':extra={'source_term':(('後'+o['surface'])if rule=='heir_offer_then_named_son'else('奉'+o['surface']+'後')),'succession_kind':'ritual_heir_designation','biological_parentage':'not_inferred'}
  elif pred=='grandmother':extra={'source_term':'外孫','generation_difference':-2,'lineage':'maternal','mother_person_id':None}
  elif rule=='wife_children'and pred=='father'and hits[0][1]in('daughter1','daughter2'):extra={'source_term':'前妻…生二女','interpretation_basis':'marital_biographical_birth_context','explicit_biological_paternity':False}
  if rule=='collateral_fiefs_named_list'and hits[0][1]=='junior2':extra['interpretation_basis']='coordinated_collateral_grandsons'
  if rule=='four_named_siblings_execution'and hits[0][1]=='younger3':extra['interpretation_basis']='coordinated_younger_brother_list'
  if rule=='named_parentage_head'and hits[0][1]=='mother':extra.update(source_term='少女',birth_order={'parent_person_id':o['person_id'],'scope':'daughters_of_parent','ordinal':None,'position':'younger_or_youngest','interpretation_status':'ambiguous'})
  if pred=='maternal_role':extra.update(source_term='母',role='mother_unspecified',biological_mother=None,father_person_id=None)
  if pred=='mother':
   basis={'wife_children':'explicit_birth_verb','named_parentage_head':'named_parents_and_marriage_in_same_biography','four_named_siblings_execution':'same_source_named_parents_and_marriage','named_mother_daughter_princess':'explicit_daughter_designation','queen_mother_title':'same_source_explicit_daughter_designation'}[rule]
   extra['birth_mother_interpretation']={'status':'source_attested'if basis=='explicit_birth_verb'else'contextual_provisional','basis':basis,'explicit_birth_verb':basis=='explicit_birth_verb'}
  assert q=={'received_family_frame':b,**extra}
  return True
 except (AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration):return False
