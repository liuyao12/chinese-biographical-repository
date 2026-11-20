"""An unresolved identity group suppresses only its cited family edges."""
def parallel_child_errors(group, assertions, person_ids, chapters):
    candidates = group.get('candidate_person_ids', [])
    parent = group.get('common_person_id')
    ids = group.get('assertion_ids', [])
    refs = group.get('references', [])
    if (group.get('predicate') != 'father'
            or group.get('status') != 'unresolved'
            or group.get('same_person', False) is not None
            or group.get('distinct_people', False) is not None
            or group.get('human_reviewed') is not False or not group.get('rationale')
            or len(candidates) != 2 or len(set(candidates)) != 2
            or not set(candidates).issubset(person_ids) or parent not in person_ids or parent in candidates
            or len(ids) != 2 or len(set(ids)) != 2
            or [r.get('assertion_id') for r in refs] != ids):
        return ['平行子嗣記載須綁共同父親、兩個來源人物及明示同異未決']
    works, children = set(), set()
    for ref in refs:
        chapter = chapters.get(ref.get('chapter_id'), {})
        paragraph = next((p for p in chapter.get('paragraphs', []) if p['id'] == ref.get('paragraph_id')), {})
        assertion = assertions.get(ref['assertion_id'], {})
        child = assertion.get('subject_person_id')
        term = assertion.get('qualifiers', {}).get('source_term')
        span = ref.get('span', {})
        start, end = span.get('start'), span.get('end')
        text = paragraph.get('text', '')
        source_keys = ('work_id', 'book_id', 'source_id', 'chapter_id', 'paragraph_id', 'quote')
        evidence = next((e for e in assertion.get('evidence', [])
                         if all(e.get(k) == ref.get(k) for k in source_keys)), {})
        parent_anchor = any(
            any(m.get('id') == e.get('object_person_mention_id') and m.get('person_id') == parent
                and m.get('kind') == 'person' for m in p.get('mentions', []))
            for p in chapter.get('paragraphs', [])
            for e in assertion.get('evidence', []) if e.get('paragraph_id') == p['id']
        )
        if (not chapter or not evidence or not parent_anchor or child not in candidates
                or ref.get('candidate_person_id') != child
                or assertion.get('object_person_id') != parent or assertion.get('predicate') != 'father'
                or assertion.get('status') != 'source_attested'
                or not all(ref.get(k) == chapter.get(k) for k in ('work_id', 'book_id', 'source_id'))
                or type(ref.get('revision_id')) is not int or ref['revision_id'] != chapter['source'].get('revision_id')
                or type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text)
                or text[start:end] != span.get('surface') or span.get('surface') != term
                or not isinstance(term, str) or not term.startswith('子')
                or not isinstance(ref.get('quote'), str) or not ref['quote'].startswith(term)
                or not text.startswith(ref['quote'], start)
                or not any(m.get('id') == evidence.get('subject_person_mention_id')
                           and m.get('person_id') == child and m.get('kind') == 'person'
                           and m['start'] == start + 1 and m['end'] == end for m in paragraph.get('mentions', []))):
            return ['平行子嗣記載缺固定版本、原句、子名錨點或相符父系陳述']
        children.add(child)
        works.add(chapter['work_id'])
    if len(works) != 2 or children != set(candidates):
        return ['平行子嗣記載須分屬兩書，來源端點須各對應一名候選']
    return []


