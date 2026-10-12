import {escapeHTML as h} from './core.js';
import {t, ui, getLocale} from './i18n.js';
import {safeSourceURL, yearLabel, continuousRows, layoutCells, findCells, parseTableHash} from './historical-tables.js';
const $ = id => document.getElementById(id);
const cache = new Map();
let index, table, state, matches = [], matchIndex = -1, request = 0;
function setHash(next) {
  const p = new URLSearchParams({table: next.id, axis: next.axis});
  if (next.cell) p.set('cell', next.cell);
  history.replaceState(null, '', '#' + p);
  state = next;
}
function sourceLink(label, url) {
  const safe = safeSourceURL(url);
  return safe ? `<a href="${h(safe)}" target="_blank" rel="noopener">${ui(label)} ↗</a>` : '';
}
function focusCell(id) {
  const node = document.getElementById(id);
  if (!node || !node.classList.contains('source-cell')) return;
  const scroller = $('table-scroll'), box = node.getBoundingClientRect(), outer = scroller.getBoundingClientRect();
  // Leave room for the sticky year/column headings in either orientation.
  scroller.scrollTop += box.top - outer.top - 120;
  scroller.scrollLeft += box.left - outer.left - 195;
  document.querySelector('.active-cell')?.classList.remove('active-cell');
  node.classList.add('active-cell');
  node.focus({preventScroll: true});
  $('year-select').value = node.dataset.row;
  setHash({...state, cell: id});
}
function search() {
  matches = findCells(table, $('table-search').value);
  matchIndex = -1;
  document.querySelectorAll('.matched').forEach(n => n.classList.remove('matched'));
  matches.forEach(id => document.getElementById(id)?.classList.add('matched'));
  $('search-status').textContent = $('table-search').value.trim() ? t('{count} matching cells', {count: matches.length}) : '';
  $('search-next').disabled = !matches.length;
}
function showCell(id) {
  const row = continuousRows(table).find(r => r.cells.some(c => c.id === id));
  const cell = row?.cells.find(c => c.id === id);
  if (!cell) return;
  focusCell(id);
  $('cell-details').innerHTML = `<p>${h(table.title)} · ${h(yearLabel(row.year, getLocale()))}</p><blockquote data-source-text>${h(cell.text)}</blockquote><p>${ui('Digital table row {row}, cell {cell}', {row: cell.source_row, cell: cell.source_column})}</p><p>${ui('Original span: {rows} rows, {columns} columns', {rows: cell.rowspan, columns: cell.colspan})}</p><p>${ui('Printed page and image position have not been verified.')}</p><p>${sourceLink('Fixed source version', table.source.revision_url)}</p><p><code>${h(cell.id)}</code> · <code>${h(table.source.chapter_id)}</code></p>`;
  $('cell-dialog').showModal();
}
function render() {
  const horizontal = state.axis === 'horizontal', rows = continuousRows(table), cells = layoutCells(table, horizontal);
  $('table-select').value = state.id;
  $('axis-vertical').setAttribute('aria-pressed', String(!horizontal));
  $('axis-horizontal').setAttribute('aria-pressed', String(horizontal));
  $('table-title').textContent = table.title;
  document.title = table.title + ' · 人文';
  $('table-coverage').textContent = t('{years} year rows · {cells} source cells · structural import, review pending', {years: rows.length, cells: cells.length});
  $('table-source-links').innerHTML = sourceLink('Fixed source version', table.source.revision_url) + `<a href="data/historical-tables/${h(table.id)}.json">${ui('Download table JSON')}</a>`;
  $('table-source-details').innerHTML = `<p data-original>${h(table.source.note)}</p><p data-original>${h(table.source.rights)}</p>${sourceLink('Source licensing', table.source.rights_url)}<p>${ui('Original headings')}: <span data-source-text>${table.columns.map(c => h(c.text)).join(' · ')}</span></p><p>${ui('Source revision')}: <code>${h(table.source.revision)}</code> · ${h(table.source.accessed)}</p><p><code>${h(table.source.response_sha256)}</code></p>`;
  $('year-select').innerHTML = rows.map(row => `<option value="${h(row.id)}">${h(yearLabel(row.year, getLocale()))}</option>`).join('');
  const heading = (text, x, y, cls) => `<div role="columnheader" class="grid-cell ${cls}" style="grid-column:${x + 1};grid-row:${y + 1}">${text}</div>`;
  let headers = '';
  if (horizontal) {
    headers = heading(ui('Time / source column'), 0, 0, 'corner-heading');
    headers += rows.map((row, i) => heading(h(yearLabel(row.year, getLocale())), i + 1, 0, 'axis-heading')).join('');
    headers += table.columns.map((c, i) => `<div role="rowheader" class="grid-cell side-heading" style="grid-column:1;grid-row:${i + 2}">${c.kind === 'western_year' ? ui('Western year') : h(c.text)}</div>`).join('');
  } else {
    headers = table.columns.map((c, i) => heading(c.kind === 'western_year' ? ui('Western year') : h(c.text), i, 0, i === 0 ? 'corner-heading' : 'axis-heading')).join('');
  }
  const content = cells.map(c => {
    const western = c.column === 0;
    const text = western ? yearLabel(c.year, getLocale()) : c.text;
    return `<button type="button" role="cell" id="${h(c.id)}" data-row="${h(c.row_id)}" class="grid-cell source-cell ${western ? 'year-cell' : ''}" style="grid-column:${c.x + (horizontal ? 2 : 1)} / span ${c.width};grid-row:${c.y + 2} / span ${c.height}" aria-label="${h(text || t('Empty source cell'))}" data-source-text>${h(text)}${text ? '' : '<span aria-hidden="true">&nbsp;</span>'}</button>`;
  }).join('');
  const grid = $('table-grid');
  grid.className = 'historical-grid' + (horizontal ? ' horizontal' : '');
  grid.setAttribute('role', 'table');
  grid.setAttribute('aria-label', table.title);
  grid.style.gridTemplateColumns = horizontal ? `11rem repeat(${rows.length}, 14rem)` : `11rem repeat(${table.columns.length - 1}, 13rem)`;
  grid.innerHTML = headers + content;
  $('table-scroll').scrollTop = 0;
  $('table-scroll').scrollLeft = 0;
  search();
  if (state.cell) focusCell(state.cell);
}
async function open() {
  const ticket = ++request;
  state = parseTableHash(location.hash, index.tables.map(t => t.id));
  const entry = index.tables.find(t => t.id === state.id);
  if (!cache.has(entry.id)) {
    const response = await fetch(entry.path);
    if (!response.ok) throw new Error(t('Table data could not be loaded.'));
    cache.set(entry.id, await response.json());
  }
  if (ticket !== request) return;
  table = cache.get(entry.id);
  setHash(state);
  render();
}
function fail(error) { $('table-coverage').textContent = error.message; $('table-coverage').setAttribute('role', 'alert'); }
(async () => {
  try {
    const response = await fetch('data/historical-tables/index.json');
    if (!response.ok) throw new Error(t('Table data could not be loaded.'));
    index = await response.json();
    $('table-select').innerHTML = index.tables.map(e => `<option value="${h(e.id)}">${h(e.title)}</option>`).join('');
    $('table-select').onchange = () => { setHash({...state, id: $('table-select').value, cell: ''}); open().catch(fail); };
    for (const axis of ['vertical', 'horizontal']) $('axis-' + axis).onclick = () => {
      const visible = [...document.querySelectorAll('.source-cell')].find(n => { const box = n.getBoundingClientRect(), outer = $('table-scroll').getBoundingClientRect(); return box.top > outer.top + 110 && box.top < outer.bottom && box.left > outer.left + 180 && box.left < outer.right; });
      setHash({...state, axis, cell: state.cell || visible?.id || ''}); render();
    };
    $('year-select').onchange = () => { const row = continuousRows(table).find(r => r.id === $('year-select').value); if (row) focusCell(row.cells[0].id); };
    $('table-search').oninput = search;
    $('search-next').onclick = () => { if (matches.length) focusCell(matches[++matchIndex % matches.length]); };
    $('table-grid').onclick = e => { const cell = e.target.closest('.source-cell'); if (cell) showCell(cell.id); };
    window.addEventListener('hashchange', () => open().catch(fail));
    window.addEventListener('renwen:languagechange', () => { if (table) render(); });
    await open();
  } catch (error) { fail(error); }
})();
