import {principalOccurrences,occurrenceCountLabel} from './occurrence-counts.js';
import {referentCasesHTML} from './referent-interpretations.js';
import {escapeHTML as h} from './core.js';
import {sourcePassageURL} from './corpus-reader.js';
import {yearLabel} from './historical-tables.js';
import {traceFamily} from './person-family.js';
import {summarizeLife, ageLabel, lifeYearLabel, civilYearLabelData, sourceDateLabel, studyReferencesHTML} from './person-life.js';
import {t,ui} from './i18n.js';
import {summarizeNameComponents, nameAliases} from './name-components.js';
export const loadFamily = p => traceFamily(p, loadPerson);
export {nativeTableURL as tableOccurrenceURL} from './native-table-links.js';
import {nativeTableURL as tableOccurrenceURL, nativeProfileURL} from './native-table-links.js';
export function sourceReferenceQuote(reference) {
  const raw = typeof reference?.quote === 'string' ? reference.quote : '';
  if (reference?.quote_format !== 'kanripo_line_wrapped' || typeof reference.display_quote !== 'string') return raw;
  const plain = raw.replace(/<pb:[^>]*>/g, '').replace(/[\s¶/]/g, '');
  return reference.display_quote === plain ? reference.display_quote : raw;
}
const cache = new Map();
export const profileURL = (id, tableID = '') => 'person.html' + (/^shiji-\d{3}$/.test(tableID) ? '?table=' + encodeURIComponent(tableID) : '') + '#' + encodeURIComponent(id);
export async function loadPerson(id) {
  if (!cache.has(id)) cache.set(id, fetch('data/corpus/profiles/' + encodeURIComponent(id) + '.json').then(r => {if (!r.ok) throw Error('人物資料尚未載入'); return r.json();}).catch(e => {cache.delete(id); throw e;}));
  return cache.get(id);
}
const sourceEvidenceLinks = (evidence, sources = []) => (evidence || []).map(e => {
  if (e.kind === 'table_cell') {
    const url = tableOccurrenceURL({...e, cell_id:e.table_cell_id});
    const witness = sources.find(x => x.source_id === e.source_id && x.work_id === e.work_id
      && x.book_id === e.book_id && x.chapter_id === e.chapter_id
      && x.source?.revision === e.source_revision);
    let fixed = '';
    try {const u = new URL(witness?.source?.revision_url); if (['http:', 'https:'].includes(u.protocol)) fixed = u.href;} catch {}
    const subjectURL = e.subject_table_cell_id && tableOccurrenceURL({...e, cell_id:e.subject_table_cell_id});
    return (url ? `<a href="${h(url)}">來源表格 →</a>` : '')
      + (subjectURL ? ` · <a class="person-table-subject-source" href="${h(subjectURL)}">${ui('Name in same row')}</a>` : '')
      + (fixed ? ` · <a class="person-fixed-table-source" href="${h(fixed)}" target="_blank" rel="noopener">${ui('Fixed source revision')}</a>` : '');
  }
  const url=sourcePassageURL(e);
  return url ? `<a href="${h(url)}">來源原文 →</a>` : '';
}).join(' · ');
export function personBundleURL(id, sourceRef = 'main') {
  const ref = /^[a-f0-9]{40}$/.test(sourceRef) ? sourceRef : 'main';
  return 'https://github.com/liuyao12/chinese-biographical-repository/blob/' + ref + '/exports/persons/' + encodeURIComponent(id) + '.json';
}
export function titleUsageHTML(usages = [], full = false, sources = []) {
  const unique = new Map();
  for (const usage of usages) {
    const a = usage.attestation || {};
    const date = lifeYearLabel(a);
    if (!a.date_expression && !date) continue;
    const evidence = (usage.evidence || []).filter(e => !a.paragraph_id || e.paragraph_id === a.paragraph_id);
    const value = {a, date, evidence};
    unique.set(JSON.stringify([a.date_expression, a.normalized_date, a.normalized_date_range, evidence]), value);
  }
  return [...unique.values()].map(({a, date, evidence}) => {
    const d = a.normalized_date || a.normalized_date_range;
    const refs = full ? (d?.references || []).filter(r => r?.quote).map(r => {
      let url = '';
      try { const u = new URL(r.url); if (['http:', 'https:'].includes(u.protocol)) url = u.href; } catch {}
      return `<blockquote>${h(r.quote)}</blockquote>${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>` : ''}`;
    }).join('') : '';
    return `<div class="person-title-usage"><p>來源用稱：${[a.date_expression, date].filter(Boolean).map(h).join(' · ')}</p>${full ? `<details><summary>用稱紀年依據</summary>${evidence.map(e => `<blockquote>${h(e.quote || '')}</blockquote>`).join('')}${sourceEvidenceLinks(evidence, sources)}${d?.rationale ? `<p>${h(d.rationale)}</p>` : ''}${refs}</details>` : ''}</div>`;
  }).join('');
}

export function personCard(p, full = false, sourceRef = 'main', family = null) {
  const evidenceLinks = evidence => sourceEvidenceLinks(evidence, p.sources || []);
  const evidenceQuotes = e => `<blockquote>${h(e.quote)}</blockquote>` + (e.kind === 'table_cell' && e.subject_quote ? `<blockquote class="person-table-subject-quote">${h(e.subject_quote)}</blockquote>` : '');
  const titleReadings=new Map((p.preferred_title_readings || []).map(x=>[x.holding_id,x]));
  const unassumedAppointments = (p.title_proposals || []).filter(x => x.proposal_kind === 'unassumed_appointment' && x.outcome === 'not_assumed');
  const titleLabel=x=>{
    const reading=titleReadings.get(x.id);
    const inherited = x.inheritance?.resolved_title;
    const label=reading?`<strong>${h(reading.preferred_title)}</strong><br><small>${ui('Provisional reading; source spelling: {text}',{text:reading.source_title})}</small>`:inherited ? `<strong>${h(inherited)}</strong><br><small>${ui('Inherited title inferred from predecessor; source wording: {text}', {text:x.title})}</small>` : `<strong>${h(x.title)}</strong>`;
    return label+(x.mode === 'posthumous_grant' ? ' <small class="person-posthumous-grant">追贈（非生前實任）</small>' : '')+(x.appointment_role==='acting'?` <small class="person-acting-office">${ui('Acting appointment')}</small>`:'')
      +(x.mode==='attestation'&&unassumedAppointments.some(a=>a.title===x.title)?` <small class="person-unassumed-office">${ui('Separate record of appointment not taken up')}</small>`:'');
  };
  const titleSuccessionEvidence = x => x.inheritance ? `<details class="person-holding-succession"><summary>${ui('Title succession evidence')}</summary><p>${h(x.inheritance.rationale)}</p><p>${ui('Predecessor')}: <a href="${h(profileURL(x.inheritance.predecessor_person_id))}">${h(p.related_people?.[x.inheritance.predecessor_person_id] || x.inheritance.predecessor_person_id)}</a></p><p><q>${h(x.inheritance.source_term)}</q></p>${(x.inheritance.evidence || []).map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>` : '';
  const ancestryPathsHTML = x => x.ancestry_paths?.length ? `<details class="person-ancestry-paths"><summary>世系路徑與限定</summary>${x.ancestry_paths.map(route => `<section class="person-ancestry-path" data-qualification="${h(route.qualification)}"><h5>${route.qualification === 'assembly_inferred' ? '含父系暫定連接的推導路徑' : '原文關係連接路徑'}${route.cycle ? '（循環，停止追溯）' : ''}${route.unavailable ? '（資料未載入）' : ''}</h5>${route.steps.map(step => `<p>${h(step.from_label)} → ${h(step.to_label)} · ${step.qualification === 'assembly_inferred' ? '父系暫定連接' : '原文明記' + ({father:'父',grandfather:'祖父',great_grandfather:'曾祖父'}[step.relationship] || '親屬')}${step.inference_note ? `<br>${h(step.inference_note)}` : ''}</p>${step.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}`).join('')}</section>`).join('')}</details>` : '';
  const relativeList = entries => entries?.length ? entries.map(x => `<div class="person-family-member"><a href="${h(profileURL(x.person?.id || x.id))}">${h(x.label)}</a>${x.cycle ? '（世系循環，停止追溯）' : ''}${x.unavailable ? '（資料未載入）' : ''}${x.role === 'legal_or_dynastic' ? '（法定／宗統）' : ''}${x.role === 'assembly_inferred' ? '（父系暫定）' : ''}${x.marriage_status === 'source_attested_divorce' ? ` <small>（${h(t('Divorced (source-attested)'))}）</small>` : ''}<details><summary>親屬來源</summary>${x.inference_note ? `<p>${h(x.inference_note)}</p>` : ''}${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}${ancestryPathsHTML(x)}</details></div>`).join('') : '';
  const familyRows = family ? [
    ...family.ancestors.map((entries, i) => [ ['父','祖','曾祖'][i], entries, entries.length > 1 ? '多項來源主張，尚未統一' : '' ]),
    ['生母', family.mother, family.mother.length > 1 ? '多項生母記錄，身份或說法待整合' : ''],
    [t('Adoptive father (source-attested chuji)'), family.adoptive_father || [], ''],
    [t('Adopted children (source-attested chuji)'), family.adopted_children || [], ''],
    ['配偶', family.spouses, ''], ['子女', family.children, '']
  ].filter(([, entries]) => entries.length).map(([label, entries, note]) => `<dt>${label}</dt><dd>${note ? `<small>${note}</small><br>` : ''}${relativeList(entries)}</dd>`).join('') : '';
  const unresolvedSpouses = (family?.unresolved_spouse_groups || []).map(g => `<div class="person-pending-spouse-group" data-identity-group="${h(g.id)}"><strong>配偶指涉未決：是否同一人尚未判定</strong><p>${h(g.rationale)}</p><ul>${g.references.map(r => `<li>來源稱法：${h(r.span.surface)}${evidenceQuotes(r)}${evidenceLinks([r])}</li>`).join('')}</ul><small>此組不表示已證一人或兩人；原始配偶陳述均保留。</small></div>`).join('');
  const familyHTML = familyRows || unresolvedSpouses ? `<section class="person-family"><h4>家族</h4><dl>${familyRows}</dl>${unresolvedSpouses}</section>` : '';
  const ownIDs = new Set(p.person_ids || [p.id]);
  const successions = (p.relations || []).filter(r => ownIDs.has(r.subject_person_id) && r.qualifiers?.succession).map(r => {
    const s=r.qualifiers.succession;
    const parent=family?.ancestors?.[0]?.find(x=>(x.person?.id || x.id)===s.predecessor_person_id)?.person;
    const holding=parent?.titles?.find(x=>x.id===s.predecessor_holding_id);
    if (!holding || r.predicate!=='father' || s.status!=='contextual_provisional'
        || !['noble_rank','royal_rank'].includes(holding.kind)) return '';
    const reading=parent.preferred_title_readings?.find(x=>x.holding_id===holding.id);
    const title=reading?.preferred_title || holding.inheritance?.resolved_title || holding.title;
    return `<div class="person-title-succession"><strong>${h(title)}</strong> <small>承前爵稱 · 暫定</small><p><q>${h(s.source_term)}</q></p>${full ? `<details><summary>承襲依據</summary><p>${h(s.rationale)}</p><a href="${h(profileURL(parent.id))}">前任人物 →</a>${(r.evidence || []).map(e=>`${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>` : ''}</div>`;
  }).filter(Boolean);
  const successionHTML=successions.length?`<section class="person-title-successions"><h4>來源所記承襲</h4>${successions.join('')}</section>`:'';
  const nameDisplay = summarizeNameComponents(p.name_components);
  const {names, records:components, conflicts:nameConflicts} = nameDisplay;
  const personalName = names?.clan_style?.value || names?.full_name || (names ? `${names.surname || ''}${names.ming || ''}` : '');
  const heading = names && nameDisplay.canHead ? `${names.title || ''} ${personalName}`.trim() || p.label : p.label;
  const additional = names ? nameAliases(names) : [];
  const componentAlternatives = components.flatMap(x => x.component_alternatives || []).map(a => {
    const c=a.components || {}, labels=[['surname','Surname'],['ming','Given name'],['zi','Courtesy name']].filter(([k])=>c[k]).map(([k,label])=>`${ui(label)} ${h(c[k])}`);
    const ref=a.reference || {}; let url='';
    try {const u=new URL(ref.url);if(['http:','https:'].includes(u.protocol))url=u.href;}catch{}
    return `<p class="person-name-alternative">${ui('Name component alternative')}：${labels.join('、')}（${ui('Not selected as default')}）</p><blockquote>${h(ref.quote || '')}</blockquote>${url?`<a href="${h(url)}" target="_blank" rel="noopener">${ref.title?h(ref.title):ui('Source')}</a>`:''}`;
  }).join('');
  const life = summarizeLife(p);
  const lifeChoice = event => {
    const d=(p.life_event_date_decisions || []).find(d=>d.candidate_event_ids.includes(event.id));
    if (!d) return '';
    const choice=d.status==='unresolved'?'unresolved':d.preferred_event_id===event.id?'preferred':'alternative';
    const key={preferred:'Provisional preferred date',alternative:'Source alternative date',unresolved:'Date choice unresolved'}[choice];
    return ` <small class="person-life-choice" data-event-id="${h(event.id)}" data-choice="${choice}">${ui(key)}</small>`;
  };
  const lifeRow = (label, events) => {
    const dated = events.filter(e => lifeYearLabel(e) || e.date_expression);
    return dated.length ? `<dt>${label}</dt><dd>${dated.map(e => {
      const civil=civilYearLabelData(e);
      const values = [lifeYearLabel(e) ? `<strong>${civil?ui(civil.key,civil.params):h(lifeYearLabel(e))}</strong>` : '', sourceDateLabel(e) ? h(sourceDateLabel(e)) : ''].filter(Boolean);
      return `<div>${values.join(' · ')}${lifeChoice(e)}<details><summary>原文與紀年依據</summary>${(e.evidence || []).map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}${civil?civilYearEvidence(e):e.normalized_date_range && full ? dateReferences(e.normalized_date_range) : ''}</details></div>`;
    }).join('')}</dd>` : '';
  };
  const ages = life.ages.filter(e => Number.isInteger(e.value) || e.qualified_source_term || e.source_term);
  const ageWhen = e => {
    const values = [sourceDateLabel(e), lifeYearLabel(e)].filter(Boolean);
    return values.length ? `<small> · ${values.map(h).join(' · ')}（報齡時）</small>` : '';
  };
  const stableTitleFacts=value=>Array.isArray(value)?value.map(stableTitleFacts):value && typeof value==='object'
    ?Object.fromEntries(Object.keys(value).sort().map(key=>[key,stableTitleFacts(value[key])])):value;
  const grouped = new Map();
  for (const x of p.titles || []) {
    const duration=x.reported_duration?Object.fromEntries(Object.entries(x.reported_duration).filter(([key])=>key!=='evidence')):null;
    const factsKey = x.title + '|' + JSON.stringify(x.reported_office_event_counts || null) + '|' + JSON.stringify(stableTitleFacts([x.kind || null, x.jurisdictions || null, duration, x.duration_scope || null, x.appointment_role || null, x.punctuation_attribution || null, x.inheritance ? {resolved_title:x.inheritance.resolved_title, predecessor_person_id:x.inheritance.predecessor_person_id, predecessor_holding_id:x.inheritance.predecessor_holding_id, status:x.inheritance.status} : null]));
    const key = factsKey + '|' + x.period + (x.mode === 'posthumous_grant' ? '|posthumous_grant' : '');
    if (!grouped.has(key)) grouped.set(key, {...x, factsKey, evidence: [], date_periods: [], source_usages: []});
    grouped.get(key).evidence.push(...(x.evidence || []));
    grouped.get(key).date_periods.push(x.effective_period);
    if (x.mode === 'attestation') grouped.get(key).source_usages.push(...(x.attestations || []).map(a => ({attestation: a, evidence: x.evidence || []})));
  }
  const titleGroups = [...grouped.values()];
  const titleChronology = (x, summaryOnly = false) => {
    const preference = x.chronology_preference;
    if (preference) {
      const start = x.effective_period?.start || {};
      const preferred = `<p class="person-title-preferred-date">${ui('Provisional preferred date')}：${h(start.date_expression || '')}${lifeYearLabel(start) ? ` · ${h(lifeYearLabel(start))}` : ''}</p>`;
      if (summaryOnly || !full) return preferred;
      const alternatives = (p.titles || []).filter(t => t.id !== preference.preferred_holding_id
        && preference.candidate_holding_ids?.includes(t.id));
      return `<details class="person-title-chronology-preference"><summary>${ui('Title chronology source choice')}</summary><p>${h(preference.rationale || '')}</p>${alternatives.map(t => {
        const boundary = t.effective_period?.start || {};
        return `<p>${ui('Other source wording')}：${h(boundary.date_expression || '')}${lifeYearLabel(boundary) ? ` · ${h(lifeYearLabel(boundary))}` : ''}</p>${(t.evidence || []).map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}`;
      }).join('')}</details>`;
    }
    if (summaryOnly) return '';
    const c=x.chronology_source_choice;
    if (!full || !c) return '';
    const refs=(c.references || []).map(r=>{
      let url='';try{const u=new URL(r.url);if(['http:','https:'].includes(u.protocol))url=u.href;}catch{}
      return `<blockquote>${h(r.display_quote || r.quote || '')}</blockquote>${url?`<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>`:''}`;
    }).join('');
    return `<details class="person-title-chronology-choice"><summary>${ui('Title chronology source choice')}</summary><p>${ui('Provisional preferred date')}：${h(c.preferred_source_expression)}</p><p>${ui('Other source wording')}：<q>${h(c.alternative_source_term)}</q></p><blockquote>${h(c.alternative_evidence?.quote || '')}</blockquote>${c.alternative_evidence?evidenceLinks([c.alternative_evidence]):''}<p>${h(c.rationale)}</p>${refs}</details>`;
  };
  const officeAttribution = x => {
    const a=x.punctuation_attribution;
    if (!full || !a) return '';
    const refs=(a.references || []).map(r=>{
      let url='';try{const u=new URL(r.url);if(['http:','https:'].includes(u.protocol))url=u.href;}catch{}
      return `<blockquote>${h(r.display_quote || r.quote || '')}</blockquote>${url?`<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>`:''}`;
    }).join('');
    return `<div class="person-office-attribution"><h5>${ui('Office punctuation reading')}</h5><p>${ui('Received punctuation')}：<q>${h(a.received_segment)}</q></p><p>${ui('Preferred segmentation')}：<q>${h(a.preferred_segmentation)}</q></p><p>${h(a.rationale)}</p>${refs}</div>`;
  };
  const hasPeriod = x => (x.period || '').split(' → ').some(v => !['', '未定', '起訖未定'].includes(v));
  const datedFacts = new Set(titleGroups.filter(hasPeriod).map(x => x.factsKey));
  const titles = full ? titleGroups : titleGroups.filter(x => hasPeriod(x) || !datedFacts.has(x.factsKey))
    .sort((a,b) => Number(Boolean(b.inheritance)) - Number(Boolean(a.inheritance)) || Number(hasPeriod(b)) - Number(hasPeriod(a)));
  const occurrences = p.occurrences || [];
  const principals = principalOccurrences(occurrences);
  const principal = principals[0];
  const tableExample = (p.table_occurrences || [])[0];
  const lifeEvents = p.life_events || [], dateDecisions = p.life_event_date_decisions || [];
  const datePriority = x => {
    const d = dateDecisions.find(d => d.candidate_event_ids.includes(x.record_id));
    return d?.status === 'editorial_provisional' ? (d.preferred_event_id === x.record_id ? 0 : 2) : 1;
  };
  const dates = (p.dates || []).filter(x => x.era_year && x.original_quote).sort((a,b) => datePriority(a) - datePriority(b));
  const dateChoice = x => {
    const d = dateDecisions.find(d => d.candidate_event_ids.includes(x.record_id));
    return !d ? '' : d.status === 'unresolved' ? ' · 取捨未定' : d.preferred_event_id === x.record_id ? ' · 本項預設' : ' · 來源異說';
  };
  const officeCounts = x => Object.entries(x.reported_office_event_counts || {}).map(([key, c]) =>
    `<p class="person-office-count">${key === 'departure' ? '離相' : '復位'} ${h(c.value)} 次 <q>${h(c.source_term)}</q></p>`).join('');
  const titleDuration = x => {
    const d=x.reported_duration;
    if (!d?.source_term) return '';
    const unit=d.unit==='title_month'?'月':'年';
    const number=Number.isInteger(d.value)?`<strong>${h(d.value)}${unit}</strong> · `:'';
    const scope=x.duration_scope?.kind==='multiple_holdings'?' · 涵蓋多項稱號，不重複計數':'';
    return `<p class="person-title-duration">原記時長：${number}<q>${h(d.source_term)}</q><small> · 來源計數，起訖未由此推定${scope}</small></p>`;
  };
  const titleJurisdictions = x => {
    const names = Array.isArray(x.jurisdictions) ? x.jurisdictions.map(p => p?.source_name).filter(n => typeof n === 'string' && n) : [];
    return names.length ? `<br><small class="person-title-jurisdictions">${x.kind === 'royal_rank' ? '所王地' : '所屬地'}：${h(names.join('、'))}</small>` : '';
  };
  const titleKind = x => {
    if (!x.kind || !titles.some(y => y.title === x.title && y.kind && y.kind !== x.kind)) return '';
    const label = {royal_rank:'王號',imperial_rank:'帝號',noble_rank:'爵位',office:'官稱',honorific:'尊稱',unclassified:'性質待考'}[x.kind];
    return label ? ` <small class="person-title-kind">${h(label)}</small>` : '';
  };
  const titlePeriod = x => {
    const bounds = (x.period || '').split(' → ');
    if (bounds.length === 2) return bounds.every(v => !v || v === '未定') ? '' : bounds[0] === '未定' ? '止於 ' + bounds[1] : bounds[1] === '未定' ? '始於 ' + bounds[0] : bounds.join(' → ');
    return ['未定', '起訖未定'].includes(x.period) ? '' : x.period || '';
  };
  const dateReferences = date => (Array.isArray(date?.references) ? date.references : []).filter(r => r?.quote).map(r => {
    let url = '';
    try { const parsed = new URL(r.url); if (['http:', 'https:'].includes(parsed.protocol)) url = parsed.href; } catch {}
    return `<blockquote>${h(sourceReferenceQuote(r))}</blockquote>${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>` : h(r.title || '')}`;
  }).join('');
  const nameFieldLabels = {surname:ui('Surname'),ming:ui('Given name'),zi:ui('Courtesy name'),xiaozhi:ui('Childhood name'),xiaoming:ui('Childhood name (xiaoming)'),hao:'號',former_ming:ui('Former given name'),full_name:'全名',clan_style:'氏稱'};
  const nameConflictHTML = nameConflicts.length ? `<p class="person-name-conflicts">姓名構件有異說：${nameConflicts.map(x => `${nameFieldLabels[x.field]} ${x.values.map(h).join('／')}`).join('；')}。${nameDisplay.coreConflict ? '姓名標題沿用人物標籤；未任選來源構件。' : '有差異的欄位未選作預設。'}</p>` : '';
  const nameEvidence = names ? `${nameConflictHTML}<details class="person-name-evidence"><summary>姓名依據</summary>${components.map(n => {
    const fields = ['surname','ming','zi','xiaozhi','xiaoming','hao','former_ming','full_name'].filter(k => typeof n[k] === 'string' && n[k].trim());
    const source = {...(p.sources || []).find(x => x.chapter_id === n.chapter_id), ...n};
    return `<div class="person-name-source">${fields.length ? `<p>${fields.map(k => `${nameFieldLabels[k]} ${h(n[k])}`).join(' · ')}</p>` : ''}${typeof n.title === 'string' && n.title.trim() ? `<p class="person-name-source-title">本筆姓名來源所列稱號：${h(n.title)}</p>` : ''}<blockquote>${h(n.quote || '')}</blockquote>${evidenceLinks([source])}${n.note ? `<p>${h(n.note)}</p>` : ''}${dateReferences(n)}</div>`;
  }).join('')}${componentAlternatives}</details>` : '';
  const civilYearEvidence = event => {
    const normalized=event.normalized_date;
    if (!event.chinese_civil_year && normalized?.calendar==='chinese_civil') {
      return `<section class="person-civil-year-evidence"><h5>${ui('Chinese civil year evidence')}</h5><p>${ui('Original calendar expression')}：<q>${h(normalized.source_expression)}</q></p><p>${ui('Year label, not an exact Gregorian date')}</p><p>${h(normalized.rationale)}</p>${dateReferences(normalized)}</section>`;
    }
    const value=event.chinese_civil_year, eq=value?.year_equivalence;
    if (!eq || typeof eq!=='object' || Array.isArray(eq)) return '';
    const labels={regnal_era:'Received era anchor',regnal_year:'Received regnal year',event:'Received year events',editorial_year:'Digital editorial year label'};
    const tableRefs=Object.entries(labels).map(([stem,label])=>{
      const citation={kind:'table_cell',table_id:eq.table_id,table_cell_id:eq[stem+'_cell_id'],quote:eq[stem+'_quote'],work_id:eq.work_id,book_id:eq.book_id,chapter_id:eq.chapter_id,source_id:eq.source_id,source_revision:eq.source_revision};
      return `<p>${ui(label)}</p><blockquote>${h(citation.quote)}</blockquote>${evidenceLinks([citation])}`;
    }).join('');
    const context=(value.context_evidence || []).map(e=>`<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('');
    const window=full && event.normalized_date_range?`<details class="person-gregorian-window"><summary>${ui('Gregorian projection window')} · ${h(lifeYearLabel({...event,chinese_civil_year:undefined}))}</summary>${dateReferences(event.normalized_date_range)}</details>`:'';
    return `<section class="person-civil-year-evidence"><h5>${ui('Chinese civil year evidence')}</h5><p>${ui('Original calendar expression')}：<q>${h(value.source_expression)}</q></p><p>${ui('Year label, not an exact Gregorian date')}</p>${context}${tableRefs}<p>${h(value.rationale)}</p>${window}</section>`;
  };
  const lifeDateSources = date => {
    const refs = full ? dateReferences(date) : '';
    return refs ? `<details class="person-date-references"><summary>紀年依據</summary>${date.rationale ? `<p>${h(date.rationale)}</p>` : ''}${refs}</details>` : '';
  };
  const titleDateSources = x => !full ? '' : [['start', '始年'], ['end', '終年']].map(([key, label]) => {
    const dates = new Map();
    for (const period of x.date_periods) {
      const date = period?.[key]?.normalized_date || period?.[key]?.normalized_date_range;
      const refs = Array.isArray(date?.references) ? date.references.filter(r => r?.quote) : [];
      if (refs.length) dates.set(JSON.stringify([date.original_quote, date.rationale, refs]), {date, refs});
    }
    if (!dates.size) return '';
    return `<details class="person-title-dates"><summary>${label}紀年依據</summary>${[...dates.values()].map(({date, refs}) =>
      `${date.original_quote ? `<blockquote>${h(date.original_quote)}</blockquote>` : ''}${date.rationale ? `<p>${h(date.rationale)}</p>` : ''}${refs.map(r => {
        let url = '';
        try { const parsed = new URL(r.url); if (['http:', 'https:'].includes(parsed.protocol)) url = parsed.href; } catch {}
        return `<blockquote>${h(r.quote)}</blockquote>${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>` : h(r.title || '')}`;
      }).join('')}`
    ).join('')}</details>`;
  }).join('');
  const addresses = p.addresses || [];
  const addressHeading = x => {
    const label = {biographical_origin: '籍貫', native_place: '籍貫', ancestral_origin: '祖先出身',
      birth_place: '出生地', residence: '居地', capital_location: '所都', service_location: '任事地', death_place: '卒地', burial_place: '葬地'}[x.relation];
    return label && x.place?.source_name ? label + '：' + x.place.source_name : x.term;
  };
  const ageApproximation = age => age.approximation?.kind === 'adjacent_age_numbers' ? `（${ui('Source age approximation')}）` : '';
  const lifeRows = lifeRow('生', life.birth) + lifeRow('卒', life.death) + (ages.length ? `<dt>年齡</dt><dd>${ages.map(e => `${h(ageLabel(e))}${ageApproximation(e)}${ageWhen(e)}<details><summary>報齡原文</summary>${(e.evidence || []).map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}</details>`).join('')}</dd>` : '');
  const lifeHTML = lifeRows ? `<section class="person-life-summary"><dl>${lifeRows}</dl></section>` : '';
  const orderDecisions = p.relative_birth_order_decisions || [];
  const orderWarning = orderDecisions.length ? `<section class="person-relative-order-decisions"><p>${ui('Sibling age order has conflicting accounts; no order is preferred.')}</p>${full ? orderDecisions.map(d => `<details><summary>${ui('Age-order accounts and sources')}</summary><p>${h(d.rationale)}</p>${d.claims.map(c => `<blockquote>${h(c.witness.quote)}</blockquote><p><a href="${h(c.witness.fixed_url)}" target="_blank" rel="noopener">${ui('Fixed source text')}</a></p>`).join('')}</details>`).join('') : ''}</section>` : '';
  const unresolvedSourceTitles = full && p.unresolved_title_attestations?.length ? `<section class="person-unresolved-source-titles"><h4>${ui('Source titles with unresolved holders')}</h4><p>${ui('Not assigned as this person’s holdings.')}</p>${p.unresolved_title_attestations.map(a => `<details><summary>${h(a.title)} · ${h(a.holder_surface)}</summary><p>${h(a.interpretation_note)}</p>${a.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>`).join('')}</section>` : '';
  const collateralAgeWarning = (p.relations || []).some(r => r.qualifiers?.relative_age_interpretation?.status === 'chronology_unresolved') ? `<p class="person-collateral-age-warning">${ui('Age order in the source kinship term remains unresolved.')}</p>` : '';
  const variants = p.reported_variants || [];
  const teaching = (p.relations || []).filter(r => r.predicate === 'teacher');
  const relations = (p.relations || []).filter(r => r.predicate !== 'teacher'), labels = {raised_by:t('Caregiver'),ritual_successor_of:t('Ritual predecessor'),father:'父',mother:'生母',stepmother:'後母',adoptive_mother:'所母',adoptive_father:t('Adoptive father (source-attested chuji)'),spouse:'配偶',son:'子',daughter:'女',brother:'兄弟',grandfather:'祖父',great_grandfather:'曾祖父',ancestor:t('Ancestor'),paternal_uncle:t('Paternal uncle'),maternal_uncle:t('Maternal uncle'),maternal_aunt:t('Maternal aunt'),agnatic_senior_kin:t('Paternal collateral relative one generation senior'),agnatic_cousin:t('Paternal same-generation collateral relative'),maternal_cousin:t('Maternal aunt cousin')};
  const relationPersonLink = id => `<a class="person-kinship-link" href="${h(profileURL(id))}">${h(p.related_people?.[id] || id)}</a>`;
  const relationLabel = x => {
    if (x.predicate === 'maternal_role') return x.qualifiers?.role === 'prior_mother' ? t('Prior mother (source wording)') : t('Mother (birth unspecified)');
    if (x.predicate === 'grandfather' && x.qualifiers?.lineage === 'maternal') return t('Maternal grandfather');
    const order=x.qualifiers?.relative_birth_order;
    if(x.predicate==='sister' && order?.operator==='lt') {
      if(order.older_person_id===x.object_person_id && order.younger_person_id===x.subject_person_id) return t('Elder sister');
      if(order.younger_person_id===x.object_person_id && order.older_person_id===x.subject_person_id) return t('Younger sister');
    }
    return labels[x.predicate] || x.qualifiers?.source_term || x.predicate;
  };
  const referentCases = full ? referentCasesHTML(p.referent_interpretations || [], Object.fromEntries(Object.entries(p.related_people || {}).map(([id,label])=>[id,{label}]))) : '';
  const identityCasesHTML = full && p.unresolved_identity_cases?.length ? `<section class="person-identity-cases"><h4>身份待考</h4>${p.unresolved_identity_cases.map(c => `<details><summary>${c.candidate_list_exhaustive === false ? '已列候選人物（未窮盡）' : '分開保留的候選人物'}</summary><p>${h(c.note)}</p><p>${c.candidate_person_ids.map(id => `<a href="${h(profileURL(id))}">${h(p.related_people?.[id] || id)}</a>`).join('、')}</p>${evidenceLinks(c.paragraph_ids.map(paragraph_id => ({chapter_id:paragraph_id.split(':')[0],paragraph_id})))}${dateReferences(c)}</details>`).join('')}</section>` : '';
  const distinctionsHTML = full && p.identity_distinctions?.length ? `<section class="person-identity-distinctions"><h4>${ui('Distinct people')}</h4>${p.identity_distinctions.map(d => `<details><summary>${ui('Identity distinction evidence')}</summary><p>${h(d.rationale)}</p><p>${d.person_ids.filter(id => !(p.person_ids || [p.id]).includes(id)).map(id => `<a href="${h(profileURL(id))}">${h(p.related_people?.[id] || id)}</a>`).join('、')}</p>${(d.evidence || []).map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>`).join('')}</section>` : '';
  const readingHTML = full && p.reading_decisions?.length ? `<section class="person-reading-evidence"><h4>名物辨讀</h4>${p.reading_decisions.map(d => `<details><summary>讀法與來源</summary><p>${h(d.rationale)}</p>${evidenceLinks(d.evidence.map(e => ({...e,chapter_id:e.chapter_id || e.paragraph_id.split(':')[0]})))}${dateReferences(d)}</details>`).join('')}</section>` : '';
  const chronologyWarning = !full && (p.reading_decisions || []).some(d=>d.chronology_caution?.status==='unresolved' && d.chronology_caution?.no_tenure_interpolation===true) ? `<p class="note person-chronology-warning">${ui('Title chronology unresolved; no tenure inferred for this event.')}</p>` : '';
  const unenactedProposals = (p.title_proposals || []).filter(x => x.outcome === 'not_enacted');
  const proposalHTML = full && unenactedProposals.length ? `<section class="person-title-proposals"><h4>擬議而未授的稱號</h4>${unenactedProposals.map(x => `<details><summary>${h(x.title)} · 未實行提議</summary><p>${h(x.interpretation_note)}</p>${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>`).join('')}</section>` : '';
  const unassumedHTML = full && unassumedAppointments.length ? `<section class="person-unassumed-appointments"><h4>${ui('Declined or unassumed appointments')}</h4>${unassumedAppointments.map(x => `<details><summary>${h(x.title)} · ${ui(x.non_assumption_kind === 'declined' ? 'Declined appointment' : 'Appointment not taken up')}</summary><p>${h(x.interpretation_note)}</p>${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details>`).join('')}</section>` : '';
  const arrangements = (p.title_proposals || []).filter(x => x.proposal_kind === 'agreed_appointment' && x.outcome === 'not_reported');
  const arrangementHTML = full && arrangements.length ? `<section class="person-appointment-arrangements"><h4>任官安排</h4><ul>${arrangements.map(x => `<li><strong>${h(x.title)}</strong> · 實行情況未載<p>${h(x.interpretation_note || '')}</p><details><summary>約定原文</summary>${(x.evidence || []).map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details></li>`).join('')}</ul></section>` : '';
  return `<article class="cbr-profile"><p class="eyebrow">人物資料 · ${p.review === 'source_local_candidate' ? '來源局部候選' : '來源辨認暫定'}</p><h${full ? 1 : 3}>${h(heading)}</h${full ? 1 : 3}>${p.historicity === 'legendary_tradition' ? '<p class="person-historicity">傳說敘事人物</p>' : ''}${additional.length ? `<p class="person-aliases">${additional.map(x => `<span>${x.kind === 'zi' ? ui('Courtesy name') + ' ' : x.kind === 'xiaozhi' ? ui('Childhood name') + ' ' : x.kind === 'xiaoming' ? ui('Childhood name (xiaoming)') + ' ' : x.kind === 'former_ming' ? ui('Former given name') + ' ' : ''}${h(x.value)}</span>`).join(' ')}</p>` : ''}${nameEvidence}${(p.names || []).length ? `<details class="person-source-names"><summary>來源中的其他稱呼</summary><p>${p.names.map(x => h(x)).join('、')}</p></details>` : ''}${lifeHTML}${chronologyWarning}${orderWarning}${collateralAgeWarning}${familyHTML}${successionHTML}${unresolvedSourceTitles}${full && p.identity_note ? `<p class="note">${h(p.identity_note)}</p>` : ''}${identityCasesHTML}${referentCases}${distinctionsHTML}${readingHTML}${proposalHTML}${unassumedHTML}${arrangementHTML}${principal ? `<blockquote class="person-overview">${h(principal.quote.slice(0, full ? 220 : 110))}</blockquote><p class="person-principal-source"><a href="${h(sourcePassageURL(principal))}">《${h(principal.work_title || '史記')}·${h(principal.title)}》 →</a>${principals.slice(1).map(x => ` · <a href="${h(sourcePassageURL(x))}">《${h(x.work_title || '史記')}·${h(x.title)}》 →</a>`).join('')}<br><small>已標記正文中最多提及的來源（頻次不代表來源權威度）</small></p>` : ''}
  ${!principal && tableExample ? `<blockquote class="person-overview">${h(tableExample.quote.slice(0, full ? 220 : 150))}</blockquote><p class="person-principal-source"><a href="${h(tableOccurrenceURL(tableExample))}">${h(tableExample.title)} · 查看原格 →</a></p>${!full && p.identity_note ? `<p class="note">${h(p.identity_note)}</p>` : ''}` : ''}
  ${dates.length ? `<section class="person-date-evidence"><h4>紀年對照</h4>${dates.slice(0, full ? undefined : 2).map(x => `<div class="person-date-item"><p><strong>西元${x.era === 'BCE' ? '前' : ''}${x.era_year}年</strong> <small>編輯對照 · 暫定${h(dateChoice(x))}</small><br><q>${h(x.original_quote)}</q>${full ? '<br>' + evidenceLinks(x.evidence) : ''}</p>${lifeDateSources(x)}</div>`).join('')}</section>` : ''}
  ${full && dateDecisions.length ? `<section class="person-date-decisions"><h4>生卒紀年取捨 · 暫定</h4>${dateDecisions.map(d => `<p>${h(d.rationale)}</p>${evidenceLinks(d.evidence)}${dateReferences(d)}`).join('')}</section>` : ''}
  ${full && variants.length ? `<section class="person-textual-variants"><h4>校勘參考</h4><p>其他來源所載或注家所議，尚未核書影；未採改正文。</p><ul>${variants.map(v => `<li>正文「${h(v.received_reading)}」 · 所報或所議「${h(v.reported_reading)}」<details><summary>${h(v.commentator)}</summary><blockquote>${h(v.quote)}</blockquote><a href="${h(v.url)}" target="_blank" rel="noopener">異文來源</a>${v.interpretation_note ? `<p>${h(v.interpretation_note)}</p>` : ''}${studyReferencesHTML(v.study_references)}</details></li>`).join('')}</ul></section>` : ''}
  ${full && lifeEvents.length ? `<section class="person-life-events"><h4>來源所記生卒</h4>${lifeEvents.map(e => `<div><strong>${e.event_type === 'death' ? '死亡' : '出生'}</strong>${e.date_expression ? ' · ' + h(e.date_expression) : ''}<details><summary>${h(e.source_term || '查看原文')}</summary>${e.evidence.map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}${e.interpretation_note ? `<p>${h(e.interpretation_note)}</p>` : ''}</details>${studyReferencesHTML(e.study_references)}</div>`).join('')}</section>` : ''}
  ${titles.length || addresses.length ? `<div class="person-facts">${titles.length ? `<section><h4>稱號與持職</h4>${titles.slice(0, full ? undefined : 2).map(x => `<div class="person-title">${titleLabel(x)}${titleKind(x)}${titleJurisdictions(x)}${titlePeriod(x) ? `<br><small>${h(titlePeriod(x))}</small>` : ''}${titleUsageHTML(x.source_usages, full, p.sources || [])}${officeCounts(x)}${titleDuration(x)}${titleSuccessionEvidence(x)}${titleChronology(x, true)}${full ? `<details><summary>${x.evidence.length} 筆來源證據</summary>${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}${x.interpretation_note ? `<p>${h(x.interpretation_note)}</p>` : ''}${officeAttribution(x)}${titleChronology(x)}${dateReferences(x)}</details>` : ''}${titleDateSources(x)}${!full && x.mode !== 'attestation' && x.evidence.length ? `<p class="person-title-source">${evidenceLinks(x.evidence)}</p>` : ''}</div>`).join('')}</section>` : ''}
  ${addresses.length ? `<section><h4>來源所記地望</h4>${addresses.slice(0, full ? undefined : 2).map(x => `<div class="person-address"><strong>${h(addressHeading(x))}</strong>${full ? `<details><summary>查看原文證據</summary><blockquote>${h(x.quote)}</blockquote>${evidenceLinks(x.evidence)}${x.interpretation_note ? `<p>${h(x.interpretation_note)}</p>` : ''}</details>` : ''}</div>`).join('')}</section>` : ''}</div>` : ''}
  ${full && teaching.length ? `<section class="person-teaching"><h4>${ui('Teaching and learning')}</h4><ul>${teaching.map(x => `<li><a href="${h(profileURL(x.subject_person_id))}">${h(p.related_people?.[x.subject_person_id] || x.subject_person_id)}</a> · ${ui('Studied with')} <a href="${h(profileURL(x.object_person_id))}">${h(p.related_people?.[x.object_person_id] || x.object_person_id)}</a><details><summary>${ui('Source evidence')}</summary><p>${h(x.qualifiers?.source_term || '')}</p>${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details></li>`).join('')}</ul></section>` : ''}
  ${full && relations.length ? `<section><h4>來源所記親屬</h4><ul>${relations.map(x => `<li>${relationPersonLink(x.subject_person_id)} · ${h(relationLabel(x))}：${relationPersonLink(x.object_person_id)}${x.qualifiers?.adopted_for_family_tree === false ? ' <small class="person-unadopted-ancestry">'+ui('Relationship claim not adopted into family tree')+'</small>' : ''}<details><summary>來源與關係原詞</summary><p>${h(x.qualifiers?.source_term || '')}</p>${x.evidence.map(e => `${evidenceQuotes(e)}${evidenceLinks([e])}`).join('')}</details></li>`).join('')}</ul></section>` : ''}
  ${full && p.table_occurrences?.length ? `<section><h4>表中原文</h4><ul class="person-occurrences">${(p.table_occurrences || []).map(x => `<li><a href="${h(tableOccurrenceURL(x))}">${h(x.title)} · ${h(yearLabel(x.year))} →</a><blockquote>${h(x.quote)}</blockquote>${x.mention?.identity_evidence?.length ? `<details class="person-identity-evidence"><summary>人物同指的篇文證據 · 暫定</summary>${x.mention.identity_evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}${e.source_revision ? `<p><small>固定修訂 <code>${h(e.source_revision)}</code></small></p>` : ''}`).join('')}</details>` : ''}</li>`).join('')}</ul></section>` : ''}
  ${occurrences.length ? `<section><h4>出現篇章</h4><ul class="person-occurrences">${occurrences.slice(0, full ? undefined : 3).map(x => `<li><a href="${h(sourcePassageURL(x))}">《${h(x.work_title || '史記')}·${h(x.title)}》 →</a>${full ? `<p><q>${h(x.quote)}</q></p>` : ''}<small>${h(occurrenceCountLabel(x))}</small></li>`).join('')}</ul></section>` : ''}
  ${full ? `<details class="person-data-download"><summary>資料識別與機讀檔案</summary><code>${h(p.id)}</code><p><a href="data/corpus/profiles/${encodeURIComponent(p.id)}.json">人物頁 JSON</a>${p.review !== 'source_local_candidate' ? ` · <a class="person-source-bundle-link" href="${h(personBundleURL(p.id, sourceRef))}">CBR 完整來源包</a>` : ''}</p></details>` : `<a class="person-profile-button" href="${h(profileURL(p.id))}">閱讀完整人物頁 →</a>`}</article>`;
}
export function markCell(cell, context = null) {
  const chars = Array.from(cell.text), out = []; let end = 0;
  for (const m of [...(cell.person_mentions || []), ...(cell.unresolved_mentions || [])].sort((a,b) => a.start - b.start)) {
    if (m.start < end || chars.slice(m.start, m.end).join('') !== m.surface) throw Error('年表人物標記與原文不符');
    out.push(h(chars.slice(end, m.start).join('')));
    if (!m.person_id) {out.push(`<span class="table-unresolved-mention" tabindex="0" role="button" title="${h(m.interpretation_note)}">${h(m.surface)}</span>`); end = m.end; continue;}
    out.push(`<a class="table-person-link" data-person-id="${h(m.person_id)}" href="${h(context?.work_id && context.work_id !== 'w-shiji' ? nativeProfileURL(m.person_id, {...context,cell_id:cell.id}) : profileURL(m.person_id, /^shiji-\d{3}/.exec(cell.id || '')?.[0]))}" title="查看人物資料">${h(m.surface)}</a>`); end = m.end;
  }
  out.push(h(chars.slice(end).join(''))); return out.join('');
}
export function personCardPosition(anchor, viewport, width, height) {
  const margin = 16, gap = 12;
  const cardWidth = Math.max(1, Math.min(width, viewport.width - 2 * margin));
  const cardHeight = Math.max(1, Math.min(height, viewport.height - 2 * margin));
  const clamp = (value, low, high) => Math.max(low, Math.min(value, Math.max(low, high)));
  const left = clamp(anchor.left, margin, viewport.width - margin - cardWidth);
  const maxHeight = Math.max(1, viewport.height - 2 * margin);
  if (viewport.width - margin - anchor.right - gap >= cardWidth) {
    return {left: anchor.right + gap, top: clamp(anchor.top, margin, viewport.height - margin - cardHeight), width: cardWidth, maxHeight};
  }
  if (anchor.left - gap - margin >= cardWidth) {
    return {left: anchor.left - gap - cardWidth, top: clamp(anchor.top, margin, viewport.height - margin - cardHeight), width: cardWidth, maxHeight};
  }
  const below = viewport.height - margin - anchor.bottom - gap;
  if (below >= Math.min(240, maxHeight / 2) || below >= anchor.top - gap - margin) {
    const top = clamp(anchor.bottom + gap, margin, viewport.height - margin - 1);
    return {left, top, width: cardWidth, maxHeight: Math.max(1, viewport.height - margin - top)};
  }
  const available = Math.max(1, Math.min(maxHeight, anchor.top - gap - margin));
  return {left, top: clamp(anchor.top - gap - Math.min(cardHeight, available), margin,
    viewport.height - margin - Math.min(cardHeight, available)), width: cardWidth, maxHeight: available};
}

export function bindPersonCards(root) {
  const card = document.createElement('aside'); card.className = 'table-person-card'; card.hidden = true; card.setAttribute('aria-label', '人物資料'); root.append(card);
  let ticket = 0, timer, pinned = false, hoverArmed = true, activeAnchor = null;
  const view = root.ownerDocument?.defaultView || (typeof window === 'undefined' ? null : window);
  function place() {
    if (card.hidden || !activeAnchor?.getBoundingClientRect || !card.getBoundingClientRect || !card.style || !view) return;
    card.style.width = '';
    card.style.maxHeight = `${Math.max(1, view.innerHeight - 32)}px`;
    const size = card.getBoundingClientRect();
    const p = personCardPosition(activeAnchor.getBoundingClientRect(), {width: view.innerWidth, height: view.innerHeight}, size.width, size.height);
    Object.assign(card.style, {left: `${p.left}px`, right: 'auto', top: `${p.top}px`, width: `${p.width}px`, maxHeight: `${p.maxHeight}px`});
  }
  async function show(node, focus = false) {
    clearTimeout(timer); const current = ++ticket; activeAnchor = node; card.hidden = false;
    card.innerHTML = '<p role="status">載入人物資料…</p>';
    place();
    try {const p = await loadPerson(node.dataset.personId); const family = await loadFamily(p); if (current !== ticket) return; card.innerHTML = `<button type="button" class="close-person-card" aria-label="關閉人物資料">關閉</button>` + personCard(p, false, 'main', family); card.querySelector('button').onclick = hide; card.querySelector('.person-profile-button').href = node.href; card.scrollTop = 0; place(); if (focus) card.querySelector('.close-person-card').focus({preventScroll:true});}
    catch {if (current === ticket) {card.innerHTML = `<p>人物資料尚未載入。</p><a href="${h(profileURL(node.dataset.personId))}">開啟人物頁</a>`; place();}}
  }
  function hide() {clearTimeout(timer); ticket++; pinned = false; hoverArmed = false; activeAnchor = null; card.hidden = true;}
  const over = e => {if (e.type !== 'focusin' && (!hoverArmed || pinned || e.pointerType === 'touch')) return; const n = e.target.closest('.table-person-link, .cbr-person-link'); if (n && (e.type !== 'focusin' || n.matches(':focus-visible'))) {if (e.type === 'focusin') {pinned = false; hoverArmed = true;} show(n);}};
  const move = e => {if (!hoverArmed && e.pointerType !== 'touch') {hoverArmed = true; over(e);}};
  const out = e => {if (pinned || e.pointerType === 'touch') return; if (!e.target?.closest?.('.table-person-link, .cbr-person-link') && !card.contains(e.target)) return; if (e.relatedTarget && (card.contains(e.relatedTarget) || e.relatedTarget.closest?.('.table-person-link, .cbr-person-link'))) return; clearTimeout(timer); timer = setTimeout(hide, 250);};
  const click = e => {const n = e.target.closest('.table-person-link, .cbr-person-link'); if (n && !e.metaKey && !e.ctrlKey) {e.preventDefault(); e.stopPropagation(); pinned = true; show(n, true);}};
  root.addEventListener('pointerover', over); root.addEventListener('pointermove', move); root.addEventListener('focusin', over); root.addEventListener('pointerout', out); root.addEventListener('click', click, true);
  card.onpointerenter = () => clearTimeout(timer); card.onpointerleave = out;
  const keyTarget = root.ownerDocument || root;
  const key = e => {if (e.key === 'Escape' && !card.hidden) hide();}; keyTarget.addEventListener('keydown', key);
  view?.addEventListener?.('resize', place);
  view?.addEventListener?.('scroll', place, {passive:true});
  return () => {hide(); clearTimeout(timer); root.removeEventListener('pointerover', over); root.removeEventListener('pointermove', move); root.removeEventListener('focusin', over); root.removeEventListener('pointerout', out); root.removeEventListener('click', click, true); keyTarget.removeEventListener('keydown', key); view?.removeEventListener?.('resize', place); view?.removeEventListener?.('scroll', place); card.remove();};
}
