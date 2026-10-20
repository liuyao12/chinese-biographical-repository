"""Explicit reading/archival partition; never infer similarity or remove anchors."""
import json,hashlib
from pathlib import Path

def partition(chapter):
    paragraphs=chapter['paragraphs'];by={p['id']:p for p in paragraphs};layout=chapter.get('reading_layout')
    if layout is None:return [(p,None,None)for p in paragraphs]
    def need(x,msg):
        if not x:raise ValueError('閱讀版面：'+msg)
    need(type(layout.get('version'))is int and layout.get('version')==1 and layout.get('human_reviewed') is False,'格式無效')
    primary=layout['primary_paragraph_ids'];archives=layout['archival_excerpts'];archids=[a['paragraph_id']for a in archives];ids=primary+archids
    need(len(by)==len(paragraphs) and len(ids)==len(set(ids)) and set(ids)==set(by),'主文／封存須完整不重複分割全部段落')
    for a in archives:need(a.get('default_collapsed') is True and a.get('reason')=='same_fixed_witness_expanded_reading_unit' and bool(a.get('label')),'封存角色或說明無效')
    return [(by[p],'primary',i+1)for i,p in enumerate(primary)]+[(by[a['paragraph_id']],'archival-excerpt',i+1)for i,a in enumerate(archives)]

def _body_positions(chapter,p,lines):
    e=next(e for e in chapter['source']['normalization']['excerpts']if e['proposed_paragraph_id']==p['id']);first,last=e['source_lines'];raw='\n'.join(lines[first-1:last]);q=e['raw_quote']
    if q not in (raw,raw+'\n')or hashlib.sha256(q.encode()).hexdigest()!=e['raw_quote_sha256']:raise ValueError('閱讀版面：節引原行／SHA不符')
    positions=[];chars=[];depth=0
    for n in range(first,last+1):
        i=0;line=lines[n-1]
        while i<len(line):
            if line.startswith('<pb:',i):i=line.index('>',i)+1;continue
            c=line[i]
            if c=='(':depth+=1
            elif c==')':depth-=1
            elif depth==0 and c not in '¶\r\n':chars.append(c);positions.append((n,i))
            if depth<0:raise ValueError('閱讀版面：括注不平衡')
            i+=1
    if depth or ''.join(chars)!=p['text']:raise ValueError('閱讀版面：節引正文投影不符')
    return positions

def _fragments(p,lines,literal):
    chars=[];positions=[]
    for f in p['witness_fragments']:
        n,a,b=f['line'],f['raw_line_start'],f['raw_line_end'];raw=lines[n-1][a:b]
        if type(n)is not int or not 1<=n<=len(lines)or type(a)is not int or type(b)is not int or not 0<=a<b<=len(lines[n-1])or raw!=f['raw_fragment']:raise ValueError('閱讀版面：原行片段不符')
        if literal and raw!=f['text']:raise ValueError('閱讀版面：封存映射只允許literal正文')
        chars.append(f['text']);positions.extend((n,i)for i in range(a,b))
    if ''.join(chars)!=p['text']:raise ValueError('閱讀版面：原段正文不符')
    return positions

def validate_chapter(chapter,root):
    rows=partition(chapter);layout=chapter.get('reading_layout')
    if layout is None:return
    root=Path(root).resolve();source=layout['source'];path=Path(source['raw_path']);conpath=Path(layout['concordance_path'])
    if path.is_absolute()or path.parts[:2]!=('sources','witnesses')or'..'in path.parts or conpath.is_absolute()or conpath.parts[:1]!=('corpus',)or'..'in conpath.parts:raise ValueError('閱讀版面：不可攜來源路徑')
    rawpath=(root/path).resolve()
    if not rawpath.is_relative_to(root):raise ValueError('閱讀版面：raw越界')
    raw=rawpath.read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();s=chapter['source']
    if source['source_id']!=chapter['source_id']or source['revision_id']!=s['revision_id']or source['raw_file_sha256']!=s['response_sha256']or source['source_blob_sha']!=s['source_blob_sha']or source['url']!=s['permalink']or hashlib.sha256(raw).hexdigest()!=source['raw_file_sha256']or blob!=source['source_blob_sha']:raise ValueError('閱讀版面：跨source／revision或raw不符')
    confile=(root/conpath).resolve()
    if not confile.is_relative_to(root):raise ValueError('閱讀版面：concordance越界')
    concordance=json.loads(confile.read_text())
    if concordance.get('record_type')!='source_occurrence_concordance_set'or concordance['source']!=source:raise ValueError('閱讀版面：固定見證對應不符')
    try:from .occurrence_concordance import occurrence_catalog
    except ImportError:from occurrence_concordance import occurrence_catalog
    occurrence_catalog(root,[chapter,concordance])
    lines=raw.decode().splitlines();by={p['id']:p for p in chapter['paragraphs']};primary=set(layout['primary_paragraph_ids']);order=[]
    for p,role,_ in rows:
        if role=='primary':
            pts=_fragments(p,lines,False)if p.get('witness_fragments')else _body_positions(chapter,p,lines);order.append(pts[0])
    if order!=sorted(order)or len(order)!=len(set(order)):raise ValueError('閱讀版面：主文不是fixedraw順序')
    for a in layout['archival_excerpts']:
        p=by[a['paragraph_id']];oldpos=_body_positions(chapter,p,lines);cursor=0;targets=set()
        for seg in a['canonical_segments']:
            start,end,cs,ce=seg['excerpt_start'],seg['excerpt_end'],seg['canonical_start'],seg['canonical_end'];target=by[seg['canonical_paragraph_id']]
            if any(type(x)is not int for x in (start,end,cs,ce))or start!=cursor or not start<end<=len(p['text'])or target['id']not in primary or not 0<=cs<ce<=len(target['text']):raise ValueError('閱讀版面：封存映射須完整逐字覆蓋')
            if p['text'][start:end]!=seg['quote']or target['text'][cs:ce]!=seg['quote']or oldpos[start:end]!=_fragments(target,lines,True)[cs:ce]:raise ValueError('閱讀版面：不同字／raw位置不得封存')
            cursor=end;targets.add(target['id'])
        if cursor!=len(p['text']):raise ValueError('閱讀版面：封存未完整覆蓋')
        links=[r for r in concordance['records']if r['duplicate']['paragraph_id']==p['id']]
        if {r['duplicate_mention_id']for r in links}!={m['id']for m in p['mentions']}or any(r['canonical']['paragraph_id']not in targets for r in links):raise ValueError('閱讀版面：舊錨點缺對應')

def validate(root):
    try:
        for f in(Path(root)/'corpus').glob('*/*.json'):
            c=json.loads(f.read_text())
            if c.get('record_type')=='marked_chapter'and'reading_layout'in c:validate_chapter(c,root)
        return []
    except(KeyError,ValueError,TypeError,OSError,IndexError,StopIteration,AttributeError)as exc:return ['閱讀版面無效：'+str(exc)]
