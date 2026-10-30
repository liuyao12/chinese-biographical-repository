// Explicit validated source-event groups only. No inference from names, dates, or prose.
function originalSourceGroupedLifeEvents(events,groups=[],own=new Set()) {
  if (!Array.isArray(groups)) throw new Error('Invalid life-event group list');
  if (!groups.length) return events;
  const seen=new Set(),memberIds=new Set(),representatives=new Map(),hidden=new Set();
  for (const g of groups) {
    if (!g || g.kind!=='fixed_jin076_jin098_same_death' || g.event_type!=='death'
        || g.status!=='editorial_provisional' || g.human_reviewed!==false || g.date!==null
        || g.date_status!=='not_reported' || !own.has(g.person_id) || seen.has(g.id)
        || !Array.isArray(g.member_event_ids) || g.member_event_ids.length!==2
        || new Set(g.member_event_ids).size!==2 || !g.member_event_ids.includes(g.representative_event_id)
        || !Array.isArray(g.member_bindings) || g.member_bindings.length!==2
        || !Array.isArray(g.evidence) || g.evidence.length!==2) throw new Error('Invalid bounded same-death group');
    const members=g.member_event_ids.map(id=>{
      const matches=events.filter(e=>e.id===id);
      if (matches.length!==1 || memberIds.has(id)) throw new Error('Missing or repeated life-event group member');
      const e=matches[0];
      if(e.person_id!==g.person_id || e.event_type!=='death' || e.date_expression!==null
          || e.normalized_date!=null || e.normalized_date_range!=null || e.chinese_civil_year!=null) throw new Error('Same-death person/type/date mismatch');
      return e;
    });
    const paragraphs=['c-jinshu-076-wangbin:line050','c-jinshu-098-wangdun-comparison:p034'];
    for(let i=0;i<2;i++){
      const b=g.member_bindings[i],e=g.evidence[i],event=members[i];
      if(!b || b.event_id!==event.id || b.person_mention_id!==e.person_mention_id || e.paragraph_id!==paragraphs[i]
          || !event.evidence?.some(raw=>raw.person_mention_id===b.event_evidence_mention_id
              && ['work_id','book_id','source_id','chapter_id','paragraph_id','quote'].every(k=>raw[k]===e[k]))) throw new Error('Same-death source witness mismatch');
    }
    const representative=members.find(e=>e.id===g.representative_event_id);
    if(representative.id!==g.member_event_ids[1])throw new Error('Unexpected representative source');
    const row={...representative,evidence:g.evidence.map(e=>({...e})),source_event_ids:[...g.member_event_ids],source_event_group:{...g,date:null}};
    const first=events.find(e=>g.member_event_ids.includes(e.id));representatives.set(first.id,row);
    for(const e of members){memberIds.add(e.id);if(e.id!==first.id)hidden.add(e.id);}
    seen.add(g.id);
  }
  return events.filter(e=>!hidden.has(e.id)).map(e=>representatives.get(e.id)||e);
}

function jiaSourceGroup(events,g,own) {
  if(!g || g.kind!=='fixed_jin039_jin040_jiachong_same_death' || g.event_type!=='death'
      || g.status!=='editorial_provisional' || g.human_reviewed!==false || !own.has(g.person_id)
      || g.date_status!=='year_month_reported_by_representative_source'
      || (!g.date || Object.keys(g.date).sort().join(',')!=='calendar,day,month,year' || g.date.year!==282 || g.date.calendar!=='chinese_civil' || g.date.month!==4 || g.date.day!==null)
      || !Array.isArray(g.member_event_ids) || g.member_event_ids.length!==2 || new Set(g.member_event_ids).size!==2
      || g.representative_event_id!==g.member_event_ids[1] || !Array.isArray(g.evidence) || g.evidence.length!==2
      || !Array.isArray(g.member_bindings) || g.member_bindings.length!==2) throw new Error('Invalid Jia same-death group');
  const members=g.member_event_ids.map(id=>{const found=events.filter(e=>e.id===id);if(found.length!==1)throw new Error('Missing Jia death member');return found[0];});
  const [old,newer]=members;
  if(members.some(e=>e.person_id!==g.person_id || e.event_type!=='death')
      || old.date_expression!==null || old.normalized_date!=null || old.normalized_date_range!=null
      || newer.date_expression!=='太康三年四月' || newer.normalized_date?.year!==282 || newer.normalized_date?.calendar!=='chinese_civil'
      || newer.source_date_parts?.kind!=='fixed_jin040_explicit_chinese_calendar_month' || newer.source_date_parts?.month!==4
      || newer.source_date_parts?.day!==null || newer.source_date_parts?.person_id!==g.person_id
      || newer.source_date_parts?.life_event_id!==newer.id)throw new Error('Jia death/date mismatch');
  const paragraphs=['c-jinshu-039-wangxun-feng:xu-full:l092','c-jinshu-040-wyd1739-jiachong:p012'];
  members.forEach((e,i)=>{const q=g.evidence[i],b=g.member_bindings[i];
    if(!q || !b || q.paragraph_id!==paragraphs[i] || b.event_id!==e.id || b.person_mention_id!==q.person_mention_id
        || !e.evidence?.some(x=>x.person_mention_id===b.event_evidence_mention_id
          && ['work_id','book_id','source_id','chapter_id','paragraph_id','quote'].every(k=>x[k]===q[k])))throw new Error('Jia witness mismatch');
  });
  return {...newer,evidence:g.evidence.map(e=>({...e})),source_event_ids:[...g.member_event_ids],source_event_group:{...g,date:{...g.date}}};
}
export function sourceGroupedLifeEvents(events,groups=[],own=new Set()) {
  if(!Array.isArray(groups))throw new Error('Invalid life-event group list');
  const jia=groups.filter(g=>g?.kind==='fixed_jin039_jin040_jiachong_same_death');
  const old=groups.filter(g=>g?.kind!=='fixed_jin039_jin040_jiachong_same_death');
  const ids=new Set(),groupIds=new Set();
  for(const g of groups){if(!g || groupIds.has(g.id) || !Array.isArray(g.member_event_ids))throw new Error('Invalid/repeated group');groupIds.add(g.id);for(const id of g.member_event_ids){if(ids.has(id))throw new Error('Repeated grouped event');ids.add(id);}}
  let result=originalSourceGroupedLifeEvents(events,old,own);
  for(const g of jia){const row=jiaSourceGroup(events,g,own),first=events.find(e=>g.member_event_ids.includes(e.id));result=result.filter(e=>!g.member_event_ids.includes(e.id)||e.id===first.id).map(e=>e.id===first.id?row:e);}
  return result;
}
