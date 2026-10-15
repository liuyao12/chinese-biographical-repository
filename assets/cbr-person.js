import {escapeHTML as h} from './core.js';
import {chapterURL} from './corpus-reader.js';
import {yearLabel} from './historical-tables.js';
import {traceFamily} from './person-family.js';
import {summarizeLife, ageLabel, lifeYearLabel} from './person-life.js';
export const loadFamily = p => traceFamily(p, loadPerson);
export function tableOccurrenceURL(x) {
  const match = /^shiji-(\d{3})$/.exec(x.table_id || '');
  if (!match) return '';
  return 'shiji.html#' + new URLSearchParams({chapter: String(Number(match[1])), category: 'biao', cell: x.cell_id});
}
const cache = new Map();
export const profileURL = (id, tableID = '') => 'person.html' + (/^shiji-\d{3}$/.test(tableID) ? '?table=' + encodeURIComponent(tableID) : '') + '#' + encodeURIComponent(id);
export async function loadPerson(id) {
  if (!cache.has(id)) cache.set(id, fetch('data/corpus/profiles/' + encodeURIComponent(id) + '.json').then(r => {if (!r.ok) throw Error('人物資料尚未載入'); return r.json();}).catch(e => {cache.delete(id); throw e;}));
  return cache.get(id);
}
const evidenceLinks = evidence => (evidence || []).map(e => {
  const number = Number(/shiji-(\d{3})/.exec(e.chapter_id || '')?.[1]);
  return number ? `<a href="${h(chapterURL(number, '', e.paragraph_id))}">來源原文 →</a>` : '';
}).join(' · ');
export function personBundleURL(id, sourceRef = 'main') {
  const ref = /^[a-f0-9]{40}$/.test(sourceRef) ? sourceRef : 'main';
  return 'https://github.com/liuyao12/chinese-biographical-repository/blob/' + ref + '/exports/persons/' + encodeURIComponent(id) + '.json';
}
export function personCard(p, full = false, sourceRef = 'main', family = null) {
  const relativeList = entries => entries?.length ? entries.map(x => `<a href="${h(profileURL(x.person?.id || x.id))}">${h(x.label)}</a>${x.cycle ? '（世系循環，停止追溯）' : ''}${x.unavailable ? '（資料未載入）' : ''}${x.role === 'legal_or_dynastic' ? '（法定／宗統）' : ''}${x.role === 'assembly_inferred' ? '（父系暫定）' : ''}<details><summary>親屬來源</summary>${x.inference_note ? `<p>${h(x.inference_note)}</p>` : ''}${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details>`).join('、') : '';
  const familyRows = family ? [
    ...family.ancestors.map((entries, i) => [ ['父','祖','曾祖'][i], entries, entries.length > 1 ? '多項來源主張，尚未統一' : '' ]),
    ['生母', family.mother, family.mother.length > 1 ? '多項生母記錄，身份或說法待整合' : ''],
    ['配偶', family.spouses, ''], ['子女', family.children, '']
  ].filter(([, entries]) => entries.length).map(([label, entries, note]) => `<dt>${label}</dt><dd>${note ? `<small>${note}</small><br>` : ''}${relativeList(entries)}</dd>`).join('') : '';
  const familyHTML = familyRows ? `<section class="person-family"><h4>家族</h4><dl>${familyRows}</dl></section>` : '';
  const components = p.name_components || [];
  const names = components.length === 1 ? components[0] : null;
  const heading = names ? `${names.title || ''} ${names.surname || ''}${names.ming || ''}`.trim() : p.label;
  const additional = names?.additional_names?.length ? names.additional_names : (p.names || []).filter(x => ![p.label, heading, names?.title, names?.ming, names?.surname + names?.ming].includes(x)).slice(0, 5);
  const nameEvidence = names ? `<details class="person-name-evidence"><summary>姓名依據</summary><blockquote>${h(names.quote)}</blockquote>${evidenceLinks([names])}<p>${h(names.note)}</p></details>` : '';
  const life = summarizeLife(p);
  const lifeRow = (label, events) => {
    const dated = events.filter(e => lifeYearLabel(e) || e.date_expression);
    return dated.length ? `<dt>${label}</dt><dd>${dated.map(e => {
      const values = [lifeYearLabel(e) ? `<strong>${h(lifeYearLabel(e))}</strong>` : '', e.date_expression ? h(e.date_expression) : ''].filter(Boolean);
      return `<div>${values.join(' · ')}<details><summary>原文與紀年依據</summary>${(e.evidence || []).map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}${e.normalized_date_range && full ? dateReferences(e.normalized_date_range) : ''}</details></div>`;
    }).join('')}</dd>` : '';
  };
  const ages = life.ages.filter(e => Number.isInteger(e.value) || e.qualified_source_term || e.source_term);
  const ageWhen = e => {
    const date = e.normalized_date;
    const values = [e.date_expression, date?.era_year ? `西元${date.era === 'BCE' ? '前' : ''}${date.era_year}年` : ''].filter(Boolean);
    return values.length ? `<small> · ${values.map(h).join(' · ')}（報齡時）</small>` : '';
  };
  const grouped = new Map();
  for (const x of p.titles || []) {
    const key = x.title + '|' + x.period + '|' + JSON.stringify(x.reported_office_event_counts || null) + '|' + JSON.stringify([x.kind || null, x.jurisdictions || null]);
    if (!grouped.has(key)) grouped.set(key, {...x, evidence: [], date_periods: []});
    grouped.get(key).evidence.push(...(x.evidence || []));
    grouped.get(key).date_periods.push(x.effective_period);
  }
  const titles = [...grouped.values()], occurrences = p.occurrences || [];
  const principal = [...occurrences].sort((a,b) => b.count - a.count)[0];
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
    return `<blockquote>${h(r.quote)}</blockquote>${url ? `<a href="${h(url)}" target="_blank" rel="noopener">${h(r.title || '來源')}</a>` : h(r.title || '')}`;
  }).join('');
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
      birth_place: '出生地', residence: '居地', service_location: '任事地', death_place: '卒地', burial_place: '葬地'}[x.relation];
    return label && x.place?.source_name ? label + '：' + x.place.source_name : x.term;
  };
  const lifeRows = lifeRow('生', life.birth) + lifeRow('卒', life.death) + (ages.length ? `<dt>年齡</dt><dd>${ages.map(e => `${h(ageLabel(e))}${ageWhen(e)}<details><summary>報齡原文</summary>${(e.evidence || []).map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}</details>`).join('')}</dd>` : '');
  const lifeHTML = lifeRows ? `<section class="person-life-summary"><dl>${lifeRows}</dl></section>` : '';
  const variants = p.reported_variants || [];
  const relations = p.relations || [], labels = {father:'父',mother:'生母',stepmother:'後母',adoptive_mother:'所母',spouse:'配偶',son:'子',daughter:'女',brother:'兄弟',grandfather:'祖父'};
  const identityCasesHTML = full && p.unresolved_identity_cases?.length ? `<section class="person-identity-cases"><h4>身份待考</h4>${p.unresolved_identity_cases.map(c => `<details><summary>分開保留的候選人物</summary><p>${h(c.note)}</p><p>${c.candidate_person_ids.map(id => `<a href="${h(profileURL(id))}">${h(p.related_people?.[id] || id)}</a>`).join('、')}</p>${evidenceLinks(c.paragraph_ids.map(paragraph_id => ({chapter_id:paragraph_id.split(':')[0],paragraph_id})))}${dateReferences(c)}</details>`).join('')}</section>` : '';
  const readingHTML = full && p.reading_decisions?.length ? `<section class="person-reading-evidence"><h4>名物辨讀</h4>${p.reading_decisions.map(d => `<details><summary>讀法與來源</summary><p>${h(d.rationale)}</p>${evidenceLinks(d.evidence.map(e => ({...e,chapter_id:e.chapter_id || e.paragraph_id.split(':')[0]})))}${dateReferences(d)}</details>`).join('')}</section>` : '';
  const proposalHTML = full && p.title_proposals?.length ? `<section class="person-title-proposals"><h4>擬議而未授的稱號</h4>${p.title_proposals.filter(x => x.outcome === 'not_enacted').map(x => `<details><summary>${h(x.title)} · 未實行提議</summary><p>${h(x.interpretation_note)}</p>${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details>`).join('')}</section>` : '';
  return `<article class="cbr-profile"><p class="eyebrow">人物資料 · ${p.review === 'source_local_candidate' ? '來源局部候選' : '來源辨認暫定'}</p><h${full ? 1 : 3}>${h(heading)}</h${full ? 1 : 3}>${p.historicity === 'legendary_tradition' ? '<p class="person-historicity">傳說敘事人物</p>' : ''}${additional.length ? `<p class="person-aliases">${additional.map(x => `<span>${h(x)}</span>`).join(' ')}</p>` : ''}${nameEvidence}${(p.names || []).length ? `<details class="person-source-names"><summary>來源中的其他稱呼</summary><p>${p.names.map(x => h(x)).join('、')}</p></details>` : ''}${lifeHTML}${familyHTML}${full && p.identity_note ? `<p class="note">${h(p.identity_note)}</p>` : ''}${identityCasesHTML}${readingHTML}${proposalHTML}${principal ? `<blockquote class="person-overview">${h(principal.quote.slice(0, full ? 220 : 110))}</blockquote><p class="person-principal-source"><a href="${h(chapterURL(principal.number, principal.category, principal.paragraph_id))}">《史記·${h(principal.title)}》 →</a><br><small>已標記正文中最多提及的來源</small></p>` : ''}
  ${!principal && tableExample ? `<blockquote class="person-overview">${h(tableExample.quote.slice(0, full ? 220 : 150))}</blockquote><p class="person-principal-source"><a href="${h(tableOccurrenceURL(tableExample))}">${h(tableExample.title)} · 查看原格 →</a></p>${!full && p.identity_note ? `<p class="note">${h(p.identity_note)}</p>` : ''}` : ''}
  ${dates.length ? `<section class="person-date-evidence"><h4>紀年對照</h4>${dates.slice(0, full ? undefined : 2).map(x => `<div class="person-date-item"><p><strong>西元${x.era === 'BCE' ? '前' : ''}${x.era_year}年</strong> <small>編輯對照 · 暫定${h(dateChoice(x))}</small><br><q>${h(x.original_quote)}</q>${full ? '<br>' + evidenceLinks(x.evidence) : ''}</p>${lifeDateSources(x)}</div>`).join('')}</section>` : ''}
  ${full && dateDecisions.length ? `<section class="person-date-decisions"><h4>生卒紀年取捨 · 暫定</h4>${dateDecisions.map(d => `<p>${h(d.rationale)}</p>${evidenceLinks(d.evidence)}`).join('')}</section>` : ''}
  ${full && variants.length ? `<section class="person-textual-variants"><h4>校勘參考</h4><p>其他來源所載或注家所議，尚未核書影；未採改正文。</p><ul>${variants.map(v => `<li>正文「${h(v.received_reading)}」 · 所報或所議「${h(v.reported_reading)}」<details><summary>${h(v.commentator)}</summary><blockquote>${h(v.quote)}</blockquote><a href="${h(v.url)}" target="_blank" rel="noopener">異文來源</a></details></li>`).join('')}</ul></section>` : ''}
  ${full && lifeEvents.length ? `<section class="person-life-events"><h4>來源所記生卒</h4>${lifeEvents.map(e => `<div><strong>${e.event_type === 'death' ? '死亡' : '出生'}</strong>${e.date_expression ? ' · ' + h(e.date_expression) : ''}<details><summary>${h(e.source_term || '查看原文')}</summary>${e.evidence.map(x => `<blockquote>${h(x.quote)}</blockquote>${evidenceLinks([x])}`).join('')}${e.interpretation_note ? `<p>${h(e.interpretation_note)}</p>` : ''}</details></div>`).join('')}</section>` : ''}
  ${titles.length || addresses.length ? `<div class="person-facts">${titles.length ? `<section><h4>稱號與持職</h4>${titles.slice(0, full ? undefined : 2).map(x => `<div class="person-title"><strong>${h(x.title)}</strong>${titleKind(x)}${titleJurisdictions(x)}${titlePeriod(x) ? `<br><small>${h(titlePeriod(x))}</small>` : ''}${officeCounts(x)}${full ? `<details><summary>${x.evidence.length} 筆來源證據</summary>${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details>` : ''}${titleDateSources(x)}</div>`).join('')}</section>` : ''}
  ${addresses.length ? `<section><h4>來源所記地望</h4>${addresses.slice(0, full ? undefined : 2).map(x => `<div class="person-address"><strong>${h(addressHeading(x))}</strong>${full ? `<details><summary>查看原文證據</summary><blockquote>${h(x.quote)}</blockquote>${evidenceLinks(x.evidence)}${x.interpretation_note ? `<p>${h(x.interpretation_note)}</p>` : ''}</details>` : ''}</div>`).join('')}</section>` : ''}</div>` : ''}
  ${full && relations.length ? `<section><h4>來源所記親屬</h4><ul>${relations.map(x => `<li>${h(p.related_people?.[x.subject_person_id] || x.subject_person_id)} · ${h(labels[x.predicate] || x.qualifiers?.source_term || x.predicate)}：${h(p.related_people?.[x.object_person_id] || x.object_person_id)}<details><summary>來源與關係原詞</summary><p>${h(x.qualifiers?.source_term || '')}</p>${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details></li>`).join('')}</ul></section>` : ''}
  ${full && p.table_occurrences?.length ? `<section><h4>表中原文</h4><ul class="person-occurrences">${(p.table_occurrences || []).map(x => `<li><a href="${h(tableOccurrenceURL(x))}">${h(x.title)} · ${h(yearLabel(x.year))} →</a><blockquote>${h(x.quote)}</blockquote>${x.mention?.identity_evidence?.length ? `<details class="person-identity-evidence"><summary>人物同指的篇文證據 · 暫定</summary>${x.mention.identity_evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}${e.source_revision ? `<p><small>固定修訂 <code>${h(e.source_revision)}</code></small></p>` : ''}`).join('')}</details>` : ''}</li>`).join('')}</ul></section>` : ''}
  ${occurrences.length ? `<section><h4>出現篇章</h4><ul class="person-occurrences">${occurrences.slice(0, full ? undefined : 3).map(x => `<li><a href="${h(chapterURL(x.number, x.category, x.paragraph_id))}">《史記·${h(x.title)}》 →</a>${full ? `<p><q>${h(x.quote)}</q></p>` : ''}<small>${h(x.count)} 處標記</small></li>`).join('')}</ul></section>` : ''}
  ${full ? `<details class="person-data-download"><summary>資料識別與機讀檔案</summary><code>${h(p.id)}</code><p><a href="data/corpus/profiles/${encodeURIComponent(p.id)}.json">人物頁 JSON</a>${p.review !== 'source_local_candidate' ? ` · <a class="person-source-bundle-link" href="${h(personBundleURL(p.id, sourceRef))}">CBR 完整來源包</a>` : ''}</p></details>` : `<a class="person-profile-button" href="${h(profileURL(p.id))}">閱讀完整人物頁 →</a>`}</article>`;
}
export function markCell(cell) {
  const chars = Array.from(cell.text), out = []; let end = 0;
  for (const m of [...(cell.person_mentions || []), ...(cell.unresolved_mentions || [])].sort((a,b) => a.start - b.start)) {
    if (m.start < end || chars.slice(m.start, m.end).join('') !== m.surface) throw Error('年表人物標記與原文不符');
    out.push(h(chars.slice(end, m.start).join('')));
    if (!m.person_id) {out.push(`<span class="table-unresolved-mention" tabindex="0" role="button" title="${h(m.interpretation_note)}">${h(m.surface)}</span>`); end = m.end; continue;}
    out.push(`<a class="table-person-link" data-person-id="${h(m.person_id)}" href="${h(profileURL(m.person_id, /^shiji-\d{3}/.exec(cell.id || '')?.[0]))}" title="查看人物資料">${h(m.surface)}</a>`); end = m.end;
  }
  out.push(h(chars.slice(end).join(''))); return out.join('');
}
export function bindPersonCards(root) {
  const card = document.createElement('aside'); card.className = 'table-person-card'; card.hidden = true; card.setAttribute('aria-label', '人物資料'); root.append(card);
  let ticket = 0, timer;
  async function show(node, focus = false) {
    clearTimeout(timer); const current = ++ticket; card.hidden = false;
    card.innerHTML = '<p role="status">載入人物資料…</p>';
    try {const p = await loadPerson(node.dataset.personId); const family = await loadFamily(p); if (current !== ticket) return; card.innerHTML = `<button type="button" class="close-person-card" aria-label="關閉人物資料">關閉</button>` + personCard(p, false, 'main', family); card.querySelector('button').onclick = hide; card.querySelector('.person-profile-button').href = node.href; card.scrollTop = 0; if (focus) card.querySelector('.close-person-card').focus({preventScroll:true});}
    catch {if (current === ticket) card.innerHTML = `<p>人物資料尚未載入。</p><a href="${h(profileURL(node.dataset.personId))}">開啟人物頁</a>`;}
  }
  function hide() {ticket++; card.hidden = true;}
  const over = e => {if (e.type === 'pointerover' && e.pointerType === 'touch') return; const n = e.target.closest('.table-person-link, .cbr-person-link'); if (n && (e.type !== 'focusin' || n.matches(':focus-visible'))) show(n);};
  const out = e => {if (e.pointerType === 'touch') return; if (e.relatedTarget && (card.contains(e.relatedTarget) || e.relatedTarget.closest?.('.table-person-link, .cbr-person-link'))) return; timer = setTimeout(hide, 250);};
  const click = e => {const n = e.target.closest('.table-person-link, .cbr-person-link'); if (n && !e.metaKey && !e.ctrlKey) {e.preventDefault(); e.stopPropagation(); show(n, true);}};
  root.addEventListener('pointerover', over); root.addEventListener('focusin', over); root.addEventListener('pointerout', out); root.addEventListener('click', click, true);
  card.onpointerenter = () => clearTimeout(timer); card.onpointerleave = out;
  const key = e => {if (e.key === 'Escape') hide();}; root.addEventListener('keydown', key);
  return () => {hide(); clearTimeout(timer); root.removeEventListener('pointerover', over); root.removeEventListener('focusin', over); root.removeEventListener('pointerout', out); root.removeEventListener('click', click, true); root.removeEventListener('keydown', key); card.remove();};
}
