import {summarizeNameComponents} from './name-components.js';
import {profileTitlePreference} from './profile-title.js';
/** Discovery uses published indexes only; aliases never become extra people. */
export const WORK_GROUPS = [
  {key:'early',title:'Early histories and chronological works',ids:['w-shiji','w-hanshu','w-houhanshu','w-zizhitongjian','w-zuozhuan-zhushu']},
  {key:'medieval',title:'Three Kingdoms, Jin and Northern and Southern Dynasties',ids:['w-sanguozhi','w-jinshu','w-songshu','w-nanqishu','w-liangshu','w-chenshu','w-beiqishu','w-zhoushu','w-weishu-weishou','w-beishi','w-nanshi']},
  {key:'later',title:'Sui, Tang and later dynastic histories',ids:['w-suishu','w-jiutangshu','w-xintangshu','w-jiuwudaishi','w-xinwudaishi','w-songshi','w-liaoshi','w-jinshi','w-yuanshi','w-mingshi']},
  {key:'other',title:'Epitaphs, genealogies and reference works',ids:[]}
];
export function groupWorks(works) {
  const assigned=new Set();
  return WORK_GROUPS.map(group=>({...group,works:works.filter(w=>{
    const match=group.key==='other'?!assigned.has(w.id):group.ids.includes(w.id);
    if(match)assigned.add(w.id);return match;
  })})).filter(g=>g.works.length);
}
export function workURL(work) {
  return work.reader_kind==='shiji'?'shiji.html':'reader.html#'+new URLSearchParams({work:work.id});
}
export function canonicalProfiles(people, index, directory = null) {
  const profiles=new Map((index.profiles || []).map(p=>[p.id,p]));
  return Object.entries(people).filter(([id,p])=>p && p.id===id && profiles.has(id)).map(([id,p])=>{
    const entry=profiles.get(id);
    const metadata=directory?.persons?.[id];
    const display=directoryDisplay(metadata,p.label);
    const facets=directoryFacets(metadata);
    return {id,label:p.label,names:[...new Set([p.label,...(entry.names || []),...(p.aliases || []),display.name,display.title,...display.additional].filter(n=>typeof n==='string'&&n.trim()))],review:p.review,display,facets};
  }).sort((a,b)=>a.label.localeCompare(b.label,'zh-Hant')||a.id.localeCompare(b.id));
}
export function searchPeople(people, query) {
  const q=query.trim().toLocaleLowerCase();if(!q)return people;
  const ranked=[];
  for(const p of people){
    const names=p.names.map(n=>n.toLocaleLowerCase());
    const rank=names.includes(q)?0:names.some(n=>n.startsWith(q))?1:names.some(n=>n.includes(q))?2:p.id.toLowerCase().includes(q)?3:-1;
    if(rank>=0)ranked.push({p,rank});
  }
  return ranked.sort((a,b)=>a.rank-b.rank).map(x=>x.p);
}

export const UNKNOWN_FACET = '__unknown__';
const present = value => typeof value==='string' && value.trim() ? value.trim() : '';
const unique = values => [...new Set(values.map(present).filter(Boolean))];
const facetValues = values => {const found=unique(values);return found.length?found:[UNKNOWN_FACET];};
export function directoryDisplay(metadata, label='') {
  const summary=summarizeNameComponents(metadata?.name_components,metadata?.preferred_name_component_readings);
  const n=summary.names;
  const partial=Boolean(n&&!n.clan_style?.value&&!n.full_name&&n.ming&&!n.surname&&label?.endsWith(n.ming)&&label.length>n.ming.length);
  const personal=n?.clan_style?.value||n?.full_name||(n?`${n.surname||''}${n.ming||''}`:'');
  const name=!partial&&summary.canHead&&personal?personal:label;
  const preferred=profileTitlePreference(metadata);
  let title=preferred&&!partial&&summary.canHead&&personal?preferred.title:summary.canHead?present(n?.title):'';
  const usingFallback=partial||!summary.canHead||!personal;
  if(title&&(title===name||(usingFallback&&name.startsWith(title))))title='';
  const additional=n?unique([n.zi?`字${n.zi}`:'',n.hao?`號${n.hao}`:'']):[];
  return {title,jiguan:unique((metadata?.jiguan||[]).map(x=>x.value)).join('／'),name,additional};
}
export function directoryFacets(metadata) {
  const summary=summarizeNameComponents(metadata?.name_components,metadata?.preferred_name_component_readings),n=summary.names;
  return {dynasty:facetValues((metadata?.period_assignments||[]).map(x=>x.value)),surname:facetValues([n?.surname||n?.clan_style?.value]),jiguan:facetValues((metadata?.jiguan||[]).map(x=>x.value))};
}
const DIMENSIONS=['dynasty','surname','jiguan'];
function matchesSelection(person, selection={}, except=null) {
  return DIMENSIONS.every(key=>key===except||!Array.isArray(selection[key])||!selection[key].length||selection[key].some(v=>(person.facets?.[key]?.length?person.facets[key]:[UNKNOWN_FACET]).includes(v)));
}
export function filterPeople(people, query='', selection={}) {
  return searchPeople(people,query).filter(p=>matchesSelection(p,selection));
}
export function facetCounts(people, query='', selection={}) {
  const searched=searchPeople(people,query),result={};
  for(const key of DIMENSIONS){
    const counts=new Map();
    for(const p of searched.filter(p=>matchesSelection(p,selection,key))){
      for(const value of new Set(p.facets?.[key]?.length?p.facets[key]:[UNKNOWN_FACET]))counts.set(value,(counts.get(value)||0)+1);
    }
    for(const value of selection[key]||[])if(!counts.has(value))counts.set(value,0);
    result[key]=[...counts].map(([value,count])=>({value,count})).sort((a,b)=>a.value===UNKNOWN_FACET?1:b.value===UNKNOWN_FACET?-1:a.value.localeCompare(b.value,'zh-Hant'));
  }
  return result;
}
