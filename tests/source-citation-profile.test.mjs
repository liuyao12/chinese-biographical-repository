import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {personCard} from '../assets/cbr-person.js';import {profileSourceContext,sourcePassageURL} from '../assets/corpus-reader.js';
import {chapterDirectoryMap,sourceCitation} from '../assets/source-caption.js';
const directoryData={schema_version:1,works:[{work_id:'w-jinshu',title:'晉書',books:[{book_id:'b-jinshu-079',title:'卷七十九',citation_title:'謝尚 謝安'}]}]};
const directory=chapterDirectoryMap(directoryData);
test('actual published Xie An occurrences use catalogue title in compact/full views without changing source data',()=>{
 const registry=JSON.parse(fs.readFileSync(new URL('../data/corpus/persons.json',import.meta.url)));const row=Object.values(registry).find(x=>x.label==='謝安');assert.ok(row);
 const raw=JSON.parse(fs.readFileSync(new URL('../data/corpus/profiles/'+encodeURIComponent(row.id)+'.json',import.meta.url)));const source=raw.occurrences.find(x=>x.work_id==='w-jinshu'&&x.book_id==='b-jinshu-079');assert.ok(source);const before=JSON.stringify(raw);
 const p={...raw,occurrences:[source],source_chapter_directory:directory};
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,/《晉書・謝尚 謝安》 · 卷七十九/);assert.doesNotMatch(html,/《[^》]*(?:完整單元|編輯選錄題|家族選段)[^》]*》/);assert.ok(html.includes(sourcePassageURL(source).replaceAll('&','&amp;')));}
 assert.equal(JSON.stringify(raw),before);
 const result=profileSourceContext(p,new URLSearchParams({work:source.work_id,book:source.book_id,chapter:source.chapter_id,passage:source.paragraph_id}));assert.equal(result.text,'回到《晉書・謝尚 謝安》 · 卷七十九 →');assert.equal(result.href,sourcePassageURL({...source,mention_id:undefined}));
});
test('untrusted display text remains escaped at production HTML boundary',()=>{
 const bad=chapterDirectoryMap({schema_version:1,works:[{work_id:'w-jinshu',title:'<img src=x>',books:[{book_id:'b-jinshu-079',title:'卷79',citation_title:'<script>bad</script>'}]}]});
 const p={id:'synthetic_caption',label:'測試人',occurrences:[{work_id:'w-jinshu',book_id:'b-jinshu-079',chapter_id:'c-jinshu-079-synthetic',number:79,count:1,quote:'原句',paragraph_id:'synthetic-p'}],source_chapter_directory:bad};const html=personCard(p,true);assert.match(html,/&lt;script&gt;bad&lt;\/script&gt;/);assert.doesNotMatch(html,/<script>|<img src=x>/);
});
test('ordinary source-only profiles load shared title/directory indexes once without mutating downloaded JSON',async()=>{
 const previous=globalThis.fetch,calls=[],raw={id:'caption-load-only',label:'測試人',occurrences:[{work_id:'w-jinshu',book_id:'b-jinshu-079',number:79,title:'編輯選段'}]};
 globalThis.fetch=async url=>{calls.push(url);return {ok:true,json:async()=>url==='data/corpus/work-titles.json'?{schema_version:1,works:[{id:'w-jinshu',title:'晉書'}]}:url==='data/corpus/chapter-directory.json'?directoryData:raw};};
 try{const {loadPerson}=await import('../assets/cbr-person.js?source-caption-loader');const p=await loadPerson(raw.id);assert.equal(sourceCitation(p.occurrences[0],p.source_chapter_directory,p.source_work_titles),'《晉書・謝尚 謝安》 · 卷七十九');await loadPerson(raw.id);assert.equal(calls.filter(x=>x==='data/corpus/chapter-directory.json').length,1);assert.equal(calls.filter(x=>x==='data/corpus/work-titles.json').length,1);assert.equal(raw.source_chapter_directory,undefined);assert.equal(raw.source_work_titles,undefined);}finally{globalThis.fetch=previous;}
});
