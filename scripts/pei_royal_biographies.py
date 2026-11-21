"""核裴后兩傳、庾妃附敘及相關親屬、卒年引句。"""
from pathlib import Path
from hashlib import sha256
import json
import re

CIDS = ('c-nanshi-011-peihuizhao', 'c-nanqishu-020-peihuizhao', 'c-nanshi-042-yuzhang-wangfei', 'c-nanshi-044-mu-empress-children', 'c-nanshi-026-yuanfei-family', 'c-nanqishu-048-yuantuan-ancestry', 'c-songshu-052-yuantan-line', 'c-nanqishu-020-liuzhirong-ancestry', 'c-nanshi-042-zhaohou-children', 'c-nanqishu-040-yuanfei-raised', 'c-nanqishu-002-peihuizhao-death')
UNITS = 'source-evidence/qinan-pei/units.json'
UNITS_SHA = 'e3e93470799d2a6f48ccab7d8cebb840c964e74f1f4e11374515ff6c9e37779a'
FRAMES = 'source-evidence/qinan-pei/kinship-frames.json'
FRAMES_SHA = '57b6881b47ac50c0c0659ded6515435ac545df0fb247f252abdd451a914c758a'
DEATHS = 'source-evidence/qinan-pei/death-frames.json'
DEATHS_SHA = '75ce81d17fa1b429a511a2feb83acbc98ce30393c549ff8711a837fe2d0beed5'

def checked(root,rel,digest):
    root=Path(root).resolve()
    path=root/rel
    if path.resolve()!=path or not path.is_relative_to(root) or sha256(path.read_bytes()).hexdigest()!=digest:
        raise ValueError('固定來源')
    return path.read_text()

def errors(ch,root):
    if ch['id'] not in CIDS:return []
    try:
        u=json.loads(checked(root,UNITS,UNITS_SHA))[ch['id']]
        raw=checked(root,u['raw_path'],u['sha256'])
        s=ch['source']
        if (s['raw_path'],s['raw_file_sha256'],s['revision_id'],ch['source_id'],s['image_verified'])!=(u['raw_path'],u['sha256'],u['revision'],u['source_id'],False):raise ValueError('來源')
        ls=raw.splitlines(keepends=True)
        if len(ch['paragraphs'])!=len(u['segs']):raise ValueError('段數')
        notes=[]
        for p,seg in zip(ch['paragraphs'],u['segs']):
            n=seg[0];ln=ls[n-1].rstrip('\r\n');a=0;b=len(ln)
            if len(seg)==3:
                if ln.count(seg[1])!=1:raise ValueError('起界')
                a=ln.index(seg[1]);b=ln.index(seg[2],a)+len(seg[2])
            base=sum(map(len,ls[:n-1]));off=base+a;drop=set()
            for m in re.finditer(r'<ref>.*?</ref>|\{\{YL\|([^{}|]*)\}\}|-\{([^{}])\}-',ln[a:b]):
                if m[0].startswith('<ref>'):
                    drop.update(range(m.start(),m.end()))
                    notes.append(dict(paragraph_id=p['id'],raw_start=off+m.start(),raw_end=off+m.end(),raw_text=m[0],layer='modern_received_witness_collation_report',image_verified=False))
                else:
                    group=1 if m[1] is not None else 2
                    drop.update(range(m.start(),m.start(group)));drop.update(range(m.end(group),m.end()))
            ix=[off+j for j in range(b-a)if j not in drop];txt=''.join(raw[j]for j in ix)
            want=dict(revision_id=u['revision'],first_line=n,last_line=n,line_start=a,line_end=b,raw_start=off,raw_end=base+b,raw_character_offsets=ix,projection_sha256=sha256((json.dumps(ix,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography')
            if want!=p['source_position'] or p['text']!=txt or p['text_layer']!='received_chapter':raise ValueError('原字')
        if notes!=ch['annotation']['modern_collation_reports']:raise ValueError('校記')
        if ch['text_sha256']!=sha256('\n\n'.join(p['text']for p in ch['paragraphs']).encode()).hexdigest():raise ValueError('全文')
        if ch['id']=='c-nanqishu-002-peihuizhao-death' and not (ls[32].strip()=='==建元二年==' and ls[45].startswith('秋七月甲寅')):raise ValueError('本紀建元二年、秋七月')
        return []
    except (TypeError,ValueError,KeyError,IndexError,OSError):return ['裴后、兩妃及其家人固定見證原字或行段不合']

def kin_valid(a,ch,root):
    try:
        if ch['id'] not in CIDS or errors(ch,root):return False
        f=json.loads(checked(root,FRAMES,FRAMES_SHA))[a['id']]
        if (a['status']!='source_attested' or f['chapter_id']!=ch['id'] or f['qualifiers']!=a['qualifiers']
                or f['predicate']!=a['predicate'] or a['subject_person_id']==a['object_person_id']):return False
        ps={p['id']:p for p in ch['paragraphs']};ev={}
        for role in f['roles']:
            field=role['field'];pid=role['paragraph_id'];source=role['clause'];s=role['surface'];pers=role['person_id'];p=ps[pid]
            if p['text'].count(source)!=1 or source.count(s)!=1:return False
            i=p['text'].index(source)+source.index(s)
            hits=[r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id']==pid and r['referent_role']=='third_person'] if field.endswith('_reference_id') else [m for m in p['mentions'] if m['kind']=='person']
            hit,=[m for m in hits if m['start']==i and m['end']==i+len(s) and m['surface']==s]
            if hit['person_id']!=pers or a[field.split('_')[0]+'_person_id']!=pers:return False
            e=ev.setdefault(pid,dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=pid,quote=p['text']))
            e[field]=hit['id']
        return a['evidence']==list(ev.values())
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return False


def death_valid(event,e,ch,root):
    try:
        if errors(ch,root):return False
        row=json.loads(checked(root,DEATHS,DEATHS_SHA))[event['id']]
        p,=(p for p in ch['paragraphs']if p['id']==row['paragraph_id'])
        def anchor(word,clause):
            if p['text'].count(clause)!=1 or clause.count(word)!=1:raise ValueError('詞位')
            i=p['text'].index(clause)+clause.index(word)
            return dict(paragraph_id=p['id'],start=i,end=i+len(word),surface=word)
        a=anchor(row['person_word'],row['person_clause'])
        hits=[r for r in ch['annotation']['person_reference_occurrences']if r['paragraph_id']==p['id'] and r['referent_role']=='third_person']+p['mentions']
        m,=(x for x in hits if x['start']==a['start']and x['end']==a['end']and x['surface']==a['surface'])
        f='person_reference_id'if 'referent_role'in m else'person_mention_id'
        expect=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],**{f:m['id']})
        return (row['chapter_id']==ch['id'] and event['event_type']=='death'and event['status']=='source_attested' and event['date_expression']==row['date']
                and m['person_id']==event['person_id']==row['person_id']and row['term']==event['source_term']and event['source_anchor']==anchor(row['term'],row['term_clause'])and e==expect and event['evidence']==[expect])
    except(TypeError,ValueError,KeyError,IndexError,OSError):return False
