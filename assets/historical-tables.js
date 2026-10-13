/** Pure source-table layout: transpose geometry, never reinterpret cell text. */
export function safeSourceURL(value) {
  try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : ''; } catch { return ''; }
}
export function yearLabel(year, language = 'zh-Hant') {
  if (!year || !['BCE', 'CE'].includes(year.era) || !Number.isInteger(year.value) || year.value < 1) return language === 'en' ? 'Unresolved year' : '年份未定';
  return language === 'en' ? `${year.value} ${year.era}` : `西元${year.era === 'BCE' ? '前' : ''} ${year.value} 年`;
}
export function continuousRows(table) {
  const rows = [], ids = new Set();
  for (const [index, fragment] of table.fragments.entries()) {
    if (fragment.source_id !== table.source.id) throw new Error('不可混接不同版本的表格');
    if (index && !table.independent_sections && (fragment.continuation?.status !== 'confirmed' || fragment.continuation?.direction !== 'rows' || fragment.continuation?.previous_fragment_id !== table.fragments[index - 1].id)) throw new Error('表格接續未定');
    if (index && !table.independent_sections && JSON.stringify(fragment.source_header) !== JSON.stringify(table.fragments[0].source_header)) throw new Error('欄題改變，須分段檢視');
    for (const row of fragment.rows) {
      if (ids.has(row.id)) throw new Error('年列 ID 重複');
      ids.add(row.id);
      rows.push({...row, fragment_id: fragment.id});
    }
  }
  return rows;
}
export function layoutCells(table, horizontal = false) {
  return continuousRows(table).flatMap((row, rowIndex) => row.cells.map(cell => ({
    ...cell, row_id: row.id, fragment_id: row.fragment_id, year: row.year,
    x: horizontal ? rowIndex : cell.column,
    y: horizontal ? cell.column : rowIndex,
    width: horizontal ? cell.rowspan : cell.colspan,
    height: horizontal ? cell.colspan : cell.rowspan
  })));
}
export function findCells(table, query) {
  const term = String(query).trim();
  return term ? continuousRows(table).flatMap(row => row.cells.filter(c => c.text.includes(term)).map(c => c.id)) : [];
}
export function parseTableHash(hash, allowedIDs) {
  const p = new URLSearchParams(hash.replace(/^#/, ''));
  return {id: allowedIDs.includes(p.get('table')) ? p.get('table') : allowedIDs[0],
    axis: p.get('axis') === 'horizontal' ? 'horizontal' : 'vertical', cell: p.get('cell') || ''};
}
