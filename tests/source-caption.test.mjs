import test from 'node:test';
import assert from 'node:assert/strict';
import {sourceCaption,chapterDirectoryMap,sourceCitation,sourceChapterTitle,loadChapterDirectory} from '../assets/source-caption.js';
const directory=chapterDirectoryMap({schema_version:1,works:[{work_id:'w-jinshu',title:'晉書',books:[{book_id:'b-jinshu-079',title:'卷七十九',citation_title:'謝尚 謝安'},{book_id:'b-jinshu-079a',title:'卷七十九上',citation_title:'上卷正式篇名'}]},{work_id:'w-other',title:'別史',books:[{book_id:'b-other-079',title:'卷七十九',citation_title:'另一篇'}]}]});
test('book and explicitly registered chapter stay inside brackets; volume stays outside',()=>{
 assert.equal(sourceCaption('史記','秦始皇本紀'),'《史記・秦始皇本紀》');
 assert.equal(sourceCitation({work_id:'w-jinshu',book_id:'b-jinshu-079',title:'《晉書》謝氏完整單元（編輯選錄題）'},directory),'《晉書・謝尚 謝安》 · 卷七十九');
 assert.equal(sourceCitation({work_id:'w-jinshu',book_id:'b-jinshu-079a',number:79},directory),'《晉書・上卷正式篇名》 · 卷七十九上');
});
test('same volume number never substitutes for the precise work and book key',()=>{
 assert.equal(sourceCitation({work_id:'w-other',book_id:'b-jinshu-079',number:79,title:'謝安'},directory),'《別史》 · 卷79');
 assert.equal(sourceCitation({work_id:'w-jinshu',book_id:'b-jinshu-999',number:79,title:'謝安'},directory),'《晉書》 · 卷79');
});
test('unknown chapter never guesses by stripping source prose, person label or ID',()=>{
 const source={work_id:'w-unknown',book_id:'b-unknown-001',work_title:'合成史',number:1,title:'《合成史》全本傳家族選段（編輯題）'};
 const before=JSON.stringify(source);assert.equal(sourceCitation(source,{}),'《合成史》 · 卷1');assert.equal(JSON.stringify(source),before);
 assert.equal(sourceChapterTitle(source,{}),'卷1');assert.equal(sourceCitation({title:'史記秦始皇本紀'},{}),'來源');
});
test('registered work qualification is not a formal book title',()=>{
 assert.equal(sourceCitation({work_id:'w-weishu',number:2},{},{'w-weishu':{title:'魏書',qualification:'某人裴注所引，作者未詳'}}),'《魏書》 · 卷2');
});
test('duplicate or malformed directory keys fail closed rather than replacing titles',()=>{
 assert.throws(()=>chapterDirectoryMap({schema_version:1,works:[{work_id:'w-a',title:'甲',books:[{book_id:'b-a-001',citation_title:'甲'},{book_id:'b-a-001',citation_title:'乙'}]}]}));
 assert.throws(()=>chapterDirectoryMap({schema_version:1,works:[{work_id:'w-a',title:'甲',books:[{book_id:'b-a-001',citation_title:{title:'壞值'}}]}]}));
});
test('missing or unavailable directory keeps readable safe fallback',async()=>{
 for(const fetcher of [async()=>({ok:false}),async()=>({ok:true,json:async()=>({schema_version:2,works:[]})}),async()=>{throw Error('offline');}]){
  const result=await loadChapterDirectory(fetcher);assert.equal(Object.keys(result).length,0);assert.equal(sourceCitation({work_title:'晉書',number:79},result),'《晉書》 · 卷79');
 }
});
