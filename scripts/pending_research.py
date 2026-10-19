"""待決研究不是active assertion；只核外層契約，不改寫proposal原始欄位。"""
import json
from pathlib import Path

COLLECTION_STATUS='unadopted_not_active_assertions'
RECORD_STATUSES={'unadopted_pending_review'}

def pending_errors(data, person_ids, active_ids=()):
    errors=[]
    def check(ok,msg):
        if not ok:errors.append(msg)
    if not isinstance(data,dict):return ['待決研究集須為物件']
    check(data.get('record_type')=='source_backed_pending_research','待決研究集類型不符')
    check(data.get('status')==COLLECTION_STATUS,'待決研究集不得標為active或已採用')
    def inactive_flags(value,label):
        for key in ('active','is_active','adopted','is_adopted','applied'):
            if key in value:check(value[key] is False,label+'不得標為'+key)
    inactive_flags(data,'待決研究集')
    rows=data.get('records');index=data.get('person_index')
    if not isinstance(rows,list) or not isinstance(index,dict):return errors+['待決records/person_index結構不符']
    expected={};seen=set()
    def people(value,path):
        if isinstance(value,dict):
            for k,v in value.items():
                if k=='person_id' or k.endswith('_person_id'):
                    check(v is None or isinstance(v,str) and v in person_ids,path+'/'+k+'人物ID不存在')
                elif k=='person_ids' or k.endswith('_person_ids'):
                    check(isinstance(v,list) and all(isinstance(pid,str) and pid in person_ids for pid in v),path+'/'+k+'人物ID列表不存在或格式不符')
                people(v,path+'/'+k)
        elif isinstance(value,list):
            for i,v in enumerate(value):people(v,path+'/'+str(i))
    for i,row in enumerate(rows):
        if not isinstance(row,dict):errors.append('待決記錄須為物件');continue
        rid=row.get('id');label='待決記錄'+str(rid)
        valid_id=isinstance(rid,str) and bool(rid)
        check(valid_id,label+'缺ID')
        if valid_id:
            check(rid not in seen,label+'ID重複');seen.add(rid)
            check(rid not in active_ids,label+'不得同時作active記錄')
        check(isinstance(row.get('status'),str) and row['status'] in RECORD_STATUSES,label+'須明確為unadopted_pending_review')
        inactive_flags(row,label)
        pids=row.get('person_ids')
        valid_people=(isinstance(pids,list) and all(isinstance(pid,str)for pid in pids))
        check(valid_people,label+'person_ids須為字串列表（無具名對象可留空）')
        if valid_people:
            check(len(pids)==len(set(pids)),label+'person_ids重複')
            if valid_id:
                for pid in pids:expected.setdefault(pid,set()).add(rid)
        people(row,'records/'+str(i))
    check(set(index)==set(expected),'person_index人物鍵缺漏或多餘')
    for pid,ids in index.items():
        check(pid in person_ids,'person_index人物ID不存在：'+str(pid))
        valid=isinstance(ids,list) and all(isinstance(rid,str) and bool(rid)for rid in ids)
        check(valid,'person_index值須為record ID列表：'+str(pid))
        if valid:
            check(len(ids)==len(set(ids)),'person_index含重複反向：'+str(pid))
            check(set(ids)==expected.get(pid,set()),'person_index反向缺漏／多餘／錯配：'+str(pid))
    return errors

def validate(root):
    """讀取原生registry/research/corpus；不建立、修復或寫回資料。"""
    root=Path(root);out=[]
    try:
        people={p['id'] for p in json.loads((root/'registry/persons.json').read_text())['persons']}
        active=set()
        def ids(value):
            if isinstance(value,dict):
                if isinstance(value.get('id'),str):active.add(value['id'])
                for v in value.values():ids(v)
            elif isinstance(value,list):
                for v in value:ids(v)
        for f in sorted((root/'corpus').rglob('*.json')):
            d=json.loads(f.read_text())
            if d.get('record_type')=='source_backed_pending_research':out.append('待決研究集不得放入active corpus：'+str(f.relative_to(root)))
            ids(d)
        research_seen=set()
        for f in sorted((root/'data/research').glob('*.json')):
            d=json.loads(f.read_text())
            if d.get('record_type')=='source_backed_pending_research' or f.name=='early-medieval-family-pending.json':
                out.extend(str(f.relative_to(root))+'：'+e for e in pending_errors(d,people,active))
                for row in d.get('records',[]):
                    rid=row.get('id') if isinstance(row,dict) else None
                    if isinstance(rid,str):
                        if rid in research_seen:out.append('待決研究跨檔record ID重複：'+rid)
                        research_seen.add(rid)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        out.append('待決研究結構無效：'+str(exc))
    return out
