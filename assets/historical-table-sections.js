import {escapeHTML as h} from './core.js';
import {markCell} from './cbr-person.js';
import {layoutCells, yearLabel} from './historical-tables.js';

/** Keep independent source tables separate while transposing their geometry. */
export function sectionMarkup(table, horizontal, language = 'zh-Hant') {
  return table.fragments.map((fragment, sectionIndex) => {
    const columns = fragment.columns;
    const western = columns[0]?.kind === 'western_year';
    const local = {...table, independent_sections: false, columns, fragments: [fragment]};
    const heading = (text, column, row, side = false) => `<div role="${side ? 'rowheader' : 'columnheader'}" class="grid-cell ${side ? 'side-heading' : 'axis-heading'}" style="grid-column:${column};grid-row:${row}">${h(text)}</div>`;
    const editorial = language === 'en' ? 'Western year · editorial addition · axis 0' : '西元對照 · 編輯增補 · 第零軸';
    let headers = '';
    if (horizontal) {
      headers = columns.map((c, i) => heading(c.kind === 'western_year' ? editorial : c.text, 1, i + (western ? 1 : 2), true)).join('');
    } else {
      headers = columns.map((c, i) => heading(c.kind === 'western_year' ? editorial : c.text, i + 1, 1)).join('');
    }
    const cells = layoutCells(local, horizontal).map(c => {
      const isYear = columns[c.column]?.kind === 'western_year';
      const text = isYear && c.year ? yearLabel(c.year, language) : c.text;
      const x = c.x + (horizontal ? 2 : 1), y = c.y + (horizontal ? (western ? 1 : 2) : 2);
      return `<div tabindex="0" role="cell" id="${h(c.id)}" data-row="${h(c.row_id)}" class="grid-cell source-cell ${isYear ? 'year-cell' : ''}" style="grid-column:${x} / span ${c.width};grid-row:${y} / span ${c.height}" aria-label="${h(text)}" ${isYear ? 'data-editorial-year="true"' : 'data-source-text'}>${isYear ? h(text) : markCell(c)}</div>`;
    }).join('');
    const widths = horizontal ? `11rem repeat(${fragment.rows.length}, 14rem)` : `repeat(${columns.length}, 13rem)`;
    const label = language === 'en' ? `Source table section ${sectionIndex + 1}` : `原表分組 ${sectionIndex + 1}`;
    return `<section class="historical-table-section"><h3>${h(label)}</h3><div role="table" aria-label="${h(table.title + ' · ' + label)}" class="historical-grid${horizontal ? ' horizontal' : ''}" style="grid-template-columns:${widths}">${headers}${cells}</div></section>`;
  }).join('');
}
