import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {groupWorks, workURL} from './corpus-discovery.js';

let loading;

async function showCatalog() {
  const response = await fetch('data/corpus/works.json');
  if (!response.ok) throw Error('catalog');
  const {works} = await response.json();
  const groups = groupWorks(works.map(w => ({...w, title:w.display_title || w.title})));
  const root = document.getElementById('home-source-catalog');
  const query = document.getElementById('book-query');
  const total = document.getElementById('home-source-total');
  root.innerHTML = groups.map(group => `<section class="home-source-group" id="home-sources-${h(group.key)}">
    <h2>${ui(group.title)}</h2>
    <div class="home-source-grid">${group.works.map(w => `<article class="home-source-card" data-work="${h(w.id)}">
      <h3><a href="${h(workURL(w))}">《${h(w.title)}》</a></h3>
      <p class="home-source-author">${h(w.author || '')}</p>
      <p class="home-source-count">${Number.isInteger(w.reading_unit_count)
        ? (w.reading_unit_count ? ui('{count} reading units', {count:w.reading_unit_count}) : ui('Source text not yet imported'))
        : ui('Browse volume directory →')}</p>
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

}

export function loadHomeCatalog() {
  loading ??= showCatalog().catch(() => {
    document.getElementById('home-source-catalog').innerHTML =
      `<p role="status">${ui('The index could not be loaded. Please reload.')}</p><a href="reader.html">${ui('Read source texts')}</a>`;
    loading = null;
  });
  return loading;
}
