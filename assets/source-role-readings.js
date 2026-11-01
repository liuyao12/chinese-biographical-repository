import {escapeHTML as h} from './core.js';
import {t} from './i18n.js';
function group(m){
  const g=m?.source_person_group;if(g==null)return null;
  if(m.kind!=='unresolved'||m.person_id!=null||g.completeness!=='complete'||g.unknown_members!==false
    ||!Array.isArray(g.group_marker_ids)||!g.group_marker_ids.includes(m.id)||!Array.isArray(g.members)||g.members.length!==2
    ||new Set(g.members.map(v=>v.person_id)).size!==2||!(g.reported_count==null||Number.isInteger(g.reported_count)&&g.reported_count===2)
    ||g.members.some(v=>typeof v.person_id!=='string'||typeof v.label!=='string'||!v.label.trim()))throw Error('Invalid source collective reading');
  return g;
}
export function collectiveMarkerHTML(m){const g=group(m);if(!g)return null;return `<span id="${h(m.id)}" class="unresolved-mention cbr-collective-reference" data-collective-id="${h(g.id)}" title="${h(m.surface+'：'+g.members.map(v=>v.label).join('、'))}">${h(m.surface)}</span>`;}
export function collectiveNotesHTML(paragraph){
  const seen=new Set(),rows=[];
  for(const m of paragraph.mentions||[]){const g=group(m);if(!g||seen.has(g.id))continue;seen.add(g.id);rows.push(`<details data-source-person-group="${h(g.id)}"><summary>${h(m.surface)}：${h(g.members.map(v=>v.label).join('、'))}</summary><ul>${g.members.map(v=>`<li><a class="collective-member-profile" href="person.html#${h(encodeURIComponent(v.person_id))}">${h(v.label)}</a></li>`).join('')}</ul><p data-original>${h(g.scope_qualification)}</p></details>`);}
  return rows.length?`<aside class="cross-chapter-references cbr-collective-readings" aria-label="${h(t('Referent interpretations'))}">${rows.join('')}</aside>`:'';
}
export function chapterTitleHTML(m,paragraph,urlForSource){
 const r=m?.chapter_reference;if(r==null)return null;
 const s=r.source,t=r.target,chars=Array.from(paragraph.text);
 if(m.kind!=='work'||m.person_id!=null||m.work_id!=='w-shiji'||r.kind!=='explicit_cross_chapter_reference'
   ||s?.mention_id!==m.id||s.paragraph_id!==paragraph.id||s.paragraph_text!==paragraph.text||!Number.isInteger(s.start)||!Number.isInteger(s.end)
   ||s.start!==m.start||s.end<m.end||chars.slice(s.start,s.end).join('')!==s.surface||t?.work_id!=='w-shiji'||t.text_status!=='imported'
   ||!/^b-shiji-\d{3}$/.test(t.book_id)||!/^c-shiji-\d{3}-[a-z0-9-]+$/.test(t.chapter_id)
   ||t.chapter_id.slice(8,11)!==t.book_id.slice(-3)||typeof t.paragraph_id!=='string'||!t.paragraph_id.startsWith(t.chapter_id+':'))throw Error('Invalid chapter title reference');
 const href=urlForSource(t);if(!href)throw Error('Missing chapter title target');
 return `<a id="${h(m.id)}" class="cbr-work-mention cbr-chapter-reference" data-chapter-reference="${h(r.id)}" href="${h(href)}" title="${h('《史記·'+t.section_label+'》')}">${h(m.surface)}</a>`;
}
