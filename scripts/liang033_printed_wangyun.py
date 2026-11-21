"""武英殿本梁書卷三十三王筠傳的原欄、原音注及親屬、任官原證。"""
import hashlib
import json
from pathlib import Path

CID='c-liangshu-033-wangyun-wyd'
LEDGER='source-evidence/liang033-wangyun/wyd-native-reading.json'
LEDGER_SHA='8003adf68ddb1f395be20fd15ecff9dcb405e0c3389f783820e8d0fa12fff834'
FRAMES='source-evidence/liang033-wangyun/wyd-native-frames.json'
FRAMES_SHA='231957cd023296bf72ce773569cfc536c5c9d8a9549706567f20177c6aa9d505'
RAW='source-evidence/liang033-wangyun/wyd-columns.txt'
RAW_SHA='7053558e6ae66bd8cf78b874c228cebd0f6693575c192ac8fc72b37815b9569a'
COMPARE='source-evidence/liang033-wangyun/wyd-comparison.json'
COMPARE_SHA='79de2787ef521b15778419833c7b15b1740c2ce5972047906f1d8d24a06df5b2'

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()

def hash_data(data):
    return digest(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def fixed(root,relative,sha):
    root=Path(root).resolve();file=root/relative
    data=file.read_text()
    if file!=file.resolve() or not file.is_relative_to(root) or digest(data)!=sha:raise ValueError('固定校本')
    return data

def frames(root):
    return json.loads(fixed(root,FRAMES,FRAMES_SHA))

def errors(ch,root):
    if ch['id']!=CID:return []
    try:
        l=json.loads(fixed(root,LEDGER,LEDGER_SHA));proof=frames(root);comp=json.loads(fixed(root,COMPARE,COMPARE_SHA))
        raw=fixed(root,RAW,RAW_SHA);lines=[line.split()for line in raw.splitlines()];cols=dict(lines);flat=''.join(cols.values());pos=0;lookup={}
        if len(cols)!=60 or len(flat)!=1251 or len(l['columns'])!=60 or comp['transcription_sha256']!=RAW_SHA or ch['source_id']!=proof['source_id'] or hash_data(ch['source'])!=proof['source_sha256']:raise ValueError('刊本身分')
        for row,(key,val) in zip(l['columns'],lines):
            if row['column']!=key or row['text']!=val or row['start_codepoint']!=pos or row['end_codepoint']!=pos+len(val):raise ValueError('不連續原欄')
            lookup[key]=row;pos+=len(val)
        pos=0
        if len(ch['paragraphs'])!=6 or len(l['paragraph_spans'])!=6:raise ValueError('段數')
        for p,span in zip(ch['paragraphs'],l['paragraph_spans']):
            if p['id']!=span['paragraph_id'] or pos!=span['start_codepoint'] or p['source_position']['revision_id']!=ch['source']['revision_id'] or p['text_layer']!='received_chapter':raise ValueError('段頭')
            ext=span['end_codepoint'];fragments=[]
            for row in l['columns']:
                begin=row['start_codepoint'];end=row['end_codepoint'];a=max(begin,pos);b=min(end,ext)
                if a>=b:continue
                fragments.append(dict(column=row['column'],pdf_page=row['pdf_page'],half=row['half'],leaf=row['leaf'],column_from_right=row['column_from_right'],start=a-begin,end=b-begin,text=row['text'][a-begin:b-begin]))
            if p['text']!=flat[pos:ext] or p['source_position']['column_projection']!=fragments or p['source_position']['source_layer']!='received_biography':raise ValueError('逐字映射')
            pos=ext
        if pos!=len(flat) or ch['text_sha256']!=proof['body_sha256'] or digest('\n\n'.join(p['text']for p in ch['paragraphs']))!=proof['body_sha256']:raise ValueError('全文')
        a=ch['annotation'];notes=a['printed_phonetic_glosses'];graw=fixed(root,l['gloss_transcription_path'],l['gloss_sha256']);p=ch['paragraphs'][2];offset=l['paragraph_spans'][2]['start_codepoint']
        if notes!=l['printed_phonetic_glosses'] or len(notes)!=2 or len(graw.splitlines())!=3:raise ValueError('音注數')
        for q,(label,gloss),row in zip(notes,[('58L07','五激反'),('58L08','五鷄反')],graw.splitlines()[1:]):
            col=lookup[label];i=col['text'].index('霓');j=col['start_codepoint']+i-offset
            if row!=f'{label}\t{i}\t霓\t{gloss}' or q!=dict(pdf_page=58,half='左',leaf='十七上',column_from_right=int(label[-2:]),headword_column_offset=i,headword='霓',gloss=gloss,text_layer='printed_small_type',paragraph_id=p['id'],headword_start=j) or p['text'][j]!='霓':raise ValueError('書影原字與雙行音注')
        if hash_data(a)!=proof['annotation_sha256'] or hash_data([p['mentions']for p in ch['paragraphs']])!=proof['mention_sha256']:raise ValueError('官事語義、各人物與書影原字')
        return []
    except (TypeError,ValueError,KeyError,IndexError,OSError) as exc:return ['梁書殿本王筠原欄、原人與霓字兩處音注不合：'+str(exc)]

def side_errors(record,ch,root,field):
    if ch['id']!=CID:return []
    try:
        if record[field]!=frames(root)[field]:raise ValueError('原證')
        return []
    except (TypeError,ValueError,KeyError,IndexError,OSError):return ['梁書殿本親屬、職序或三人的死亡原證不合']

def kin_valid(a,ch,root):
    return ch['id']==CID and not errors(ch,root) and a in frames(root)['assertions']

def death_valid(event,e,ch,root):
    return ch['id']==CID and not errors(ch,root) and event['evidence']==[e] and event in frames(root)['events']

def declined_valid(q,ch):
    try:
        p=ch['paragraphs'][4];t=p['text'];clause='出為明威將軍永嘉太守以疾固辭徙為光祿大夫';name='筠';xi=t.index('筠有孝性');m,=[a for a in p['mentions']if a['start']==xi and a['surface']==name and a['kind']=='person']
        def anchor(w):
            j=t.index(clause)+clause.index(w);return dict(paragraph_id=p['id'],start=j,end=j+len(w),surface=w)
        e=dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=CID,source_id=ch['source_id'],paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
        return ch['id']==CID and ch['source']['raw_file_sha256']==RAW_SHA and digest(t)=='5d9365f86660422515d05efb71e9cff4ae4f1314c58a67a658d383c8631d960c' and q['proposal_kind']=='unassumed_appointment' and q['outcome']=='not_assumed' and q['non_assumption_kind']=='declined' and q['appointment_stage']=='appointment' and q['title']in('明威將軍','永嘉太守') and q['role_anchor']==anchor(q['title']) and q['appointment_anchor']==anchor('出為') and q['non_assumption_anchor']==anchor('以疾固辭') and q['person_id']==m['person_id']=='mxz_qw8_acd_A' and q['person_mention_id']==m['id'] and q['evidence']==[e]
    except (TypeError,ValueError,KeyError,IndexError):return False
