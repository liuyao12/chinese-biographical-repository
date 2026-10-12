import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {yearLabel, continuousRows, layoutCells, findCells, parseTableHash, safeSourceURL} from '../assets/historical-tables.js';
const load = n => JSON.parse(readFileSync(new URL(`../data/historical-tables/shiji-${n}.json`, import.meta.url)));
test('complete received tables retain each year and every original cell in both directions', () => {
  for (const [n, count, first, last] of [['014',365,841,477],['015',270,476,207]]) {
    const table = load(n), rows = continuousRows(table);
    assert.equal(rows.length, count);
    assert.equal(rows[0].year.value, first);
    assert.equal(rows.at(-1).year.value, last);
    const vertical = layoutCells(table), horizontal = layoutCells(table, true);
    assert.equal(horizontal.length, vertical.length);
    for (let i = 0; i < vertical.length; i++) {
      assert.equal(horizontal[i].id, vertical[i].id);
      assert.equal(horizontal[i].text, vertical[i].text);
      assert.equal(horizontal[i].x, vertical[i].y);
      assert.equal(horizontal[i].y, vertical[i].x);
      assert.equal(horizontal[i].width, vertical[i].height);
      assert.equal(horizontal[i].height, vertical[i].width);
    }
  }
});
test('Qin unified-table colspan survives as rowspan after axis switch, without duplicating text', () => {
  const table = load('015'), row = continuousRows(table).at(-1);
  assert.equal(row.cells.length, 2);
  assert.equal(row.cells[1].colspan, 8);
  const cell = layoutCells(table, true).find(c => c.id === row.cells[1].id);
  assert.equal(cell.height, 8);
  assert.equal(cell.width, 1);
  assert.equal(cell.text, row.cells[1].text);
});
test('Western labels preserve BCE/CE and never create a year zero or resolve missing dates', () => {
  assert.equal(yearLabel({era:'BCE',value:841}), '西元前 841 年');
  assert.equal(yearLabel({era:'CE',value:1},'en'), '1 CE');
  assert.equal(yearLabel({era:'BCE',value:0}), '年份未定');
  assert.equal(yearLabel(null), '年份未定');
});
test('unconfirmed continuation, changed headings and mixed witnesses refuse joining', () => {
  const original = load('015');
  const split = () => {const t=structuredClone(original), f=t.fragments[0];t.fragments.push({...structuredClone(f),id:'synthetic-second-fragment',rows:f.rows.slice(5)});f.rows=f.rows.slice(0,5);return t;};
  let table = split();assert.throws(() => continuousRows(table), /接續未定/);
  table.fragments[1].continuation={status:'confirmed',direction:'rows',previous_fragment_id:table.fragments[0].id};
  assert.equal(continuousRows(table).length,270);
  table.fragments[1].source_id='synthetic-other-edition';assert.throws(() => continuousRows(table), /不同版本/);
  table=split();table.fragments[1].continuation={status:'confirmed',direction:'rows',previous_fragment_id:table.fragments[0].id};table.fragments[1].source_header=['synthetic changed heading'];assert.throws(() => continuousRows(table),/欄題改變/);
});
test('search includes cells at the end; URLs and fragment state reject unsafe values', () => {
  const table = load('015'), last = continuousRows(table).at(-1).cells[1];
  assert.ok(findCells(table,'子嬰').includes(last.id));
  assert.deepEqual(findCells(table,' '),[]);
  assert.equal(safeSourceURL('javascript:alert(1)'), '');
  assert.equal(safeSourceURL('https://zh.wikisource.org/'), 'https://zh.wikisource.org/');
  assert.deepEqual(parseTableHash('#table=unknown&axis=bad',['shiji-014']),{id:'shiji-014',axis:'vertical',cell:''});
});
