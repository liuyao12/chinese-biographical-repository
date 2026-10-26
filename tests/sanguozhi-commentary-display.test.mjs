import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chapterParagraph} from '../assets/corpus-reader.js';

for (const [file,layer,label] of [
  ['009-caoxiu','witness_appended_pei_songzhi_note','裴松之注'],
  ['015-pei-simabiao','witness_peisongzhi_quoted_simabiao_xuzhuan','裴松之注 · 引司馬彪序傳'],
]) {
  test(`${file}: commentary is visibly attributed outside preserved source paragraph`,()=>{
    const chapter=JSON.parse(fs.readFileSync(new URL(`../corpus/sanguozhi/${file}.json`,import.meta.url)));
    const paragraph=chapter.paragraphs.find(p=>p.text_layer===layer);
    assert(paragraph);
    const html=chapterParagraph(paragraph);
    assert(html.includes(`data-text-layer-label="${layer}"`));
    assert(html.replace(/<[^>]*>/g,'').includes(label));
    assert(html.indexOf('data-text-layer-label')<html.indexOf('data-source-text'));
    const source=html.slice(html.indexOf('data-source-text>')+'data-source-text>'.length,html.lastIndexOf('</p>'));
    assert.equal(source.replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'"),paragraph.text);
  });
}
test('received Sanguozhi body is not relabelled as commentary',()=>{
  const chapter=JSON.parse(fs.readFileSync(new URL('../corpus/sanguozhi/009-caoxiu.json',import.meta.url)));
  const body=chapter.paragraphs.find(p=>p.text_layer==='received_chapter');
  assert(body);assert(!chapterParagraph(body).includes('data-text-layer-label'));
});
