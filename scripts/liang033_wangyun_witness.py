"""核梁書王筠本傳及南史謝氏親屬原句。"""
import hashlib
import json
from pathlib import Path

UNITS = 'source-evidence/liang033-wangyun/verified-units.json'
UNIT_SHA = '77354203dbee428fe73d04f9576d76d46ce9fd8a5b822bd901e2486d9afec591'
READING = 'source-evidence/liang033-wangyun/reading.json'
READING_SHA = '3546a7907d1ac352821507ba7363711b8902498891629d5ac02c9772c4c53931'
CIDS = ('c-liangshu-033-wangyun', 'c-nanshi-020-xielan-xieju-wangyun')
PRINT = 'source-evidence/liang033-wangyun/wyd-comparison.json'
PRINT_SHA = '79de2787ef521b15778419833c7b15b1740c2ce5972047906f1d8d24a06df5b2'

def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()

def data_hash(value):
    return digest(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def fixed(root, path, expected):
    root=Path(root).resolve()
    file=root/path
    raw=file.read_text()
    if file.resolve()!=file or not file.is_relative_to(root) or digest(raw)!=expected:
        raise ValueError('固定來源不符')
    return raw

def unit(ch,root):
    return json.loads(fixed(root,UNITS,UNIT_SHA))[ch['id']]

def errors(ch,root):
    if ch.get('id') == 'c-liangshu-033-wangyun-wyd':
        try: from scripts.liang033_printed_wangyun import errors as printed_reading
        except ImportError: from liang033_printed_wangyun import errors as printed_reading
        return printed_reading(ch,root)
    if ch['id'] not in CIDS:
        return []
    try:
        u=unit(ch,root)
        s=ch['source']
        if (s['raw_path'],s['raw_file_sha256'],s['revision_id'],ch['source_id'],s['image_verified'])!=(u['raw_path'],u['sha256'],u['revision'],u['source_id'],False):
            raise ValueError('版本')
        raw=fixed(root,u['raw_path'],u['sha256']);ls=raw.splitlines(keepends=True)
        if len(ch['paragraphs'])!=len(u['projection']):
            raise ValueError('段數')
        for p,(line,a,b) in zip(ch['paragraphs'],u['projection']):
            off=sum(map(len,ls[:line-1]));ix=list(range(off+a,off+b))
            expected=dict(revision_id=u['revision'],source_layer='received_biography',first_line=line,last_line=line,line_start=a,line_end=b,raw_start=off+a,raw_end=off+b,raw_character_offsets=ix,projection_sha256=data_hash(ix))
            if p['text']!=ls[line-1][a:b] or p['source_position']!=expected or p['text_layer']!='received_chapter':
                raise ValueError('原字')
        if ch['text_sha256']!=u['body_sha256'] or digest('\n\n'.join(p['text']for p in ch['paragraphs']))!=u['body_sha256']:
            raise ValueError('全文')
        names=[[{key:m[key]for key in ('id','surface','start','end','person_id','kind')}for m in p['mentions']]for p in ch['paragraphs']]
        a=ch['annotation']
        for item, field in [(names,'names_sha256'),(a['person_reference_occurrences'],'references_sha256'),(a['narrative_readings'],'narrative_sha256'),(a.get('title_proposals',[]),'proposal_sha256'),(a.get('age_assertions',[]),'ages_sha256')]:
            if data_hash(item)!=u[field]:raise ValueError('讀法、姓名或提議')
        if ch['id']==CIDS[0]:
            r=json.loads(fixed(root,READING,READING_SHA));pr=json.loads(fixed(root,PRINT,PRINT_SHA))
            fixed(root,pr['transcription'],pr['transcription_sha256'])
            if a['item_reading']!=READING or a['parallel_print_comparison']!=PRINT:raise ValueError('校讀')
            ps={p['id']:p['text'] for p in ch['paragraphs']}
            for pair in r['comparisons']:
                span=pair['source_anchor'];ref=pair['reference'];line=fixed(root,ref['path'],ref['sha256']).splitlines()[ref['first_line']-1]
                if line[ref['start_codepoint']:ref['end_codepoint']]!=ref['quote'] or ps[span['paragraph_id']][span['start']:span['end']]!=span['surface'] or span['surface']!=pair['source_quote']:
                    raise ValueError('旁證')
        return []
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return ['梁書王筠及謝氏親屬原句、引文或殿本校讀不符']

def side_errors(record,ch,root,field):
    if ch.get('id') == 'c-liangshu-033-wangyun-wyd':
        try: from scripts.liang033_printed_wangyun import side_errors as printed_reading
        except ImportError: from liang033_printed_wangyun import side_errors as printed_reading
        return printed_reading(record,ch,root,field)
    if ch['id'] not in CIDS:
        return []
    try:
        key={'assertions':'kinship','holdings':'offices','events':'deaths'}[field]
        if unit(ch,root)[key]!=record[field]:
            raise ValueError('資料組')
        return []
    except (IndexError,KeyError,OSError,TypeError,ValueError):
        return ['王筠與謝氏本條親屬、職序或生卒的原讀與端點不合']

def kin_valid(record,ch,root):
    if ch.get('id') == 'c-liangshu-033-wangyun-wyd':
        try: from scripts.liang033_printed_wangyun import kin_valid as printed_reading
        except ImportError: from liang033_printed_wangyun import kin_valid as printed_reading
        return printed_reading(record,ch,root)
    try:
        return record in unit(ch,root)['kinship'] and not errors(ch,root)
    except (IndexError,KeyError,OSError,TypeError,ValueError):
        return False

def death_valid(record,e,ch,root):
    if ch.get('id') == 'c-liangshu-033-wangyun-wyd':
        try: from scripts.liang033_printed_wangyun import death_valid as printed_reading
        except ImportError: from liang033_printed_wangyun import death_valid as printed_reading
        return printed_reading(record,e,ch,root)
    try:
        return record in unit(ch,root)['deaths'] and record['evidence']==[e] and not errors(ch,root)
    except (IndexError,KeyError,OSError,TypeError,ValueError):
        return False

def declined_valid(proposal,ch):
    if ch.get('id') == 'c-liangshu-033-wangyun-wyd':
        try: from scripts.liang033_printed_wangyun import declined_valid as printed_reading
        except ImportError: from liang033_printed_wangyun import declined_valid as printed_reading
        return printed_reading(proposal,ch)
    try:
        p=ch['paragraphs'][4];text=p['text']
        clause='出爲明威將軍、永嘉太守，以疾固辭，徙爲光祿大夫'
        if ch['id']!=CIDS[0] or ch['source']['revision_id']!=1514481 or text.count(clause)!=1 or digest(text)!='ec25e11cf85f69f329fe9d3dbf6715b155d98dfde916ed00facc3efbc59ad6d2':
            return False
        def anchor(word):
            i=text.index(clause)+clause.index(word)
            return dict(paragraph_id=p['id'],start=i,end=i+len(word),surface=word)
        title=proposal['title'];word=text.index('筠有孝性')
        m,=[m for m in p['mentions'] if m['start']==word and m['surface']=='筠' and m['kind']=='person' and m['person_id']=='mxz_qw8_acd_A']
        return (title in ('明威將軍','永嘉太守') and proposal['appointment_stage']=='appointment' and proposal['proposal_kind']=='unassumed_appointment' and proposal['outcome']=='not_assumed' and proposal['non_assumption_kind']=='declined'
                and proposal['person_mention_id']==m['id'] and proposal['person_id']==m['person_id'] and proposal['role_anchor']==anchor(title) and proposal['appointment_anchor']==anchor('出爲') and proposal['non_assumption_anchor']==anchor('以疾固辭')
                and proposal['evidence']==[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=text,person_mention_id=m['id'])])
    except (IndexError,KeyError,TypeError,ValueError):
        return False
