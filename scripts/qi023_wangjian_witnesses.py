"""核對王儉、王遜題及所引傳首、帝女表。"""
from hashlib import sha256
import json
from pathlib import Path

UNITS = 'source-evidence/nanqi023-wangjian/units.json'
UNITS_SHA = 'f5d7f2d294427b44dc529803464d28a85f58a9c21d3247992b85fece5f220c21'
FRAMES = 'source-evidence/nanqi023-wangjian/kinship-frames.json'
FRAMES_SHA = '3a2d7364000e6dc18b59f2c0c26b10ef8ba26e58daa7f7a3c4a685b23e088358'
CIDS = ('c-nanqishu-023-wangjian', 'c-nanqishu-039-lucheng-wangjian', 'c-nanshi-048-lucheng-wangjian', 'c-nanqishu-044-shenwenji-wangjian', 'c-sanguozhi-052-zhangzhao-wangjian', 'c-wenxiantongkao-258-yangxian')

def checked(root,rel,digest):
    r=Path(root).resolve()
    p=r/rel
    if not p.is_relative_to(r) or p.resolve()!=p or sha256(p.read_bytes()).hexdigest()!=digest:
        raise ValueError('固定來源雜湊')
    return p.read_text()

def errors(ch,root):
    if ch['id'] not in CIDS:
        return []
    try:
        u=json.loads(checked(root,UNITS,UNITS_SHA))[ch['id']]
        raw=checked(root,u['raw_path'],u['raw_sha256'])
        s=ch['source']
        if (s['raw_path'],s['raw_file_sha256'],s['revision_id'],ch['source_id'])!=(u['raw_path'],u['raw_sha256'],u['revision'],u['source_id']):
            raise ValueError('修訂')
        if ch['annotation']['unit_projection_ref']!=UNITS or ch['annotation']['human_reviewed'] is not False or s['image_verified'] is not False:
            raise ValueError('校驗層')
        lines=raw.splitlines(keepends=True)
        if len(ch['paragraphs'])!=len(u['paragraphs']):raise ValueError('段數')
        for p,row in zip(ch['paragraphs'],u['paragraphs']):
            num=row['line'];lo=row['start'];hi=row['end'];base=sum(len(t) for t in lines[:num-1]);loc=p['source_position']
            if (p['id'],loc['first_line'],loc['last_line'],loc['line_start'],loc['line_end'],loc['raw_start'],loc['raw_end'],loc['revision_id'])!=(row['paragraph_id'],num,num,lo,hi,base+lo,base+hi,u['revision']):
                raise ValueError('原行字位')
            if p['text']!=lines[num-1][lo:hi] or p['text_layer']!='received_chapter':
                raise ValueError('原字')
        if ch['text_sha256']!=sha256(('\n\n'.join(p['text'] for p in ch['paragraphs'])).encode()).hexdigest():
            raise ValueError('全文')
        if ch['id']=='c-wenxiantongkao-258-yangxian' and ('宋公主' not in lines[50] or not lines[55].startswith('　　明帝女　陽羡公主適王儉')):
            raise ValueError('宋明帝分部、表格條目')
        return []
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return ['《南齊書》王儉傳及相關證據的固定原卷、分題或精確原字不合']

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

def award_valid(h,ch,events,root):
    try:
        if ch['id']!='c-nanqishu-023-wangjian' or errors(ch,root):return False
        title=h['title'];mode,kind,clause={'太尉':('posthumous_grant','office','追贈太尉'),'文憲公':('posthumous_naming','honorific','謚文憲公')}[title]
        key='posthumous_basis' if mode=='posthumous_grant' else 'naming_basis';b=h[key]
        p=ch['paragraphs'][12];d=events[b['death_event_id']];deathp=ch['paragraphs'][11]
        if (p['source_position']['first_line'],deathp['source_position']['first_line'])!=(87,85):return False
        def anchor(p,t):
            assert p['text'].count(t)==1
            i=p['text'].index(t)
            return dict(paragraph_id=p['id'],start=i,end=i+len(t),surface=t)
        word=next(m for m in p['mentions']if m['start']==p['text'].index('南昌公儉')+3 and m['surface']=='儉')
        issuer=next(r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id'] and r['start']==p['text'].index('及贊朕躬')+2 and r['surface']=='朕' and r['referent_role']=='speaker_self')
        e,=h['evidence'];t,=h['attestations']
        return ((h['mode'],h['kind'],h['status'])==(mode,kind,'source_attested')
                and b['kind']=='qi23_wang_death_award' and b['source_term']==clause and b['source_anchor']==anchor(p,clause)
                and d['person_id']==h['person_id']==word['person_id']=='7r6_k52_qji_ABAAAAEAA'
                and d['id']=='le-nanqi023-wangjian' and d['source_anchor']==anchor(deathp,'薨')
                and b['death_term']==d['source_term']=='薨' and d['status']=='source_attested'
                and issuer['person_id']=='kix_r92_2ed' and b['issuer_person_reference_id']==issuer['id']
                and b['recipient_person_mention_id']==e['person_mention_id']==t['person_mention_id']==word['id']
                and b['evidence']==[e] and e['quote']==p['text'] and e['chapter_id']==ch['id'] and e['paragraph_id']==p['id'] and e['source_id']==ch['source_id']
                and t['usage']=='posthumous_usage' and all(t[k]==v for k,v in anchor(p,title).items())
                and h['effective_period']['start']==dict(status='source_event',event_type=mode,date_expression=None,evidence=[e]))
    except (KeyError,AssertionError,IndexError,StopIteration,TypeError,ValueError,OSError):
        return False


def death_subject_valid(event, evidence, ch, root):
    """王儉本傳由上崩轉世祖即位，明示死者為齊太祖。"""
    try:
        if ch['id']!='c-nanqishu-023-wangjian' or errors(ch,root):
            return False
        p=ch['paragraphs'][8]; t=p['text']; clause='上崩，遺詔以儉爲侍中、尚書令、鎮軍將軍。世祖卽位'
        if t.count(clause)!=1 or p['source_position']['first_line']!=79:
            return False
        i=t.index(clause); refs=ch['annotation']['person_reference_occurrences']
        who,=[r for r in refs if r['paragraph_id']==p['id'] and r['start']==i and r['surface']=='上']
        successor,=[r for r in refs if r['paragraph_id']==p['id'] and r['start']==t.index('世祖卽位') and r['surface']=='世祖']
        expected=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_reference_id=who['id'])
        return (event['id']=='le-nanqi023-taizu' and event['event_type']=='death' and event['source_term']=='崩'
                and who['person_id']==event['person_id']=='47p_kjh_ez7' and successor['person_id']=='kix_r92_2ed'
                and who['referent_role']==successor['referent_role']=='third_person'
                and expected==evidence and event['evidence']==[expected]
                and event['source_anchor']==dict(paragraph_id=p['id'],start=i+1,end=i+2,surface='崩'))
    except (ValueError,KeyError,TypeError,IndexError,OSError):
        return False
