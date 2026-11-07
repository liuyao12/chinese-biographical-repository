import {escapeHTML as h,safeURL} from './core.js';
import {ui} from './i18n.js';
import {chapterDirectoryMap,sourceCitation} from './source-caption.js';
import {readingWitnessBadge} from './reading-witness.js';
import {sourcePassageURL} from './corpus-reader.js';
const empty=()=>({schema_version:1,works:[]});
export function usableVolumeDirectory(value) {
 if(value?.schema_version!==1 || !Array.isArray(value.works))return empty();
 const seen=new Set(),works=[];
 for(const w of value.works){
  if(!/^w-[a-z0-9-]+$/.test(w?.work_id) || typeof w.title!=='string' || !w.title.trim() || !Array.isArray(w.books) || seen.has(w.work_id))return empty();
  seen.add(w.work_id);const ids=new Set();
  for(const b of w.books){if(!/^b-[a-z0-9-]+$/.test(b?.book_id)||ids.has(b.book_id)||(b.title!=null&&typeof b.title!=='string')||(b.citation_title!=null&&typeof b.citation_title!=='string'))return empty();ids.add(b.book_id);}
  works.push(w);
 }
 return {...value,works};
}
export async function loadVolumeDirectory(fetcher=globalThis.fetch) {
 try {const response=await fetcher('data/corpus/chapter-directory.json');return response.ok?usableVolumeDirectory(await response.json()):empty();}catch{return empty();}
}
export const volumeURL=(work,book)=>'reader.html#'+new URLSearchParams({work,book});
const imported=e=>e?.available==='marked_text'&&/^data\/corpus\/[a-z0-9-]+\/[a-zA-Z0-9_-]+\.json$/.test(e.path || '') || e?.available==='table'&&/^[a-z][a-z0-9-]*-\d{3}[a-z]?$/.test(e.table_id || '');
export function volumeModel(directory,workId,index,query='') {
 const work=directory?.works?.find(w=>w.work_id===workId);
 if(!work)return null;
 const entries=(index?.chapters || []).filter(e=>e.work_id===workId&&imported(e));
 const term=String(query).trim();
 const books=work.books.map(book=>({...book,entries:entries.filter(e=>e.book_id===book.book_id)}))
  .filter(b=>!term || [b.title,b.citation_title,b.category,b.book_id,String(b.number),...b.entries.map(e=>e.title)].some(s=>typeof s==='string'&&s.includes(term)));
 return {work,books,volume_count:work.books.length,imported_count:entries.length};
}
const bookLabel=b=>[b.title || (Number.isInteger(b.number)?`卷${b.number}`:''),b.citation_title].filter(x=>typeof x==='string'&&x).join(' · ') || b.book_id;
const citation=(model,book)=>sourceCitation({work_id:model.work.work_id,book_id:book.book_id,work_title:model.work.title,book_title:book.title || (Number.isInteger(book.number)?`卷${book.number}`:'')},chapterDirectoryMap({schema_version:1,works:[model.work]}));
const selection=(entry,number)=>`<small class="volume-selection-scope">${ui('Imported section {number}',{number})}${typeof (entry.selection_label || entry.title)==='string'&&(entry.selection_label || entry.title)?` · ${ui('Selected scope')}: ${h(entry.selection_label || entry.title)}`:''}</small>${readingWitnessBadge(entry)}`;
export function volumeNavigation(model,selectedBook='',selectedChapter='') {
 if(!model)return '';
 return model.books.map(b=>`<section class="volume-directory-entry"><a class="chapter-entry volume-entry" href="${h(volumeURL(model.work.work_id,b.book_id))}" aria-current="${b.book_id===selectedBook&&!selectedChapter?'page':'false'}">${h(bookLabel(b))}</a>${b.entries.map((e,i)=>`<a class="chapter-entry volume-subchapter" href="${h(sourcePassageURL(e))}" aria-current="${e.chapter_id===selectedChapter?'page':'false'}">${h(citation(model,b))}${selection(e,i+1)}${e.text_scope?.startsWith('partial')?` <small>${ui('Partial chapter')}</small>`:''}</a>`).join('')}</section>`).join('');
}
export function volumeLanding(model,bookId) {
 const book=model?.books?.find(b=>b.book_id===bookId);
 if(!book)return null;
 const title=citation(model,book);
 const source=model.work.source;
 const url=safeURL(source?.revision_url || source?.url);
 const footer=url?`<footer class="corpus-note"><a href="${h(url)}" target="_blank" rel="noopener">${ui('Navigation directory source')} ↗</a><p>${h(source.qualification || '')}</p></footer>`:'';
 const html=`<div class="chapter-intro" data-volume-placeholder="${h(book.book_id)}"><h1>${h(title)}</h1><p>${ui('Volume directory; not an imported source text')}</p>${book.entries.length?`<nav>${book.entries.map((e,i)=>`<p><a href="${h(sourcePassageURL(e))}">${h(title)}${selection(e,i+1)}</a></p>`).join('')}</nav>`:`<p>${ui('Source text not yet imported')}</p>`}${footer}</div>`;
 return {title,html,imported_count:book.entries.length};
}
