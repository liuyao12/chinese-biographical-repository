import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
const file=p=>readFileSync(new URL('../'+p,import.meta.url)),read=p=>JSON.parse(file(p)),sha=b=>createHash('sha256').update(b).digest('hex');
const q=read('source-evidence/jin098-wang-han-ying/reading.json'),sv=read('source-evidence/jin098-wangdun-survey/survey.json'),c=read('corpus/jinshu/098-jin033-wangji.json');
test('四原題、兩處史臣論的分界與卷33傳首四原錨',()=>{
 assert.deepEqual(sv.heading_rows.filter(r=>r.unit_kind==='headed_account').map(r=>r.title),['王敦','沈充','桓溫','孟嘉']);
 assert.deepEqual(sv.unheaded_discussions.map(p=>p.line),[93,165]);assert.equal(c.paragraphs.length,37);
 const old=sv.inherited_records[0],p=c.paragraphs[0];assert.ok(p.text.startsWith(old.source_quote));assert.equal(p.id,old.paragraph_id);
 for(const id of old.mention_ids)assert.ok(p.mentions.some(m=>m.id===id));
 assert.deepEqual(sv.print_witness.map(f=>f.pdf_page),[3,11,16,17,18,19,32,33]);
 for(const f of sv.print_witness){
  assert.match(f.source_url,new RegExp(`^https://upload\\.wikimedia\\.org/.+%E7%AC%AC25%E5%86%8A\\.pdf#page=${f.pdf_page}$`));
  assert.match(f.capture_sha256,/^[0-9a-f]{64}$/);
 }
});
test('王含、王應逐段具名，王瑜同名不併，王邃按兩處來源身份',()=>{
 for(const k of q.source_readings){const w=q.witnesses[k.witness],raw=file(w.raw_path);assert.equal(sha(raw),w.raw_sha256);assert.equal(Array.from(raw.toString()).slice(k.raw_start,k.raw_end).join(''),k.quote);}
 const p=q.parentage,all=read('corpus/jinshu/098-jin033-wangji-assertions.json').assertions;assert.equal(all.find(a=>a.id===p.birth).object_person_id,p.father);assert.ok(all.some(a=>a.predicate==='adoptive_father'&&a.subject_person_id===p.child&&a.object_person_id===p.adopter));const yu=q.yu_homonyms;
 assert.equal(new Set([yu.person_id,...yu.different_or_unresolved.map(a=>a.person_id)]).size,3);assert.ok(all.some(a=>a.subject_person_id===yu.person_id&&a.object_person_id===p.father&&a.predicate==='father'));
 for(const u of q.units){const p=u.paragraph_ids.map(id=>c.paragraphs.find(x=>x.id===id));assert.ok(p.every(x=>x.annotation_status==='reviewed'));}
 const s=read('corpus/shishuoxinyu/008-jin098-wang-family-assertions.json').assertions;
 assert.ok(s.some(a=>a.subject_person_id===q.unresolved_sui.source_id&&a.predicate==='brother'));
});
