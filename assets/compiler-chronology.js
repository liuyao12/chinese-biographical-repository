// Explicit qualified timeline input. Never feed this into the direct death-year scalar.
export function compilerChronologyPlacements(person) {
  const own = new Set([person?.id, ...(Array.isArray(person?.person_ids) ? person.person_ids : [])]);
  const events = Array.isArray(person?.life_events) ? person.life_events : [];
  return (Array.isArray(person?.source_details) ? person.source_details : []).flatMap(record => {
    if (record?.kind !== 'compiler_chronological_placement' || !own.has(record.person_id)) return [];
    const p = record.placement, t = record.timeline_use, proof = record.external_evidence;
    const linked = events.filter(e => e.id === record.linked_life_event_id && e.person_id === record.person_id);
    if (linked.length !== 1 || linked[0].event_type !== 'death' || linked[0].date_expression != null || linked[0].normalized_date || linked[0].normalized_date_range
        || !Number.isInteger(p?.year) || p.year === 0 || p.calendar !== 'chinese_civil' || p.precision !== 'year' || p.month !== null || p.day !== null
        || !p.source_expression || p.evidence_kind !== 'received_compiler_editorial_placement' || p.selection_status !== 'preferred_provisional' || p.human_reviewed !== false
        || t?.eligible !== true || t.required_qualification !== 'compiler_editorial_placement_provisional' || t.must_display_qualification !== true
        || t.replace_source_event_date !== false || t.birth_year_inference_permitted !== false
        || record.human_reviewed !== false || record.status !== 'contextual_provisional'
        || !proof?.qualification || !proof?.source?.url || !Array.isArray(proof.anchors)) return [];
    return [{record_id:record.id, person_id:record.person_id, linked_event_id:record.linked_life_event_id, event_type:'death',
      year:p.year, calendar:p.calendar, source_expression:p.source_expression,
      required_qualification:t.required_qualification, must_display_qualification:true,
      selection_status:p.selection_status, replace_source_event_date:false, birth_year_inference_permitted:false,
      qualification:proof.qualification, evidence:proof}];
  });
}
