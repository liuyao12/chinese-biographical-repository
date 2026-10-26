import {escapeHTML as h} from './core.js';
import {ui,t} from './i18n.js';
import {sourceCaption} from './source-caption.js';
const id = (value,prefix) => typeof value==='string' && new RegExp('^'+prefix+'[a-z0-9-]+$').test(value);
export function boundCrossChapterReferences(chapter, paragraphId) {
  const entries=chapter?.cross_chapter_references;
  if(entries==null)return [];
  if(!Array.isArray(entries))throw Error('Invalid cross-chapter references');
  const paragraph=chapter.paragraphs?.find(p=>p.id===paragraphId);
  if(!paragraph)return [];
  return entries.filter(e=>e?.source?.paragraph_id===paragraphId).map(e=>{
    const s=e.source, chars=Array.from(paragraph.text);
    if(e.kind!=='explicit_cross_chapter_reference' || typeof e.id!=='string'
      || s.work_id!==chapter.work_id || s.book_id!==chapter.book_id || s.chapter_id!==chapter.id
      || s.source_id!==chapter.source_id || s.revision_id!==chapter.source?.revision_id
      || s.paragraph_text!==paragraph.text || !Number.isInteger(s.start) || !Number.isInteger(s.end)
      || s.start<0 || s.end<=s.start || s.end>chars.length
      || chars.slice(s.start,s.end).join('')!==s.surface)
      throw Error('Cross-chapter reference does not match its fixed source');
    return e;
  });
}
export function crossChapterTarget(target,directory) {
  if(!id(target?.work_id,'w-') || !id(target?.book_id,'b-'))return null;
  const works=directory?.works;
  if(!Array.isArray(works))return null;
  const matching=works.filter(w=>w.work_id===target.work_id);
  if(matching.length!==1)return null;
  const work=matching[0],books=work.books?.filter(b=>b.book_id===target.book_id);
  if(books?.length!==1)return null;
  const book=books[0];
  if(typeof work.title!=='string' || typeof book.title!=='string')return null;
  const params=new URLSearchParams({work:target.work_id,book:target.book_id});
  // A registered whole-volume landing is valid even before any text is imported.
  return {href:'reader.html#'+params,label:sourceCaption(work.title,book.citation_title)+' · '+book.title};
}
export function crossChapterReferences(chapter,paragraphId,directory) {
  const entries=boundCrossChapterReferences(chapter,paragraphId);
  if(!entries.length)return '';
  return `<aside class="cross-chapter-references" aria-label="${h(t('Cross-reference'))}">${entries.map(e=>{
    const target=crossChapterTarget(e.target,directory);
    const section=e.target?.section_label?` · ${h(e.target.section_label)}`:'';
    return `<div data-cross-chapter-reference="${h(e.id)}">${ui('Cross-reference')}: ${target
      ? `<a href="${h(target.href)}">${h(e.source.surface)} → ${h(target.label)}${section}</a>${e.target.text_status==='not_imported'?` <small>${ui('Target passage not yet imported')}</small>`:''}`
      : `<span>${h(e.source.surface)}${section} · ${ui('Target volume not registered')}</span>`}</div>`;
  }).join('')}</aside>`;
}
