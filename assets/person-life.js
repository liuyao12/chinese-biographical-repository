// Birth/death summaries use typed events, never office dates or age arithmetic.
export function ageLabel(age) {
  if (!Number.isInteger(age.value) || age.reporting_status === 'qualified_report') return age.qualified_source_term || age.source_term || '來源報齡未定';
  return `${age.value} 歲（來源報齡）`;
}
export function summarizeLife(p) {
  const own = new Set(p.person_ids || [p.id]);
  const events = (p.life_events || []).filter(e => own.has(e.person_id));
  const decisions = p.life_event_date_decisions || [];
  const rank = e => {
    const decision = decisions.find(d => d.candidate_event_ids.includes(e.id));
    return decision?.status === 'editorial_provisional' ? (decision.preferred_event_id === e.id ? 0 : 2) : 1;
  };
  const provenance=new Set(['evidence','references','original_quote','rationale','reviewer','human_reviewed','model']);
  const facts=value=>Array.isArray(value)?value.map(facts):value && typeof value==='object'
    ?Object.fromEntries(Object.keys(value).filter(key=>!provenance.has(key)).sort().map(key=>[key,facts(value[key])])):value;
  function summary(kind) {
    const rows=[], grouped=new Map();
    for (const event of events.filter(e=>e.event_type===kind).sort((a,b)=>rank(a)-rank(b))) {
      const date=event.normalized_date || event.normalized_date_range;
      const key=date?JSON.stringify([rank(event),event.date_expression,facts(date)]):null;
      if (!key || !grouped.has(key)) {
        const row={...event,evidence:[...(event.evidence || [])]};rows.push(row);
        if (key) grouped.set(key,row);
      } else {
        const row=grouped.get(key);
        for (const evidence of event.evidence || []) {
          if (!row.evidence.some(e=>JSON.stringify(e)===JSON.stringify(evidence))) row.evidence.push(evidence);
        }
      }
    }
    return rows;
  }
  return {
    birth: summary('birth'),
    death: summary('death'),
    ages: (p.age_assertions || []).filter(e => own.has(e.person_id)),
  };
}


// Ranges are explicit data. Never choose either endpoint as an event year.
export function lifeYearLabel(event) {
  const date = event.normalized_date;
  if (date?.era_year) return `西元${date.era === 'BCE' ? '前' : ''}${date.era_year}年`;
  const range = event.normalized_date_range;
  const a = range?.earliest, b = range?.latest;
  if (!a?.era_year || !b?.era_year) return '';
  const prefix = p => `西元${p.era === 'BCE' ? '前' : ''}`;
  return `${prefix(a)}${a.era_year}至${a.era === b.era ? '' : prefix(b)}${b.era_year}年（暫定範圍）`;
}
