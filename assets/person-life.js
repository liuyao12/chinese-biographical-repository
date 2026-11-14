import {escapeHTML as h} from './core.js';
import {t} from './i18n.js';
import {chineseNumber} from './person-display.js';
export function sourceDateLabel(event) {
  const raw = event.date_expression || '';
  const date = event.normalized_date, mapping = date?.regnal_year_mapping;
  if (!['relative_ce_regnal_era_span', 'annal_ce_regnal_era_span'].includes(mapping?.kind)
      || !Number.isSafeInteger(mapping.target_regnal_year) || mapping.target_regnal_year < 1
      || typeof mapping.era_name !== 'string' || !mapping.era_name) return raw;
  const resolved = `${mapping.era_name}${mapping.target_regnal_year === 1 ? '元' : chineseNumber(mapping.target_regnal_year)}年`;
  return raw && raw !== resolved ? `${resolved}（${t('Source wording: {text}', {text:raw})}）` : resolved;
}

// Birth/death summaries use typed events, never office dates or age arithmetic.
export function ageLabel(age) {
  if (age.approximation?.kind === 'adjacent_age_numbers' && typeof age.source_number === 'string') return `${age.source_number}歲`;
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
  const provenance=new Set(['evidence','references','original_quote','rationale','reviewer','human_reviewed','model','relative_year_reference']);
  const facts=value=>Array.isArray(value)?value.map(facts):value && typeof value==='object'
    ?Object.fromEntries(Object.keys(value).filter(key=>!provenance.has(key)).sort().map(key=>[key,facts(value[key])])):value;
  function summary(kind) {
    const rows=[], grouped=new Map();
    for (const event of events.filter(e=>e.event_type===kind).sort((a,b)=>rank(a)-rank(b))) {
      const date=event.normalized_date || event.normalized_date_range;
      const civil=event.chinese_civil_year;
      const key=date || civil?JSON.stringify([rank(event),event.date_expression,facts(date),facts(civil)]):null;
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
  const ages = [], ageGroups = new Map();
  for (const age of (p.age_assertions || []).filter(e => own.has(e.person_id))) {
    const date = age.normalized_date || age.normalized_date_range;
    const key = date ? JSON.stringify(facts([age.value, age.unit, age.counting, age.reporting_status,
      age.age_context?.kind ?? null, age.source_number, age.source_term, age.qualified_source_term, age.bounds,
      age.approximation, age.group_reference, age.date_expression, date])) : null;
    if (!key || !ageGroups.has(key)) {
      const row = {...age, evidence:[...(age.evidence || [])]}; ages.push(row);
      if (key) ageGroups.set(key,row);
    } else {
      const row = ageGroups.get(key);
      for (const evidence of age.evidence || []) {
        if (!row.evidence.some(e=>JSON.stringify(e)===JSON.stringify(evidence))) row.evidence.push(evidence);
      }
    }
  }
  return {
    birth: summary('birth'),
    death: summary('death'),
    ages,
  };
}


// Ranges are explicit data. Never choose either endpoint as an event year.
export function civilYearLabelData(event) {
  const civil=event?.chinese_civil_year || (event?.normalized_date?.calendar==='chinese_civil' ? event.normalized_date : null);
  if (civil?.calendar!=='chinese_civil' || civil.year_numbering!=='astronomical' || civil.precision!=='year'
      || !['BCE','CE'].includes(civil.era) || !Number.isSafeInteger(civil.era_year) || civil.era_year<=0
      || !Number.isSafeInteger(civil.year) || civil.year!==(civil.era==='BCE'?1-civil.era_year:civil.era_year)) return null;
  return {key:civil.era==='BCE'?'{year} BCE (Chinese civil year)':'{year} CE (Chinese civil year)',params:{year:civil.era_year}};
}
export function lifeYearLabel(event) {
  const civil=civilYearLabelData(event);
  if (civil) return t(civil.key,civil.params);
  const date = event.normalized_date;
  if (date?.era_year) return `西元${date.era === 'BCE' ? '前' : ''}${date.era_year}年`;
  const range = event.normalized_date_range;
  const a = range?.earliest, b = range?.latest;
  if (!a?.era_year || !b?.era_year) return '';
  const prefix = p => `西元${p.era === 'BCE' ? '前' : ''}`;
  const suffix=range.basis==='within_named_era'&&range.calendar==='chinese_civil'?'中國曆年範圍':'暫定範圍';
  return `${prefix(a)}${a.era_year}至${a.era === b.era ? '' : prefix(b)}${b.era_year}年（${suffix}）`;
}

// Bibliography is reference material, separate from the received event quote.
export function studyReferencesHTML(refs) {
  if (!Array.isArray(refs) || !refs.length) return '';
  const rows=refs.filter(r=>r && (r.display_title || r.source_title)).map(r=>{
    let url='';
    try {const u=new URL(r.url);if (['http:','https:'].includes(u.protocol)) url=u.href;} catch {}
    const title=h(r.display_title || r.source_title);
    const author=r.display_author || r.author || r.source_author;
    const year=r.year || r.publication_year;
    return `<li>${author ? h(author)+'：' : ''}${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${title}</a>` : title}${year ? '（'+h(year)+'）' : ''}${r.reviewed_scope ? `<p>已閱範圍：${h(r.reviewed_scope)}</p>` : ''}${r.reference_note ? `<p>${h(r.reference_note)}</p>` : ''}${r.opinion_validation === 'not_attempted' ? '<small>研究意見未獨立驗證</small>' : ''}</li>`;
  });
  return rows.length ? `<details class="person-study-references"><summary>研究參考</summary><ul>${rows.join('')}</ul></details>` : '';
}
