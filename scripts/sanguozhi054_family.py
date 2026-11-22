RULES={
 'su-grandmother':('lusu','041','grandmother','與祖母居','魯肅字子敬','魯肅','與祖母居','祖母',{}),
 'yu-jing':('zhouyu','011','kinship_unspecified','從祖父景','周瑜字公瑾','周瑜','從祖父景','景',{}),
 'yu-shang':('zhouyu','011','paternal_uncle','瑜從父尚','瑜從父尚','瑜','瑜從父尚','尚',{}),
 'jun-yu':('zhouyu','038','paternal_uncle','瑜兄子峻','瑜兄子峻','峻','瑜兄子峻','瑜',{}),
 'yin-shu':('zhouyu','011','agnatic_cousin','袁術遣從弟胤','袁術遣從弟胤','胤','袁術遣從弟胤','袁術',{}),
}
def anchor(p,ctx,word):
    if p['text'].count(ctx)!=1:return None
    i=p['text'].index(ctx)+ctx.index(word)
    return next((m for m in p['mentions']if m['start']==i and m['end']==i+len(word) and m['surface']==word and m['kind']=='person'),None)
def valid(a,paragraphs):
    q=a.get('qualifiers',{});k=q.get('sanguozhi054_family')
    if k not in RULES or len(a.get('evidence',[]))!=1:return False
    slug,line,pred,term,sc,sw,oc,ow,extra=RULES[k]
    cid='c-sanguozhi-054-'+slug;pid=cid+':line'+line;e=a['evidence'][0];hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid or (e.get('chapter_id'),e.get('paragraph_id'))!=(cid,pid):return False
    p=hit[1]
    if (p['source_position']['revision_id']!=2387393 or e.get('quote')!=p['text'] or p['text'].count(term)!=1 or
        a.get('predicate')!=pred or q!={'sanguozhi054_family':k,'source_term':term,**extra}):return False
    for end,ctx,w in [('subject',sc,sw),('object',oc,ow)]:
        m=anchor(p,ctx,w)
        if not m or (a.get(end+'_person_id'),e.get(end+'_person_mention_id'))!=(m['person_id'],m['id']):return False
    return True
