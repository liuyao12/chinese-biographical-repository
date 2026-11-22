"""《徐盛傳》卷末兩個相鄰正文段之間夾有干寶、魏氏春秋兩則裴注。"""
from pathlib import Path
from hashlib import sha256

def xukai_father(a, chapter, root):
    cid='c-sanguozhi-055-xusheng'
    if (chapter.get('id')!=cid or a.get('id')!='a-wu055-xukai-father'
            or a.get('predicate')!='father' or a.get('qualifiers')!={'source_term':'子楷，襲爵領兵'}
            or chapter['source'].get('revision_id')!=2603286):
        return False
    before=cid+':line112';after=cid+':line114'
    if a.get('context')!={'kind':'sanguozhi055_xukai_after_notes','paragraph_ids':[before,after]}:
        return False
    ps=chapter['paragraphs']
    if [p['id']for p in ps[-4:]]!=[before,before+'-pei01-01',before+'-pei01-02',after]:
        return False
    first,one,two,last=ps[-4:]
    if (any(n.get('attachment',{}).get('received_paragraph_id')!=before for n in [one,two])
            or first['text_layer']!=last['text_layer'] or last['text_layer']!='received_chapter'
            or last['text']!='黃武中卒。子楷，襲爵領兵。'):
        return False
    raw=(Path(root)/chapter['source']['raw_path']).read_bytes()
    if sha256(raw).hexdigest()!=chapter['source']['raw_file_sha256'] or raw.decode().splitlines()[112]!='':
        return False
    evidence=a.get('evidence',[])
    if len(evidence)!=2:return False
    for role,para,term,surface,ev in [('object',first,'盛建計','盛',evidence[0]),('subject',last,'子楷','楷',evidence[1])]:
        if para['text'].count(term)!=1 or (ev.get('chapter_id'),ev.get('paragraph_id'),ev.get('quote'))!=(cid,para['id'],para['text']):
            return False
        at=para['text'].index(term)+term.index(surface)
        if not any(m.get('kind')=='person' and m['surface']==surface and m['start']==at
                   and m['id']==ev.get(role+'_person_mention_id') and m['person_id']==a.get(role+'_person_id')for m in para['mentions']):
            return False
    return True

def xusheng_death(context,event,chapter,evidence,root):
    cid='c-sanguozhi-055-xusheng'
    if (event.get('event_type'),event.get('source_term'),event.get('date_expression'))!=('death','黃武中卒','黃武中'):return False
    if len(chapter.get('paragraphs',[]))<4:return False
    first,one,two,last=chapter['paragraphs'][-4:]
    child=next((m for m in last['mentions']if m['surface']=='楷'),None)
    if not child:return False
    if context!={'kind':'sanguozhi055_xusheng_death','paragraph_id':first['id'],'person_mention_id':context.get('person_mention_id'),'quote':first['text'],'intervening_paragraph_ids':[one['id'],two['id']]}:return False
    if (evidence.get('paragraph_id'),evidence.get('chapter_id'),evidence.get('quote'))!=(last['id'],cid,last['text']):return False
    a={'id':'a-wu055-xukai-father','predicate':'father','qualifiers':{'source_term':'子楷，襲爵領兵'},'subject_person_id':child['person_id'],'object_person_id':event['person_id'],'context':{'kind':'sanguozhi055_xukai_after_notes','paragraph_ids':[first['id'],last['id']]},'evidence':[{'chapter_id':cid,'paragraph_id':first['id'],'quote':first['text'],'object_person_mention_id':context['person_mention_id']},{'chapter_id':cid,'paragraph_id':last['id'],'quote':last['text'],'subject_person_mention_id':child['id']}]}
    return xukai_father(a,chapter,root)
