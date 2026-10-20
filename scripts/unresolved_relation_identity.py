"""An unresolved same/distinct identity group suppresses only its named spouse edges."""
def group_errors(chapter, assertions, person_ids):
 errors=[];seen=set();claimed=set();local={p['id']:p for p in chapter['paragraphs']}
 for g in chapter.get('annotation',{}).get('unresolved_relation_identity_groups',[]):
  def check(ok,msg):
   if not ok:errors.append('未決配偶同人組 '+str(g.get('id'))+'：'+msg)
  check(bool(g.get('id'))and g['id']not in seen,'ID重複或缺失');seen.add(g.get('id'))
  candidates=g.get('candidate_person_ids',[]);common=g.get('common_person_id');aids=g.get('assertion_ids',[])
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
  errors=group_errors(c,assertions,person_ids)
  if errors:raise ValueError('；'.join(errors))
  for g in c.get('annotation',{}).get('unresolved_relation_identity_groups',[]):
   if set(selected).intersection([g['common_person_id']]+g['candidate_person_ids']):result.append(dict(g,chapter_id=c['id'],source_id=c['source_id']))
 return result
