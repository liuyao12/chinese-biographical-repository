"""吳宗室傳的親屬原稱與具名字位。"""
RULES = {
 'shao-he': ('shao','047','paternal_uncle','伯父河','孫韶字','孫韶','伯父河','河',{}),
 'miao-an': ('ben','034','paternal_uncle','叔父安、熙、績','苗弟旅','苗','叔父安、熙、績','安',{}),
 'miao-xi': ('ben','034','paternal_uncle','叔父安、熙、績','苗弟旅','苗','叔父安、熙、績','熙',{}),
 'miao-ji': ('ben','034','paternal_uncle','叔父安、熙、績','苗弟旅','苗','叔父安、熙、績','績',{}),
 'yi-succession': ('huan','029','ritual_successor_of','封承庶弟壹奉奐後','承庶弟壹奉','壹','壹奉奐後','奐',{'succession_kind':'奉後'}),
 'fu-raised': ('ben','032','raised_by','弟輔嬰孩，賁自贍育','弟輔嬰孩','輔','賁自贍育','賁',{'care_basis':'贍育'}),
 'qiao-adoption': ('yi','041','adoptive_father','亮養子喬','由亮養子喬','喬','由亮養子喬','亮',{}),
 'ju-affinity': ('huan','029','affinity_unspecified','據、胤皆壹皆之妹夫也','據、胤皆壹皆之妹夫也','據','據、胤皆壹皆之妹夫也','壹',{'relationship_basis':'具名妹夫'}),
 'yin-affinity': ('huan','029','affinity_unspecified','據、胤皆壹皆之妹夫也','據、胤皆壹皆之妹夫也','胤','據、胤皆壹皆之妹夫也','壹',{'relationship_basis':'具名妹夫'}),
 'hui-ben': ('ben','034-pei03-01','ancestor','賁曾孫惠','賁曾孫惠','惠','賁曾孫惠','賁',{'generation_distance':3,'connecting_person_ids':None}),
 'he-clan': ('shao','047-pei01-01','kinship_unspecified','河，坚族子也','河，坚族子也','河','河，坚族子也','坚',{}),
 'xiang-clan': ('ben','032-pei01-01','kinship_unspecified','策族兄香','策族兄香','香','策族兄香','策',{}),
 'ru-jian': ('ben','032-pei01-02','agnatic_cousin','堅再從弟也','父孺，字仲孺','孺','堅再從弟也','堅',{}),
}
def anchor(p,ctx,word):
    if p['text'].count(ctx)!=1:return None
    i=p['text'].index(ctx)+ctx.index(word)
    return next((m for m in p['mentions']if m['start']==i and m['end']==i+len(word) and m['surface']==word and m['kind']=='person'),None)
def valid(a,paragraphs):
    q=a.get('qualifiers',{});k=q.get('sanguozhi051_family')
    if k not in RULES or len(a.get('evidence',[]))!=1:return False
    slug,line,pred,term,sc,sw,oc,ow,extra=RULES[k]
    cid='c-sanguozhi-051-'+slug;pid=cid+':line'+line;e=a['evidence'][0];hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid or (e.get('chapter_id'),e.get('paragraph_id'))!=(cid,pid):return False
    p=hit[1]
    if (p['source_position']['revision_id']!=12758417 or e.get('quote')!=p['text'] or p['text'].count(term)!=1 or
        a.get('predicate')!=pred or q!={'sanguozhi051_family':k,'source_term':term,**extra}):return False
    for end,ctx,w in [('subject',sc,sw),('object',oc,ow)]:
        m=anchor(p,ctx,w)
        if not m or (a.get(end+'_person_id'),e.get(end+'_person_mention_id'))!=(m['person_id'],m['id']):return False
    return True
