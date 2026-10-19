import test from 'node:test';
import assert from 'node:assert/strict';
import {chapterParagraph} from '../assets/corpus-reader.js';
const p={id:'test:p001',text:'○劉攽曰案正文多一者字',mentions:[]};
for(const [layer,label] of Object.entries({witness_appended_lixian_note:'唐・李賢注',witness_appended_liuban_collation:'宋・劉攽校',witness_appended_qing_siku_collation:'清・四庫考證'}))test(layer,()=>{
 const html=chapterParagraph({...p,text_layer:layer});
 assert.ok(html.includes(label));
 assert.equal(html.match(/<p[^>]*data-source-text>(.*?)<\/p>/s)[1],p.text);
 assert.ok(html.indexOf(label)<html.indexOf('data-source-text'));
});
test('legacy byte output unchanged',()=>assert.equal(chapterParagraph(p),'<p id="test:p001" data-source-text>○劉攽曰案正文多一者字</p>'));
test('mention ID and links unchanged by layer',()=>{
 const q={...p,text:'陳寔',mentions:[{id:'m001',start:0,end:2,surface:'陳寔',kind:'person',person_id:'9w8_tqh_ysn'}]};
 const plain=chapterParagraph(q),layered=chapterParagraph({...q,text_layer:'witness_appended_lixian_note'});
 assert.equal(layered.slice(layered.indexOf('<p ')),plain);assert.ok(plain.includes('id="m001"'));
});
test('invalid anchors still rejected',()=>assert.throws(()=>chapterParagraph({...p,mentions:[{start:0,end:2,surface:'錯字'}]})));
