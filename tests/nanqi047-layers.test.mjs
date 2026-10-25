import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {chapterParagraph} from '../assets/corpus-reader.js';
const load=name=>JSON.parse(readFileSync(new URL(`../corpus/nanqishu/${name}.json`,import.meta.url)));
const plain=html=>html.replace(/<[^>]+>/g,'').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&quot;','"').replaceAll('&#39;',"'").replaceAll('&amp;','&');
test('史臣曰、贊及清考證的標籤在收到原文之外，逐字原文及人物錨不變',()=>{
 const labels={received_compiler_appraisal:'史臣曰・史評',received_compiler_praise:'贊',witness_appended_qing_siku_collation:'清・四庫考證'};
 for(const name of ['047-xietiao','047-compiler-appraisal','047-qing-collation']){
  const c=load(name);
  for(const p of c.paragraphs){
   const html=chapterParagraph(p,{}, {work_id:c.work_id,book_id:c.book_id,chapter_id:c.id});
   const body=/<p [^>]*data-source-text>([\s\S]*)<\/p>$/.exec(html);assert(body,p.id);assert.equal(plain(body[1]),p.text);
   if(labels[p.text_layer]){assert(html.startsWith('<div class="corpus-text-layer"'));assert(html.includes(`>${labels[p.text_layer]}</div><p`));}else assert(!html.includes('data-text-layer-label'));
   for(const m of p.mentions.filter(m=>m.kind==='person'))assert(html.includes(`id="${m.id}"`));
  }
 }
});
