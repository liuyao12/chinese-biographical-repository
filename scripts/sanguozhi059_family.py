"""按吳主五子傳的具名原句及裴注界線核親屬。"""
from hashlib import sha256

RULES = {
    'ji-grandmother': ('ba','043','grandmother','祖母','削基、壹爵土','基','祖母謝姬','謝姬',{'lineage':'unspecified','generation_difference':-2,'parent_person_id':None}),
    'yi-grandmother': ('ba','043','grandmother','祖母','削基、壹爵土','壹','祖母謝姬','謝姬',{'lineage':'unspecified','generation_difference':-2,'parent_person_id':None}),
    'zhang-xiu': ('he','032','paternal_uncle','和妃叔父張休','和妃叔父','妃','叔父張休','張休',{}),
    'zhuge-ke': ('he','034','maternal_uncle','恪即和妃張之舅也','恪即和妃張','妃張','恪即和妃張','恪',{'lineage':'maternal','generation_difference':-1,'mother_person_id':None}),
    'jun-zhang': ('he','036-pei02-01','grandfather','俊，張承外孫','俊，張承外孫','俊','俊，張承外孫','張承',{'lineage':'maternal','generation_difference':-2,'mother_person_id':None}),
    'liang-fen': ('fen','048-pei02-01','brother','孤有兄獨爾云何','載亮詔曰','亮','齊王奮前坐','齊王奮',{}),
    'left-wang': ('fen','050','spouse','孫皓左夫人王氏卒','左夫人王氏卒','王氏','孫皓左夫人','孫皓',{}),
}
CHILDREN = {'pan':'璠','xi':'希','ying':'英'}

def anchor(paragraph, context, word):
    text = paragraph['text']
    if text.count(context) != 1 or context.count(word) != 1:
        return None
    offset = text.index(context) + context.index(word)
    return next((m for m in paragraph['mentions'] if m['kind']=='person' and
                 (m['start'],m['end'],m['surface']) == (offset,offset+len(word),word)),None)

def valid(assertion, paragraphs):
    qualifiers = assertion.get('qualifiers',{})
    tag = qualifiers.get('sanguozhi059_family')
    if tag not in RULES or len(assertion.get('evidence',[]))!=1:
        return False
    slug,line,predicate,term,subctx,subword,objctx,objword,extra=RULES[tag]
    cid='c-sanguozhi-059-'+slug
    pid=cid+':line'+line
    e=assertion['evidence'][0]
    hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid:
        return False
    p=hit[1]
    if (assertion['predicate']!=predicate or qualifiers!={'sanguozhi059_family':tag,'source_term':term,**extra}
        or p['source_position']['revision_id']!=2085159 or p['text'].count(term)!=1
        or (e.get('paragraph_id'),e.get('chapter_id'),e.get('quote'))!=(pid,cid,p['text'])):
        return False
    for end,ctx,word in [('subject',subctx,subword),('object',objctx,objword)]:
        m=anchor(p,ctx,word)
        if not m or (assertion.get(end+'_person_id'),e.get(end+'_person_mention_id'))!=(m['person_id'],m['id']):
            return False
    return True

def deng_children(assertion, chapter):
    ctx = assertion.get('context',{})
    key=ctx.get('child')
    cid='c-sanguozhi-059-deng'
    if key not in CHILDREN or chapter.get('id')!=cid:
        return False
    segs=chapter['paragraphs']
    listing=next((i for i,p in enumerate(segs) if p['id']==cid+':line020'),-1)
    if listing<2:
        return False
    prior,annotation,children=segs[listing-2:listing+1]
    name=CHILDREN[key]
    ev=assertion.get('evidence',[])
    term='子璠、希，皆早卒，次子英'
    if (assertion.get('predicate')!='father' or assertion['qualifiers']!={'source_term':term}
        or ctx!={'kind':'wu059_deng_children','child':key,'paragraph_ids':[prior['id'],children['id']]}
        or not prior['id'].endswith(':line018') or not annotation['id'].endswith(':line018-pei01-01')
        or not all(p['source_position']['revision_id']==2085159 for p in [prior,annotation,children])
        or prior['text_layer']!=children['text_layer'] or children['text_layer']!='received_chapter'
        or annotation['text']!='《吳書》曰：初葬句容，置園邑，奉守如法，後三年改葬蔣陵。'
        or not prior['text'].endswith('謚登曰宣太子。') or not children['text'].startswith(term)
        or len(ev)!=2 or any(e.get('chapter_id')!=cid or e.get('paragraph_id')!=p['id']
                            or e.get('quote')!=p['text'] for e,p in zip(ev,[prior,children]))):
        return False
    father=anchor(prior,'謚登曰宣太子','登')
    child=anchor(children,term,name)
    return bool(father and child and
        (assertion.get('object_person_id'),ev[0].get('object_person_mention_id'))==(father['person_id'],father['id']) and
        (assertion.get('subject_person_id'),ev[1].get('subject_person_mention_id'))==(child['person_id'],child['id']))
