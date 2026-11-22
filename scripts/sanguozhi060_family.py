"""以固定正文及引書錨定卷六十的婚親、伯叔父、外祖父。"""
RULES={
  'he-uncle': ('heqi', '011-pei01-01', 'paternal_uncle', '齐伯父纯', '齐伯父纯', '齐', '齐伯父纯', '纯', {}),
  'xiong-zhang': ('heqi', '011', 'father_in_law', '雅與女婿何雄', '女婿何雄', '何雄', '雅與女婿何雄', '雅', {}),
  'wu-sun': ('quancong', '042-pei01-01', 'grandfather', '小子吴，孙权外孙', '小子吴', '吴', '孙权外孙', '孙权', {'lineage': 'maternal', 'generation_difference': -2, 'mother_person_id': None}),
  'yi-uncle-禕': ('quancong', '042', 'paternal_uncle', '懌兄子禕、儀、靜', '懌兄子禕、儀、靜', '禕', '懌兄子禕、儀、靜', '懌', {}),
  'yi-uncle-儀': ('quancong', '042', 'paternal_uncle', '懌兄子禕、儀、靜', '懌兄子禕、儀、靜', '儀', '懌兄子禕、儀、靜', '懌', {}),
  'yi-uncle-靜': ('quancong', '042', 'paternal_uncle', '懌兄子禕、儀、靜', '懌兄子禕、儀、靜', '靜', '懌兄子禕、儀、靜', '懌', {}),
}
def anchor(p,ctx,word):
    if p['text'].count(ctx)!=1:return None
    i=p['text'].index(ctx)+ctx.index(word)
    return next((m for m in p['mentions']if m['start']==i and m['end']==i+len(word) and m['surface']==word and m['kind']=='person'),None)
def valid(a,paragraphs):
    q=a.get('qualifiers',{});k=q.get('sanguozhi060_family')
    if k not in RULES or len(a.get('evidence',[]))!=1:return False
    slug,line,pred,term,sc,sw,oc,ow,extra=RULES[k]
    cid='c-sanguozhi-060-'+slug;pid=cid+':line'+line;e=a['evidence'][0];hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid or (e.get('chapter_id'),e.get('paragraph_id'))!=(cid,pid):return False
    p=hit[1]
    if (p['source_position']['revision_id']!=2120830 or e.get('quote')!=p['text'] or p['text'].count(term)!=1 or
        a.get('predicate')!=pred or q!={'sanguozhi060_family':k,'source_term':term,**extra}):return False
    for end,ctx,w in [('subject',sc,sw),('object',oc,ow)]:
        m=anchor(p,ctx,w)
        if not m or (a.get(end+'_person_id'),e.get(end+'_person_mention_id'))!=(m['person_id'],m['id']):return False
    return True
from pathlib import Path
from hashlib import sha256
def continued_child(a, chapter, root):
    cid='c-sanguozhi-060-zhonglimu'
    if (chapter.get('id')!=cid or a.get('id')!='a-wu060-zhongliyi-father'
            or a.get('predicate')!='father' or a.get('qualifiers')!={'source_term':'子褘嗣，代領兵'}
            or chapter['source'].get('revision_id')!=2120830):
        return False
    before=cid+':line097';after=cid+':line099'
    if a.get('context')!={'kind':'sanguozhi060_zhongliyi_after_note','paragraph_ids':[before,after]}:
        return False
    ps=chapter['paragraphs']
    if [p['id']for p in ps[-4:]]!=[before,before+'-pei01-01',after,after+'-pei01-01']:
        return False
    first,one,last,_=ps[-4:]
    if (any(n.get('attachment',{}).get('received_paragraph_id')!=before for n in [one])
            or first['text_layer']!=last['text_layer'] or last['text_layer']!='received_chapter'
            or last['text']!='　　卒官。家無餘財，士民思之。子褘嗣，代領兵。'):
        return False
    raw=(Path(root)/chapter['source']['raw_path']).read_bytes()
    if sha256(raw).hexdigest()!=chapter['source']['raw_file_sha256'] or raw.decode().splitlines()[97]!='':
        return False
    evidence=a.get('evidence',[])
    if len(evidence)!=2:return False
    for role,para,term,surface,ev in [('object',first,'乃以牧為平魏將軍','牧',evidence[0]),('subject',last,'子褘嗣','褘',evidence[1])]:
        if para['text'].count(term)!=1 or (ev.get('chapter_id'),ev.get('paragraph_id'),ev.get('quote'))!=(cid,para['id'],para['text']):
            return False
        at=para['text'].index(term)+term.index(surface)
        if not any(m.get('kind')=='person' and m['surface']==surface and m['start']==at
                   and m['id']==ev.get(role+'_person_mention_id') and m['person_id']==a.get(role+'_person_id')for m in para['mentions']):
            return False
    return True
