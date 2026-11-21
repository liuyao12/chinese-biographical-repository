import test from 'node:test'
import assert from 'node:assert/strict'
import {readFileSync} from 'node:fs'
import {createHash} from 'node:crypto'
const bytes=p=>readFileSync(new URL('../'+p,import.meta.url))
const read=p=>JSON.parse(bytes(p))
const r=read('source-evidence/jin080-xumai-appraisal/reading.json')
test('卦名、絕跡報年和妻父各據所出版本',()=>{
  for(const a of r.comparisons)for(const q of a.witnesses){
    const w=r.external_witnesses[q.witness],b=bytes(w.raw_path)
    assert.equal(createHash('sha256').update(b).digest('hex'),w.raw_sha256)
    assert.equal([...b.toString()].slice(q.raw_start,q.raw_end).join(''),q.quote)
  }
  const c=read('corpus/zhengao/020-jin080-xumai.json')
  assert.equal(c.annotation.person_reference_occurrences[0].surface,'女')
  assert.ok(c.paragraphs.find(p=>p.id.endsWith(':names')).text.includes('改名遠遊'))
  const records=read('corpus/jinshu/080-wangxizhi-family-life-events.json')
  assert.ok(records.events.every(e=>e.person_id!=='972_dh9_hz4'))
})
test('卷末書論分層，武英殿作制曰',()=>{
  const c=read('corpus/jinshu/080-wangxizhi-family.json')
  assert.equal(c.paragraphs.at(-1).text_layer,'received_compiler_appraisal')
  assert.equal(r.attribution.printed_opening,'制曰')
  for (const page of r.print_witness.pages) {
    assert.equal(page.source_url, r.print_witness.url + '#page=' + page.pdf_page);
    assert.match(page.capture_sha256, /^[0-9a-f]{64}$/);
  }
})
