"""Finite selected-WYD063 readings. No years, names, or kinship are inferred at runtime."""
from pathlib import Path
import copy,json,hashlib,importlib.util
CID='c-songshu-063-wyd1739-wangtanshou'
PATH='corpus/songshu/063-wyd1739-wangtanshou.json'
BASE='corpus/songshu/063-wyd1739-wangtanshou-'
KEY='fixed_wyd063_basic_facts'
LAYER={'kind':'complete_selected_wyd063_first_family_life','human_reviewed':False,'model':None}
ROW='source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json'
ROW_SHA='fc8a17ad4e6050f84622b4dd3360c3e37eecfc4fdac0be4608d9281dc121847c'
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True)==json.dumps(b,ensure_ascii=False,sort_keys=True)
def module(root,name):
 s=importlib.util.spec_from_file_location('basic063_'+name,Path(root)/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def build(ch,root):
 if not isinstance(ch,dict)or ch.get('id')!=CID:raise ValueError('063 basic source')
 rolemod=module(root,'wyd_song063_roles');c=rolemod.load_contract(root);roles=rolemod.resolve_roles(ch,root,c)
 ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};spec={p['id']:p for p in c['paragraphs']}
 def mark(p,role,surface=None):
  candidates=[s for s in spec[p['id']]['mentions']if s.get('role_key')==role and(surface is None or s['surface']==surface)]
  if not candidates:raise ValueError('063 required source role')
  return next(m for m in p['mentions']if m['id']==candidates[0]['id'])
 def anchor(p,term):
  if p['text'].count(term)!=1:raise ValueError('063 exact source phrase')
  i=p['text'].index(term);return dict(paragraph_id=p['id'],start=i,end=i+len(term),surface=term)
 def ev(p,**extra):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],**extra)
 def relation(key,subject,predicate,obj,term,pkey,extra=None):
  p=ps[pkey];s=mark(p,subject);q={'source_term':term};q.update(extra or{})
  evidence=[]
  if obj=='tanshou'and pkey=='p006':
   prior=ps['p005'];o=mark(prior,obj);evidence=[ev(prior,object_person_mention_id=o['id']),ev(p,subject_person_mention_id=s['id'])]
  else:o=mark(p,obj);evidence=[ev(p,subject_person_mention_id=s['id'],object_person_mention_id=o['id'],relationship_anchor=anchor(p,term))]
  a=dict(id='a-song063-wyd-'+key,subject_person_id=roles[subject],predicate=predicate,object_person_id=roles[obj],status='source_attested',qualifiers=q,evidence=evidence,reviewer='Codex（AI代理）',human_reviewed=False,model=None)
  if len(evidence)==2:a['context']={'kind':'adjacent_paragraphs','paragraph_ids':[ps['p005']['id'],p['id']],'rationale':'本傳死亡/追贈與篇末明子句連續，前段曇首主體、後段子名；不指最後出現的世祖。'}
  return a
 kin=[relation('hong-younger','tanshou','brother','hong','弘少弟','p001',{'relative_birth_order':{'older_person_id':roles['hong'],'younger_person_id':roles['tanshou'],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}}),
      relation('qiu-congdi','qiu','agnatic_cousin','tanshou','從弟球','p001',{'kinship_structure':{'lineage':'paternal','generation_difference':0,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'younger'},'relative_birth_order':{'older_person_id':roles['tanshou'],'younger_person_id':roles['qiu'],'operator':'lt','scope':'agnatic_cousins','older_ordinal':None,'younger_ordinal':None}}),
      relation('sengchuo-father','sengchuo','father','tanshou','子僧綽','p006',{'lineage':'paternal'}),
      relation('sengqian-father','sengqian','father','tanshou','少子僧虔','p006',{'lineage':'paternal','birth_order':{'parent_person_id':roles['tanshou'],'scope':'sons_of_parent','ordinal':None,'position':'younger_or_youngest','interpretation_status':'ambiguous'}})]
 names=[]
 for role,surname,ming,pkey,surface in [('tanshou','王','曇首','p001','王曇首'),('hong',None,'弘','p001','弘'),('qiu',None,'球','p001','球'),('sengchuo',None,'僧綽','p006','僧綽'),('sengqian',None,'僧虔','p006','僧虔')]:
  p=ps[pkey];m=mark(p,role,surface);names.append(dict(id='n-song063-wyd-'+role+'-literal',person_id=roles[role],surname=surname,ming=ming,additional_names=[],chapter_id=CID,paragraph_id=p['id'],person_mention_id=m['id'],quote=p['text'],status='source_attested',human_reviewed=False,model=None))
 for role,aid in [('hong','hong-younger'),('qiu','qiu-congdi'),('sengchuo','sengchuo-father'),('sengqian','sengqian-father')]:
  literal=next(n for n in names if n['id']=='n-song063-wyd-'+role+'-literal');n=copy.deepcopy(literal);n.update(id='n-song063-wyd-'+role+'-contextual',surname='王',status='contextual_provisional')
  n['surname_basis']={'kind':'contextual_surname_from_wyd063_fixed_near_kin','source_name_record_id':'n-song063-wyd-tanshou-literal','relationship_assertion_ids':['a-song063-wyd-'+aid],'status':'contextual_provisional','human_reviewed':False,'rationale':'本傳王曇首明全名及所列明父/少弟/父系從弟的來源語境；原單名literal不改，不用家族ID、編輯父鏈或label補姓。'};names.append(n)
 p=ps['p001'];m=mark(p,'tanshou','王曇首');origin=dict(id='ad-song063-wyd-tanshou-origin',person_id=roles['tanshou'],relation='biographical_origin',source_term='琅邪臨沂人',place={'source_name':'琅邪臨沂','modern_place_id':None},date_expression=None,status='source_attested',evidence=[ev(p,person_mention_id=m['id'],place_anchor=anchor(p,'琅邪臨沂'))],interpretation_note='本傳籍貫，不作出生、居住、死亡或葬地。',human_reviewed=False,model=None)
 p=ps['p005'];m=mark(p,'tanshou');rowraw=(Path(root)/ROW).read_bytes()
 if sha(rowraw)!=ROW_SHA:raise ValueError('063 calendar row SHA')
 row=json.loads(rowraw)
 if row['columns']!={'dynasty':'宋','era_name':'元嘉','first_year':'424','last_year':'453'}:raise ValueError('063 calendar dynasty/era')
 event=dict(id='le-song063-wyd-tanshou-death',person_id=roles['tanshou'],event_type='death',source_term='卒',date_expression='七年',status='source_attested',reviewer='Codex（AI代理）',evidence=[ev(p,person_mention_id=m['id'])],human_reviewed=False,model=None,interpretation_note='本傳曇首七年卒；無報齡，不倒算生年，不以死亡關閉所有任職。')
 ref={'title':'教育部中國歷代年號表宋元嘉欄','url':row['url'],'scope':'modern_era_year_equivalence_only','quote':'元嘉','columns':row['columns'],'fixed_row_reference':{'path':ROW,'sha256':ROW_SHA},'image_verified':False}
 date=dict(era='CE',year=430,era_year=430,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression='七年',original_quote=p['text'],status='editorial_provisional',evidence=[ev(ps[k],person_mention_id=mark(ps[k],'tanshou')['id'])for k in ['p003','p004','p005']],references=[ref],rationale='宋元嘉424起，七年為430；p003元嘉四年主敘接七年。p004元嘉二年位於曇首啟語回述前事，不改成主敘年、不借予其他人物。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
 date['event_evidence_binding']={'kind':'fixed_wyd063_death_local_year','event_id':event['id'],'person_id':event['person_id'],'subject_mention_id':m['id'],'era_anchor':anchor(ps['p003'],'元嘉四年'),'quoted_retrospection_anchor':anchor(ps['p004'],'元嘉二年雖有再開門例此乃前事之違'),'event_anchor':anchor(p,'七年卒'),'calendar_row':{'path':ROW,'sha256':ROW_SHA},'human_reviewed':False}
 date['regnal_year_mapping']={'kind':'relative_ce_regnal_era_span','era_name':'元嘉','source_number':'七','start_ce_year':424,'end_ce_year':453,'regnal_year':7,'year_offset':0,'target_regnal_year':7,'reference_index':0}
 date['relative_year_reference']={'kind':'omitted_era_regnal_year','source_term':'七年','era_evidence_index':0,'antecedent_evidence_index':2,'event_evidence_index':2,'era_expression':'元嘉四年','antecedent_expression':'七年'};event['normalized_date']=date
 p=ps['p001'];m=mark(p,'hong','弘');a=anchor(p,'太保');unknown={'status':'unknown','date_expression':None,'evidence':[]}
 h={'id':'th-song063-wyd-hong-taibao-use','person_id':roles['hong'],'title':'太保','kind':'office','mode':'attestation','appointment_role':'source_attested_use','status':'source_attested','evidence':[ev(p,person_mention_id=m['id'])],'attestations':[dict(id='att-song063-wyd-hong-taibao',usage='narrative',date_expression=None,paragraph_id=p['id'],person_mention_id=m['id'],start=a['start'],end=a['end'],surface=a['surface'])],'effective_period':{'start':copy.deepcopy(unknown),'end':copy.deepcopy(unknown)},'source_career_role':{'kind':'fixed_wyd063_related_title_attestation','source_revision':ch['source']['revision_id'],'raw_sha256':ch['source']['raw_sha256'],'paragraph_sha256':sha(p['text'].encode()),'scope_anchor':anchor(p,'王曇首琅邪臨沂人太保弘少弟也'),'person_mention_id':m['id'],'title_anchor':a,'role_contract_ref':'source-evidence/song063-wyd1739-wangtanshou/ner-role-contract.json'},'interpretation_note':'傳首太保弘為來源用稱；不從此處補授官/追贈時點或任終，不以最高官自動選頭。','human_reviewed':False,'model':None}
 pref={'id':'ptp-song063-wyd-hong-taibao','person_id':roles['hong'],'selection_kind':'default_profile_title','holding_id':h['id'],'attestation_id':h['attestations'][0]['id'],'source_ref':dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],person_mention_id=m['id'],start=a['start'],end=a['end'],surface=a['surface']),'scope':'timeless_profile_heading','temporal_claim':'none','status':'editorial_provisional','rationale':'本次武英殿宋063傳首明稱太保弘；編輯選太保作人物頭，非最高官推選、不表任何敘事時點必有效。舊車騎將軍name.title保持原值，不與車騎大將軍自動等同。','human_reviewed':False}
 return {'assertions':kin,'name_components':names,'addresses':[origin],'life_events':[event],'title_holdings':[h],'profile_title_preferences':[pref]}
