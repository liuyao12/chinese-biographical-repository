import test from 'node:test'
import assert from 'node:assert/strict'
import {readFileSync} from 'node:fs'
import {createHash} from 'node:crypto'
const bytes = p=>readFileSync(new URL('../'+p,import.meta.url))
const read = p=>JSON.parse(bytes(p))
const R=read('source-evidence/jin080-wang-xianzhi/reading.json')
const data=read('corpus/jinshu/080-wangxizhi-family.json')
const relations=read('corpus/jinshu/080-wangxizhi-family-assertions.json').assertions
test('原字、引書和先後婚姻分證',()=>{
  for(const q of R.comparisons.flatMap(v=>v.witnesses)){
    const s=R.external_witnesses[q.witness],raw=bytes(s.raw_path)
    assert.equal(createHash('sha256').update(raw).digest('hex'),s.raw_sha256)
    assert.equal([...raw.toString()].slice(q.raw_start,q.raw_end).join(''),q.quote)
  }
  const u=read('corpus/taipingyulan/152-wang080-xianzhi.json').paragraphs[0]
  assert.equal(u.attribution.quoted_work,'晋中興書')
  assert.equal(u.attribution.source_marker_chain.length,4)
  const t=read('corpus/jinshu/032-wang080-xianzhi.json')
  assert.ok(t.cross_chapter_references[0].target.paragraph_id.endsWith(':line116'))
  assert.ok(t.paragraphs[0].text.includes('諱神愛'))
  assert.ok(read('corpus/taipingyulan/149-wang080-xianzhi.json').paragraphs[0].text.includes('字神受'))
})
test('王靜之承嗣、父系祖父及未名生父',()=>{
  const king=read('registry/persons.json').persons.find(p=>p.id==='326_faf_cd3_*A')
  assert.equal(king.family_path.parent_person_id,null)
  assert.deepEqual(king.family_path.intermediate_person_ids,[null])
  const kin=relations.filter(a=>a.subject_person_id===king.id)
  assert.deepEqual(new Set(kin.map(a=>a.predicate)),new Set(['grandfather','ritual_successor_of']))
  assert.equal(kin.find(a=>a.predicate==='ritual_successor_of').object_person_id,'sm1_jfi_7k2')
})
test('后父追贈、安帝紀崩月及傳本書幀',()=>{
  const gifts=read('corpus/jinshu/080-wangxizhi-family-titles.json').holdings.filter(h=>h.posthumous_basis?.kind==='w080_empress_father_gift')
  assert.equal(gifts.length,4)
  for(const h of gifts)assert.equal(h.person_id,'sm1_jfi_7k2')
  const q=R.comparisons.find(c=>c.sexagenary_day_of_burial)
  assert.equal(q.death_day,null);assert.equal(q.sexagenary_day_of_burial,'癸酉')
  assert.equal(R.literary_and_material_witnesses[1].museum_work_number,'贈帖00000100029')
  const months=read('corpus/jinshu/010-wang080-xianzhi.json').paragraphs
  assert.ok(months[0].text.endsWith('八月，皇后王氏崩。'))
  assert.ok(months[1].text.endsWith('九月癸酉，葬僖皇后于休平陵。'))
})
