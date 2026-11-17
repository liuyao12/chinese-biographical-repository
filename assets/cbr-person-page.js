import {sourceCitation} from './source-caption.js';
import {loadPerson, loadPersonFast, loadFamily, personCard, tableOccurrenceURL} from './cbr-person.js';
import {loadPersonSummary, personSummaryCard} from './person-summary.js';
import {chapterURL, profileSourceContext, sourcePassageURL} from './corpus-reader.js';

let request = 0;
const sourceRef = fetch('deployment.json').then(async response => {
  if (!response.ok) return 'main';
  const deployment = await response.json();
  return /^[a-f0-9]{40}$/.test(deployment.commit) ? deployment.commit : 'main';
}).catch(() => 'main');

function setReturnLink(person, context) {
  const link = document.getElementById('cbr-person-table-back');
  if (!link) return;
  const separator = document.getElementById('cbr-person-table-separator');
  let destination = null;
  const tableId = context.get('table');
  if (tableId) {
    const occurrence = (person.table_occurrences || []).find(item => item.table_id === tableId);
    const href = occurrence && tableOccurrenceURL(occurrence);
    if (href) destination = {href, text: `回到${occurrence.title} →`};
  }

  const chapter = Number(context.get('chapter'));
  if (!destination && Number.isSafeInteger(chapter) && chapter > 0) {
    const occurrence = (person.occurrences || []).find(item => item.number === chapter && item.work_id === 'w-shiji');
    if (occurrence) {
      const passage = context.get('passage');
      const prefix = `c-shiji-${String(chapter).padStart(3, '0')}-`;
      const validPassage = passage?.startsWith(prefix) && /^[a-z0-9-]+:p\d{3}$/.test(passage.slice(prefix.length));
      destination = {
        href: chapterURL(chapter, occurrence.category, validPassage ? passage : occurrence.paragraph_id),
        text: `回到${sourceCitation({...occurrence, work_id: 'w-shiji', work_title: '史記'}, person.source_chapter_directory, person.source_work_titles)} →`
      };
    }
  }

  if (!destination) destination = profileSourceContext(person, context);
  if (!destination && !context.toString()) destination = profileSourceContext(person, new URLSearchParams());
  if (!destination) {
    const principal = [...(person.occurrences || [])].sort((a, b) => (b.count || 0) - (a.count || 0))[0];
    const href = principal && sourcePassageURL(principal);
    if (href) destination = {
      href,
      text: `回到${sourceCitation(principal, person.source_chapter_directory, person.source_work_titles)} →`
    };
  }

  link.href = destination?.href || 'cbr.html';
  link.textContent = destination?.text || '回到人物索引 →';
  link.hidden = !destination || destination.href === 'cbr.html';
  if (separator) separator.hidden = link.hidden;
}

function showUnavailable(root) {
  root.innerHTML = '<h1>無法載入人物資料</h1><p>請確認連結有效，或從人物索引搜尋姓名。</p><a href="cbr.html">開啟人物索引 →</a>';
}

async function render() {
  const ticket = ++request;
  const root = document.getElementById('cbr-profile');
  let summaryShown = false;
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = ''; }
  const context = new URLSearchParams(location.search);
  if (!id) {
    root.innerHTML = '<h1>查閱人物資料</h1><p>請從 CBR 人物索引搜尋姓名，再開啟人物頁。</p><a href="cbr.html">開啟人物索引 →</a>';
    document.title = '人物資料 · 人文';
    return;
  }

  try {
    const summaryPromise = loadPersonSummary(id).catch(() => null);
    const profilePromise = loadPersonFast(id);
    const first = await Promise.race([
      summaryPromise.then(summary => summary ? {kind: 'summary', value: summary} : profilePromise.then(value => ({kind: 'profile', value}))),
      profilePromise.then(value => ({kind: 'profile', value}))
    ]);
    if (ticket !== request) return;
    if (first.kind === 'summary') {
      root.innerHTML = personSummaryCard(first.value, null, false);
      document.title = `${first.value.heading} · 人文`;
      summaryShown = true;
    }

    const fastProfile = first.kind === 'profile' ? first.value : await profilePromise;
    if (ticket !== request) return;
    setReturnLink(fastProfile, context);
    root.innerHTML = personCard(fastProfile, true, 'main', null);
    document.title = `${fastProfile.label} · 人文`;

    const [person, family, ref] = await Promise.all([loadPerson(id), loadFamily(fastProfile), sourceRef]);
    if (ticket !== request) return;
    root.innerHTML = personCard(person, true, ref, family);
    setReturnLink(person, context);
  } catch {
    if (ticket === request) {
      if (summaryShown) root.insertAdjacentHTML('beforeend', '<p role="status">完整來源資料暫時無法載入；可稍後重新整理。</p>');
      else showUnavailable(root);
    }
  }
}

window.addEventListener('hashchange', render);
render();
