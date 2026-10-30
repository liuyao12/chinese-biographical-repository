"""Only explicit source-validated event groups; no matching by names, dates or prose."""
TYPE='person_life_event_group_set'
def validated_groups(records,people,root,*,person_ids=None):
 if not isinstance(records,list)or not isinstance(people,dict)or not all(isinstance(r,dict)for r in records):raise ValueError('同事件catalog型別不符')
 chapters={r['id']:r for r in records if isinstance(r,dict)and r.get('record_type')=='marked_chapter'}
 staged=[c for c in chapters.values()if isinstance(c.get('annotation'),dict)and c['annotation'].get('life_stage')=='fixed_jin098_three_basics_and_same_death']
 try:from scripts.fixed_jin098_wangdun_life import stage_present,stage_subject_ids
 except ImportError:from fixed_jin098_wangdun_life import stage_present,stage_subject_ids
 root_active=stage_present(root);root_subjects,root_group_person=stage_subject_ids(root)if root_active else(set(),None)
 root_staged=root_active and(person_ids is None or bool(root_subjects.intersection(person_ids)))
 if root_staged or staged or any(r.get('record_type')==TYPE for r in records):
  try:from scripts.fixed_jin098_wangdun_life import catalog_basics_valid
  except ImportError:from fixed_jin098_wangdun_life import catalog_basics_valid
  catalog_basics_valid(records,root)
 events={}
 for r in records:
  if r.get('record_type')=='person_life_event_assertion_set':
   for e in r['events']:
    if e['id']in events:raise ValueError('同事件原event ID重複')
    events[e['id']]=e
 selected_events={e['id']for e in events.values()if person_ids is None or e.get('person_id')in person_ids}
 groups=[];seen=set();members=set()
 for r in records:
  if r.get('record_type')!=TYPE:continue
  if set(r)!={'format_version','record_type','work_id','chapter_id','groups'}or r['format_version']!='0.1'or not isinstance(r['groups'],list)or not r['groups']:raise ValueError('同事件資料集欄位不符')
  if r['work_id']!='w-jinshu'or r['chapter_id']not in('c-jinshu-098-wangdun-comparison','c-jinshu-040-wyd1739-jiachong'):raise ValueError('同死亡記錄作品/篇範圍不符')
  for g in r['groups']:
   if isinstance(g,dict)and g.get('kind')=='fixed_jin039_jin040_jiachong_same_death':
    if r['chapter_id']!='c-jinshu-040-wyd1739-jiachong':raise ValueError('賈充同死亡group篇不符')
    ids=g.get('member_event_ids')
    if not isinstance(ids,list)or len(ids)!=2 or not all(isinstance(x,str)for x in ids):raise ValueError('賈充同死亡成員格式不符')
    if person_ids is not None and g.get('person_id')not in person_ids and not selected_events.intersection(ids):continue
    try:from scripts.fixed_wuyingdian_jin040_jiachong import death_group_valid
    except ImportError:from fixed_wuyingdian_jin040_jiachong import death_group_valid
    if g.get('id')in seen or not death_group_valid(g,events,chapters,people,root):raise ValueError('賈充039/040同死來源/角色/日期/原事件不符')
    if any(eid in members for eid in ids):raise ValueError('同事件成員不得重複分組')
    seen.add(g['id']);members.update(ids);groups.append(g);continue
   if r['chapter_id']!='c-jinshu-098-wangdun-comparison':raise ValueError('076/098分組不可移至其他篇')
   if not isinstance(g,dict)or g.get('kind')!='fixed_jin076_jin098_same_death':raise ValueError('不支援的同事件資格')
   if not isinstance(g.get('member_event_ids'),list)or not all(isinstance(x,str)for x in g['member_event_ids']):raise ValueError('同事件成員格式不符')
   if person_ids is not None and g.get('person_id')not in person_ids and not selected_events.intersection(g['member_event_ids']):continue
   try:from scripts.fixed_jin098_wangdun_life import group_valid
   except ImportError:from fixed_jin098_wangdun_life import group_valid
   if g.get('id')in seen or not group_valid(g,events,chapters,people,root):raise ValueError('同死亡須有076/098完整兩源、真卒角色、原事件、未知年與AI資格')
   if any(eid in members for eid in g['member_event_ids']):raise ValueError('同事件成員不得重複分組')
   seen.add(g['id']);members.update(g['member_event_ids']);groups.append(g)
 required=(root_active and(person_ids is None or root_group_person in person_ids))or(bool(staged)and person_ids is None)
 if required and not groups:raise ValueError('已登記098生命階段不能漏同死亡分組')
 try:from scripts.fixed_wuyingdian_jin040_jiachong import death_group_required
 except ImportError:from fixed_wuyingdian_jin040_jiachong import death_group_required
 if death_group_required(root,person_ids)and not any(g.get('kind')=='fixed_jin039_jin040_jiachong_same_death'for g in groups):raise ValueError('賈充生命階段不得漏039/040同死亡分組')
 return groups
