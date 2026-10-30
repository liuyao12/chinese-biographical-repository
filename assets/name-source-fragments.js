import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {sourcePassageURL} from './corpus-reader.js';
export function nameSourceFragmentsHTML(p){
 const own=new Set([p?.id,...(Array.isArray(p?.person_ids)?p.person_ids:[])]),groups=[];
 for(const g of Array.isArray(p?.source_name_fragments)?p.source_name_fragments:[]){
  if(g?.kind!=='source_bound_name_fragment_group'||!own.has(g.person_id)||g.status!=='contextual_provisional'||g.human_reviewed!==false||g.source_mentions_and_registry_aliases_retained!==true)continue;
  const c=g.complete_component;
  if(!c||!['zi','hao','ming','full_name'].includes(c.field)||typeof c.record_id!=='string'||!c.record_id||typeof c.value!=='string'||!c.value)continue;
  const n=(Array.isArray(p.name_components)?p.name_components:[]).find(n=>n&&typeof n==='object'&&n.id===c.record_id&&n.person_id===g.person_id&&n[c.field]===c.value);
  if(!n||n.chapter_id!==g.chapter_id||n.source_id!==g.source_id)continue;
  const f=g.fragments;if(!Array.isArray(f)||f.length<2||!Array.isArray(g.mention_ids)||g.mention_ids.length!==f.length||new Set(g.mention_ids).size!==f.length)continue;
  if(!f.every((x,i)=>x&&x.kind==='person'&&x.person_id===g.person_id&&typeof x.surface==='string'&&x.surface&&Number.isInteger(x.start)&&Number.isInteger(x.end)&&x.start>=0&&x.end>x.start&&typeof x.paragraph_id==='string'&&x.paragraph_id.startsWith(g.chapter_id+':')&&typeof x.id==='string'&&x.id.startsWith(x.paragraph_id+':m')&&g.mention_ids[i]===x.id)||f.map(x=>x.surface).join('')!==c.value)continue;
  const links=f.map(x=>({surface:x.surface,url:sourcePassageURL({...n,paragraph_id:x.paragraph_id,mention_id:x.id})}));
  if(links.some(x=>!x.url))continue;
  groups.push(`<p class="person-name-fragments"><span>${ui('Name read across source fragments (provisional)')}: ${h(c.value)}</span> · ${links.map(x=>`<a href="${h(x.url)}">${h(x.surface)}</a>`).join(' · ')}</p>`);
 }
 return groups.join('');
}
