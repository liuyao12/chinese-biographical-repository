import test from 'node:test'
import assert from 'node:assert/strict'
import {readFileSync} from 'node:fs'
import {createHash} from 'node:crypto'
const read = path => JSON.parse(readFileSync(new URL('../'+path,import.meta.url),'utf8'))
const main = read('corpus/jinshu/080-wangxizhi-family.json')
const line = n => main.paragraphs.find(p => p.source_position.first_line === n)
const review = read('source-evidence/jin080-wang-short/reading.json')
const material = path => readFileSync(new URL('../'+path,import.meta.url))
test('卷80的五個短傳均有可重算的固定起訖',()=>{
  const entries=read('data/corpus/six-dynasties-biographies.json').biographies.filter(b=>b.book_id===main.book_id)
  const names=['王玄之','王凝之','王徽之','王楨之','王操之']
  assert.equal(entries.length,9)
  for(const n of names)assert.ok(entries.find(x=>x.title===n)?.item_reviewed,n)
  for(const p of main.paragraphs) assert.equal([...material(main.source.raw_path).toString()].slice(p.source_position.raw_start,p.source_position.raw_end).join(''),material(main.source.raw_path).toString().split('\n')[p.source_position.first_line-1])
  const x=entries.find(x=>x.title==='王玄之')
  const slice=x.paragraph_slices[line(86).id]
  assert.equal([...line(86).text].slice(slice.start,slice.end).join(''),'玄之早卒。')
  assert.equal(main.paragraphs.length,50)
})
test('古注、書影與固定字串直接重算',()=>{
  for(const link of review.comparisons.flatMap(c=>c.anchors)){
    const witness=review.external_witnesses[link.witness]
    const bytes=material(witness.raw_path)
    assert.equal(createHash('sha256').update(bytes).digest('hex'),witness.raw_sha256)
    assert.equal([...bytes.toString()].slice(link.raw_start,link.raw_end).join(''),link.quote)
  }
  for (const page of review.print_witness.pages)assert.equal(createHash('sha256').update(material(page.local_path)).digest('hex'),page.sha256)
})
test('第七叔是劉注自案，譜引公榦、晉書公幹',()=>{
  const p=read('corpus/shishuoxinyu/009-wang080-short.json').paragraphs
  assert.equal(p.find(x=>x.id.endsWith(':liunote')).attribution.quoted_work,null)
  assert.equal(p.find(x=>x.id.endsWith(':wangshipu')).attribution.quoted_work,'王氏譜')
  assert.equal(line(98).mentions.find(x=>x.surface==='公幹').person_id,p.find(x=>x.id.endsWith(':wangshipu')).mentions.find(x=>x.surface==='公榦').person_id)
  const kin=read('corpus/shishuoxinyu/009-wang080-short-assertions.json').assertions.find(k=>k.predicate==='paternal_uncle')
  assert.deepEqual([kin.subject_person_id,kin.object_person_id],['326_faf_cd3_BA','sm1_jfi_7k2'])
})
test('會稽同日紀事、謝道韞父與夫及徽獻卒次分證',()=>{
  const ev=read('corpus/jinshu/010-wang080-short-life-events.json').events[0]
  assert.ok(ev.evidence[0].quote.includes('十一月甲寅，妖賊孫恩陷會稽，內史王凝之死之'))
  assert.equal(ev.normalized_date.year,399)
  const kin=read('corpus/jinshu/096-wang080-short-assertions.json').assertions.filter(x=>x.subject_person_id==='aa6_83c_juy_CE')
  assert.deepEqual(new Set(kin.map(k=>k.predicate)),new Set(['father','spouse']))
  const s=read('corpus/shishuoxinyu/017-wang080-short.json')
  assert.equal(s.annotation.age_assertions[0].value,45)
  assert.ok(line(94).text.includes('月餘亦卒'))
})
