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
    continuation_proofs = {}
    for key, fragment_kind in [('source_appellation_fragments','appellation'),('source_name_fragments','name')]:
        for proof in bundle.get(key, []):
            gid = proof['id'] if fragment_kind == 'appellation' else proof['complete_component']['record_id']
            if gid in continuation_proofs:
                raise ValueError('文字續接證據重複')
            continuation_proofs[gid] = (proof,fragment_kind)
    seen_continuations = set()
    for group in groups:
        if 'continuation_fragment_count' not in group:
            continue
        gid = group.get('source_fragment_group_id'); item = continuation_proofs.get(gid)
        if item is None:
            raise ValueError('文字續接須有完整來源證據')
        proof, fragment_kind = item
        complete_key = 'complete_appellation' if fragment_kind == 'appellation' else 'complete_component'
        if (gid in seen_continuations or group.get('counting_basis') != 'source_bound_fragment_continuation'
                or group.get('fragment_kind') != fragment_kind
                or group.get('canonical_mention_id') != proof.get('canonical_mention_id',proof['mention_ids'][0])
                or group.get('mention_ids') != proof['mention_ids']
                or type(group['continuation_fragment_count']) is not int
                or group['continuation_fragment_count'] != len(proof['mention_ids']) - 1
                or group['continuation_fragment_count'] < 1
                or group.get(complete_key) != proof[complete_key]):
            raise ValueError('人物頁文字續接group與完整來源證據不符')
        seen_continuations.add(gid)
    if seen_continuations != set(continuation_proofs):
        raise ValueError('人物頁不可漏計已驗文字續接')
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
    for cid, ms in sorted(by_chapter.items(),key=lambda x:(chapters.get(x[0],{}).get('number',999) is None, chapters.get(x[0],{}).get('number',999) or 0)):
        ch = chapters.get(cid)
        if not ch:
            raise ValueError('人物提及的卷篇未列入閱讀目錄：'+cid)
        owned = [m for m in ms if by_mention[m['id']]['canonical_mention_id']==m['id']]
        m = (owned or ms)[0]; p = passages[m['paragraph_id']]; start = max(0,m['start']-35)
        count = len(owned)
        local_groups = {by_mention[m['id']]['canonical_mention_id']:by_mention[m['id']]for m in ms}
        continuation = sum(g.get('continuation_fragment_count',0) for g in local_groups.values())
        row = {'number':ch['number'],'category':ch.get('category',''),'title':ch['title'],
            'paragraph_id':p['id'],'count':count,'raw_count':len(ms),'duplicate_count':len(ms)-count-continuation,
            **({'continuation_fragment_count':continuation} if continuation else {}),
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
