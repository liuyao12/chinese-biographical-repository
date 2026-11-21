"""核南史王儉、王遜及相關固定親屬世系、個別典故。"""
from pathlib import Path
from hashlib import sha256
import json
import re

CIDS=('c-nanshi-022-wangjian', 'c-houhanshu-052-cuiyuan-wangjian', 'c-nanqishu-033-zhangxu-wangjian', 'c-nanshi-031-zhangxu-wangjian', 'c-nanqishu-024-liushilong-wangjian', 'c-songshu-077-liuping-wangjian')
UNITS='source-evidence/nanshi022-wangjian-digital/units.json'
UNITS_SHA='df4c77ea5b097b662410082347fed757c6b69d7bf508d1f6b67941132adf9fa3'
FRAMES='source-evidence/nanshi022-wangjian-digital/kinship-frames.json'
FRAMES_SHA='1fffecc29fc5f52418a3ceb82cff420a29ed18d7a19c5aebec680f3c5d7f41f8'
DEATHS='source-evidence/nanshi022-wangjian-digital/death-frames.json'
DEATHS_SHA='94ad63f3eeada38e1c8f04030f37802342f7a8b295a113f3728da3d3e244e27d'
QUOTES='source-evidence/nanshi022-wangjian-digital/parallel-quotes.json'
QUOTES_SHA='2e80d7e1e940ce8bff67ab7c1952a9f0d48780022396b021f32303795e97bc6a'

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
        if ch['id']=='c-nanshi-022-wangjian':
            if ls[27].strip()!='====僧綽子 儉====' or ls[57].strip()!='=====儉子 騫=====' or not ls[59].startswith('騫字思寂，本字玄成，'):raise ValueError('傳題父子')
            links=json.loads(checked(root,QUOTES,QUOTES_SHA))['readings']
            for item in links:
                for e in item['evidence']:
                    raw=checked(root,e['raw_path'],e['sha256']).splitlines()[e['line']-1]
                    if raw[e['start']:e['end']]!=e['quote']:raise ValueError('旁證引句')
        return []
    except (TypeError,ValueError,KeyError,IndexError,OSError):return ['王儉、王遜傳及所引親屬見證的原字或原行不合']

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

def award_valid(h,ch,events,root):
    try:
        if ch['id']!='c-nanshi-022-wangjian' or errors(ch,root):return False
        p=ch['paragraphs'][11];t=p['text'];mode,kind,term={'太尉':('posthumous_grant','office','追贈太尉'),'文憲公':('posthumous_naming','honorific','諡文憲公')}[h['title']]
        b=h['posthumous_basis' if mode=='posthumous_grant'else'naming_basis']
        def anchor(w):
            if t.count(w)!=1:raise ValueError('詞位')
            i=t.index(w);return dict(paragraph_id=p['id'],start=i,end=i+len(w),surface=w)
        index=t.index('五年，儉即')+3
        m,=(m for m in p['mentions']if m['start']==index and m['surface']=='儉')
        r,=(r for r in ch['annotation']['person_reference_occurrences']if r['paragraph_id']==p['id']and r['start']==t.index('上親臨視')and r['surface']=='上'and r['referent_role']=='third_person')
        e=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
        death=events[b['death_event_id']]
        att,=h['attestations']
        return (h['status']=='source_attested'and h['mode']==mode and h['kind']==kind and b['kind']=='nan22jian_funeral_award'
                and b['source_term']==term and b['source_anchor']==anchor(term)and b['issuer_person_reference_id']==r['id']and r['person_id']=='kix_r92_2ed'
                and b['recipient_person_mention_id']==att['person_mention_id']==m['id']and m['person_id']==h['person_id']==death['person_id']=='7r6_k52_qji_ABAAAAEAA'
                and b['death_term']==death['source_term']=='薨'and death_valid(death,death['evidence'][0],ch,root)
                and b['evidence']==h['evidence']==[e]and att['usage']=='posthumous_usage'and all(att[k]==val for k,val in anchor(h['title']).items())
                and h['effective_period']['start']==dict(status='source_event',event_type=mode,date_expression=None,evidence=[e]))
    except (KeyError,IndexError,TypeError,ValueError,OSError):return False
