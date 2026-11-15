import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';

// Cards have their own small projection. A failed request must never silently
// download the full evidence bundle or the relatives' full profiles.
export function createSummaryLoader(fetchSummary = (...args) => fetch(...args)) {
  const cache = new Map();
  return function loadSummary(id) {
    if (!cache.has(id)) cache.set(id, Promise.resolve().then(() =>
      fetchSummary('data/corpus/summaries/' + encodeURIComponent(id) + '.json'))
      .then(async response => {
        if (!response.ok) throw Error('人物摘要尚未載入');
        const summary = await response.json();
        if (summary.schema_version !== 1 || summary.id !== id || typeof summary.heading !== 'string')
          throw Error('人物摘要格式不符');
        return summary;
      }).catch(error => {cache.delete(id); throw error;}));
    return cache.get(id);
  };
}
export const loadPersonSummary = createSummaryLoader();
const personURL = id => 'person.html#' + encodeURIComponent(id);
const choiceLabels = {preferred:'Provisional preferred date', alternative:'Source alternative date', unresolved:'Date choice unresolved'};

export function personSummaryCard(p, mention = null) {
  const rows = [];
  for (const [label, events] of [['Birth', p.life?.birth], ['Death', p.life?.death]]) {
    const dates = (events || []).filter(event => event.year_label || event.source_date);
    if (dates.length) rows.push(`<dt>${ui(label)}</dt><dd>${dates.map(event =>
      `<div>${[event.year_label, event.source_date].filter(Boolean).map(h).join(' · ')}${choiceLabels[event.choice] ? ` <small>${ui(choiceLabels[event.choice])}</small>` : ''}</div>`).join('')}</dd>`);
  }
  if (p.life?.ages?.length) rows.push(`<dt>${ui('Age')}</dt><dd>${p.life.ages.map(age => `<div>${h(age.label)}${age.approximate ? ` <small>（${ui('Source age approximation')}）</small>` : ''}${[age.source_date, age.year_label].filter(Boolean).length ? ` <small>· ${[age.source_date, age.year_label].filter(Boolean).map(h).join(' · ')}</small>` : ''}</div>`).join('')}</dd>`);
  const entryHTML = entry => `<a href="${h(personURL(entry.id))}">${h(entry.label)}</a>${entry.role === 'assembly_inferred' || entry.route_qualification?.includes('assembly_inferred') ? ` <small>${ui('Provisional paternal connection')}</small>` : ''}${entry.role === 'legal_or_dynastic' ? ` <small>${ui('Legal or dynastic relationship')}</small>` : ''}${entry.marriage_status === 'source_attested_divorce' ? ` <small>${ui('Divorced (source-attested)')}</small>` : ''}${entry.cycle || entry.ancestry_cycle ? ` <small>${ui('Ancestry cycle; tracing stopped')}</small>` : ''}${entry.unavailable || entry.ancestry_unavailable ? ` <small>${ui('Person unavailable')}</small>` : ''}`;
  const family = p.family || {};
  const familyRows = [
    ...(['Father','Grandfather','Great-grandfather'].map((label, index) => [label, family.ancestors?.[index]])),
    ['Birth mother', family.mother], ['Adoptive father (source-attested chuji)', family.adoptive_father],
    ['Spouses', family.spouses], ['Children', family.children],
    [family.family_namespace?.namespace_kind === 'explicit_received_brothers_parent_unidentified' ? 'Source-attested brothers (parent unidentified)' : 'Collateral family branches', family.family_namespace?.roots],
    ['Adopted children (source-attested chuji)', family.adopted_children],
  ].filter(([, entries]) => entries?.length).map(([label, entries]) => `<dt>${ui(label)}</dt><dd>${entries.map(entryHTML).join('、')}${entries.length > 1 && ['Father','Grandfather','Great-grandfather','Birth mother'].includes(label) ? ` <small>${ui('Multiple accounts; unresolved')}</small>` : ''}</dd>`).join('');
  const aliasLabels = {zi:'Courtesy name',hao:'Art name',xiaozhi:'Childhood name',xiaoming:'Childhood name (xiaoming)',former_ming:'Former given name'};
  const reading = typeof mention?.interpretation_note === 'string' && mention.interpretation_note.trim()
    ? `<p class="person-mention-reading"><small>${ui('Identification of “{name}” here', {name:mention.surface || ''})}：${h(mention.interpretation_note)}</small></p>` : '';
  return `<article class="cbr-profile person-summary"><h3>${h(p.heading)}</h3>${reading}${p.jiguan?.length ? `<p class="person-summary-jiguan">${ui('Native place')}：${p.jiguan.map(h).join('、')}</p>` : ''}${p.aliases?.length ? `<p class="person-aliases">${p.aliases.map(alias => `<span><small>${aliasLabels[alias.kind] ? ui(aliasLabels[alias.kind]) + ' ' : ''}${h(alias.value)}</small></span>`).join(' ')}</p>` : ''}${p.historicity === 'legendary_tradition' ? `<p>${ui('Legendary narrative figure')}</p>` : ''}${rows.length ? `<section class="person-life-summary"><dl>${rows.join('')}</dl></section>` : ''}${familyRows ? `<section class="person-family"><dl>${familyRows}</dl></section>` : ''}${family.unresolved_spouse_groups?.length ? `<p class="note">${ui('Spouse identity unresolved')}</p>` : ''}${family.child_order_conflicts?.length ? `<p class="note">${ui('Sibling age order has conflicting accounts; no order is preferred.')}</p>` : ''}${(p.qualifications || []).map(note => `<p class="note">${h(note)}</p>`).join('')}<a class="person-profile-button" href="${h(personURL(p.id))}">${ui('Read full profile')}</a></article>`;
}
