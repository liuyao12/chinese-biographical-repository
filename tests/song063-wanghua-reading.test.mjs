import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';
import {sourceDetailsHTML} from '../assets/person-source-details.js';

const load = path => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));

test('孔甯子的人物頁保留引語、原典連結與未名古例之考證界線', () => {
  const page = load('../data/corpus/profiles/430_f4c_1b9.json');
  const markup = sourceDetailsHTML(page);
  assert.ok(markup.includes('治阿之宰'));
  assert.ok(markup.includes('子奇年十六'));
  assert.ok(markup.includes('免徒之守'));
  assert.ok(markup.includes('無明文指為奏中此人'));
  assert.ok(markup.includes('oldid=1753957'));
  assert.ok(!markup.includes('{{ProperNoun'));
});

test('王華的人物頁可從十三及殿本十二分別返回所在原段', () => {
  const page = load('../data/corpus/profiles/7r6_k52_qji_ABAAFAB.json');
  const markup = sourceDetailsHTML(page);
  for (const quote of ['華時年十二', '華時年十三', '五月壬午，中護軍王華卒']) {
    assert.ok(markup.includes(quote));
  }
  for (const paragraph of ['c-songshu-063-wanghua-tanshou:line010', 'c-songshu-063-wanghua-wyd:p001']) {
    assert.ok(decodeURIComponent(markup).includes(paragraph));
  }
});
