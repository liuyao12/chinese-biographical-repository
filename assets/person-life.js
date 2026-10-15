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
  return {
    birth: events.filter(e => e.event_type === 'birth').sort((a,b) => rank(a)-rank(b)),
    death: events.filter(e => e.event_type === 'death').sort((a,b) => rank(a)-rank(b)),
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
