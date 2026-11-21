import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const read = f => JSON.parse(readFileSync(new URL('../' + f, import.meta.url), 'utf8'));
const chapter = read('corpus/jinshu/080-wangxizhi-family.json');
const proof = read('source-evidence/jin080-wang-xizhi/reading.json');
const paragraphs = new Map(chapter.paragraphs.map(p => [p.id,p]));
const textAt = a => Array.from(paragraphs.get(a.paragraph_id).text).slice(a.start,a.end).join('');
const root = new URL('../', import.meta.url);
const raw = new Map(Object.entries(proof.external_witnesses).map(([key,w]) => {
  const bytes = readFileSync(new URL(w.raw_path,root));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),w.raw_sha256);
  return [key,Array.from(bytes.toString('utf8'))];
}));

test('主傳引書、年齡及殿本保全逐字起訖', () => {
  for (const entry of proof.comparisons) {
    assert.equal(textAt(entry.anchor),entry.anchor.quote);
    for (const x of entry.witnesses) assert.equal(raw.get(x.witness).slice(x.raw_start,x.raw_end).join(''),x.quote);
  }
  for (const item of [...proof.items,...proof.source_years]) assert.equal(textAt(item.anchor),item.anchor.quote);
  for (const page of proof.print_witness.pages) {
    assert.equal(page.source_url, proof.print_witness.url + '#page=' + page.pdf_page);
    assert.match(page.capture_sha256, /^[0-9a-f]{64}$/);
  }
  assert.equal(proof.material_witness.item_number,'故書00014100000');
  assert.equal(chapter.annotation.age_assertions.find(x => x.id==='age-w080-xi59').birth_year,null);
  const own = read('corpus/jinshu/080-wangxizhi-family-life-events.json').events.find(x => x.id==='le-w080-xizhi');
  const later = read('corpus/shuduan/002-jin080-xizhi-life-events.json').events[0];
  assert.equal(own.date_expression,null); assert.equal(later.normalized_date.year,361);
});
test('書信說者、受者及署名各據本文', () => {
  const writings = chapter.annotation.embedded_writings;
  const first = writings.find(x=>x.id==='writing-w080-hao-to-wang');
  const reply = writings.find(x=>x.id==='writing-w080-wang-to-hao');
  assert.equal(first.writer_person_id,reply.recipient_person_id);
  assert.equal(first.recipient_person_id,reply.writer_person_id);
  for (const x of writings) for (const key of ['attestation','opening','closing']) assert.equal(textAt(x[key]),x[key].quote);
  assert.equal(new Set(writings.map(x=>x.id)).size,14);
  const ref = chapter.annotation.person_reference_occurrences.find(x=>x.surface==='安西');
  const office = read('corpus/jinshu/008-jin080-xizhi-titles.json').holdings.find(x=>x.title==='安西將軍');
  assert.equal(ref.person_id,office.person_id);
});
test('三項未受官與其後實任分別有原句，從伯兩端各有所指', () => {
  const proposals = chapter.annotation.title_proposals.filter(x=>x.id.startsWith('tp-w080-xizhi-'));
  assert.deepEqual(proposals.map(x=>x.title),['侍中','吏部尚書','護軍將軍']);
  for(const p of proposals) for(const a of [p.role_anchor,p.appointment_anchor,p.non_assumption_anchor]) assert.equal(textAt(a),a.surface);
  const r = read('corpus/jinshu/080-wangxizhi-family-assertions.json').assertions.filter(x=>x.qualifiers.source_clause_binding?.kind==='jin080_named_congbo');
  assert.equal(r.length,2); assert.equal(new Set(r.map(x=>x.object_person_id)).size,2);
  const report = chapter.annotation.posthumous_honour_reports.find(x=>x.id==='hr-w080-xizhi');
  assert.equal(textAt(report.family_response),'諸子遵父先旨，固讓不受');
});
test('漕運書署名及校議、五條有來源的子次分層', () => {
  const x = chapter.annotation.embedded_writings.find(w => w.id === 'writing-w080-xiean');
  assert.equal(x.recipient_person_id,null);
  assert.equal(x.recipient_status,'disputed_attribution');
  assert.notEqual(x.received_recipient_person_id,x.proposed_corrected_recipient_person_id);
  assert.equal(x.apparatus.length,2);
  assert.deepEqual(proof.sons_by_source.map(s=>s.ordinal),[2,4,5,6,7]);
  for(const x of [...proof.sons_by_source,proof.later_book_story]){
    const s=x.source;
    assert.equal(raw.get(s.witness).slice(s.raw_start,s.raw_end).join(''),s.quote);
  }
});
test('卷末父的指代、兩位從伯及未任條不可交換端點',async ()=>{
  const {spawnSync}=await import('node:child_process');
  const cases = [
    'import copy, json',
    'from scripts.jin080_xizhi import end_subject_valid, collateral_valid, unassumed_valid',
    'read=lambda p: json.load(open("corpus/jinshu/080-wangxizhi-family"+p+".json"))',
    'c=read(""); aa=read("-assertions")["assertions"]; who="326_faf_cd3"',
    'paras={p["id"]:(c["id"],p) for p in c["paragraphs"]}',
    'e=next(a for a in c["annotation"]["age_assertions"] if a["id"]=="age-w080-xi59")["evidence"][0]',
    'assert end_subject_valid(e["context"],e,who,c)',
    'assert not end_subject_valid(dict(e["context"],intervening_paragraph_ids=[]),e,who,c)',
    'a=next(a for a in aa if a["id"]=="a-w080-xi-congdao")',
    'assert collateral_valid(a,paras) and not collateral_valid(dict(a,object_person_id="39o_b6y_n74"),paras)',
    'o=next(r for r in c["annotation"]["title_proposals"] if r.get("jin080_office_form"))',
    'assert unassumed_valid(o,c) and not unassumed_valid(dict(o,role_anchor=o["appointment_anchor"]),c)',
  ].join('\n');
  const result=spawnSync('python3',['-c',cases],{cwd:root,encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
});
