# coding: utf-8
"""Finite titles and life records for Songshu 51 p018/p019 Yibin and Yiqi."""
from pathlib import Path
import copy,hashlib,json
CID='c-songshu-051-wyd1739-zongshi';CH='corpus/songshu/051-wyd1739.json';CAL='source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json';KIND='fixed_wyd_song051_p018_p019_title';DATE_KIND='fixed_wyd_song051_p018_p019_life_date';TITLE_DATE_KIND='fixed_wyd_song051_p018_p019_title_date';UNKNOWN={'status':'unknown','date_expression':None,'evidence':[]}
def read(root,path):return json.loads((Path(root)/path).read_text(encoding='utf-8'))
def source(root):return read(root,CH)
def evidence(ch,p,mid):return {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':mid}
def anchor(p,surface,occ=0):
 pos=[i for i in range(len(p['text']))if p['text'].startswith(surface,i)];i=pos[occ];return {'paragraph_id':p['id'],'start':i,'end':i+len(surface),'surface':surface}
def norm(root,p,mid,era,regnal,year,expr,mapping_kind=TITLE_DATE_KIND):
 row=read(root,CAL);ref={'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':row['url'],'quote':'元嘉','scope':'modern_era_year_equivalence_only','columns':copy.deepcopy(row['columns']),'fixed_row_reference':{'path':CAL,'sha256':hashlib.sha256((Path(root)/CAL).read_bytes()).hexdigest()},'image_verified':False}
 ev=[evidence(source(root),p,mid)]
 return {'era':'CE','era_year':year,'year':year,'year_numbering':'astronomical','precision':'year','calendar':'chinese_civil','source_expression':expr,'original_quote':p['text'],'evidence':ev,'references':[ref],'regnal_year_mapping':{'kind':mapping_kind,'era_name':era,'year':regnal,'source_expression':expr,'status':'editorial_provisional'},'status':'editorial_provisional','rationale':f'本傳沿用元嘉年號語境；元嘉元年424年，{expr}換算為{year}年。僅記年，不推月日。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
def titles(root):
 ch=source(root);p18=next(p for p in ch['paragraphs']if p['id'].endswith(':p018'));p19=next(p for p in ch['paragraphs']if p['id'].endswith(':p019'))
 specs=[
 ('th-song051-p018-yibin-xinye','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','新野縣侯','noble_rank','grant','元嘉二年封新野縣侯','元嘉二年','元嘉','二',425),
 ('th-song051-p018-yibin-xingan','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','興安縣侯','noble_rank','grant','改封興安縣侯','元嘉六年','元嘉','六',429),
 ('th-song051-p018-yiqi-yingdao','3qs_nqa_ioa_AABF',p18,'c-songshu-051-wyd1739-zongshi:p018:m0181','營道縣侯','noble_rank','grant','元嘉六年封營道縣侯','元嘉六年','元嘉','六',429),
 ('th-song051-p018-yibin-huangmen','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','黃門郎','office','attestation','黃門郎祕書監左衞將軍','',None,None,None),
 ('th-song051-p018-yibin-mishu','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','祕書監','office','attestation','黃門郎祕書監左衞將軍','',None,None,None),
 ('th-song051-p018-yibin-zuowei','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','左衞將軍','office','attestation','黃門郎祕書監左衞將軍','',None,None,None),
 ('th-song051-p018-yibin-fuguo','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','輔國將軍','office','attestation','位至輔國將軍徐州刺史','',None,None,None),
 ('th-song051-p018-yibin-xuzhou','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','徐州刺史','office','attestation','位至輔國將軍徐州刺史','',None,None,None),
 ('th-song051-p019-yiqi-zuowei','3qs_nqa_ioa_AABF',p19,'c-songshu-051-wyd1739-zongshi:p019:m0001','左衞將軍','office','attestation','歷左衞將軍湘州刺史','',None,None,None),
 ('th-song051-p019-yiqi-xiangzhou','3qs_nqa_ioa_AABF',p19,'c-songshu-051-wyd1739-zongshi:p019:m0001','湘州刺史','office','attestation','歷左衞將軍湘州刺史','',None,None,None),
 ('th-song051-p018-zong-hou','3qs_nqa_ioa_AABEA',p18,'c-songshu-051-wyd1739-zongshi:p018:m0156','惠侯','noble_rank','attestation','子惠侯綜嗣','',None,None,None),
 ('th-song051-p018-yibin-houjiangjun-posthumous','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','後將軍','office','posthumous_grant','追贈後將軍','',None,None,None),
 ('th-song051-p018-yibin-suhou-posthumous','3qs_nqa_ioa_AABE',p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','肅侯','honorific','posthumous_naming','諡曰肅侯','',None,None,None),
 ('th-song051-p019-yiqi-pingnan-posthumous','3qs_nqa_ioa_AABF',p19,'c-songshu-051-wyd1739-zongshi:p019:m0001','平南將軍','office','posthumous_grant','贈平南將軍','',None,None,None),
 ('th-song051-p019-yiqi-xihou-posthumous','3qs_nqa_ioa_AABF',p19,'c-songshu-051-wyd1739-zongshi:p019:m0001','僖侯','honorific','posthumous_naming','諡曰僖侯','',None,None,None),
 ]
 out=[]
 for ident,pid,p,mid,title,kind,mode,context,date,era,regnal,yr in specs:
  ev=evidence(ch,p,mid);a=anchor(p,title);ctx=anchor(p,context) if context else a
  if mode=='attestation':start={'status':'unknown','date_expression':None,'evidence':[]}
  elif mode in ('posthumous_grant','posthumous_naming'):start={'status':'source_event','event_type':mode,'date_expression':None,'evidence':[ev]}
  else:start={'status':'source_event','event_type':'grant','date_expression':date,'evidence':[ev],'normalized_date':norm(root,p,mid,era,regnal,yr,date)}
  end=copy.deepcopy(UNKNOWN)
  if ident=='th-song051-p018-yibin-xinye':end={'status':'source_event','event_type':'explicit_end','date_expression':'元嘉六年','evidence':[ev],'normalized_date':norm(root,p,mid,'元嘉','六',429,'元嘉六年')}
  if ident=='th-song051-p018-yibin-xingan':end={'status':'source_event','event_type':'explicit_end','date_expression':'二十五年','evidence':[ev],'normalized_date':norm(root,p,mid,'元嘉','二十五',448,'二十五年')}
  if ident=='th-song051-p018-yiqi-yingdao':
   p19=next(x for x in ch['paragraphs']if x['id'].endswith(':p019'));end={'status':'source_event','event_type':'explicit_end','date_expression':'孝建三年卒','evidence':[evidence(ch,p19,'c-songshu-051-wyd1739-zongshi:p019:m0001')]}
  holding={'id':ident,'person_id':pid,'title':title,'kind':kind,'mode':mode,'status':'source_attested','appointment_role':'source_report','source_career_role':{'kind':KIND,'record_id':ident,'paragraph_id':p['id'],'subject_mention_id':mid,'source_anchor':a,'context_anchor':ctx,'source_revision':ch['source']['revision_id'],'human_reviewed':False},'evidence':[ev],'attestations':[{'id':'att-'+ident,'paragraph_id':p['id'],'start':a['start'],'end':a['end'],'surface':title,'person_mention_id':mid,'usage':'narrative','date_expression':date or None}],'effective_period':{'start':start,'end':end},'interpretation_note':'保存本傳明載的封爵或官職用稱；未載年月的官職不推始終，追贈另行標記；不以卒年補職期。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
  if mode=='posthumous_grant':holding['posthumous_basis']={'source_term':context,'evidence':[ev]}
  if mode=='posthumous_naming':holding['naming_basis']={'source_term':context,'death_term':'二十五年卒' if p is p18 else '孝建三年卒','evidence':[ev]}
  out.append(holding)
 return {'format_version':'0.2','record_type':'title_holding_assertion_set','chapter_id':CID,'holdings':out}
def holding_valid(h,ch,root):
 try:return h in titles(root)['holdings'] and next(x for x in titles(root)['holdings']if x['id']==h['id'])==h and ch['id']==CID
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False
def life_events(root):
 ch=source(root);p18=next(p for p in ch['paragraphs']if p['id'].endswith(':p018'));p19=next(p for p in ch['paragraphs']if p['id'].endswith(':p019'))
 yibin={'id':'le-song051-p018-yibin-death','person_id':'3qs_nqa_ioa_AABE','event_type':'death','status':'source_attested','date_expression':'二十五年','source_term':'二十五年卒','evidence':[evidence(ch,p18,'c-songshu-051-wyd1739-zongshi:p018:m0095')],'interpretation_note':'同一傳記先明載元嘉二年、六年；後文「二十五年卒」依本傳連續紀年解作元嘉二十五年。教育部年號表列元嘉424–453，換算為448年；只記年份，不推月日。','reviewer':'Codex（AI代理）','human_reviewed':False,'normalized_date':norm(root,p18,'c-songshu-051-wyd1739-zongshi:p018:m0095','元嘉','二十五',448,'二十五年',DATE_KIND)}
 yiqi={'id':'le-song051-p019-yiqi-death','person_id':'3qs_nqa_ioa_AABF','event_type':'death','status':'source_attested','date_expression':'孝建三年','source_term':'孝建三年卒','evidence':[evidence(ch,p19,'c-songshu-051-wyd1739-zongshi:p019:m0001')],'interpretation_note':'保留武英殿本轉錄所記孝建三年；識典／ctext比較作孝建二年，故此事件不指派單一西元年，待更強版本校勘。','reviewer':'Codex（AI代理）','human_reviewed':False,'date_dispute':{'comparison_path':'source-evidence/song051-wyd1739-zongshi/p018-p019-textual-comparisons.json','status':'unresolved'}}
 changxin={'id':'le-song051-p019-changxin-death','person_id':'3qs_nqa_ioa_AABFA','event_type':'death','status':'source_attested','date_expression':'昇平三年','source_term':'昇平三年卒','evidence':[evidence(ch,p19,'c-songshu-051-wyd1739-zongshi:p019:m0066')],'interpretation_note':'保留武英殿本轉錄所記昇平三年，不換算西元年。此紀年早於父義綦孝建三年卒的時序，且比較本有昇明二年異文，年代矛盾仍未解。','reviewer':'Codex（AI代理）','human_reviewed':False,'date_dispute':{'comparison_path':'source-evidence/song051-wyd1739-zongshi/p018-p019-textual-comparisons.json','status':'unresolved'}}
 return {'format_version':'0.1','record_type':'person_life_event_assertion_set','chapter_id':CID,'events':[yibin,yiqi,changxin]}
def date_valid(d,event,root):
 try:return d=={x['id']:x for x in life_events(root)['events']}[event['id']]['normalized_date'] and event=={x['id']:x for x in life_events(root)['events']}[event['id']]
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False
def valid_event(e,root):
 try:return e in life_events(root)['events']
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False


def person_events(root):
 ch=source(root);p=next(p for p in ch['paragraphs']if p['id'].endswith(':p018'))
 p19=next(p for p in ch['paragraphs']if p['id'].endswith(':p019'))
 return {'format_version':'0.2','record_type':'person_event_assertion_set','chapter_id':CID,'events':[{'id':'pe-song051-yibin-to-zong-succession','person_id':'3qs_nqa_ioa_AABEA','event_type':'noble_title_succession','status':'source_attested','date_expression':'二十五年','source_term':'子惠侯綜嗣','title':None,'predecessor_person_id':'3qs_nqa_ioa_AABE','evidence':[evidence(ch,p,'c-songshu-051-wyd1739-zongshi:p018:m0156')],'interpretation_note':'原文明載義賓卒後其子綜嗣；所承縣侯名未重述。另將「惠侯」作綜的來源稱號記錄，未由該稱號補造所承縣名。承嗣年份依緊接的二十五年卒上下文記錄為年，不推月日。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},{'id':'pe-song051-zong-to-xian-succession','person_id':'3qs_nqa_ioa_AABEAA','event_type':'noble_title_succession','status':'source_attested','date_expression':None,'source_term':'卒子憲嗣','title':None,'predecessor_person_id':'3qs_nqa_ioa_AABEA','evidence':[evidence(ch,p,'c-songshu-051-wyd1739-zongshi:p018:m0160')],'interpretation_note':'原文次序為「子惠侯綜嗣，卒，子憲嗣」；保留綜至憲的承嗣，不推綜卒年或所承爵名。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},{'id':'pe-song051-yibin-line-title-abolition','person_id':'3qs_nqa_ioa_AABEAA','event_type':'noble_state_abolition','status':'source_attested','date_expression':'昇明二年','source_term':'昇明二年齊受禪國除','title':None,'predecessor_person_id':None,'evidence':[evidence(ch,p,'c-songshu-051-wyd1739-zongshi:p018:m0160')],'interpretation_note':'承憲嗣之後，原文記「昇明二年齊受禪，國除」。保留原紀年與國除敘述，不換算西元年；年號年次與齊受禪時序存在張力，未據此推定憲卒年。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},{'id':'pe-song051-yiqi-to-changxin-succession','person_id':'3qs_nqa_ioa_AABFA','event_type':'noble_title_succession','status':'source_attested','date_expression':'孝建三年','source_term':'子長歆嗣','title':None,'predecessor_person_id':'3qs_nqa_ioa_AABF','evidence':[evidence(ch,p19,'c-songshu-051-wyd1739-zongshi:p019:m0066')],'interpretation_note':'本傳明載義綦卒、子長歆嗣；此句未重述所承爵名，故只記承嗣關係事件，不把營道縣侯直接設為長歆持有爵。承嗣時間隨父卒年異文未決，不換算西元。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None},{'id':'pe-song051-changxin-title-abolition','person_id':'3qs_nqa_ioa_AABFA','event_type':'noble_state_abolition','status':'source_attested','date_expression':'齊受禪','source_term':'齊受禪國除','title':None,'predecessor_person_id':None,'evidence':[evidence(ch,p19,'c-songshu-051-wyd1739-zongshi:p019:m0066')],'interpretation_note':'本傳記長歆卒後接「齊受禪，國除」。保留爵國除的原文後果，不按不相容的昇平三年換算西元，亦不修正文句。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}]}
