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
export function canonicalProfiles(people, index) {
  const profiles=new Map((index.profiles || []).map(p=>[p.id,p]));
  return Object.entries(people).filter(([id,p])=>p && p.id===id && profiles.has(id)).map(([id,p])=>{
    const entry=profiles.get(id);
    return {id,label:p.label,names:[...new Set([p.label,...(entry.names || []),...(p.aliases || [])].filter(n=>typeof n==='string'&&n.trim()))],review:p.review};
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
