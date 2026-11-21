import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import test from 'node:test';
import assert from 'node:assert/strict';
const b=p=>readFileSync(new URL('../'+p,import.meta.url)),j=p=>JSON.parse(b(p)),h=b=>createHash('sha256').update(b).digest('hex');
const q=j('source-evidence/jin033-wanglan/reading.json'),c=j('corpus/jinshu/033.json'),de=j('corpus/shishuoxinyu/001-jin033-wanglan.json');
test('祥世家分載融兩妻與兩子，兩位王氏婦人另見晉陽秋',()=>{
 const a=j('corpus/shishuoxinyu/001-jin033-wanglan-assertions.json').assertions,house=de.paragraphs.find(p=>p.id.endsWith(':house'));assert.equal(house.attribution.quoted_work,'祥世家');
 for(const [child,mother]of [['7r6_k52_qji_AA',q.source_roles.other_wife_of_wangrong],['7r6_k52_qji_AB',q.source_roles.mother]])assert.ok(a.some(v=>v.subject_person_id===child&&v.predicate==='mother'&&v.object_person_id===mother));
 assert.ok(de.paragraphs.find(p=>p.id.endsWith(':yangqiu')).mentions.some(m=>m.person_id==='jmt_uha_exg'));
 for(const case0 of q.comparisons)for(const e of case0.sources){const w=q.witnesses[e.witness],raw=b(w.raw_path);assert.equal(h(raw),w.raw_sha256);assert.equal(Array.from(raw.toString()).slice(e.raw_start,e.raw_end).join(''),e.quote);}
});
test('王祥、覽所說卿汝及父母親稱的十三個既有原錨保留於指涉層',()=>{
 const roles=c.annotation.person_reference_occurrences.filter(r=>r.id.includes(':m')&&['母','父','卿','汝'].includes(r.surface));assert.equal(roles.length,13);
 const life=j('corpus/jinshu/033-life-events.json').events,ev=life.find(a=>a.source_term==='母終').evidence[0];assert.ok(roles.some(r=>r.id===ev.person_reference_id&&r.start===29));assert.ok(roles.some(r=>r.id.endsWith('p008:m0074')&&r.referent_role==='addressee'));
 const r=j('registry/persons.json').persons;for(const role of roles){const p=r.find(x=>x.id===role.person_id);assert.equal(p.aliases.some(a=>a.mention_ids.includes(role.id)),false);}
});
