import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';

const preferred = 'preferred_received_selection';
const comparison = 'comparison_transcription';

export function readingWitnessBadge(entry) {
  if (![preferred, comparison].includes(entry?.reading_role)) return '';
  const label = entry.reading_role === preferred
    ? ui('Preferred source transcription') : ui('Comparison transcription');
  const edition = typeof entry.edition_label === 'string' && entry.edition_label
    ? h(entry.edition_label) : ui('Base edition not researched');
  return `<span class="reading-witness-badge" data-reading-role="${entry.reading_role}">${label} · ${edition}</span>`;
}

export function readingWitnessNote(entry) {
  const badge = readingWitnessBadge(entry);
  if (!badge) return '';
  const note = entry.reading_role === preferred
    ? ui('Reading preference covers only the recorded selection.')
    : ui('Comparison witness; not selected as the reading base.');
  const reason = entry.reading_role === preferred && typeof entry.reading_preference_note === 'string'
    ? `<details><summary>${ui('Reading selection rationale')}</summary><p>${h(entry.reading_preference_note)}</p></details>` : '';
  return `<section class="reading-witness-info">${badge}<p>${note}</p>${reason}</section>`;
}
