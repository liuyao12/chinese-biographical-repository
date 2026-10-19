"""Project validated occurrence groups into reader profiles without losing anchors."""
try:
    from .occurrence_concordance import index_counts
except ImportError:
    from occurrence_concordance import index_counts


def profile_occurrences(bundle, chapters, work_titles):
    # Shared bundle/index contract; never recalculate frequency from len(mentions).
    totals = index_counts(bundle)
    passages = {p['id']:p for p in bundle['passages']}
    groups = [g for row in bundle['source_mention_summary'] for g in row['occurrence_groups']
              if g['kind'] == 'paragraph']
    by_mention = {}
    for group in groups:
        for mid in group['mention_ids']:
            if mid in by_mention:
                raise ValueError('profile occurrence group重複錨點')
            by_mention[mid] = group
    mentions = bundle['mentions']; by_chapter = {}
    if set(by_mention) != {m['id']for m in mentions}:
        raise ValueError('須先由concordance-aware bundle重建完整occurrence groups')
    for m in mentions:
        by_chapter.setdefault(m['chapter_id'],[]).append(m)
    result = []
    for cid, ms in sorted(by_chapter.items(),key=lambda x:chapters.get(x[0],{}).get('number',999)):
        ch = chapters.get(cid)
        if not ch:
            raise ValueError('人物提及的卷篇未列入閱讀目錄：'+cid)
        owned = [m for m in ms if by_mention[m['id']]['canonical_mention_id']==m['id']]
        m = (owned or ms)[0]; p = passages[m['paragraph_id']]; start = max(0,m['start']-35)
        count = len(owned)
        local_groups = {by_mention[m['id']]['canonical_mention_id']:by_mention[m['id']]for m in ms}
        row = {'number':ch['number'],'category':ch.get('category',''),'title':ch['title'],
            'paragraph_id':p['id'],'count':count,'raw_count':len(ms),'duplicate_count':len(ms)-count,
            'counting_policy':'independent_fixed_witness_occurrences',
            'quote':p['text'][start:m['end']+100],
            'paragraph_ids':sorted({m['paragraph_id']for m in ms}),
            'mention_ids':[m['id']for m in ms], 'mention_paragraph_ids':{m['id']:m['paragraph_id']for m in ms}, 'mention_id':m['id'], 'occurrence_groups':list(local_groups.values())}
        row.update({k:p[k]for k in ('work_id','book_id','chapter_id','source_id')})
        row['work_title'] = work_titles[p['work_id']]
        result.append(row)
    if sum(r['count']for r in result) != totals['paragraph_mention_count']:
        raise ValueError('profile／bundle／index位置數不一致')
    return result
