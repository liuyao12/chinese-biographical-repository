import {nativeProfileReturn} from './native-table-links.js';
import {escapeHTML as h} from './core.js';
export function chapterURL(number, category = '', passage = '') {
  const p = new URLSearchParams({chapter: String(number)});
  if (category) p.set('category', category);
  if (passage) p.set('passage', passage);
  return 'shiji.html#' + p;
}
export function sourcePassageURL(source) {
  if (source.work_id && source.work_id !== 'w-shiji') {
    if (!/^w-[a-z0-9-]+$/.test(source.work_id) || !source.chapter_id) return '';
    const params = new URLSearchParams({work:source.work_id, chapter:source.chapter_id});
    if (source.book_id) params.set('book',source.book_id);
    if (source.paragraph_id) params.set('passage',source.paragraph_id);
    return 'reader.html#'+params;
  }
  const number = source.number || Number(/shiji-(\d{3})/.exec(source.chapter_id || '')?.[1]);
  return number ? chapterURL(number,source.category || '',source.paragraph_id || '') : '';
}
export function profileSourceContext(person, params) {
  const table=nativeProfileReturn(person,params);
  if(table)return table;
  const work=params.get('work');
  if (!work && !params.toString()) {
    const principal=[...(person.occurrences || [])].sort((a,b)=>(b.count || 0)-(a.count || 0))[0];
    if (principal?.work_id && principal.work_id!=='w-shiji') {
      return profileSourceContext(person,new URLSearchParams({work:principal.work_id,
        book:principal.book_id,chapter:principal.chapter_id,passage:principal.paragraph_id}));
    }
  }
  if (!work || work==='w-shiji') return null;
  const occurrence=(person.occurrences || []).find(x=>x.work_id===work
    && x.chapter_id===params.get('chapter') && (!params.has('book') || x.book_id===params.get('book')));
  if (!occurrence) return null;
  const requested=params.get('passage');
  const passage=occurrence.paragraph_ids?.includes(requested)?requested:occurrence.paragraph_id;
  const href=sourcePassageURL({...occurrence,paragraph_id:passage});
  return href?{href,text:`回到《${occurrence.work_title}·${occurrence.title}》 →`}:null;
}
export function chapterParagraph(paragraph, people = {}, context = null) {
  const chars = Array.from(paragraph.text), fragments = [];
  let end = 0;
  for (const mention of paragraph.mentions) {
    if (mention.start < end || mention.end > chars.length || chars.slice(mention.start, mention.end).join('') !== mention.surface) throw new Error('人物錨點與原文不符');
    fragments.push(h(chars.slice(end, mention.start).join('')));
    const text = h(mention.surface);
    if (mention.kind === 'person' && mention.person_id) {
      const person = people[mention.person_id];
      const number = Number(/^c-shiji-(\d{3})-/.exec(paragraph.id || '')?.[1]);
      const params = context?.work_id && context.work_id !== 'w-shiji'
        ? new URLSearchParams({work:context.work_id,book:context.book_id,chapter:context.chapter_id,passage:paragraph.id})
        : number ? new URLSearchParams({chapter:String(number),passage:paragraph.id}) : null;
      const href = 'person.html' + (params ? '?'+params : '') + '#' + encodeURIComponent(mention.person_id);
      fragments.push(`<a id="${h(mention.id)}" class="cbr-person-link" data-person-id="${h(mention.person_id)}" href="${h(href)}" title="${h(person?.label || mention.surface)}">${text}</a>`);
    } else if (mention.kind === 'work' && mention.work_id && mention.person_id == null) {
      fragments.push(`<cite id="${h(mention.id)}" class="cbr-work-mention" data-work-id="${h(mention.work_id)}" title="著作：${text}">${text}</cite>`);
    } else if (mention.kind === 'non_person' && mention.person_id == null) {
      fragments.push(`<span id="${h(mention.id)}" class="cbr-non-person" data-lexical-role="${h(mention.lexical_role)}" title="${h(mention.interpretation_note)}">${text}</span>`);
    } else fragments.push(`<span id="${h(mention.id)}" class="unresolved-mention" title="${h(mention.interpretation_note || '未定指稱')}">${text}</span>`);
    end = mention.end;
  }
  fragments.push(h(chars.slice(end).join('')));
  return `<p id="${h(paragraph.id)}" data-source-text>${fragments.join('')}</p>`;
}
export function filteredChapters(index, category, query = '') {
  const term = query.trim();
  return index.chapters.filter(c => (!category || category === 'all' || c.category === category) && (!term || c.title.includes(term) || String(c.number) === term));
}
