// Birth/death summaries use typed events, never office dates or age arithmetic.
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
