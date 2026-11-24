import {ui} from './i18n.js';

let installed = false;
export function loadHomeCatalog() {
  if (installed) return;
  installed = true;
  const root = document.getElementById('home-source-catalog');
  const query = document.getElementById('book-query');
  const total = document.getElementById('home-source-total');
  const groups = [...root.querySelectorAll('.home-source-group')].map(section => ({
    section,
    cards: [...section.querySelectorAll('[data-work]')].map(card => ({
      card,
      terms: [card.querySelector('h3').textContent, card.querySelector('.home-source-author').textContent]
        .map(value => value.toLocaleLowerCase())
    }))
  }));
  function filter() {
    const term = query.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const {section, cards} of groups) {
      let matches = 0;
      for (const {card, terms} of cards) {
        card.hidden = !terms.some(value => value.includes(term));
        if (!card.hidden) matches++;
      }
      section.hidden = !matches;
      count += matches;
    }
    total.innerHTML = count ? ui('{count} source works', {count}) : ui('No matching works. Try another title or author.');
  }
  query.addEventListener('input', filter);
  filter();
  const section = new URLSearchParams(location.search).get('section');
  if (section) document.getElementById('home-sources-' + section)?.scrollIntoView();
}
