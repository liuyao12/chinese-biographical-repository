"""卷五十各親稱限於該句兩端，撫養者與生母分錄。"""
import hashlib

RULES = {
 'bu-clan': ('bu','031','kinship_unspecified','與丞相騭同族','步夫人','步夫人','丞相騭','騭'),
 'xu-nurture': ('xu','028','raised_by','使母養子登','母養子登','登','琨生夫人','夫人'),
 'he-nurture': ('he','058','raised_by','遂拊育皓及其三弟','遂拊育皓','皓','孫和何姬','何姬'),
 'teng-clan': ('teng','062','kinship_unspecified','故太常胤之族女也','孫皓滕夫人','滕夫人','太常胤','胤'),
 'quan-grandkin': ('quan','050','kinship_unspecified','（尚）從祖母公主愛之','（尚）','尚','從祖母公主','公主'),
}

def valid(assertion, paragraphs):
    q=assertion.get('qualifiers',{});rule=RULES.get(q.get('sanguozhi050_family'))
    if rule is None or len(assertion.get('evidence',[]))!=1:return False
    slug,line,pred,term,subctx,subword,objctx,objword=rule
    cid='c-sanguozhi-050-'+slug;pid=cid+':line'+line;e=assertion['evidence'][0];hit=paragraphs.get(pid)
    if not hit or hit[0]!=cid or e.get('paragraph_id')!=pid:return False
    p=hit[1];t=p['text'];pos=p['source_position']
    if pos['revision_id']!=2085144 or e.get('quote')!=t or t.count(term)!=1 or q.get('source_term')!=term or assertion.get('predicate')!=pred:return False
    if not all(q.get(k) is None for k in ('shared_mother','shared_father','exact_distance','connecting_person_ids')):return False
    for end,ctx,word in [('subject',subctx,subword),('object',objctx,objword)]:
        if t.count(ctx)!=1 or word not in ctx:return False
        at=t.index(ctx)+ctx.index(word);m=next((m for m in p['mentions']if m['start']==at and m['end']==at+len(word)),None)
        if m is None or m['surface']!=word or e.get(end+'_person_mention_id')!=m['id'] or assertion.get(end+'_person_id')!=m['person_id']:return False
    return True
