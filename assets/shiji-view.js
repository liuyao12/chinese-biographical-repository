import {setReadingDirectory} from './reading-directory.js';
import {revealSourceTarget} from './reading-layout.js';
import {commentaryControls,bindCommentaryControls} from './commentary-layers.js';
import {loadWorkTitles, bindWorkTitles} from './work-titles.js';
import {createLanguageReadingTransition, restoreReadingState} from './corpus-reading-state.js';
import {referentInterpretations} from './referent-interpretations.js';
import {escapeHTML as h} from './core.js';
import {t, ui} from './i18n.js';
import {chapterURL, chapterParagraph, filteredChapters, shijiReadingEntry} from './corpus-reader.js';
import {safeSourceURL} from './historical-tables.js';
import {mountHistoricalTable} from './historical-table-view.js';
import {bindPersonCards} from './cbr-person.js';
import {historicalTableMarkup} from './historical-table-markup.js';
const $ = id => document.getElementById(id);
let index, people, selected, category = 'all', ticket = 0;
const cache = new Map();
const languageReading = createLanguageReadingTransition(()=>$('corpus-content'),()=>({ticket,hash:location.hash}));
const commentaryState=new Map();let commentaryController;
let tableReader, removeTextPersonCards, workTitles={}, removeWorkTitles;
const labels = {marked_text: 'Annotated text', excerpt: 'Partial chapter', table: 'Continuous table', pending: 'Not yet imported'};
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
  const number = Number(params.get('chapter')), volume = index.chapters.find(e => e.number === number);
  const entry = shijiReadingEntry(volume, params);
  const readingState = languageReading.start(keepReadingState && selected?.number === number && selected?.path === entry?.path,current);
  commentaryController?.destroy();commentaryController=null;
  removeWorkTitles?.(); removeWorkTitles=null;
  removeTextPersonCards?.(); removeTextPersonCards = null;
  tableReader?.destroy(); tableReader = null;
  selected = entry;
  if (!keepReadingState) setReadingDirectory(Boolean(entry));
  list();
  $('person-preview').hidden = true;
  const tablesLink = document.querySelector('.public-nav a[href="shiji.html#category=biao"]');
  const booksLink = document.querySelector('.public-nav a[href="./?section=sources"]');
  const inTables = (entry?.category || category) === 'biao';
  tablesLink.setAttribute('aria-current', inTables ? 'page' : 'false');
  booksLink.setAttribute('aria-current', inTables ? 'false' : 'page');
  if (!entry) {
    document.title = '史記 · 人文';
    const tables = category === 'biao';
    const title = tables ? t('Read a table') : category === 'all' ? t('Choose a chapter') : index.categories.find(c => c.id === category).label;
    const links = tables
      ? `<nav class="table-directory" aria-label="${h(title)}">${index.chapters.filter(c => c.category === 'biao').map(c =>
          `<a href="${h(chapterURL(c.number, 'biao'))}">${h(c.title)}</a>`).join('')}</nav>`
      : `<p><a href="${chapterURL(6, 'benji')}">${ui('Read the Qin Shihuang chapter')} →</a></p>`;
    $('corpus-content').innerHTML = `<div class="chapter-intro"><p class="eyebrow">史記</p><h1>${h(title)}</h1>
      <p>${ui(tables ? 'Open a table to follow a year or inspect the original cells.' : 'Choose a chapter from the categorized contents to read the received text and its linked people.')}</p>
      ${links}<p>${ext(index.contents_source.revision_url, 'Contents source')}</p></div>
      ${tables ? `<aside class="related-table"><h2>${ui('Tables in other histories')}</h2>
        <a href="reader.html#work=w-hanshu&amp;book=b-hanshu-016&amp;chapter=table-chapter-hanshu-016">《漢書·髙惠髙后文功臣表》曲成列</a></aside>` : ''}`;
    return;
  }
  document.title = entry.title + ' · 人文';
  const excerpts = volume.excerpts || [];
  const inExcerpt = excerpts.find(row => row.chapter_id === entry.chapter_id);
  const choices = excerpts.some(row => row.chapter_id === volume.chapter_id) ? excerpts : [volume, ...excerpts];
  const links = choices.length > 1 ? '<nav class="chapter-pagination">' + choices.map(row =>
    `<a href="${h(chapterURL(number,category,'',row === volume ? '' : row.chapter_id))}" aria-current="${row.chapter_id === entry.chapter_id}">${h(row.title)}</a>`).join(' ') + '</nav>' : '';
  const heading = navigation(entry) + `<p class="eyebrow">史記 · ${h(entry.category_label)} · ${entry.number}</p><h1>${h(volume.title)}</h1>`
    + links + (inExcerpt ? `<h2>${h(inExcerpt.title)}</h2><p data-original>${h(inExcerpt.scope_note)}</p>` : '');
  if (entry.available !== 'marked_text') {
    $('corpus-content').innerHTML = heading + (entry.available === 'table' ? `<div id="chapter-table-reader">${historicalTableMarkup}</div>` : `<p>${ui('This chapter has not been imported. The source text is available externally.')}</p><p>${ext('https://zh.wikisource.org/wiki/史記/卷' + String(entry.number).padStart(3, '0'), 'Read source text')}</p>`);
    if (entry.available === 'table') {
      tableReader = mountHistoricalTable($('chapter-table-reader'), entry.table_id);
      await tableReader.ready;
    }
    return;
  }
  $('corpus-content').innerHTML = heading + `<p role="status">${ui('Loading sources…')}</p>`;
  if (!cache.has(entry.path)) {
    const response = await fetch(entry.path);
    if (!response.ok) throw new Error(t('Source text could not be loaded.'));
    cache.set(entry.path, await response.json());
  }
  if (!people) {
    const response = await fetch('data/corpus/persons.json');
    if (!response.ok) throw new Error(t('Person index could not be loaded.'));
    people = await response.json();
  }
  if (current !== ticket) return;
  const chapter = cache.get(entry.path); selected = {...entry, chapter};
  $('corpus-content').innerHTML = heading + `<p class="corpus-note">${ui('Select an underlined name to see its profile and sources.')}</p><div class="reading-source-links"><p class="witness-link">${ext(chapter.source.permalink, 'Fixed source version')}</p><details class="corpus-sources"><summary>${ui('Source & edition')}</summary><p class="corpus-note">${ui('Annotation in progress · no independently reviewed edition claimed')}</p><nav class="chapter-pagination"><a href="${h(entry.path)}">${ui('Download chapter JSON')}</a></nav><p data-original>${h(chapter.source.extent)}</p><p data-original>${h(chapter.source.rights)}</p><p data-original>${h(chapter.source.normalization?.note || '')}</p><p><code>${h(chapter.id)}</code> · <code>${h(chapter.work_id)}</code> · <code>${h(chapter.book_id)}</code></p></details></div>${commentaryControls(chapter)}<article class="corpus-text" data-chapter-id="${h(chapter.id)}">${chapter.paragraphs.map(p => chapterParagraph(p, people, null, workTitles, referentInterpretations(chapter, p.id, people))).join('')}</article>${navigation(entry)}`;
  removeTextPersonCards = bindPersonCards($('corpus-content'));
  removeWorkTitles=bindWorkTitles($('corpus-content'));
  commentaryController=bindCommentaryControls($('corpus-content'),chapter,commentaryState);
  if(!readingState)commentaryController.reveal(params);
  const passage = params.get('passage');
  if (readingState) restoreReadingState($('corpus-content'), readingState);
  else if (revealSourceTarget($('corpus-content'),chapter,params)) { /* Exact source anchor revealed. */ }
  else window.scrollTo(0, 0);
  languageReading.finish(current);
}
function fail(error) { $('corpus-content').innerHTML = `<p role="alert">${h(error.message)}</p>`; }
(async () => {
  try {
    const response = await fetch('data/corpus/index.json');
    if (!response.ok) throw new Error(t('Source text could not be loaded.'));
    index = await response.json();
    workTitles=await loadWorkTitles();
    $('chapter-search').oninput = list;
    window.addEventListener('hashchange', () => {
      const p = new URLSearchParams(location.hash.slice(1));
      if (tableReader && Number(p.get('chapter')) === selected?.number && (p.get('category') || 'all') === category
          && shijiReadingEntry(index.chapters.find(e => e.number === selected.number), p)?.available === 'table') return;
      render().catch(fail);
    });
    window.addEventListener('renwen:beforelanguagechange',()=>languageReading.before());
    window.addEventListener('renwen:languagechange', () => render(true).catch(fail));
    await render();
  } catch (error) { fail(error); }
})();
