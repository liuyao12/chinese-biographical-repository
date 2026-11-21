"""核王泰、王慈、所任二王府及祁廓的原字和不同親屬關係。"""
from hashlib import sha256
import json
from pathlib import Path

CIDS=('c-liangshu-021-wangtai-wangyun', 'c-liangshu-029-xiaoji-wangtai', 'c-nanshi-053-xiaozong-wangtai', 'c-liangshu-002-nanxu-wangtai')
F='source-evidence/liang021-wangtai/frames.json'
FS='b5c56836f8749420d97f35f2440af9976d5366bef5665e79a2491d2a343cc9a4'
R='source-evidence/liang021-wangtai/reading.json'
RS='a89df28b311efd58aa5bda6d68fa50dc6fa6211f551dc41b8ae737ecfbaffcaf'

def digest(text):
    return sha256(text.encode()).hexdigest()

def datahash(data):
    return digest(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def fixed(root,rel,want):
    root=Path(root).resolve();p=root/rel;text=p.read_text()
    if p!=p.resolve() or not p.is_relative_to(root) or digest(text)!=want:raise ValueError('固定版本')
    return text

def frame(ch,root):
    return json.loads(fixed(root,F,FS))[ch['id']]

def errors(ch,root):
    if ch['id'] not in CIDS:return []
    try:
        q=frame(ch,root);s=ch['source'];ps=ch['paragraphs']
        if (ch['source_id'],s['raw_path'],s['raw_file_sha256'],s['revision_id'],s['image_verified'])!=(q['source_id'],q['source_path'],q['raw_sha256'],q['revision_id'],False):raise ValueError('定本')
        raw=fixed(root,q['source_path'],q['raw_sha256']);lines=raw.splitlines(keepends=True)
        if datahash([p['source_position']for p in ps])!=q['positions_sha256']:raise ValueError('原行與字位')
        for i,p in enumerate(ps,1):
            pos=p['source_position'];ix=pos['raw_character_offsets'];n=pos['first_line'];offset=sum(map(len,lines[:n-1]))
            if p['id']!=ch['id']+f':p{i:03}'or pos['last_line']!=n or pos['raw_start']!=offset+pos['line_start'] or pos['raw_end']!=offset+pos['line_end'] or ''.join(raw[j]for j in ix)!=p['text'] or ix!=sorted(set(ix)) or datahash(ix)!=pos['projection_sha256']:raise ValueError('逐字映射')
        if digest('\n\n'.join(p['text']for p in ps))!=q['body_sha256'] or ch['text_sha256']!=q['body_sha256'] or datahash(ch['annotation'])!=q['annotation_sha256'] or datahash([p['mentions']for p in ps])!=q['mentions_sha256']:raise ValueError('全文判讀')
        if ch['id']==CIDS[0]:
            book=json.loads(fixed(root,R,RS));old=book['before_expansion']
            if datahash(ps[0])!=old['paragraph_sha256'] or [m['id']for m in ps[0]['mentions']]!=old['mentions']:raise ValueError('原證保全')
            for r in book['cross_readings']:
                src=fixed(root,r['fixed_path'],r['sha256']).splitlines()[r['source_line']-1]
                if src[r['start']:r['end']]!=r['quote']:raise ValueError('旁證')
        return []
    except (TypeError,KeyError,IndexError,ValueError,OSError):return ['王泰、二王府及親屬原行或字詞角色不合']

def kin_valid(a,ch,root):
    return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']

def side_errors(data,ch,root,field):
    if ch['id']not in CIDS:return []
    try:
        key={'assertions':'kin','holdings':'offices','events':'life'}[field]
        if frame(ch,root)[key]!=data[field]:raise ValueError('原證')
        return []
    except (TypeError,KeyError,IndexError,ValueError,OSError):return ['王泰及兩王府的原親屬、職事和死亡讀法不合']

def proposal_valid(q,ch):
    try:
        title=q['title'];idx,cl,verb,reject,who={'著作郎':(1,'起家爲著作郎，不拜','起家爲','不拜','泰幼敏悟'),'散騎常侍':(2,'改除散騎常侍、左驍騎將軍，未拜，卒','改除','未拜','泰能接人士'),'左驍騎將軍':(2,'改除散騎常侍、左驍騎將軍，未拜，卒','改除','未拜','泰能接人士')}[title]
        p=ch['paragraphs'][idx];t=p['text'];pers='7r6_k52_qji_ABAAAAEBAA';m,=[m for m in p['mentions']if m['start']==t.index(who)and m['surface']=='泰'and m['person_id']==pers and m['kind']=='person']
        def anchor(w):
            i=t.index(cl)+cl.index(w);return dict(paragraph_id=p['id'],start=i,end=i+len(w),surface=w)
        e=dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],paragraph_id=p['id'],source_id=ch['source_id'],quote=t,person_mention_id=m['id'])
        return (ch['id']==CIDS[0] and ch['source']['revision_id']==1544250 and digest(t)=={1: '0478864d0322d570fc7b77b81466dc3fa831cc778d08e92b6a3e696d4b2791a9', 2: '1023da41e59cf5ab0f1b821755362ca178a769f3817ad205e5bea31c14381716'}[idx] and q['person_id']==pers and q['person_mention_id']==m['id'] and q['appointment_stage']=='appointment' and q['proposal_kind']=='unassumed_appointment' and q['non_assumption_kind']=='did_not_take_up' and q['outcome']=='not_assumed' and q['role_anchor']==anchor(title) and q['appointment_anchor']==anchor(verb) and q['non_assumption_anchor']==anchor(reject) and q['evidence']==[e])
    except (TypeError,KeyError,IndexError,ValueError):return False
