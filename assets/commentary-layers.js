import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
// Exact source-layer declarations only. Never classify prose or quoted book titles.
export const layerGroups = [
 ['pei','Pei Songzhi commentary','裴松之注','注',['witness_appended_pei_songzhi_note','witness_peisongzhi_quoted_simabiao_xuzhuan']],
 ['lixian','Li Xian commentary','李賢注','注',['witness_appended_lixian_note']],
 ['liuban','Liu Ban collation','劉攽校','校',['witness_appended_liuban_collation']],
 ['siku','Qing Siku collation','四庫考證','校',['witness_appended_qing_siku_collation']],
 ['wuyingdian','Wuyingdian collation','武英殿考證','校',['witness_appended_wuyingdian_collation']],
 ['liuxiaobiao','Liu Xiaobiao commentary','劉孝標注','注',['witness_appended_liu_xiaobiao_note']],
 ['appraisal','Compiler appraisal','史評','評',['received_compiler_appraisal']],
 ['praise','Compiler praise','贊','贊',['received_compiler_praise']],
 ['bangu','Ban Gu discussion','班固論','論',['witness_appended_bangu_note']],
 ['chu','Chu Shaosun supplement','褚少孫補文','補',['witness_appended_chu_note']],
 ['zhengyi','Zhang Shoujie Zhengyi','張守節正義','注',['witness_appended_zhengyi_note']],
 ['duyu','Du Yu commentary','杜預注','注',['witness_duyu_annotation_excerpt']],
 ['suoyin','Sima Zhen Suoyin praise','司馬貞索隱述贊','贊',['witness_appended_suoyin_zan']]
];
export function layerInfo(p) { return layerGroups.find(g=>g[4].includes(p?.text_layer)) || null; }
export function layerParagraph(p, html, extra='') {
 const g=layerInfo(p); if(!g)return html+extra;
 return `<section class="corpus-layer-block layer-${g[0]}" data-commentary-group="${g[0]}" data-text-layer="${h(p.text_layer)}"><div class="corpus-text-layer" data-text-layer-label="${h(p.text_layer)}"><span class="corpus-layer-marker">${h(g[3])}</span> ${ui(g[1])}${p.text_layer==='witness_peisongzhi_quoted_simabiao_xuzhuan'?' · '+h('引司馬彪序傳'):''}</div>${html}${extra}</section>`;
}
export function commentaryControls(chapter) {
 const groups=layerGroups.filter(g=>(chapter.paragraphs||[]).some(p=>layerInfo(p)===g));
 if(!groups.length)return '';
 return `<fieldset class="corpus-layer-controls"><legend>${ui('Commentary and supplementary layers')}</legend>${groups.map(g=>`<label><input type="checkbox" data-commentary-toggle="${g[0]}" checked> ${ui(g[1])}</label>`).join('')}<p class="corpus-layer-status" aria-live="polite"></p></fieldset>`;
}
export function targetParagraph(chapter, params) {
 const ps=chapter.paragraphs||[];let id=params.get('passage'),mid=params.get('mention');
 const mentions=new Map(ps.flatMap(p=>(p.mentions||[]).map(m=>[m.id,p.id])));
 if(!mid&&mentions.has(id)){mid=id;id=mentions.get(mid);}
 if(mid){if(!mentions.has(mid)||(id&&id!==mentions.get(mid)))return null;id=mentions.get(mid);}
 return ps.find(p=>p.id===id)||null;
}
export function bindCommentaryControls(root,chapter,state=new Map()) {
 const inputs=[...root.querySelectorAll('[data-commentary-toggle]')];
 const blocks=[...root.querySelectorAll('[data-commentary-group]')];
 function apply(group,shown){state.set(group,shown);inputs.filter(n=>n.dataset.commentaryToggle===group).forEach(n=>n.checked=shown);blocks.filter(n=>n.dataset.commentaryGroup===group).forEach(n=>n.hidden=!shown);}
 const listeners=inputs.map(input=>{const group=input.dataset.commentaryToggle;apply(group,state.get(group)!==false);const fn=()=>apply(group,input.checked);input.addEventListener('change',fn);return [input,fn];});
 return {reveal(params){const p=targetParagraph(chapter,params),g=layerInfo(p);if(!g||state.get(g[0])!==false)return false;apply(g[0],true);const status=root.querySelector('.corpus-layer-status');if(status)status.innerHTML=ui('The linked source layer has been shown.');return true;},destroy(){listeners.forEach(([n,fn])=>n.removeEventListener('change',fn));}};
}
