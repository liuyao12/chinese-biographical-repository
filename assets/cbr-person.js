import {escapeHTML as h} from './core.js';
import {chapterURL} from './corpus-reader.js';
const cache = new Map();
export const profileURL = id => 'person.html#' + encodeURIComponent(id);
export async function loadPerson(id) {
  if (!cache.has(id)) cache.set(id, fetch('data/corpus/profiles/' + encodeURIComponent(id) + '.json').then(r => {if (!r.ok) throw Error('人物資料尚未載入'); return r.json();}).catch(e => {cache.delete(id); throw e;}));
  return cache.get(id);
}
const evidenceLinks = evidence => (evidence || []).map(e => {
  const number = Number(/shiji-(\d{3})/.exec(e.chapter_id || '')?.[1]);
  return number ? `<a href="${h(chapterURL(number, '', e.paragraph_id))}">來源原文 →</a>` : '';
}).join(' · ');
export function personCard(p, full = false) {
  const grouped = new Map();
  for (const x of p.titles || []) {
    const key = x.title + '|' + x.period;
    if (!grouped.has(key)) grouped.set(key, {...x, evidence: []});
    grouped.get(key).evidence.push(...(x.evidence || []));
  }
  const titles = [...grouped.values()], occurrences = p.occurrences || [];
  const principal = [...occurrences].sort((a,b) => b.count - a.count)[0];
  const dates = (p.dates || []).filter(x => x.era_year && x.original_quote);
  const relations = p.relations || [], labels = {father:'父',mother:'生母',spouse:'配偶',son:'子',daughter:'女',brother:'兄弟',grandfather:'祖父'};
  return `<article class="cbr-profile"><p class="eyebrow">人物資料 · ${p.review === 'source_local_candidate' ? '來源局部候選' : '來源辨認暫定'}</p><h${full ? 1 : 3}>${h(p.label)}</h${full ? 1 : 3}><p class="person-aliases">${(p.names || []).filter(x => x !== p.label).slice(0, full ? undefined : 5).map(x => `<span>${h(x)}</span>`).join(' ')}</p>${full && p.identity_note ? `<p class="note">${h(p.identity_note)}</p>` : ''}${principal ? `<blockquote class="person-overview">${h(principal.quote.slice(0, full ? 220 : 110))}</blockquote><p class="person-principal-source"><a href="${h(chapterURL(principal.number, principal.category, principal.paragraph_id))}">《史記·${h(principal.title)}》 →</a><br><small>已標記正文中最多提及的來源</small></p>` : ''}
  ${dates.length ? `<section class="person-date-evidence"><h4>紀年對照</h4>${dates.slice(0, full ? undefined : 2).map(x => `<p><strong>西元${x.era === 'BCE' ? '前' : ''}${x.era_year}年</strong> <small>編輯對照 · 暫定</small><br><q>${h(x.original_quote)}</q>${full ? '<br>' + evidenceLinks(x.evidence) : ''}</p>`).join('')}</section>` : ''}
  <div class="person-facts"><section><h4>稱號與持職</h4>${titles.slice(0, full ? undefined : 2).map(x => `<div class="person-title"><strong>${h(x.title)}</strong><br><small>${h(x.period === '未定 → 未定' ? '起訖未定' : x.period || '起訖未定')}</small>${full ? `<details><summary>${x.evidence.length} 筆來源證據</summary>${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details>` : ''}</div>`).join('') || '<p>尚無已整理的稱號紀錄</p>'}</section>
  <section><h4>來源所記地望</h4>${(p.addresses || []).slice(0, full ? undefined : 2).map(x => `<div class="person-address"><strong>${h(x.term)}</strong>${full ? `<details><summary>查看原文證據</summary><blockquote>${h(x.quote)}</blockquote>${evidenceLinks(x.evidence)}</details>` : ''}</div>`).join('') || '<p>尚未整理</p>'}</section></div>
  ${full && relations.length ? `<section><h4>來源所記親屬</h4><ul>${relations.map(x => `<li>${h(p.related_people?.[x.subject_person_id] || x.subject_person_id)} · ${h(labels[x.predicate] || x.qualifiers?.source_term || x.predicate)}：${h(p.related_people?.[x.object_person_id] || x.object_person_id)}<details><summary>來源與關係原詞</summary><p>${h(x.qualifiers?.source_term || '')}</p>${x.evidence.map(e => `<blockquote>${h(e.quote)}</blockquote>${evidenceLinks([e])}`).join('')}</details></li>`).join('')}</ul></section>` : ''}
  ${full ? `<section><h4>年表原文</h4><ul class="person-occurrences">${(p.table_occurrences || []).map(x => `<li><a href="shiji.html#chapter=15&category=biao&cell=${encodeURIComponent(x.cell_id)}">${h(x.title)} · 西元前${x.year.value}年 →</a><blockquote>${h(x.quote)}</blockquote></li>`).join('')}</ul></section>` : ''}
  <section><h4>出現篇章</h4><ul class="person-occurrences">${occurrences.slice(0, full ? undefined : 3).map(x => `<li><a href="${h(chapterURL(x.number, x.category, x.paragraph_id))}">《史記·${h(x.title)}》 →</a>${full ? `<p><q>${h(x.quote)}</q></p>` : ''}<small>${h(x.count)} 處標記</small></li>`).join('') || '<li>尚未確定與其他篇章的同指；可從本頁年表原文核讀。</li>'}</ul></section>
  ${full ? `<details class="person-data-download"><summary>資料識別與機讀檔案</summary><code>${h(p.id)}</code><p><a href="data/corpus/profiles/${encodeURIComponent(p.id)}.json">人物頁 JSON</a>${p.review !== 'source_local_candidate' ? ` · <a href="https://github.com/liuyao12/chinese-biographical-repository/blob/main/exports/persons/${encodeURIComponent(p.id)}.json">CBR 完整來源包</a>` : ''}</p></details>` : `<a class="person-profile-button" href="${h(profileURL(p.id))}">閱讀完整人物頁 →</a>`}</article>`;
}
export function markCell(cell) {
  const chars = Array.from(cell.text), out = []; let end = 0;
  for (const m of [...(cell.person_mentions || []), ...(cell.unresolved_mentions || [])].sort((a,b) => a.start - b.start)) {
    if (m.start < end || chars.slice(m.start, m.end).join('') !== m.surface) throw Error('年表人物標記與原文不符');
    out.push(h(chars.slice(end, m.start).join('')));
    if (!m.person_id) {out.push(`<span class="table-unresolved-mention" tabindex="0" role="button" title="${h(m.interpretation_note)}">${h(m.surface)}</span>`); end = m.end; continue;}
    out.push(`<a class="table-person-link" data-person-id="${h(m.person_id)}" href="${h(profileURL(m.person_id))}" title="查看人物資料">${h(m.surface)}</a>`); end = m.end;
  }
  out.push(h(chars.slice(end).join(''))); return out.join('');
}
export function bindPersonCards(root) {
  const card = document.createElement('aside'); card.className = 'table-person-card'; card.hidden = true; card.setAttribute('aria-label', '人物資料'); root.append(card);
  let ticket = 0, timer;
  async function show(node, focus = false) {
    clearTimeout(timer); const current = ++ticket; card.hidden = false;
    card.innerHTML = '<p role="status">載入人物資料…</p>';
    try {const p = await loadPerson(node.dataset.personId); if (current !== ticket) return; card.innerHTML = `<button type="button" class="close-person-card" aria-label="關閉人物資料">關閉</button>` + personCard(p); card.querySelector('button').onclick = hide; card.scrollTop = 0; if (focus) card.querySelector('.close-person-card').focus({preventScroll:true});}
    catch {if (current === ticket) card.innerHTML = `<p>人物資料尚未載入。</p><a href="${h(profileURL(node.dataset.personId))}">開啟人物頁</a>`;}
  }
  function hide() {ticket++; card.hidden = true;}
  const over = e => {const n = e.target.closest('.table-person-link'); if (n) show(n);};
  const out = e => {if (e.relatedTarget && (card.contains(e.relatedTarget) || e.relatedTarget.closest?.('.table-person-link'))) return; timer = setTimeout(hide, 250);};
  const click = e => {const n = e.target.closest('.table-person-link'); if (n && !e.metaKey && !e.ctrlKey) {e.preventDefault(); e.stopPropagation(); show(n, true);}};
  root.addEventListener('pointerover', over); root.addEventListener('focusin', over); root.addEventListener('pointerout', out); root.addEventListener('click', click, true);
  card.onpointerenter = () => clearTimeout(timer); card.onpointerleave = out;
  const key = e => {if (e.key === 'Escape') hide();}; root.addEventListener('keydown', key);
  return () => {hide(); clearTimeout(timer); root.removeEventListener('pointerover', over); root.removeEventListener('focusin', over); root.removeEventListener('pointerout', out); root.removeEventListener('click', click, true); root.removeEventListener('keydown', key); card.remove();};
}