def payloads(ch,root):
 data=build(ch,root);out={}
 for suffix,kind,key in [('assertions','person_assertion_set','assertions'),('name-components','person_name_component_set','records'),('addresses','person_address_assertion_set','assertions'),('life-events','person_life_event_assertion_set','events'),('titles','title_holding_assertion_set','holdings')]:
  source={'assertions':'assertions','name-components':'name_components','addresses':'addresses','life-events':'life_events','titles':'title_holdings'}[suffix]
  out[BASE+suffix+'.json']={'format_version':'0.2','record_type':kind,'chapter_id':CID,key:data[source]}
 out[BASE+'profile-title.json']={'format_version':'0.1','record_type':'profile_title_preference_set','decisions':data['profile_title_preferences']}
 return out
def strip_and_validate(ch,root):
 if not isinstance(ch,dict)or ch.get('annotation',{}).get(KEY)!=LAYER:raise ValueError('063 basic layer qualification')
 for path,expected in payloads(ch,root).items():
  if not same(json.loads((Path(root)/path).read_bytes()),expected):raise ValueError('063 basic record/source role changed')
 out=copy.deepcopy(ch);out['annotation'].pop(KEY);return out
def witness_valid(ch,root):
 rolemod=module(root,'wyd_song063_roles');projected=rolemod.source_only_projection(ch,root)
 module(root,'fixed_wuyingdian_song063_wangtanshou').validate_source(projected,root)
