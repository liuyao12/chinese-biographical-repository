"""Explicit omitted-prefix era reading, bound to a same-work fixed annal witness."""
import hashlib,re
from pathlib import Path

def valid(date,chapters,root):
 try:
  b=date['era_name_bridge'];m=date['regnal_year_mapping'];keys={'kind','chapter_id','source_id','source_expression_anchor','ruler_person_id','ruler_person_mention_id','omitted_prefix','primary_witness','rationale','human_reviewed'}
  if(set(b)!=keys or b['kind']!='same_work_fixed_annal_omitted_prefix'or b['human_reviewed']is not False or not b['rationale']):return False
  c=chapters[b['chapter_id']];source=c['source'];short=m['source_era_name'];name=m['era_name'];prefix=b['omitted_prefix']
  refs=date.get('references');index=m.get('reference_index')
  if not isinstance(refs,list)or type(index)is not int or not 0<=index<len(refs):return False
  ref=refs[index]
  if not isinstance(ref,dict)or not isinstance(ref.get('columns'),dict):return False
  if(not isinstance(short,str)or len(short)<2 or not isinstance(prefix,str)or not prefix or name!=prefix+short or ref.get('columns',{}).get('dynasty')!='北魏'):return False
  origin=b['source_expression_anchor'];p=next(p for p in c['paragraphs']if p['id']==origin['paragraph_id'])
  def exact(a,text,with_pid=False):
   return set(a)==({'paragraph_id','start','end','surface'}if with_pid else {'start','end','surface'})and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['surface']
  if(b['source_id']!=c['source_id']or not exact(origin,p['text'],True)or origin['surface']!=date['source_expression']or date['original_quote']!=p['text']or not any(e.get('chapter_id')==c['id']and e.get('source_id')==c['source_id']and e.get('paragraph_id')==p['id']and e.get('quote')==p['text']for e in date['evidence'])):return False
  ruler=next(m for p_ in c['paragraphs']for m in p_['mentions']if m['id']==b['ruler_person_mention_id'])
  if(ruler.get('kind')!='person'or ruler.get('person_id')!=b['ruler_person_id']or ruler['surface']not in ('太祖','太宗','世祖','高祖','髙祖','肅宗')):return False
  w=b['primary_witness'];keys={'work_id','source_commit','raw_path','raw_sha256','ruler_identity_anchor','ruler_annal_header_anchor','era_anchor'}
  path=Path(w['raw_path'])
  if(set(w)!=keys or path.is_absolute()or '..'in path.parts or not str(path).startswith('sources/')or w['work_id']!=c['work_id']or w['source_commit']!=source.get('source_commit')):return False
  raw=(Path(root)/path).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=w['raw_sha256']:return False
  text=raw.decode();ident,header,era=[w[k]for k in ('ruler_identity_anchor','ruler_annal_header_anchor','era_anchor')]
  if(not all(exact(a,text)for a in (ident,header,era))or not re.fullmatch(re.escape(ruler['surface'])+r'[^¶\n]{1,8}皇帝諱[^¶\n]{1,4}',ident['surface'])or not re.fullmatch(re.escape(ruler['surface'])+r'紀[上下]?',header['surface'])or not ident['end']<header['end']<era['start']or era['surface']!=name+'元年'or '帝紀'not in text[:ident['start']]):return False
  return True
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False