def group_errors(chapter, assertions, person_ids, chapters=None):
 errors=[];seen=set();claimed=set();local={p['id']:p for p in chapter['paragraphs']}
 for g in chapter.get('annotation',{}).get('unresolved_relation_identity_groups',[]):
  def check(ok,msg):
   if not ok:errors.append('未決配偶同人組 '+str(g.get('id'))+'：'+msg)
  check(bool(g.get('id'))and g['id']not in seen,'ID重複或缺失');seen.add(g.get('id'))
  candidates=g.get('candidate_person_ids',[]);common=g.get('common_person_id');aids=g.get('assertion_ids',[])
  if g.get('kind') == 'parallel_biography_child_attestations':
   check(not claimed.intersection(aids),'主張跨組重複');claimed.update(aids)
   check(g.get('source_fingerprint') == dict(chapter_id=chapter['id'], source_id=chapter['source_id'],
       revision_id=chapter['source'].get('revision_id'), source_commit=chapter['source'].get('source_commit'),
       raw_file_sha256=chapter['source'].get('raw_file_sha256')), '編輯暫掛篇指紋不符')
   errors.extend(parallel_child_errors(g, assertions, person_ids, chapters or {chapter['id']: chapter}))
   continue

  check(g.get('status')=='unresolved'and g.get('predicate')=='spouse'and 'same_person'in g and 'distinct_people'in g and g['same_person']is None and g['distinct_people']is None,'須同人／異人雙未決且僅配偶')
  check(g.get('human_reviewed')is False and bool(g.get('rationale')),'缺判讀資格')
  check(len(candidates)>=2 and len(set(candidates))==len(candidates)and set(candidates)<=set(person_ids)and common in person_ids and common not in candidates,'人物端點不符')
  check(len(aids)==len(candidates)and len(set(aids))==len(aids)and not claimed.intersection(aids),'主張數或跨組重複');claimed.update(aids)
  check(g.get('source_fingerprint')=={'chapter_id':chapter['id'],'source_id':chapter['source_id'],'revision_id':chapter['source'].get('revision_id'),'source_commit':chapter['source'].get('source_commit'),'raw_file_sha256':chapter['source'].get('raw_file_sha256')},'固定見證指紋不符')
  refs=g.get('references',[]);check(len(refs)==len(aids),'每主張須一精確來源')
  endpoints=[]
  for aid in aids:
   a=assertions.get(aid);rs=[r for r in refs if r.get('assertion_id')==aid]
   if not a:check(False,'主張不存在');continue
   check(a.get('predicate')=='spouse'and a.get('status')=='source_attested','非明文配偶主張')
   ends={a.get('subject_person_id'),a.get('object_person_id')};other=ends-{common};check(common in ends and len(other)==1,'共同配偶端點錯誤');endpoints.extend(other)
   if len(rs)!=1:check(False,'來源主張未一對一');continue
   r=rs[0];check(all(r.get(k)==chapter.get(k)for k in ['work_id','book_id','source_id'])and r.get('chapter_id')==chapter['id'],'來源作品／卷篇不符');p=local.get(r.get('paragraph_id'));span=r.get('span',{});start=span.get('start');end=span.get('end')
   if not p:check(False,'非本章完整原段');continue
   valid=type(start)is int and type(end)is int and 0<=start<end<=len(p['text'])and p['text'][start:end]==span.get('surface')
   check(valid and r.get('quote')==p['text'],'字位或完整原段不符')
   mids={m['id']:m for m in p['mentions']}
   bound=any(e.get('chapter_id')==chapter['id']and e.get('paragraph_id')==p['id']and e.get('quote')==p['text']and all(e.get(k)in mids and mids[e[k]].get('person_id')==a[field]for k,field in [('subject_person_mention_id','subject_person_id'),('object_person_mention_id','object_person_id')])for e in a.get('evidence',[]))
   check(bound,'原主張雙端點錨點失配')
   candidate_mentions=[m for m in p['mentions']if m.get('person_id')in other]
   check(valid and any(start<=m['start']and m['end']<=end for m in candidate_mentions)and a.get('qualifiers',{}).get('source_term','\0')in span.get('surface',''),'局部原詞未包含候選配偶錨點')
  check(set(endpoints)==set(candidates),'候選與原主張非精確聯集')
 return errors


def relevant_groups(chapters, assertions, person_ids, selected):
 result=[]
 for c in chapters.values():
  errors=group_errors(c,assertions,person_ids,chapters)
  if errors:raise ValueError('；'.join(errors))
  for g in c.get('annotation',{}).get('unresolved_relation_identity_groups',[]):
   if set(selected).intersection([g['common_person_id']]+g['candidate_person_ids']):result.append(dict(g,chapter_id=c['id'],source_id=c['source_id']))
 return result
