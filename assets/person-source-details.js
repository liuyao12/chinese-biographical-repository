import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {sourcePassageURL} from './corpus-reader.js';
const text = value => typeof value === 'string' && value.trim() ? value : '';
const list = value => Array.isArray(value) ? value : [];
export const challengedOffice = holding => holding?.source_qualification?.kind === 'reported_office_challenged_by_commentary';
export const challengedOfficeBadge = holding => challengedOffice(holding) ? `<small class="person-office-source-warning">${ui('Quoted office name · questioned by commentator')}</small>` : '';
function workName(person, id) {
  const map = person.source_work_titles || {};
  const entry = Object.hasOwn(map, id) ? map[id] : null;
  return text(typeof entry === 'string' ? entry : entry?.title);
}
function evidenceHTML(e, person, quote = '') {
  if (!e || typeof e !== 'object') return '';
  const source = list(person.sources).find(s => s.source_id === e.source_id && s.work_id === e.work_id && s.book_id === e.book_id && s.chapter_id === e.chapter_id);
  const title = workName(person, e.work_id) || text(source?.work_title) || text(source?.source?.title);
  const raw = text(e.quote);
  const displayed = quote && raw.includes(quote) ? quote : raw;
  const href = sourcePassageURL({...e, mention_id: e.person_mention_id});
  return `${title ? `<p class="person-detail-work"><cite>《${h(title)}》</cite></p>` : ''}${displayed ? `<blockquote>${h(displayed)}</blockquote>` : ''}${href ? `<a class="person-detail-source-link" href="${h(href)}">${ui('Read source passage →')}</a>` : ''}`;
}
export function challengedOfficeEvidence(holding, person) {
  if (!challengedOffice(holding)) return '';
  const q = holding.source_qualification, name = workName(person, q.reported_work_id);
  return `<details class="person-office-source-qualification"><summary>${ui('Quoted office and commentary objection')}</summary><section><h5>${ui('Quoted office wording')}${name ? ` · <cite>《${h(name)}》</cite>` : ''}</h5>${list(holding.evidence).map(e => evidenceHTML(e, person)).join('')}</section><section><h5>${ui('Commentary objection')}</h5>${evidenceHTML(q.objection_evidence, person)}</section>${text(q.interpretation_note) ? `<p>${h(q.interpretation_note)}</p>` : ''}<p class="note">${ui('Source wording only; not selected as a confirmed career appointment.')}</p></details>`;
}
const count = (label, value, unit) => Number.isInteger(value) && value > 0 && text(unit) ? `<p>${ui(label)}：${h(value)}${h(unit)}</p>` : '';
function detailView(record, person) {
  const v = record.values || {};
  if (record.kind === 'official_duty') {
    const key = {personnel_selection:'Personnel selection duty',general_administration_of_mobile_secretariat:'Mobile secretariat duty',lecture_attendance:'Lecture attendance duty'}[v.duty_code] || 'Source duty';
    const holding = list(person.titles).find(x => x.id === v.office_title_holding_id && x.person_id === record.person_id);
    const officeName = text(v.office_source_name) || text(holding?.title);
    return {key, values:[officeName ? `<p>${ui('Associated office')}：${h(officeName)}</p>` : '', text(v.organ_source_name) ? `<p>${ui('Source institution')}：${h(v.organ_source_name)}</p>` : ''].join('')};
  }
  if (record.kind === 'command_authority' && v.authority_code === 'command_over_source_group') return {key:'Command authority', values:text(v.subordinate_group_source_name) ? `<p>${ui('Group under command')}：${h(v.subordinate_group_source_name)}</p>` : ''};
  if (record.kind === 'fief_household_count') return {key:v.aggregation === 'cumulative_across_unspecified_awards' ? 'Cumulative fief increase' : 'Source fief count',values:count('Increase recorded',v.increase,v.unit_source_name)+count('Total recorded',v.total,v.unit_source_name)};
  if (record.kind === 'unnamed_family_title_grants') {
    const grants = list(v.grants).filter(g => g && text(g.source_rank) && Number.isInteger(g.recipient_count) && g.recipient_count > 0);
    return {key:'Unnamed family title grants',values:(text(v.recipient_group_source_term) ? `<p>${ui('Source recipient group')}：${h(v.recipient_group_source_term)}</p>` : '')+(grants.length ? `<ul>${grants.map(g => `<li>${h(g.source_rank)} · ${ui('Recipients recorded: {count}',{count:g.recipient_count})}</li>`).join('')}</ul>` : '')+`<p class="note">${ui('Recipients are unnamed; these counts are not a list of identified children.')}</p>`};
  }
  return {key:'Source detail',values:''};
}
function safeURL(value) {
  try {const url = new URL(value); return ['http:', 'https:'].includes(url.protocol) ? url.href : '';} catch {return '';}
}
export function dutyObservationHTML(record, person) {
  const d = record.date_observation;
  if (d?.kind !== 'source_duty_event_observation_window' || d.duration !== false || d.tenure_boundary !== false
      || d.calendar !== 'chinese_civil' || d.precision !== 'year_range' || d.record_id !== record.id || d.person_id !== record.person_id
      || !Number.isInteger(d.earliest) || !Number.isInteger(d.latest) || d.earliest <= 0 || d.latest < d.earliest) return '';
  const proof = d.proof || {}, url = safeURL(proof.url), calendar = safeURL(d.calendar_reference?.url);
  const quotes = ['era','year2','year3','rebellion','end','qiutou'].map(k => text(proof.anchors?.[k]?.quote)).filter(Boolean);
  return `<div class="person-duty-observation"><p>${ui('Duty observed within {start}–{end}; not a tenure.',{start:d.earliest,end:d.latest})}</p><details><summary>${ui('Duty observation date evidence')}</summary>${text(d.local_context?.surface) ? `<blockquote>${h(d.local_context.surface)}</blockquote>` : ''}${list(record.evidence).map(e => evidenceHTML(e,person,text(d.local_context?.surface))).join('')}${[...new Set(quotes)].map(q => `<blockquote>${h(q)}</blockquote>`).join('')}${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${ui('Fixed primary witness')}</a>` : ''}${calendar ? ` · <a href="${h(calendar)}" target="_blank" rel="noopener">${ui('Era-year reference')}</a>` : ''}${text(d.rationale) ? `<p>${h(d.rationale)}</p>` : ''}</details></div>`;
}
export function sourceDetailsHTML(person, full = true) {
  if (!full) return '';
  const records = list(person.source_details).filter(d => d && text(d.source_term));
  if (!records.length) return '';
  return `<section class="person-source-details"><h4>${ui('Duties and other source records')}</h4>${records.map(d => {
    const view = detailView(d, person), scope = text(d.source_detail_pattern?.scope_anchor?.surface);
    return `<article class="person-source-detail" data-detail-id="${h(d.id || '')}"><h5>${ui(view.key)}</h5><p class="person-detail-wording"><q>${h(d.source_term)}</q></p>${view.values}${dutyObservationHTML(d,person)}<details><summary>${ui('Source wording and qualification')}</summary>${list(d.evidence).map(e => evidenceHTML(e, person, scope)).join('')}${text(d.interpretation_note) ? `<p>${h(d.interpretation_note)}</p>` : ''}</details></article>`;
  }).join('')}</section>`;
}
