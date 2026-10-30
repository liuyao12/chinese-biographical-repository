import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {sourcePassageURL} from './corpus-reader.js';
const modes={grant:'Granted title',transfer:'Transferred office',accession:'Accession title',demotion:'Demoted title',self_proclamation:'Self-proclaimed title',posthumous_grant:'Posthumous grant',posthumous_enfeoffment:'Posthumous enfeoffment',posthumous_naming:'Posthumous name',attestation:'Source attestation'};
export function profileTitlePreference(p){
 const d=p?.default_profile_title;
 if(!d||d.person_id!==p.id||typeof d.title!=='string'||!d.title.trim()||d.status!=='editorial_provisional'||!Object.hasOwn(modes,d.mode))return null;
 const hs=(p.titles||[]).filter(x=>x.id===d.holding_id&&x.person_id===p.id&&x.title===d.title&&x.mode===d.mode&&x.kind===d.kind&&x.status==='source_attested'&&x.source_qualification?.kind!=='reported_office_challenged_by_commentary');
 if(hs.length!==1)return null;
 const r=d.source_ref,aa=(hs[0].attestations||[]).filter(a=>a.id===d.attestation_id);
 if(!r||aa.length!==1||!['paragraph_id','person_mention_id','start','end','surface'].every(k=>r[k]===aa[0][k])||r.surface!==d.title||!Number.isInteger(r.start)||!Number.isInteger(r.end)||r.start<0||r.end<=r.start||!(hs[0].evidence||[]).some(e=>['work_id','book_id','source_id','chapter_id','paragraph_id','person_mention_id'].every(k=>e[k]===r[k]))||!sourcePassageURL({...r,mention_id:r.person_mention_id}))return null;
 return d;
}
export function profileTitleHTML(p,canPrefix=false){
 const d=profileTitlePreference(p);if(!d)return '';
 const url=sourcePassageURL({...d.source_ref,mention_id:d.source_ref.person_mention_id});
 return `<p class="person-profile-title-choice">${canPrefix?'':`<strong>${h(d.title)}</strong> · `}<span class="person-profile-title-mode">${ui(modes[d.mode])}</span> · <span>${ui('Editorial profile title')}</span> · <a class="person-profile-title-source" href="${h(url)}">${ui('Title source')}</a></p>`;
}
