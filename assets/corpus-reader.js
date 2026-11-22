import {layerParagraph} from './commentary-layers.js';
import {sourceCitation} from './source-caption.js';
import {workMentionHTML} from './work-titles.js';
import {nativeProfileReturn} from './native-table-links.js';
import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
export function chapterURL(number, category = '', passage = '', text = '') {
  const p = new URLSearchParams({chapter: String(number)});
  if (category) p.set('category', category);
  if (passage) p.set('passage', passage);
  if (text) p.set('text', text);
  return 'shiji.html#' + p;
}
export function sourcePassageURL(source) {
  if (source.work_id && source.work_id !== 'w-shiji') {
    if (!/^w-[a-z0-9-]+$/.test(source.work_id) || !source.chapter_id) return '';
    const params = new URLSearchParams({work:source.work_id, chapter:source.chapter_id});
    if (source.book_id) params.set('book',source.book_id);
    if (source.paragraph_id) params.set('passage',source.paragraph_id);
    if (source.mention_id) params.set('mention',source.mention_id);
    return 'reader.html#'+params;
  }
  const number = source.number || Number(/shiji-(\d{3})/.exec(source.chapter_id || '')?.[1]);
  const text = source.work_id === 'w-shiji' && /^c-shiji-\d{3}-/.test(source.chapter_id || '') ? source.chapter_id : '';
  return number ? chapterURL(number,source.category || '',source.paragraph_id || '',text) : '';
}

export function shijiReadingEntry(volume, params) {
  if (!volume) return volume;
  const passage = params.get('passage') || '';
  let selected = volume.excerpts?.find(excerpt =>
    excerpt.chapter_id === params.get('text') || (!params.has('text') && passage.startsWith(excerpt.chapter_id + ':')));
  if (!selected && volume.available === 'excerpt') selected = volume.excerpts.find(e => e.chapter_id === volume.chapter_id);
  return selected ? {...volume, ...selected} : volume;
}

export function facsimilePageLinks(source, position) {
  const columns = position?.column_projection ?? position?.columns;
  if (source?.image_verified !== true || !Array.isArray(columns) || !columns.length) return '';
  let pdf;
  try {
    pdf = new URL(source.url);
    if (pdf.protocol !== 'https:' || !pdf.pathname.toLowerCase().endsWith('.pdf')) return '';
    if (pdf.hostname === 'commons.wikimedia.org' && pdf.pathname.startsWith('/wiki/File:')) {
      const file = decodeURIComponent(pdf.pathname.slice('/wiki/File:'.length));
      pdf = new URL('https://commons.wikimedia.org/wiki/Special:FilePath/' + encodeURIComponent(file));
    } else if (pdf.hostname !== 'upload.wikimedia.org') {
      return '';
    }
  } catch {
    return '';
  }
  const pages = new Set(columns.map(part => part.pdf_page)
    .filter(page => Number.isInteger(page) && page > 0));
  if (!pages.size) return '';
  const links = Array.from(pages, page => {
    pdf.hash = 'page=' + page;
    return `<a href="${h(pdf.href)}" target="_blank" rel="noopener">${ui('Facsimile page {page}', {page})} ↗</a>`;
  });
  return `<small class="facsimile-page-links">${links.join(' · ')}</small>`;
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
  const requestedMention=params.get('mention') || (occurrence.mention_ids?.includes(requested)?requested:null);
  const mention=requestedMention && occurrence.mention_ids?.includes(requestedMention)?requestedMention:null;
  const actualPassage=mention?occurrence.mention_paragraph_ids?.[mention] || passage:passage;
  const href=sourcePassageURL({...occurrence,paragraph_id:actualPassage,mention_id:mention});
  return href?{href,text:`回到${sourceCitation(occurrence,person.source_chapter_directory,person.source_work_titles)} →`}:null;
}
export function chapterParagraph(paragraph, people = {}, context = null, workTitles = {}, extraHTML = '') {
  const chars = Array.from(paragraph.text), fragments = [], biographyLinks = [];
  let end = 0;
  for (const mention of paragraph.mentions) {
    if (mention.start < end || mention.end > chars.length || chars.slice(mention.start, mention.end).join('') !== mention.surface) throw new Error('人物錨點與原文不符');
    fragments.push(h(chars.slice(end, mention.start).join('')));
    const text = h(mention.surface);
    if (mention.suppress_person_link === true) {
      fragments.push(`<span id="${h(mention.id)}">${text}</span>`);
    } else if (mention.kind === 'person' && mention.person_id) {
      const person = people[mention.person_id];
      const number = Number(/^c-shiji-(\d{3})-/.exec(paragraph.id || '')?.[1]);
      const params = context?.work_id && context.work_id !== 'w-shiji'
        ? new URLSearchParams({work:context.work_id,book:context.book_id,chapter:context.chapter_id,passage:paragraph.id})
        : number ? new URLSearchParams({chapter:String(number),passage:paragraph.id}) : null;
      if(params && context?.work_id && context.work_id !== 'w-shiji')params.set('mention',mention.id);
      const href = 'person.html' + (params ? '?'+params : '') + '#' + encodeURIComponent(mention.person_id);
      fragments.push(`<a id="${h(mention.id)}" class="cbr-person-link" data-person-id="${h(mention.person_id)}"${typeof mention.interpretation_note === 'string' && mention.interpretation_note.trim() ? ` data-person-reading-note="${h(mention.interpretation_note)}"` : ''} href="${h(href)}" title="${h(person?.label || mention.surface)}">${text}</a>`);
      for (const route of mention.editorial_biographies || []) {
        const href = sourcePassageURL(route.target);
        if (href && typeof route.label === 'string') {
          biographyLinks.push(`<li><a href="${h(href)}">${text} · ${h(route.label)}</a></li>`);
        }
      }
    } else if (mention.kind === 'work' && mention.work_id && mention.person_id == null) {
      fragments.push(workMentionHTML(mention, workTitles));
    } else if (mention.kind === 'non_person' && mention.person_id == null) {
      fragments.push(`<span id="${h(mention.id)}" class="cbr-non-person" data-lexical-role="${h(mention.lexical_role)}" title="${h(mention.interpretation_note)}">${text}</span>`);
    } else fragments.push(`<span id="${h(mention.id)}" class="unresolved-mention" title="${h(mention.interpretation_note || '未定指稱')}">${text}</span>`);
    end = mention.end;
  }
  fragments.push(h(chars.slice(end).join('')));
  const biographies = biographyLinks.length
    ? `<aside class="cross-chapter-references" data-editorial-biographies><small>另見本傳（編者連結）</small><ul>${biographyLinks.join('')}</ul></aside>`
    : '';
  return layerParagraph(paragraph,`<p id="${h(paragraph.id)}" data-source-text>${fragments.join('')}</p>`,extraHTML + biographies);
}
export function filteredChapters(index, category, query = '') {
  const term = query.trim();
  return index.chapters.filter(c => (!category || category === 'all' || c.category === category)
    && (!term || c.title.includes(term) || String(c.number) === term || c.excerpts?.some(e => e.title.includes(term))));
}
