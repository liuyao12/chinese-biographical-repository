import {captureReadingState, restoreReadingState} from './corpus-reading-state.js';
import {referentInterpretations} from './referent-interpretations.js';
import {escapeHTML as h} from './core.js';
import {t, ui} from './i18n.js';
import {chapterURL, chapterParagraph, filteredChapters} from './corpus-reader.js';
import {safeSourceURL} from './historical-tables.js';
import {mountHistoricalTable} from './historical-table-view.js';
import {bindPersonCards} from './cbr-person.js';
import {historicalTableMarkup} from './historical-table-markup.js';
const $ = id => document.getElementById(id);
let index, people, selected, category = 'all', ticket = 0;
const cache = new Map();
let tableReader, removeTextPersonCards;
const labels = {marked_text: 'Annotated text', table: 'Continuous table', pending: 'Not yet imported'};
const ext = (url, label) => safeSourceURL(url) ? `<a href="${h(safeSourceURL(url))}" rel="noopener" target="_blank">${ui(label)} ↗</a>` : '';
function list() {
  const entries = filteredChapters(index, category, $('chapter-search').value);
  $('shiji-categories').innerHTML = [{id: 'all', label: t('All chapters')}, ...index.categories].map(c => `<a href="#category=${c.id}" aria-current="${category === c.id}">${h(c.label)}</a>`).join('');
  $('chapter-count').textContent = t('{count} chapters', {count: entries.length});
  $('chapter-list').innerHTML = index.categories.map(c => {
    const group = entries.filter(e => e.category === c.id);
    return group.length ? `<section class="chapter-group"><h2>${h(c.label)} <small>${group.length}</small></h2>${group.map(e => `<a class="chapter-entry" href="${h(chapterURL(e.number, category))}" aria-current="${selected?.number === e.number ? 'page' : 'false'}"><span class="chapter-number">${String(e.number).padStart(3, '0')}</span><span>${h(e.title)}</span><small>${h(t(labels[e.available]))}</small></a>`).join('')}</section>` : '';
  }).join('') || `<p>${ui('No matching chapters.')}</p>`;
}
function navigation(entry) {
  const prev = index.chapters.find(c => c.number === entry.number - 1), next = index.chapters.find(c => c.number === entry.number + 1);
  return `<nav class="chapter-pagination"><a href="shiji.html#category=${entry.category}">${ui('Back to category')}</a>${prev ? `<a href="${h(chapterURL(prev.number, category))}">← ${h(prev.title)}</a>` : ''}${next ? `<a href="${h(chapterURL(next.number, category))}">${h(next.title)} →</a>` : ''}</nav>`;
}
async function render(keepReadingState = false) {
  const current = ++ticket, params = new URLSearchParams(location.hash.slice(1));
  category = index.categories.some(c => c.id === params.get('category')) ? params.get('category') : 'all';
  const number = Number(params.get('chapter')), entry = index.chapters.find(e => e.number === number);
  const readingState = keepReadingState && selected?.number === number && selected?.chapter
    ? captureReadingState($('corpus-content')) : null;
  removeTextPersonCards?.(); removeTextPersonCards = null;
  tableReader?.destroy(); tableReader = null;
  selected = entry;
  list();
  $('person-preview').hidden = true;
  if (!entry) {
    document.title = '史記 · 人文';
    $('corpus-content').innerHTML = `<div class="chapter-intro"><p class="eyebrow">史記 · 130 篇</p><h1>${h(category === 'all' ? t('Choose a chapter') : index.categories.find(c => c.id === category).label)}</h1><p>${ui('Choose a chapter from the categorized contents to read the received text and its linked people.')}</p><p>${ui('Imported texts remain under annotation review. Missing chapters are listed without invented text.')}</p><p><a href="${chapterURL(6, 'benji')}">${ui('Read the Qin Shihuang chapter')} →</a></p><p><a href="shiji.html#category=biao">${ui('Continuous historical tables')} →</a></p><p>${ext(index.contents_source.revision_url, 'Contents source')}</p></div>`;
    return;
  }
  document.title = entry.title + ' · 人文';
  const heading = navigation(entry) + `<p class="eyebrow">史記 · ${h(entry.category_label)} · ${entry.number}</p><h1>${h(entry.title)}</h1>`;
  if (entry.available !== 'marked_text') {
    $('corpus-content').innerHTML = heading + (entry.available === 'table' ? `<div id="chapter-table-reader">${historicalTableMarkup}</div>` : `<p>${ui('This chapter has not been imported. The source text is available externally.')}</p><p>${ext('https://zh.wikisource.org/wiki/史記/卷' + String(entry.number).padStart(3, '0'), 'Read source text')}</p>`);
    if (entry.available === 'table') {
      tableReader = mountHistoricalTable($('chapter-table-reader'), entry.table_id);
      await tableReader.ready;
    }
    return;
  }
  $('corpus-content').innerHTML = heading + `<p role="status">${ui('Loading sources…')}</p>`;
  if (!cache.has(number)) {
    const response = await fetch(entry.path);
    if (!response.ok) throw new Error(t('Source text could not be loaded.'));
    cache.set(number, await response.json());
  }
  if (!people) {
    const response = await fetch('data/corpus/persons.json');
    if (!response.ok) throw new Error(t('Person index could not be loaded.'));
    people = await response.json();
  }
  if (current !== ticket) return;
  const chapter = cache.get(number); selected = {...entry, chapter};
  $('corpus-content').innerHTML = heading + `<p class="corpus-note">${ui('Names are underlined. Hover, focus or tap to read the person profile and family; follow links to other chapters.')}</p><p class="corpus-note">${ui('Annotation in progress · no independently reviewed edition claimed')}</p><nav class="chapter-pagination">${ext(chapter.source.permalink, 'Fixed source version')}<a href="${h(entry.path)}">${ui('Download chapter JSON')}</a></nav><details class="corpus-sources"><summary>${ui('Source & edition')}</summary><p data-original>${h(chapter.source.extent)}</p><p data-original>${h(chapter.source.rights)}</p><p data-original>${h(chapter.source.normalization?.note || '')}</p><p><code>${h(chapter.id)}</code> · <code>${h(chapter.work_id)}</code> · <code>${h(chapter.book_id)}</code></p></details><article class="corpus-text" data-chapter-id="${h(chapter.id)}">${chapter.paragraphs.map(p => chapterParagraph(p, people) + referentInterpretations(chapter, p.id, people)).join('')}</article>${navigation(entry)}`;
  removeTextPersonCards = bindPersonCards($('corpus-content'));
  const passage = params.get('passage');
  if (readingState) restoreReadingState($('corpus-content'), readingState);
  else if (passage && chapter.paragraphs.some(p => p.id === passage)) document.getElementById(passage).scrollIntoView();
  else window.scrollTo(0, 0);
}
function fail(error) { $('corpus-content').innerHTML = `<p role="alert">${h(error.message)}</p>`; }
(async () => {
  try {
    const response = await fetch('data/corpus/index.json');
    if (!response.ok) throw new Error(t('Source text could not be loaded.'));
    index = await response.json();
    $('chapter-search').oninput = list;
    window.addEventListener('hashchange', () => {
      const p = new URLSearchParams(location.hash.slice(1));
      if (tableReader && Number(p.get('chapter')) === selected?.number && (p.get('category') || 'all') === category) return;
      render().catch(fail);
    });
    window.addEventListener('renwen:languagechange', () => render(true).catch(fail));
    await render();
  } catch (error) { fail(error); }
})();
