import {readFileSync} from 'node:fs';
import {groupWorks, workURL} from '../assets/corpus-discovery.js';
import {escapeHTML as h} from '../assets/core.js';
import {ui} from '../assets/i18n.js';

function catalogueHTML(works) {
  const groups = groupWorks(works.map(w => ({...w, title:w.display_title || w.title})));
  return groups.map(group => `<section class="home-source-group" id="home-sources-${h(group.key)}">
    <h2>${ui(group.title)}</h2>
    <div class="home-source-grid">${group.works.map(w => `<article class="home-source-card" data-work="${h(w.id)}">
      <h3><a href="${h(workURL(w))}">《${h(w.title)}》</a></h3>
      <p class="home-source-author">${h(w.author || '')}</p>
      <p class="home-source-count">${Number.isInteger(w.reading_unit_count)
        ? (w.reading_unit_count ? ui('{count} reading units', {count:w.reading_unit_count}) : ui('Source text not yet imported'))
        : ui('Browse volume directory →')}</p>
    </article>`).join('')}</div>
  </section>`).join('');
}

const manifest = JSON.parse(readFileSync(0, 'utf8'));
process.stdout.write(catalogueHTML(manifest.works));
