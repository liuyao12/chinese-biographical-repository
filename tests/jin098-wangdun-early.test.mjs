import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const bytes = path => readFileSync(new URL('../' + path, import.meta.url));
const read = path => JSON.parse(bytes(path));
const raw = read('source-evidence/jin098-wangdun-early/reading.json');
const chapter = read('corpus/jinshu/098-jin033-wangji.json');
test('開篇十段的固定見證、吹笛與行酒各自的主人', () => {
  assert.deepEqual(raw.reviewed_raw_lines, [11,13,15,17,19,21,23,25,27,29]);
  for (const clause of raw.parallel_clauses) {
    const w = raw.witnesses[clause.witness], b = bytes(w.raw_path);
    assert.equal(createHash('sha256').update(b).digest('hex'), w.raw_sha256);
    assert.equal([...b.toString()].slice(clause.raw_start, clause.raw_end).join(''), clause.quote);
  }
  const story = raw.episodes[0];
  assert.match(story.song_text.quote, /^石崇/); assert.match(story.liu_note.quote, /王君夫問王敦/);
  const p=chapter.paragraphs[0]; assert.match(p.text,/又造愷，愷使美人行酒/);
  assert.ok(p.mentions.every(m=>m.surface!=='太子'||p.text.slice(m.start).startsWith('太子遷許昌')));
});
test('元帝引用中的吾與卿分層；叔父兩端、襄城封號與父婚皆有對應', () => {
  const rr=chapter.annotation.person_reference_occurrences.filter(x=>x.quote==='吾與卿及茂弘');
  assert.deepEqual(rr.map(x=>[x.surface,x.person_id,x.referent_role]),[['吾','dkn_ge4_286_AAAAAAA','speaker_self'],['卿','39o_b6y_n74','addressee']]);
  const a=read('corpus/jinshu/098-jin033-wangji-assertions.json').assertions.filter(a=>a.id.includes('dun-early'));
  assert.ok(a.some(a=>a.predicate==='paternal_uncle'&&a.qualifiers.source_term==='敦叔父彥'));
  const m=a.find(x=>x.predicate==='spouse'); assert.equal(a.find(x=>x.predicate==='father').subject_person_id,m.object_person_id);
});
