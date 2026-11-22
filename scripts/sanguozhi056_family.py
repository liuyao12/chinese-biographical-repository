"""逐詞核治姊子、嗣父及從父等六條吳書原稱。"""
RULES = {
    'ran-uncle': ('zhuran', '022', 'maternal_uncle', '治姊子也', '朱然字義封', '朱然', '治姊子也', '治', {}),
    'ran-adoption': ('zhuran', '022', 'adoptive_father', '初治未有子，然年十三，乃啟策乞以為嗣', '朱然字義封', '朱然', '初治未有子', '治', {}),
    'ji-cai': ('shiji', '037', 'paternal_uncle', '叔父才卒', '績字公緒', '績', '叔父才卒', '才', {}),
    'yi-ju': ('zhuyi', '072', 'paternal_uncle', '異從父驃騎將軍據', '異從父驃騎將軍據', '異', '異從父驃騎將軍據', '據', {}),
    'lin-jun': ('lvju', '056', 'agnatic_cousin', '聞孫峻死，以從弟綝自代', '以從弟綝自代', '綝', '聞孫峻死', '孫峻', {}),
    'lü-lin': ('lvju', '056', 'agnatic_cousin', '又遣從兄慮以都下兵逆據於江都', '又遣從兄慮', '慮', '綝聞之，使中書奉詔', '綝', {}),
}
def anchor(p,ctx,word):
    if p['text'].count(ctx)!=1:return None
    i=p['text'].index(ctx)+ctx.index(word)
    return next((m for m in p['mentions']if m['start']==i and m['end']==i+len(word) and m['surface']==word and m['kind']=='person'),None)
def valid(a,paragraphs):
    q=a.get('qualifiers',{});k=q.get('sanguozhi056_family')
    if k not in RULES or len(a.get('evidence',[]))!=1:return False
    slug,line,pred,term,sc,sw,oc,ow,extra=RULES[k]
    cid='c-sanguozhi-056-'+slug;pid=cid+':line'+line;e=a['evidence'][0];hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid or (e.get('chapter_id'),e.get('paragraph_id'))!=(cid,pid):return False
    p=hit[1]
    if (p['source_position']['revision_id']!=12760859 or e.get('quote')!=p['text'] or p['text'].count(term)!=1 or
        a.get('predicate')!=pred or q!={'sanguozhi056_family':k,'source_term':term,**extra}):return False
    for end,ctx,w in [('subject',sc,sw),('object',oc,ow)]:
        m=anchor(p,ctx,w)
        if not m or (a.get(end+'_person_id'),e.get(end+'_person_mention_id'))!=(m['person_id'],m['id']):return False
    return True
