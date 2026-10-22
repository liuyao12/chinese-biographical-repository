import {loadWorkTitles, bindWorkTitles} from './work-titles.js';
import {chapterReadingLayout,revealSourceTarget} from './reading-layout.js';
import {mountHistoricalTable} from './historical-table-view.js';
import {historicalTableMarkup} from './historical-table-markup.js';
import {createLanguageReadingTransition, restoreReadingState} from './corpus-reading-state.js';
import {referentInterpretations} from './referent-interpretations.js';
import {escapeHTML as h} from './core.js';
import {t,ui} from './i18n.js';
import {chapterParagraph,filteredChapters,sourcePassageURL} from './corpus-reader.js';
import {safeSourceURL} from './historical-tables.js';
import {bindPersonCards} from './cbr-person.js';

const $=id=>document.getElementById(id);
let manifest,work,index,selected,ticket=0,removeCards,tableView,workTitles={},removeWorkTitles;
const cache=new Map();
const languageReading = createLanguageReadingTransition(()=>$('corpus-content'),()=>({ticket,hash:location.hash}));
const catalogPath=path=>/^data\/corpus\/[a-z0-9-]+\/index\.json$/.test(path);
const chapterPath=path=>/^data\/corpus\/[a-z0-9-]+\/[a-zA-Z0-9_-]+\.json$/.test(path);
async function json(path) {
  if (!cache.has(path)) {
    const response=await fetch(path);
    if(!response.ok) throw Error(t('Source text could not be loaded.'));
    cache.set(path,await response.json());
  }
  return cache.get(path);
}
function list() {
  $('corpus-work-title').textContent=work?.title || t('Choose a work');
  $('corpus-work-list').innerHTML=manifest.works.map(w=>`<a href="${h(w.reader_kind==='shiji'?'shiji.html':'reader.html#'+new URLSearchParams({work:w.id}))}" aria-current="${w.id===work?.id?'page':'false'}">${h(w.title)}</a>`).join('');
  const entries=index?filteredChapters(index,'all',$('chapter-search').value):[];
  $('chapter-count').textContent=t('{count} chapters',{count:entries.length});
  $('chapter-list').innerHTML=entries.map(e=>`<a class="chapter-entry" href="${h(sourcePassageURL(e))}" aria-current="${e.chapter_id===selected?.chapter_id?'page':'false'}"><span class="chapter-number">${h(e.book_title)}</span><span>${h(e.title)}</span>${['partial_chapter','partial_table'].includes(e.text_scope)?`<small>${ui('Partial chapter')}</small>`:''}</a>`).join('');
}
const external=(url,label)=>safeSourceURL(url)?`<a href="${h(safeSourceURL(url))}" rel="noopener" target="_blank">${ui(label)} ↗</a>`:'';
async function render(keepScroll=false) {
  const current=++ticket,params=new URLSearchParams(location.hash.slice(1));
  const readingState=languageReading.start(keepScroll && $('corpus-content').querySelector('article.corpus-text')?.dataset.chapterId===params.get('chapter'),current);
  removeWorkTitles?.(); removeWorkTitles=null;
  removeCards?.();removeCards=null;
  tableView?.destroy();tableView=null;
  work=manifest.works.find(w=>w.id===params.get('work')) || (!params.has('work')?manifest.works.find(w=>w.reader_kind==='corpus'):null);
  if (!work || work.reader_kind!=='corpus' || !catalogPath(work.catalog_path)) {
    index=null;selected=null;list();$('corpus-content').innerHTML=`<p>${ui('This source is not available in the imported catalog.')}</p>`;return;
  }
  index=await json(work.catalog_path);
  if(current!==ticket)return;
  selected=index.chapters.find(e=>e.chapter_id===params.get('chapter') && (!params.has('book') || e.book_id===params.get('book')));
  list();
  if (!selected) {
    document.title=work.title+' · 人文';
    $('corpus-content').innerHTML=`<div class="chapter-intro"><h1>${h(work.title)}</h1><p>${ui('Choose an imported chapter.')}</p><p>${ui('Only the listed passages have been imported.')}</p><p>${h(index.policy)}</p></div>`;return;
  }
  if(selected.available==='table') {
    if(!/^[a-z][a-z0-9-]*-\d{3}[a-z]?$/.test(selected.table_id))throw Error(t('Table data could not be loaded.'));
    document.title=work.title+'·'+selected.title+' · 人文';
    $('corpus-content').innerHTML=`<p class="eyebrow">${h(work.title)} · ${h(selected.book_title)}</p><h1>${h(selected.title)}</h1><p class="corpus-note" data-source-scope>${h(selected.scope_note)}</p><p class="corpus-note">${ui('Source text and identity review remain in progress.')}</p><section data-native-table>${historicalTableMarkup}</section>`;
    tableView=mountHistoricalTable($('corpus-content').querySelector('[data-native-table]'),selected.table_id);
    await tableView.ready;
    return;
  }
  if(!chapterPath(selected.path))throw Error(t('Source text could not be loaded.'));
  const chapter=await json(selected.path);
  if(current!==ticket)return;
  if(chapter.id!==selected.chapter_id || chapter.work_id!==work.id || chapter.book_id!==selected.book_id)throw Error(t('Source text could not be loaded.'));
  document.title=work.title+'·'+selected.title+' · 人文';
  const context={work_id:chapter.work_id,book_id:chapter.book_id,chapter_id:chapter.id,reading_layout:!!chapter.reading_layout};
  const layout=chapterReadingLayout(chapter), paragraphHTML=p=>chapterParagraph(p,{},context,workTitles)+referentInterpretations(chapter,p.id);
  const readingHTML=layout.primary.map(paragraphHTML).join('')+layout.archival.map(({entry,paragraph})=>`<details class="corpus-archival-excerpt" data-archival-excerpt><summary>${h(entry.label)}</summary><p class="corpus-note">這是同一固定底本的歷史節引；主文已按原行展開，原錨點與引用保留。</p>${paragraphHTML(paragraph)}</details>`).join('');
  $('corpus-content').innerHTML=`<p class="eyebrow">${h(work.title)} · ${h(selected.book_title)}</p><h1>${h(chapter.title)}</h1><p class="corpus-note" data-source-scope>${h(chapter.source.extent)}</p><p class="corpus-note">${ui('Source text and identity review remain in progress.')}</p><p class="corpus-note">${ui('Names are underlined. Hover, focus or tap to read the person profile and family; follow links to other chapters.')}</p><nav class="chapter-pagination">${external(chapter.source.permalink,'Fixed source version')}<a href="${h(selected.path)}">${ui('Download chapter JSON')}</a></nav><details class="corpus-sources"><summary>${ui('Source & edition')}</summary><p>${h(chapter.source.rights)}</p><p>${h(chapter.source.normalization?.note || '')}</p><p>${h(chapter.source.normalization?.extraction_note || '')}</p><p><code>${h(chapter.id)}</code> · <code>${h(chapter.work_id)}</code> · <code>${h(chapter.book_id)}</code></p></details><article class="corpus-text" data-chapter-id="${h(chapter.id)}">${readingHTML}</article>`;
  removeCards=bindPersonCards($('corpus-content'));
  removeWorkTitles=bindWorkTitles($('corpus-content'));
  const passage=params.get('passage');
  if(readingState)restoreReadingState($('corpus-content'),readingState);
  else if(!revealSourceTarget($('corpus-content'),chapter,params))window.scrollTo(0,0);
  languageReading.finish(current);
}
const fail=error=>{$('corpus-content').innerHTML=`<p role="alert">${h(error.message)}</p>`;};
(async()=>{
  try {
    manifest=await json('data/corpus/works.json');
    workTitles=await loadWorkTitles();
    $('chapter-search').oninput=list;
    window.addEventListener('hashchange',()=>render().catch(fail));
    window.addEventListener('renwen:beforelanguagechange',()=>languageReading.before());
    window.addEventListener('renwen:languagechange',()=>render(true).catch(fail));
    await render();
  } catch(error) {fail(error);}
})();