def date_valid(date,event,chapters,root=None):
 if not isinstance(date,dict)or not isinstance(event,dict)or not isinstance(chapters,dict)or root is None:return False
 try:
  ch=json.loads((Path(root)/PATH).read_bytes());witness_valid(ch,root);expected=build(ch,root)['life_events'][0]
  try:
   from scripts.relative_regnal_year import relative_regnal_year_valid
   from scripts.validate_corpus import source_age_number
  except ImportError:
   from relative_regnal_year import relative_regnal_year_valid
   from validate_corpus import source_age_number
  return chapters.get(CID)==ch and same(event,expected)and same(date,expected['normalized_date'])and relative_regnal_year_valid(date,source_age_number,chapters)
 except(KeyError,TypeError,ValueError,OSError,AssertionError,StopIteration,AttributeError):return False
def validate_surname(n,names,chapters,assertions,root):
 try:
  ch=chapters[CID];witness_valid(ch,root);data=build(ch,root);expected=[x for x in data['name_components']if x['id']==n.get('id')]
  assert len(expected)==1 and n==expected[0]and n.get('surname_basis')
  seed=[x for x in names if x.get('id')=='n-song063-wyd-tanshou-literal'];assert seed==[data['name_components'][0]]
  for aid in n['surname_basis']['relationship_assertion_ids']:
   actual=[a for a in assertions if a.get('id')==aid];wanted=[a for a in data['assertions']if a['id']==aid];assert actual==wanted and len(wanted)==1
 except(KeyError,TypeError,ValueError,OSError,AssertionError,StopIteration,AttributeError):raise ValueError('宋063姓氏須有本傳全名、固定來源近親與完整具名端點')

def holding_valid(h,ch,root=None):
 if not isinstance(h,dict)or not isinstance(ch,dict)or root is None:return False
 try:
  current=json.loads((Path(root)/PATH).read_bytes());witness_valid(current,root)
  return ch==current and same(h,build(current,root)['title_holdings'][0])
 except(KeyError,TypeError,ValueError,OSError,AssertionError,StopIteration,AttributeError):return False
