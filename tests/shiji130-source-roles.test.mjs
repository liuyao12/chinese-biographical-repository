import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=process.env.CBR_NATIVE_TEST_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const {chapterParagraph,sourcePassageURL}=await import(pathToFileURL(path.join(root,'assets/corpus-reader.js')));
const {chapterTitleHTML,collectiveMarkerHTML,collectiveNotesHTML}=await import(pathToFileURL(path.join(root,'assets/source-role-readings.js')));
const chapter=JSON.parse(fs.readFileSync(path.join(root,'corpus/shiji/130.json'),'utf8'));
const selected=chapter.paragraphs.filter(p=>chapter.annotation.source_role_review.scope_paragraph_ids.includes(p.id));
const marker=suffix=>selected.flatMap(p=>p.mentions.map(m=>({p,m}))).find(v=>v.m.id.endsWith(':'+suffix));
test('six paragraphs retain exact received text with notes outside source paragraph',()=>{
 for(const p of selected){const html=chapterParagraph(p);const body=/<p[^>]*data-source-text>([\s\S]*?)<\/p>/.exec(html)[1];assert.equal(body.replace(/<[^>]*>/g,'').replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>'),p.text);}
});
test('four title terms link to the actual existing chapters without person links',()=>{
 const targets=[['m047-0047',35],['m074-0021',62],['m107-0029',95],['m132-0035',120]];
 for(const [id,n]of targets){const {m,p}=marker(id);const html=chapterTitleHTML(m,p,sourcePassageURL);assert.match(html,new RegExp('chapter='+n+'&amp;passage='));assert.match(html,/class="cbr-work-mention cbr-chapter-reference"/);assert.ok(!html.includes('data-person-id'));assert.equal(html.replace(/<[^>]*>/g,''),m.surface);}
});
test('short Fan Li title is preserved while tooltip identifies the full target title',()=>{
 const {m,p}=marker('m107-0029');const html=chapterTitleHTML(m,p,sourcePassageURL);assert.match(html,/樊酈滕灌列傳第三十五/);assert.equal(m.surface,'樊酈');assert.equal(m.chapter_reference.source.surface,'樊酈列傳');
});
test('Guancai at paragraph opening is a group and closing occurrence is a title',()=>{
 const opening=marker('m047-0000'),closing=marker('m047-0047');assert.match(collectiveMarkerHTML(opening.m),/cbr-collective-reference/);assert.equal(chapterTitleHTML(opening.m,opening.p,sourcePassageURL),null);assert.equal(collectiveMarkerHTML(closing.m),null);
});
test('group notes identify the two members with profile links, separate from direct-name markup',()=>{
 const {p,m}=marker('m006-0204');const html=collectiveNotesHTML(p);assert.match(html,/文武：周文王、武王/);for(const member of m.source_person_group.members)assert.ok(html.includes('person.html#'+encodeURIComponent(member.person_id)));assert.ok(!html.includes('class="cbr-person-link"'));
});
test('ordinary work markers retain their old rendering route',()=>{
 const fake={id:'synthetic',kind:'work',work_id:'w-shiji',person_id:null,surface:'史記',start:0,end:2};assert.equal(chapterTitleHTML(fake,{text:'史記'},sourcePassageURL),null);
});
test('malformed book/chapter targets and source ranges fail closed',()=>{
 const {m,p}=marker('m074-0021');for(const change of [v=>v.chapter_reference.target.book_id='b-shiji-095',v=>v.chapter_reference.source.start--,v=>v.chapter_reference.target.chapter_id='javascript:alert(1)']){const bad=structuredClone(m);change(bad);assert.throws(()=>chapterTitleHTML(bad,p,sourcePassageURL));}
});
test('group alternatives or fabricated reported counts fail closed',()=>{
 const {m}=marker('m006-0204');for(const change of [v=>v.source_person_group.completeness='alternative',v=>v.source_person_group.reported_count=true,v=>v.source_person_group.members.pop()]){const bad=structuredClone(m);change(bad);assert.throws(()=>collectiveMarkerHTML(bad));}
});
test('group labels and target titles are escaped as text',()=>{
 const {m,p}=marker('m074-0021');const changed=structuredClone(m);changed.chapter_reference.target.section_label='<img src=x onerror=alert(1)>';assert.ok(!chapterTitleHTML(changed,p,sourcePassageURL).includes('<img'));
 const g=structuredClone(marker('m006-0204').m);g.source_person_group.members[0].label='<script>x</script>';assert.ok(!collectiveMarkerHTML(g).includes('<script>'));
});
