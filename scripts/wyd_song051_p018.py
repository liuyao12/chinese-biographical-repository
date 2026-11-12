"""Finite p018 plus p019 Liu Yiqi biography-tail annotation and source checks."""
from pathlib import Path
import hashlib, json
CID='c-songshu-051-wyd1739-zongshi'
CONTRACT='source-evidence/song051-wyd1739-zongshi/p018-p019-family-batch.json'
COMPARISON='source-evidence/song051-wyd1739-zongshi/p018-p019-textual-comparisons.json'
CONTRACT_SHA='524fc02d185f4560059b9400c19ed2301aa6f08dd9b79e7814984de36573c254'
COMPARISON_SHA='b0c4fd4f71f522045e5e0d5e09deb899688c74512dd38a6a8325f8071c4829e4'

def load(root,rel):return json.loads((Path(root)/rel).read_text(encoding='utf-8'))
def markers(root):
 p=Path(root)/CONTRACT;raw=p.read_bytes()
 if CONTRACT_SHA and hashlib.sha256(raw).hexdigest()!=CONTRACT_SHA:raise ValueError('宋051 p018/p019批次契約SHA漂移')
 return load(root,CONTRACT)['markers']
def title_uses(ch):
 p18=next(p for p in ch['paragraphs']if p['id'].endswith(':p018'))
 specs=[('tu-song051-p018-qiwang','m0183','齊王','47p_kjh_ez7','specific_reign_title'),('tu-song051-p018-xiaowu','m0185','孝武','hx8_st4_jdd','posthumous_imperial_title'),('tu-song051-p018-shixingwangjun','m0190','始興王濬','3b1_39e_aa6','named_royal_title_with_personal_name')]
 out=[]
 for ident,short,surface,pid,basis in specs:
  mid=f'{p18["id"]}:{short}';m=next(m for m in p18['mentions']if m['id']==mid)
  out.append({'id':ident,'person_id':pid,'person_mention_id':mid,'source_term':surface,'source_anchor':{'paragraph_id':p18['id'],'start':m['start'],'end':m['end'],'surface':surface},'usage_kind':'title_reference','holding_ids':[],'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p18['id'],'quote':p18['text'],'person_mention_id':mid}],'source_use_binding':{'kind':'fixed_wyd_song051_p018_p019_title_reference','basis':basis,'interpretation_note':('保留原稱及具體指涉；不將稱號列作姓名別名。' if surface=='齊王' else '此為劉遐的陳述，辨識稱號所指不等於確認其指控為事實。' if surface=='孝武' else '「始興王」為稱號，「濬」為人名；此複合提及不列作姓名別名。')},'human_reviewed':False})
 p19=next(p for p in ch['paragraphs']if p['id'].endswith(':p019'))
 # `臨川烈武王` is the title context immediately preceding the linked name mention.
 dm=next(m for m in p19['mentions']if m['id'].endswith(':m0068'))
 for ident,term,pid,short,start,end,basis,note in [
  ('tu-song051-p019-linchuan-liewuwang','臨川烈武王','3qs_nqa_ioa_AAC','m0068',85,90,'named_royal_title_context','篇首稱號修飾緊接的道規；稱號不列作姓名別名。'),
  ('tu-song051-p019-gaozu','高祖','3qs_nqa_ioa_AAA','m0070',95,97,'posthumous_imperial_title','此處指本傳所稱高祖劉裕；保留稱謂，不列作姓名別名。'),
  ('tu-song051-p019-gaozu-remark','高祖','3qs_nqa_ioa_AAA','m0071',106,108,'posthumous_imperial_title','「高祖奇之」承本傳指劉裕；保留稱謂，不列作姓名別名。')]:
  mid=f'{p19["id"]}:{short}'
  out.append({'id':ident,'person_id':pid,'person_mention_id':mid,'source_term':term,'source_anchor':{'paragraph_id':p19['id'],'start':start,'end':end,'surface':term},'usage_kind':'title_reference','holding_ids':[],'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p19['id'],'quote':p19['text'],'person_mention_id':mid}],'source_use_binding':{'kind':'fixed_wyd_song051_p018_p019_title_reference','basis':basis,'interpretation_note':note},'human_reviewed':False})
 return out

def title_use_valid(use,ch):
 try:return use in title_uses(ch) and next(x for x in title_uses(ch)if x['id']==use['id'])==use
 except (KeyError,TypeError,StopIteration):return False

def assertion_records(root):
 ch=load(root,'corpus/songshu/051-wyd1739.json');ps={p['id'].rsplit(':',1)[-1]:p for p in ch['paragraphs']}
 specs=[('a-song051-p018-xia-younger-brother-of-bing','3qs_nqa_ioa_AABDD','3qs_nqa_ioa_AABDB','兄秉','p018','m0184','m0182'),('a-song051-p018-yibin-younger-brother-of-yizong','3qs_nqa_ioa_AABE','3qs_nqa_ioa_AABD','義宗弟義賓','p018','m0095','m0092'),('a-song051-p018-yiqi-younger-brother-of-yibin','3qs_nqa_ioa_AABF','3qs_nqa_ioa_AABE','義賓弟義綦','p018','m0181','m0178'),('a-song051-p019-daogui-younger-brother-of-liuyu','3qs_nqa_ioa_AAC','3qs_nqa_ioa_AAA','高祖少弟也','p019','m0068','m0070')]
 out=[]
 for ident,subj,obj,term,pno,sm,om in specs:
  p=ps[pno];q={'source_term':term,'source_clause_binding':{'kind':'fixed_wyd_song051_p018_p019_direct_family','case':ident,'raw_sha256':ch['source']['raw_sha256']},'lineage':'paternal','shared_father':None,'subject_relative_age':'younger','interpretation_note':'原文所載的同輩親稱按父系家族關係保留；不推同母、絕對排行或未載世數。'}
  out.append({'id':ident,'subject_person_id':subj,'predicate':'brother','object_person_id':obj,'status':'source_attested','qualifiers':q,'human_reviewed':False,'model':None,'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'subject_person_mention_id':p['id']+':'+sm,'object_person_mention_id':p['id']+':'+om}]})
 return out

def name_components(root):
 ch=load(root,'corpus/songshu/051-wyd1739.json');p=next(p for p in ch['paragraphs']if p['id'].endswith(':p019'))
 return {'format_version':'0.2','record_type':'person_name_component_set','chapter_id':CID,'records':[{'id':'name-song051-p019-daogui-zi','person_id':'3qs_nqa_ioa_AAC','surname':None,'ming':'道規','zi':'道則','additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':p['id']+':m0068','quote':p['text'],'source_term':'字道則','status':'source_attested','human_reviewed':False,'model':None,'interpretation_note':'本傳明言「道規字道則」；名與字屬同一人物，分欄記錄，不把字列作本名。','source_zi_binding':{'kind':'explicit_zi_yue_form','paragraph_id':p['id'],'start':92,'end':95,'surface':'字道則','human_reviewed':False}}]}

def name_component_valid(record,root):
 try:return record in name_components(root)['records'] and load(root,'corpus/songshu/051-wyd1739-p018-p019-name-components.json')==name_components(root)
 except (KeyError,TypeError,ValueError,OSError,StopIteration):return False

def assertion_valid(a,chapters,root):
 try:
  expected={x['id']:x for x in assertion_records(root)}[a['id']]
  ch=chapters[CID]
  return a==expected and ch['id']==CID
 except (KeyError,TypeError,ValueError,StopIteration):return False

def validate_comparison(root):
 raw=(Path(root)/COMPARISON).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=COMPARISON_SHA:return False
 d=json.loads(raw);ch=load(root,'corpus/songshu/051-wyd1739.json');p=next(x for x in ch['paragraphs']if x['id'].endswith(':p019'))
 expected='孝建三年卒贈平南將軍諡曰僖侯子長歆嗣官至步兵校尉昇平三年卒齊受禪國除'
 return d['base_witness']['quote']==expected and d['base_witness']['paragraph_id']==p['id'] and d.get('editorial_assessment',{}).get('status')=='unresolved' and not d.get('human_reviewed',True)
