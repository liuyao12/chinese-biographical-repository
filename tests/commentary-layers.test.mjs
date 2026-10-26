import assert from 'node:assert/strict';
import fs from 'node:fs';import path from 'node:path';import os from 'node:os';import {pathToFileURL} from 'node:url';
const P=path.dirname(new URL(import.meta.url).pathname),H=path.resolve(P,'..');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'commentary-test-'));
try {
 fs.mkdirSync(path.join(tmp,'assets'));fs.writeFileSync(path.join(tmp,'package.json'),'{"type":"module"}');
 for(const file of fs.readdirSync(path.join(H,'assets')))if(file.endsWith('.js'))fs.copyFileSync(path.join(H,'assets',file),path.join(tmp,'assets',file));
 const {layerGroups,layerInfo,layerParagraph,commentaryControls,targetParagraph,bindCommentaryControls}=await import(pathToFileURL(path.join(tmp,'assets/commentary-layers.js')));
 const {chapterParagraph}=await import(pathToFileURL(path.join(tmp,'assets/corpus-reader.js')));
 const {setLocale}=await import(pathToFileURL(path.join(tmp,'assets/i18n.js')));
 const p=(id,layer)=>({id,text:'史臣曰(缺/)𤣥<&"',mentions:[{id:id+':m',start:0,end:3,surface:'史臣曰',kind:'unresolved'}],text_layer:layer});
 const chapter={paragraphs:[p('body','received_chapter'),p('pei','witness_appended_pei_songzhi_note'),p('sima','witness_peisongzhi_quoted_simabiao_xuzhuan'),p('unknown','unknown_note')]};
 assert.equal(layerInfo(chapter.paragraphs[0]),null);assert.equal(layerInfo(chapter.paragraphs[3]),null);
 assert.equal(layerInfo(chapter.paragraphs[1]),layerInfo(chapter.paragraphs[2]));
 assert.equal((commentaryControls(chapter).match(/type="checkbox"/g)||[]).length,1);
 for(const group of layerGroups)for(const layer of group[4])assert.equal(layerInfo(p('x',layer)),group);
 assert.equal(targetParagraph(chapter,new URLSearchParams({mention:'pei:m'})).id,'pei');
 assert.equal(targetParagraph(chapter,new URLSearchParams({passage:'body',mention:'pei:m'})),null);
 assert.equal(targetParagraph(chapter,new URLSearchParams({passage:'<script>'})),null);
 const mkInput=group=>({dataset:{commentaryToggle:group},checked:true,listeners:new Map(),addEventListener(k,fn){this.listeners.set(k,fn);},removeEventListener(k,fn){assert.equal(this.listeners.get(k),fn);this.listeners.delete(k);}});
 const input=mkInput('pei'),blocks=[{dataset:{commentaryGroup:'pei'},hidden:false},{dataset:{commentaryGroup:'pei'},hidden:false},{dataset:{commentaryGroup:'other'},hidden:false}],status={innerHTML:''};
 const root={querySelectorAll(q){return q==='[data-commentary-toggle]'?[input]:blocks;},querySelector(){return status;}};
 const state=new Map(),ctl=bindCommentaryControls(root,chapter,state);
 assert(blocks.every(b=>!b.hidden));input.checked=false;input.listeners.get('change')();assert(blocks.slice(0,2).every(b=>b.hidden));assert.equal(blocks[2].hidden,false);
 assert.equal(ctl.reveal(new URLSearchParams({passage:'body',mention:'pei:m'})),false);assert.equal(input.checked,false);
 assert.equal(ctl.reveal(new URLSearchParams({mention:'sima:m'})),true);assert(input.checked);assert(blocks.every(b=>!b.hidden));assert(status.innerHTML.includes('data-i18n'));
 input.checked=false;input.listeners.get('change')();ctl.destroy();assert.equal(input.listeners.size,0);
 const ctl2=bindCommentaryControls(root,chapter,state);assert.equal(input.checked,false);assert(blocks[0].hidden);ctl2.destroy();
 const decode=s=>s.replace(/<[^>]*>/g,'').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
 let paragraphs=0,chapters=0;
 function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isDirectory())walk(file);else if(file.endsWith('.json')){let doc;try{doc=JSON.parse(fs.readFileSync(file));}catch{continue;}if(!Array.isArray(doc.paragraphs))continue;chapters++;for(const para of doc.paragraphs){if(typeof para.text!=='string'||!Array.isArray(para.mentions))continue;const html=chapterParagraph(para,{},null,{},'<aside>qualification</aside>');const match=html.match(/<p\b[^>]*data-source-text>([\s\S]*?)<\/p>/);assert(match,file+':'+para.id);assert.equal(decode(match[1]),para.text,file+':'+para.id);assert(!match[1].includes('data-text-layer-label'));paragraphs++;}}}}
 walk(path.join(H,'corpus'));
 const sample=chapterParagraph(chapter.paragraphs[1]);assert(sample.includes('&lt;&amp;&quot;'));assert(!sample.includes('<&"'));
 setLocale('en');assert(layerParagraph(chapter.paragraphs[1],'<p data-source-text>裴曰</p>').includes('Pei Songzhi commentary'));
 // Both actual entry points mount controls, destroy previous handlers, and reveal exact targets.
 for(const f of ['corpus-view.js','shiji-view.js']){const code=fs.readFileSync(path.join(H,'assets',f),'utf8');assert(code.includes('commentaryController?.destroy()'));assert(code.includes('commentaryControls(chapter)'));assert(code.includes('commentaryController.reveal(params)'));assert(code.includes('revealSourceTarget('));}
 console.log(JSON.stringify({passed:true,groups:layerGroups.length,restored_chapters:chapters,restored_paragraphs:paragraphs,checks:'exact layers/group checkbox/default/rebuild/cleanup/deeplink/invalid target/escaping/two entrypoints/full source restoration'}));
} finally {fs.rmSync(tmp,{recursive:true,force:true});}
