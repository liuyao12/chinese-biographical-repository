import {escapeHTML as h} from './core.js';
export function workTitleMap(index) {
  if (index?.schema_version !== 1 || !Array.isArray(index.works)) throw Error('Invalid work title index');
  const titles = Object.create(null);
  for (const row of index.works) {
    if (!/^w-[a-z0-9-]+$/.test(row.id) || typeof row.title !== 'string' || !row.title.trim() || Object.hasOwn(titles,row.id)) throw Error('Invalid work title row');
    if (row.qualification !== undefined && (typeof row.qualification !== 'string' || !row.qualification.trim())) throw Error('Invalid work qualification');
    titles[row.id] = row.qualification === undefined ? row.title : {title:row.title,qualification:row.qualification};
  }
  return titles;
}
export async function loadWorkTitles(fetcher = globalThis.fetch) {
  try {
    const response = await fetcher('data/corpus/work-titles.json');
    return response.ok ? workTitleMap(await response.json()) : Object.create(null);
  } catch { return Object.create(null); }
}
export function workMentionHTML(mention, titles = {}) {
  const surface = h(mention.surface), entry = Object.hasOwn(titles,mention.work_id) ? titles[mention.work_id] : null;
  const title=typeof entry==='string'?entry:entry?.title, qualification=typeof entry==='object'&&entry?entry.qualification:'';
  if (typeof title !== 'string' || !title.trim()) return `<cite id="${h(mention.id)}" class="cbr-work-mention" data-work-id="${h(mention.work_id)}" title="著作：${surface}">${surface}</cite>`;
  const description='《'+title+'》'+(qualification?'；'+qualification:'');
  return `<button type="button" id="${h(mention.id)}" class="cbr-work-mention cbr-work-title" data-work-id="${h(mention.work_id)}" data-work-title="${h(title)}"${qualification?` data-work-qualification="${h(qualification)}"`:''} title="${h(description)}" aria-label="${surface}，引書${h(description)}" aria-expanded="false">${surface}</button>`;
}
let nextTooltip = 0;
export function bindWorkTitles(root) {
  const doc = root.ownerDocument, view = doc.defaultView;
  const tip = doc.createElement('div'); tip.className='cbr-work-tooltip';tip.id='cbr-work-tooltip-'+(++nextTooltip);tip.setAttribute('role','tooltip');tip.hidden=true;doc.body.append(tip);
  let current=null,pinned=false;
  const target = node => {const button=node?.closest?.('button.cbr-work-title');return button && root.contains(button) ? button : null;};
  const close=()=>{if(current){current.setAttribute('aria-expanded','false');current.removeAttribute('aria-describedby');}current=null;pinned=false;tip.hidden=true;};
  const place=()=>{if(!current)return;const r=current.getBoundingClientRect(),box=tip.getBoundingClientRect(),w=view.innerWidth,height=view.innerHeight;tip.style.left=Math.max(8,Math.min(r.left,w-box.width-8))+'px';tip.style.top=Math.max(8,r.bottom+6+box.height<=height?r.bottom+6:r.top-box.height-6)+'px';};
  const show=button=>{if(current!==button)close();current=button;tip.textContent='';const heading=doc.createElement('div');heading.className='cbr-work-tooltip-title';heading.textContent='《'+button.dataset.workTitle+'》';tip.append(heading);if(button.dataset.workQualification){const note=doc.createElement('div');note.className='cbr-work-tooltip-qualification';note.textContent=button.dataset.workQualification;tip.append(note);}tip.hidden=false;button.setAttribute('aria-expanded','true');button.setAttribute('aria-describedby',tip.id);place();};
  const over=e=>{if(e.pointerType && e.pointerType!=='mouse')return;const button=target(e.target);if(button&&!pinned)show(button);};
  const out=e=>{if(!pinned && current && !current.contains(e.relatedTarget) && doc.activeElement!==current)close();};
  const focus=e=>{const button=target(e.target);if(button)show(button);};
  const blur=e=>{if(!pinned && !target(e.relatedTarget))close();};
  const click=e=>{const button=target(e.target);if(!button)return;e.preventDefault();if(current===button&&pinned)close();else{show(button);pinned=true;}};
  const outside=e=>{if(!target(e.target))close();};
  const key=e=>{if(e.key==='Escape')close();};
  root.addEventListener('pointerover',over);root.addEventListener('pointerout',out);root.addEventListener('focusin',focus);root.addEventListener('focusout',blur);root.addEventListener('click',click);
  doc.addEventListener('pointerdown',outside);doc.addEventListener('keydown',key);view.addEventListener('resize',place);view.addEventListener('scroll',place,true);
  return()=>{close();tip.remove();root.removeEventListener('pointerover',over);root.removeEventListener('pointerout',out);root.removeEventListener('focusin',focus);root.removeEventListener('focusout',blur);root.removeEventListener('click',click);doc.removeEventListener('pointerdown',outside);doc.removeEventListener('keydown',key);view.removeEventListener('resize',place);view.removeEventListener('scroll',place,true);};
}
