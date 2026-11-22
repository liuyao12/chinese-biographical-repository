# coding: utf-8
"""Check literal kin expressions, role anchors and generation direction inside bounded accounts."""
def valid(a,e,c):
    bindings = {
        'a-qi032-shu-dai': ('c-nanqishu-032-zhangshu',1513918,46,'兄子瓌、弟恕','恕','岱','brother'),
        'a-qi032-bian-dai': ('c-nanqishu-032-zhangdai-family',1513918,34,'弟廣州刺史辨','辨','岱','brother'),
        'a-qi032-dai-mother': ('c-nanqishu-032-zhangdai-family',1513918,38,'母年八十','岱','母','mother'),
        'a-qi032-yizong-daolian': ('c-songshu-051-yizong-xia-family',1959959,27,'道憐六子','義宗','道憐','father'),
        'a-qi032-xia-yizong': ('c-songshu-051-yizong-xia-family',1959959,111,'義宗子 遐','遐','義宗','father'),
        'a-qi032-faxian-xiuzhi': ('c-nanqishu-032-chuxuan',1513918,53,'祖秀之，宋太常。父法顯','法顯','秀之','father'),
        'a-qi032-xuan-faxian': ('c-nanqishu-032-chuxuan',1513918,53,'父法顯','褚炫','法顯','father'),
        'a-qi032-xuan-xiuzhi': ('c-nanqishu-032-chuxuan',1513918,53,'祖秀之','褚炫','秀之','grandfather'),
        'a-qi032-zhao-faxian': ('c-nanshi-028-chuzhao-father',1511857,141,'父法顯','炤','法顯','father'),
        'a-qi032-ancheng-hao-father': ('c-nanqishu-035-ancheng-hao-parent',2401782,39,'太祖第六子','安成恭王暠','太祖','father'),
    }
    key=bindings.get(a.get('id'))
    if not key:
        return False
    cid,revision,line,term,sub,obj,pred=key
    if (c['id'],c['source']['revision_id'],a['predicate'],a['qualifiers']['source_term'])!=(cid,revision,pred,term):
        return False
    p=next((x for x in c['paragraphs'] if x['id']==e['paragraph_id']),None)
    if not p or e.get('quote')!=p['text'] or p['source_position']['first_line']!=line or p['text'].count(term)!=1:
        return False
    for role,word in [('subject',sub),('object',obj)]:
        ref=e.get(role+'_person_reference_id');mid=e.get(role+'_person_mention_id')
        pool=c['annotation'].get('person_reference_occurrences',[]) if ref else p['mentions']
        matches=[x for x in pool if x['id']==(ref or mid) and x['person_id']==a[role+'_person_id'] and x['surface']==word]
        context = {('a-qi032-shu-dai','subject'):'弟恕',('a-qi032-shu-dai','object'):'岱曰：「恕未閑',('a-qi032-dai-mother','subject'):'岱便去官',('a-qi032-dai-mother','object'):'母年八十'}.get((a['id'],role),word)
        if p['text'].count(context)!=1 or context.count(word)!=1:
            return False
        expected=p['text'].index(context)+context.index(word)
        if len(matches)!=1 or p['text'][matches[0]['start']:matches[0]['end']]!=word or matches[0]['start']!=expected:
            return False
    if a['id']=='a-qi032-xia-yizong':
        if p['source_position'].get('source_layer')!='editorial_wikisource_heading':
            return False
        sections=[x['text'] for x in c['paragraphs']]
        return (any('義融弟義宗' in x for x in sections) and any('子懷侯玠嗣' in x and '弟秉以子承繼封' in x for x in sections)
                and any('謨弟遐字彦道' in x for x in sections) and '兄秉既死，齊王遣誅之。' in sections)
    return True
