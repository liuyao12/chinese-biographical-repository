import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const bytes = p => readFileSync(new URL('../' + p, import.meta.url));
const read = p => JSON.parse(bytes(p));
const h = read('source-evidence/jin098-wangdun-main/reading.json');
const chapter = read('corpus/jinshu/098-jin033-wangji.json');
const ps = Object.fromEntries(chapter.paragraphs.map(p=>[p.id,p]));
const slice = (s,a,b) => Array.from(s).slice(a,b).join('');
const names = Object.fromEntries(chapter.paragraphs.flatMap(p=>p.mentions.map(m=>[m.id,m])));
test('王敦全傳三十七段、回讀清冊與逐碼點覆核平行原證',()=>{
  assert.equal(chapter.paragraphs.length,37);
  assert.ok(chapter.paragraphs.every(p=>p.annotation_status==='reviewed'));
  assert.deepEqual(h.reviewed_paragraphs.map(p=>p.raw_line),Array.from({length:27},(_,i)=>31+2*i));
  const row=read('data/corpus/six-dynasties-biographies.json').biographies.find(x=>x.book_id==='b-jinshu-098'&&x.title==='王敦');
  assert.ok(row.entry_checked&&row.full_text&&row.first_pass&&row.item_reviewed);
  for (const s of h.source_clauses) {
    const w=h.witnesses[s.witness],b=bytes(w.raw_path);
    assert.equal(createHash('sha256').update(b).digest('hex'),w.raw_sha256);
    assert.equal(slice(b.toString(),s.raw_start,s.raw_end),s.quote);
  }
  assert.deepEqual(h.edition_images.map(v=>v.pdf_page),[11,12,13,14,15,16,17,1374]);
  for (const v of h.edition_images) {
    assert.match(v.source_url,new RegExp(`^https://upload\\.wikimedia\\.org/.+\\.pdf#page=${v.pdf_page}$`));
    assert.match(v.capture_sha256,/^[0-9a-f]{64}$/);
  }
});
test('殿本王凌、奮威瞻辨識，保全數位異字及正確的官銜角色',()=>{
  const reference=h.comparison[0],same=h.comparison.find(r=>r.kind==='adjacent_same_written_name_different_persons');
  assert.equal(reference.received.surface,'王浚');assert.equal(reference.preferred_print,'王凌');
  const reg=read('registry/persons.json').persons;
  for(const [s,person] of [[reference.received,reference.person_id],[same.first,same.first_person_id],[same.second,same.second_person_id]]){
    const p=ps[s.paragraph_id],m=p.mentions.find(m=>m.start===s.start&&m.end===s.end);
    assert.equal(slice(p.text,s.start,s.end),s.surface);assert.equal(m.person_id,person);
    if(s!==same.second) assert.ok(!reg.find(v=>v.id===person).aliases.some(a=>a.mention_ids.includes(m.id)));
  }
  assert.notEqual(same.first_person_id,same.second_person_id);assert.match(reference.foreign_event.quote,/剖棺，暴屍/);
  assert.match(h.comparison.find(x=>x.kind==='name_vs_precedent').parallel.quote,/齊侯葬紀伯姬/);
  const names81=ps[reference.received.paragraph_id].mentions;
  assert.ok(names81.some(q=>q.surface==='王修'&&q.person_id!=='2pg_br4_mcl_A'));assert.ok(names81.some(q=>q.surface==='王淩'&&q.person_id===reference.person_id));
});
test('太寧詔的虛報、王導所致書與王含報齡不外推',()=>{
  const fake=h.reported_vs_actual.find(x=>x.kind==='false_death_report'),events=read('corpus/jinshu/098-jin033-wangji-life-events.json').events;
  assert.equal(ps[fake.source.paragraph_id].text.slice(fake.source.start,fake.source.end),fake.source.surface);
  assert.ok(events.some(e=>e.id===fake.actual_death&&e.evidence[0].paragraph_id.endsWith('line077')));
  assert.equal(h.letter[0].age_reading.lower_exclusive,60);assert.equal(h.letter[0].age_reading.exact_age,null);
  assert.match(h.letter[1].hu_sansheng.quote,/王應字安期/);assert.equal(h.letter[2].decision.status,'unresolved');
  const open=ps[Object.keys(ps).find(k=>k.endsWith('line077'))];
  assert.ok(!open.mentions.some(m=>m.surface==='導'));
});
