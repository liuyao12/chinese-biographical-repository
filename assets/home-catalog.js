import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {groupWorks, workURL} from './corpus-discovery.js';
import {loadChapterDirectory} from './source-caption.js';

let loading;

async function showCatalog() {
  const [response, directory] = await Promise.all([fetch('data/corpus/works.json'), loadChapterDirectory()]);
  if (!response.ok) throw Error('catalog');
  const {works} = await response.json();
  const groups = groupWorks(works.map(w => ({...w, title:directory[w.id]?.title || w.title})));
  const root = document.getElementById('home-source-catalog');
  const query = document.getElementById('book-query');
  const total = document.getElementById('home-source-total');
  root.innerHTML = groups.map(group => `<section class="home-source-group" id="home-sources-${h(group.key)}">
    <h2>${ui(group.title)}</h2>
    <div class="home-source-grid">${group.works.map(w => `<article class="home-source-card" data-work="${h(w.id)}">
      <h3><a href="${h(workURL(w))}">《${h(w.title)}》</a></h3>
      <p class="home-source-author">${h(w.author || '')}</p>
      <p class="home-source-count"></p>
    </article>`).join('')}</div>
  </section>`).join('');
  const cards = new Map([...root.querySelectorAll('[data-work]')].map(card => [card.dataset.work, card]));
  function filter() {
    const term = query.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const group of groups) {
      let matches = 0;
      for (const work of group.works) {
        const visible = [work.title, work.author].some(value => value?.toLocaleLowerCase().includes(term));
        cards.get(work.id).hidden = !visible;
        if (visible) matches++;
      }
      document.getElementById('home-sources-' + group.key).hidden = !matches;
      count += matches;
    }
    total.innerHTML = count ? ui('{count} source works', {count}) : ui('No matching works. Try another title or author.');
  }
  query.addEventListener('input', filter);
  filter();
  const section = new URLSearchParams(location.search).get('section');
  if (groups.some(group => group.key === section)) {
    document.getElementById('home-sources-' + section).scrollIntoView();
  }
  // Each book can be opened as soon as the manifest is ready.
  await Promise.all(works.map(async work => {
    const label = cards.get(work.id).querySelector('.home-source-count');
    try {
      if (!/^data\/corpus\/(?:[a-z0-9-]+\/)?index\.json$/.test(work.catalog_path)) throw Error('catalog path');
      const response = await fetch(work.catalog_path);
      if (!response.ok) throw Error('work catalog');
      const {chapters} = await response.json();
      label.innerHTML = chapters.length ? ui('{count} reading units', {count:chapters.length}) : ui('Source text not yet imported');
    } catch {
      label.innerHTML = ui('Browse volume directory →');
    }
  }));
}

export function loadHomeCatalog() {
  loading ??= showCatalog().catch(() => {
    document.getElementById('home-source-catalog').innerHTML =
      `<p role="status">${ui('The index could not be loaded. Please reload.')}</p><a href="reader.html">${ui('Read source texts')}</a>`;
    loading = null;
  });
  return loading;
}
