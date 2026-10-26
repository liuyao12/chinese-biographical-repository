import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {sourcePassageURL} from './corpus-reader.js';
const modes={attestation:'Source title use',grant:'Granted title',transfer:'Transferred office',accession:'Accession title',demotion:'Demoted title',self_proclamation:'Self-proclaimed title',posthumous_grant:'Posthumous grant',posthumous_enfeoffment:'Posthumous enfeoffment',posthumous_naming:'Posthumous name'};
export function profileTitlePreference(p){
 const d=p?.default_profile_title;
 if(!d||d.person_id!==p.id||typeof d.title!=='string'||!d.title.trim()||d.status!=='editorial_provisional'||!Object.hasOwn(modes,d.mode))return null;
 const hs=(p.titles||[]).filter(x=>x.id===d.holding_id&&x.person_id===p.id&&x.title===d.title&&x.mode===d.mode&&x.kind===d.kind&&x.status==='source_attested'&&x.source_qualification?.kind!=='reported_office_challenged_by_commentary');
 if(hs.length!==1)return null;
 if(d.mode==='attestation'&&(d.kind!=='noble_rank'||hs[0].appointment_role!=='source_attested_use'||hs[0].source_career_role?.kind!=='attached_received_biography_frame'||!hs[0].source_career_role?.frame||!['start','end'].every(k=>hs[0].effective_period?.[k]?.status==='unknown'&&hs[0].effective_period[k].date_expression===null)))return null;
 const r=d.source_ref,aa=(hs[0].attestations||[]).filter(a=>a.id===d.attestation_id);
 if(!r||aa.length!==1||!['paragraph_id','person_mention_id','start','end','surface'].every(k=>r[k]===aa[0][k])||r.surface!==d.title||!Number.isInteger(r.start)||!Number.isInteger(r.end)||r.start<0||r.end<=r.start||!(hs[0].evidence||[]).some(e=>['work_id','book_id','source_id','chapter_id','paragraph_id','person_mention_id'].every(k=>e[k]===r[k]))||!sourcePassageURL({...r,mention_id:r.person_mention_id}))return null;
 return d;
}
export function profileTitleHTML(p,canPrefix=false){
 const d=profileTitlePreference(p);if(!d)return '';
 const url=sourcePassageURL({...d.source_ref,mention_id:d.source_ref.person_mention_id});
 return `<p class="person-profile-title-choice">${canPrefix?'':`<strong>${h(d.title)}</strong> · `}<span class="person-profile-title-mode">${ui(modes[d.mode])}</span> · <span>${ui('Editorial profile title')}</span> · <a class="person-profile-title-source" href="${h(url)}">${ui('Title source')}</a></p>`;
}

// A local grant is a reading context, never a new lifetime/default title.
export function profileMentionContext(p, params) {
 if(!(params instanceof URLSearchParams)||params.has('table'))return null;
 const keys=['work','book','chapter','passage','mention'];
 if(keys.some(k=>params.getAll(k).length!==1||!params.get(k)))return null;
 const matches=(p?.occurrences||[]).filter(o=>o.work_id===params.get('work')&&o.book_id===params.get('book')&&o.chapter_id===params.get('chapter')&&o.mention_ids?.includes(params.get('mention'))&&o.mention_paragraph_ids?.[params.get('mention')]===params.get('passage'));
 if(matches.length!==1)return null;
 const o=matches[0];if(params.has('source')&&(params.getAll('source').length!==1||params.get('source')!==o.source_id))return null;if(params.has('source_id')&&(params.getAll('source_id').length!==1||params.get('source_id')!==o.source_id))return null;return {person_id:p.id,work_id:o.work_id,book_id:o.book_id,chapter_id:o.chapter_id,source_id:o.source_id,paragraph_id:params.get('passage'),mention_id:params.get('mention')};
}
export function profileLinkMentionContext(p,node,baseURL='https://reader.invalid/') {
 try{const u=new URL(node?.href,baseURL);return decodeURIComponent(u.hash.slice(1))===p?.id&&node?.id===u.searchParams.get('mention')?profileMentionContext(p,u.searchParams):null;}catch{return null;}
}
export function mentionGrantTitlePreference(p, context) {
 const c=context?.source_context;if(!c||c.person_id!==p?.id)return null;
 // Recheck the context against this person's occurrence index, including the exact MID.
 const params=new URLSearchParams({work:c.work_id,book:c.book_id,chapter:c.chapter_id,passage:c.paragraph_id,mention:c.mention_id});
 const checked=profileMentionContext(p,params);if(!checked||Object.keys(checked).some(k=>checked[k]!==c[k]))return null;
 const refs=['work_id','book_id','source_id','chapter_id','paragraph_id'];
 const bound=e=>e&&refs.every(k=>e[k]===c[k])&&e.person_mention_id===c.mention_id&&typeof e.quote==='string';
 const anchor=(a,text)=>a&&a.paragraph_id===c.paragraph_id&&Number.isInteger(a.start)&&Number.isInteger(a.end)&&a.start>=0&&a.end>a.start&&Array.from(text).slice(a.start,a.end).join('')===a.surface;
 const matches=(p.titles||[]).filter(x=>{
  const r=x.source_career_role,s=x.effective_period?.start;
  if(x.person_id!==p.id||x.kind!=='royal_rank'||x.mode!=='grant'||x.status!=='source_attested'||typeof x.title!=='string'||!x.title.trim()||r?.kind!=='fixed_nanqi006_royal_enfeoffment'||typeof r.source_revision!=='string'||!r.source_revision||!/^[a-f0-9]{64}$/.test(r.paragraph_sha256||'')||r.slot!==c.mention_id||r.recipient_mention_id!==c.mention_id||s?.status!=='source_event'||s.event_type!=='grant')return false;
  const sources=(p.sources||[]).filter(v=>refs.slice(0,4).every(k=>v[k]===c[k])&&v.source?.revision_id===r.source_revision&&typeof v.source?.raw_sha256==='string'&&v.source.raw_sha256.length===64);
  const evidence=(x.evidence||[]).filter(bound),starts=(s.evidence||[]).filter(bound),a=(x.attestations||[]).filter(v=>v.person_mention_id===c.mention_id&&v.paragraph_id===c.paragraph_id&&v.surface===x.title);
  if(sources.length!==1||evidence.length!==1||starts.length!==1||starts[0].quote!==evidence[0].quote||a.length!==1)return false;
  const text=evidence[0].quote,ta=r.title_anchor,clause=r.grant_clause_anchor;
  return anchor(ta,text)&&anchor(clause,text)&&ta.surface===x.title&&ta.start>=clause.start&&ta.end<=clause.end&&['start','end','surface','paragraph_id'].every(k=>a[0][k]===ta[k]);
 });
 return matches.length===1?matches[0]:null;
}
export function mentionGrantTitleHTML(holding){
 if(!holding)return '';
 const e=holding.evidence[0],url=sourcePassageURL({...e,mention_id:e.person_mention_id});
 return `<p class="person-mention-grant-title">${ui('Title granted at this mention')} · <a href="${h(url)}">${ui('Title source')}</a></p>`;
}
