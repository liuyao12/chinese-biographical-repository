"""《宋書》卷九十三王弘之既發四段的逐項校讀。"""
from pathlib import Path
import hashlib
import json
import re

CID='c-songshu-093-recluses'
HONG='7r6_k52_qji_ABDACAB'
RAW='source-evidence/nan023-wanghuan/ws1962755.wikitext'
SOURCE_HASH='006115bbb0fa72042b9926f19b6ffbc952b7955b7f3a9fdf9c6fb3be71cb98aa'
F='source-evidence/song093-wanghongzhi/frames.json'
FH='f14bd2e038acc09601082bd90c318c4d1c7f2ab36c75aa8fa0fba49c75b97916'


def sha(value):return hashlib.sha256(value.encode()).hexdigest()

def array_hash(rows):return sha(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')

def source(root,name,digest):
    r=Path(root).resolve();p=r/name
    if p!=p.resolve() or not p.is_relative_to(r):raise ValueError('非本庫來源')
    s=p.read_text()
    if sha(s)!=digest:raise ValueError('來源雜湊')
    return s

def frame(root):return json.loads(source(root,F,FH))

def projected(line):
    line=re.sub(r'<ref>[^<>]*</ref>','',line)
    return re.sub(r'-\{([^{}|:;<>\s])\}-',r'\1',line).lstrip('　')

def errors(ch,root):
    if ch.get('id')!=CID:return []
    try:
        proof=frame(root);raw=source(root,RAW,SOURCE_HASH).splitlines()
        if ch['source_id']!='s-songshu-093-recluses' or ch['source']['revision_id']!=1962755 or ch['source']['wikitext_sha256']!=SOURCE_HASH:raise ValueError('底本')
        ids=proof['unit_ids'];ps={p['id']:p for p in ch['paragraphs']}
        for record in proof['paragraphs']:
            p=ps[record['id']];line=p['source_position']['first_line'];original=raw[line-1]
            if (record['source_position']!=p['source_position'] or sha(original)!=record['raw_sha256'] or projected(original)!=p['text']
                    or p['annotation_status']!='reviewed' or sha(p['text'])!=record['text_sha256'] or array_hash(p['mentions'])!=record['mentions_sha256']):raise ValueError('弘之原段')
        an=ch['annotation']
        if [r for r in an['narrative_readings'] if r['source_anchor']['paragraph_id'] in ids]!=proof['readings']:raise ValueError('事跡')
        if [r for r in an['person_reference_occurrences'] if r['paragraph_id'] in ids]!=proof['references']:raise ValueError('稱謂')
        if [r for r in an['title_proposals'] if r['person_id']==HONG]!=proof['proposals']:raise ValueError('不就原官')
        return []
    except (KeyError,ValueError,TypeError,IndexError,OSError):return ['宋書王弘之固定原字、段落、稱謂或官事有誤']

def kin_valid(row,ch,root):
    return ch.get('id')==CID and not errors(ch,root) and row in frame(root)['kin']

def side_errors(data,ch,root,field):
    if ch.get('id')!=CID:return []
    try:
        proof=frame(root)
        records={'assertions':proof['kin'],'holdings':proof['offices'],'events':[proof['event']]}[field]
        ids={r['id'] for r in records}
        if [r for r in data[field] if r['id'] in ids]!=records:raise ValueError('源事')
        return []
    except (KeyError,ValueError,TypeError,OSError):return ['宋書王弘之的關係、官事或卒條偏離原證']

def date_valid(date,event,chapters,parse_number,root):
    try:
        try:from scripts.relative_regnal_year import relative_regnal_year_valid
        except ImportError:from relative_regnal_year import relative_regnal_year_valid
        ch=chapters[CID]
        if event!=frame(root)['event'] or date!=event['normalized_date'] or errors(ch,root):return False
        if not relative_regnal_year_valid(date,parse_number,chapters):return False
        ps={p['source_position']['first_line']:p for p in ch['paragraphs']}
        if not ps[66]['text'].startswith('弘之四年卒，時年六十三。'):return False
        if '元嘉四年，徴爲通直散騎常侍，又不就。' not in ps[62]['text'] or ps[64]['text'].count('靈運與廬陵王義眞牋曰')!=1:return False
        return [e['paragraph_id'] for e in date['evidence']]==[ps[i]['id']for i in (62,64,66)] and date['year']==427
    except (KeyError,ValueError,TypeError,OSError):return False
