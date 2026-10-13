import {escapeHTML as h} from './core.js';
export function chapterURL(number, category = '', passage = '') {
  const p = new URLSearchParams({chapter: String(number)});
  if (category) p.set('category', category);
  if (passage) p.set('passage', passage);
  return 'shiji.html#' + p;
}
export function chapterParagraph(paragraph, people = {}) {
  const chars = Array.from(paragraph.text), fragments = [];
  let end = 0;
  for (const mention of paragraph.mentions) {
    if (mention.start < end || mention.end > chars.length || chars.slice(mention.start, mention.end).join('') !== mention.surface) throw new Error('人物錨點與原文不符');
    fragments.push(h(chars.slice(end, mention.start).join('')));
    const text = h(mention.surface);
    if (mention.kind === 'person' && mention.person_id) {
      const person = people[mention.person_id];
      const number = Number(/^c-shiji-(\d{3})-/.exec(paragraph.id || '')?.[1]);
      const context = number ? '?' + new URLSearchParams({chapter: String(number), passage: paragraph.id}) : '';
      const href = 'person.html' + context + '#' + encodeURIComponent(mention.person_id);
      fragments.push(`<a id="${h(mention.id)}" class="cbr-person-link" data-person-id="${h(mention.person_id)}" href="${h(href)}" title="${h(person?.label || mention.surface)}">${text}</a>`);
    } else fragments.push(`<span id="${h(mention.id)}" class="unresolved-mention" title="未定指稱">${text}</span>`);
    end = mention.end;
  }
  fragments.push(h(chars.slice(end).join('')));
  return `<p id="${h(paragraph.id)}" data-source-text>${fragments.join('')}</p>`;
}
export function filteredChapters(index, category, query = '') {
  const term = query.trim();
  return index.chapters.filter(c => (!category || category === 'all' || c.category === category) && (!term || c.title.includes(term) || String(c.number) === term));
}
