import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
export function declinedNobleOutcomeUnreported(q){
 const d=q?.reported_declination,a=d?.source_anchor;
 return q?.proposal_kind==='appointment_declination_outcome_unreported'&&q.outcome==='not_reported'
  &&q.kind==='noble_rank'&&q.appointment_issued===true&&q.acceptance_status==='not_reported'
  &&q.effective_service_attested===false&&q.human_reviewed===false
  &&q.source_appointment_context?.kind==='wyd_song044_declined_noble_advance'
  &&d?.reported===true&&d.source_term==='固讓進封'&&a?.surface===d.source_term
  &&Number.isInteger(a.start)&&a.start>=0&&Number.isInteger(a.end)&&a.end-a.start===Array.from(a.surface).length
  &&(q.evidence||[]).some(e=>e.paragraph_id===a.paragraph_id&&typeof e.quote==='string'&&Array.from(e.quote).slice(a.start,a.end).join('')===a.surface);
}
export function nobleHouseholds(x,offered=false){
 const v=x?.reported_households,a=v?.source_anchor;
 if(!v||!Number.isInteger(v.value)||v.value<=0||typeof v.source_number!=='string'||!v.source_number||v.unit!=='戶'||v.actual_revenue!==null
   ||v.scope!==(offered?'offered_advancement_not_confirmed_held':'actual_enfeoffment_allotment')
   ||a?.surface!=='食邑'+v.source_number+'戶'||!Number.isInteger(a.start)||a.start<0||!Number.isInteger(a.end)||a.end<=a.start
   ||!(x.evidence||[]).some(e=>e.paragraph_id===a.paragraph_id&&typeof e.quote==='string'&&Array.from(e.quote).slice(a.start,a.end).join('')===a.surface)
   ||(offered?!declinedNobleOutcomeUnreported(x):x.mode!=='grant'||x.kind!=='noble_rank'||x.source_career_role?.kind!=='wyd_song044_noble_grant'))return '';
 return `<p class="person-noble-households">${ui(offered?'Offered fief households (not confirmed held)':'Fief households')}: <q>${h(a.surface)}</q></p>`;
}
