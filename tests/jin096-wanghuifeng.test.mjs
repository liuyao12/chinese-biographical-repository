import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)), read=p=>JSON.parse(file(p));
const q=read('source-evidence/jin096-wanghuifeng/reading.json');
const inv=read('data/corpus/six-dynasties-biographies.json');
const id='y5y_cch_05n',prince='74e_68c_9ae',parent='b0c_13f_c3a';
test('題目分錄、殿本五上及固定見證逐字對照',()=>{
  const row=inv.biographies.find(r=>r.book_id==='b-jinshu-096'&&r.title==='湣懷太子妃王惠風');
  assert.ok(row.full_text&&row.first_pass&&row.item_reviewed&&row.entry_checked);
  const s=inv.volume_surveys.find(v=>v.book_id===row.book_id);
  assert.ok(s.text_witness_units.some(v=>v.chapter_id==='c-jinshu-096-wanghuifeng-wyd'));
  assert.deepEqual(q.edition_image.body_columns,[6,7,8,9,10]);
  assert.equal(q.edition_image.leaf,'五上'); assert.equal(q.three_sources.heading_print,'愍懷太子妃王氏');
  for(const s of q.source_clauses){
    const w=q.witnesses[s.witness],b=file(w.raw_path);
    assert.equal(createHash('sha256').update(b).digest('hex'),w.raw_sha256);
    assert.equal([...b.toString()].slice(s.raw_start,s.raw_end).join(''),s.quote);
  }
  for(const [k,v] of [['page_image','page_sha256'],['leaf_image','leaf_sha256']]){
    assert.equal(createHash('sha256').update(file(q.edition_image[k])).digest('hex'),q.edition_image[v]);
  }
});
test('同一惠風的字、父、配偶及太子書信，擬再娶與死事分開',()=>{
  const family=read('corpus/jinshu/043-wangyan-assertions.json').assertions;
  for(const pair of [[q.identity.old_father_assertion,parent],[q.identity.old_spouse_assertion,prince]]){
    assert.ok(family.some(a=>a.id===pair[0]&&a.subject_person_id===id&&a.object_person_id===pair[1]));
  }
  for(const suffix of ['','-wyd']){
    const base='corpus/jinshu/096-wanghuifeng'+suffix;
    const n=read(base+'-name-components.json').records[0],a=read(base+'-assertions.json').assertions,l=read(base+'-life-events.json').events[0],chapter=read(base+'.json');
    assert.equal(n.person_id,id);assert.equal(n.surname,'王');assert.equal(n.zi,'惠風');assert.equal(n.ming,null);
    assert.deepEqual(a.map(x=>x.predicate).sort(),['father','spouse']);assert.ok(a.some(x=>x.object_person_id===prince));
    assert.equal(l.person_id,id);assert.equal(l.reported_perpetrator.person_id,q.three_sources.proposed_second_spouse_identifier);
    assert.ok(chapter.annotation.person_reference_occurrences.some(r=>r.surface==='皇太子妃'&&r.person_id===id&&r.referent_role==='speaker_self'));
  }
  assert.equal(q.letter.author,prince);assert.equal(q.letter.recipient,id);assert.equal(q.identity.mother_id,null);
  assert.equal(q.three_sources.second_marriage,false);assert.equal(q.chronology.exact_death_date,null);
});
