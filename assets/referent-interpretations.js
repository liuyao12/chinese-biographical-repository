import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {safeSourceURL} from './historical-tables.js';
import {sourcePassageURL} from './corpus-reader.js';
const kinds = {
  mythical_creature: 'Mythical creature reading',
  historical_person: 'Person reading', legendary_person: 'Legendary or divine reading',
  unspecified_person: 'Unspecified person reading', generic_group: 'Generic group reading',
  multiple_allusions: 'Multiple allusions reading', divinity: 'Divine referent', natural_phenomenon: 'Natural phenomenon'
};
export function referentInterpretations(chapter, paragraphID, people = {}) {
  const cases = (chapter.annotation?.referent_interpretations || []).filter(c => c.paragraph_id === paragraphID);
  return referentCasesHTML(cases, people);
}
export function referentCasesHTML(cases = [], people = {}) {
  if (!cases.length) return '';
  return `<aside class="referent-interpretations"><details><summary>${ui('Referent interpretations')}</summary>${cases.map(c => {
    const refs = new Map((c.references || []).map(r => [r.id, r]));
    const surfaces = c.source_terms || [];
    const passage = sourcePassageURL(c.evidence || {});
    return `<section data-interpretation-id="${h(c.id)}" data-referent-status="${h(c.status)}"><h4>${h(surfaces.join('、'))}</h4><p>${ui(c.status === 'editorial_provisional' ? 'Provisional referent reading; no individual identity is assigned.' : 'Unresolved: alternatives are not accepted identities.')}</p><ol>${c.alternatives.map(a => `<li data-reading-id="${h(a.id)}">${c.default_alternative_id === a.id ? `<span class="referent-preferred">${ui('Preferred reading (provisional)')}</span> ` : ''}<strong data-original>${h(a.attribution)}</strong> · ${ui(kinds[a.referent_kind] || 'Unresolved reading')}<p data-original>${h(a.interpretation)}</p>${(a.candidate_person_ids || []).map(id => `<p>${ui('Possible referent')}: <a class="candidate-profile" href="person.html#${h(encodeURIComponent(id))}">${h(people[id]?.label || id)}</a></p>`).join('')}${(a.source_reference_ids || []).map(id => {
      const r = refs.get(id); if (!r) return '';
      const url = safeSourceURL(r.url);
      return `<details><summary>${ui('Source evidence')}</summary><blockquote data-original>${h(r.quote)}</blockquote>${url ? `<a href="${h(url)}" rel="noopener" target="_blank">${ui('Ancient commentary')} ↗</a>` : ''}</details>`;
    }).join('')}</li>`).join('')}</ol><p data-original>${h(c.note)}</p>${c.selection?.rationale ? `<p data-original>${h(c.selection.rationale)}</p>` : ''}${passage ? `<details><summary>${ui('Received-text evidence')}</summary><blockquote data-original>${h(c.evidence.quote)}</blockquote><a href="${h(passage)}">${ui('Read source passage')} →</a></details>` : ''}</section>`;
  }).join('')}</details></aside>`;
}
