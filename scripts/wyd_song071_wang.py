"""武英殿刊《宋書》王僧綽傳的逐欄轉寫、親屬端點與身後贈諡。"""
import json
from hashlib import sha256
from pathlib import Path

CID = 'c-songshu-071-wangsengchuo-wyd'
SID = 's-songshu-071-wangsengchuo-wyd1739'
RAW = 'source-evidence/song071-wang/wyd-columns.txt'
DATA = 'source-evidence/song071-wang/wyd-comparison.json'
FRAMES = 'source-evidence/song071-wang/wyd-kinship-frames.json'
RAW_SHA = '60ee7e528b226268cfec0ccb2fdb23c4e886e05e02826b35d582cb08eae7c4d6'
DATA_SHA = '16cde9e9f0b5517cf003cfa22563220c6a7e83f43bd74ab8b1907940a3ec3e35'
FRAMES_SHA = 'e831b257d6cd7e9a18fa344394db4eba8b28f4d36c6fc0042aa8b1cb64b36d20'
TEXT_SHA = '37f68013bb9099e0d7ff48f6fabf5b4cdb61d1fbfa9a73a3aa9b29c1b15fd624'
WANG = '7r6_k52_qji_ABAAAAEA'
EMPEROR = 'hx8_st4_jdd'


def checked(root,rel,digest):
    root=Path(root).resolve()
    f=root/rel
    if f!=f.resolve() or sha256(f.read_bytes()).hexdigest()!=digest:
        raise ValueError('書影轉寫憑據不符')
    return f.read_text()


def errors(ch,root):
    if ch['id']!=CID:
        return []
    try:
        raw=checked(root,RAW,RAW_SHA)
        checked(root,DATA,DATA_SHA)
        s=ch['source']
        if (ch['source_id']!=SID or s['raw_file_sha256']!=RAW_SHA or s['raw_path']!=RAW
                or s['revision_id']!='cbr-ai-transcription-sha256:'+RAW_SHA
                or s['image_verified'] is not True or ch['annotation']['human_reviewed'] is not False
                or ch['annotation']['print_projection_ref']!=DATA):
            raise ValueError('書影來源')
        cols=dict(t.split() for t in raw.splitlines())
        starts={};i=0
        for k,v in cols.items():starts[k]=i;i+=len(v)
        if i!=853 or len(cols)!=41:raise ValueError('全傳長度')
        pos=0
        for n,p in enumerate(ch['paragraphs'],1):
            if p['id']!=CID+f':p{n:03d}':raise ValueError('非該本段號')
            body=[]
            for a in p['source_position']['column_projection']:
                key=a['column'];lo=a['start'];hi=a['end']
                if not (0<=lo<hi<=len(cols[key]) and cols[key][lo:hi]==a['text']
                        and starts[key]+lo==pos):raise ValueError('欄位缺文或跨欄')
                body.append(a['text']);pos+=hi-lo
            if ''.join(body)!=p['text'] or p['source_position']['revision_id']!=s['revision_id']:
                raise ValueError('段落')
        if (pos!=853 or len(ch['paragraphs'])!=5 or ch['text_sha256']!=TEXT_SHA
                or sha256('\n\n'.join(p['text'] for p in ch['paragraphs']).encode()).hexdigest()!=TEXT_SHA):
            raise ValueError('傳文總長')
    except (KeyError,ValueError,TypeError,OSError):
        return ['宋書卷71王僧綽殿本正文、固定分段或41欄的連續字位不符']
    return []


def kin_valid(a,ch,root):
    try:
        if errors(ch,root) or ch['id']!=CID:return False
        k=a['qualifiers']['wyd_song071_kin_frame']
        frame=json.loads(checked(root,FRAMES,FRAMES_SHA))[k];p=ch['paragraphs'][frame['n']-1]
        e,=a['evidence']
        if (a['id']!='a-song071-wyd-'+k or a['predicate']!=frame['predicate']
                or a['qualifiers']['source_term']!=frame['term'] or a['status']!='source_attested'
                or (e['chapter_id'],e['source_id'],e['work_id'],e['book_id'],e['paragraph_id'],e['quote'])!=
                (CID,SID,'w-songshu','b-songshu-071',p['id'],p['text'])):return False
        for field,clause,word,pid in frame['roles']:
            if p['text'].count(clause)!=1 or clause.count(word)!=1:return False
            i=p['text'].index(clause)+clause.index(word)
            if field.endswith('_reference_id'):
                rows=[m for m in ch['annotation']['person_reference_occurrences']
                      if m['paragraph_id']==p['id'] and m['referent_role']=='third_person']
            else:rows=[m for m in p['mentions'] if m['kind']=='person']
            hit,=(m for m in rows if m['start']==i and m['end']==i+len(word) and m['surface']==word)
            if hit['person_id']!=pid or e[field]!=hit['id'] or a[field.split('_')[0]+'_person_id']!=pid:
                return False
        return True
    except (KeyError,IndexError,ValueError,TypeError,OSError):
        return False


def award_valid(h,ch,events,root):
    try:
        if ch['id']!=CID or errors(ch,root):return False
        mode,term,kind={
            '散騎常侍':('posthumous_grant','追贈散騎常侍金紫光祿大夫','office'),
            '金紫光祿大夫':('posthumous_grant','追贈散騎常侍金紫光祿大夫','office'),
            '愍侯':('posthumous_naming','謚曰愍侯','honorific'),
        }[h['title']]
        b=h['naming_basis' if mode=='posthumous_naming' else 'posthumous_basis']
        p=ch['paragraphs'][3];text=p['text'];e,=h['evidence'];t,=h['attestations']
        def anchor(word):
            i=text.index(word)
            return dict(paragraph_id=p['id'],start=i,end=i+len(word),surface=word)
        d=events[b['death_event_id']]
        m,=(m for m in p['mentions'] if m['surface']=='僧綽' and m['start']==text.index('得僧綽所啓')+1)
        r,=(r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id']
            and r['start']==text.index('世祖卽位') and r['surface']=='世祖')
        return (h['person_id']==m['person_id']==d['person_id']==WANG and r['person_id']==EMPEROR
                and b['recipient_person_mention_id']==t['person_mention_id']==e['person_mention_id']==m['id']
                and b['issuer_person_reference_id']==r['id'] and b['kind']=='song071_print_wang_posthumous_awards'
                and (h['mode'],h['kind'],h['status'])==(mode,kind,'source_attested')
                and b['evidence']==d['evidence']==[e] and d['id']=='le-song071-wyd-sengchuo'
                and d['status']=='source_attested' and d['source_anchor']==anchor('收害')
                and b['source_term']==term and b['source_anchor']==anchor(term)
                and e['quote']==text and e['source_id']==SID and e['chapter_id']==CID and e['paragraph_id']==p['id']
                and t['usage']=='posthumous_usage' and all(t[k]==v for k,v in anchor(h['title']).items())
                and h['effective_period']['start']==dict(status='source_event',event_type=mode,date_expression=None,evidence=[e]))
    except (KeyError,ValueError,TypeError,OSError):
        return False
