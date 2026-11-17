import {sourceCitation} from './source-caption.js';
import {loadPerson, loadFamily, personCard, tableOccurrenceURL} from './cbr-person.js';
import {chapterURL, profileSourceContext, sourcePassageURL} from './corpus-reader.js';
import {loadPersonSummary, personSummaryCard} from './person-summary.js';

let request = 0;
const sourceRef = fetch('deployment.json').then(async response => {
  if (!response.ok) return 'main';
  const deployment = await response.json();
  return /^[a-f0-9]{40}$/.test(deployment.commit) ? deployment.commit : 'main';
}).catch(() => 'main');

function sourceReturn(person, params) {
  const tableId = params.get('table');
  if (tableId) {
    const table = (person.table_occurrences || []).find(item => item.table_id === tableId);
    const href = table && tableOccurrenceURL(table);
    if (href) return {href, text: `回到${table.title} →`};
  }

  const chapter = Number(params.get('chapter'));
  const shijiOccurrence = (person.occurrences || []).find(item => item.work_id === 'w-shiji'
    && item.number === chapter);
  if (shijiOccurrence) {
    const passage = params.get('passage');
    const prefix = `c-shiji-${String(chapter).padStart(3, '0')}-`;
    const validPassage = passage?.startsWith(prefix) && /^[a-z0-9-]+:p\d{3}$/.test(passage.slice(prefix.length));
    return {
      href: chapterURL(chapter, shijiOccurrence.category, validPassage ? passage : shijiOccurrence.paragraph_id),
      text: `回到${sourceCitation({...shijiOccurrence, work_id:'w-shiji', work_title:'史記'}, person.source_chapter_directory, person.source_work_titles)} →`
    };
  }

  const contextualSource = profileSourceContext(person, params);
  if (contextualSource) return contextualSource;

  // Directly opened profiles return to their most frequently attested source,
  // regardless of which work contains it. Never assume 《史記》 by default.
  if (!params.toString()) {
    const principal = [...(person.occurrences || [])].sort((a, b) => (b.count || 0) - (a.count || 0))[0];
    if (principal) {
      if (principal.work_id === 'w-shiji') {
        const number = principal.number || Number(/shiji-(\d{3})/.exec(principal.chapter_id || '')?.[1]);
        if (number) return {
          href: chapterURL(number, principal.category, principal.paragraph_id),
          text: `回到${sourceCitation({...principal, work_id:'w-shiji', work_title:'史記'}, person.source_chapter_directory, person.source_work_titles)} →`
        };
      } else {
        const href = sourcePassageURL(principal);
        if (href) return {href, text: `回到${sourceCitation(principal, person.source_chapter_directory, person.source_work_titles)} →`};
      }
    }
  }

  return {href:'cbr.html', text:'回到 CBR 人物目錄 →'};
}

function showReturn(person, params) {
  const back = document.getElementById('cbr-person-table-back');
  const target = sourceReturn(person, params);
  back.href = target.href;
  back.textContent = target.text;
}

async function render() {
  const ticket = ++request;
  const root = document.getElementById('cbr-profile');
  const status = document.getElementById('cbr-profile-status');
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch {}
  if (!id) {
    root.innerHTML = '<p>請從 CBR 人物目錄或文獻中的人物標記進入。</p><p><a href="cbr.html">開啟人物目錄 →</a></p>';
    status.textContent = '';
    document.title = '人物資料 · 人文';
    return;
  }

  root.innerHTML = '<p>正在載入人物摘要…</p>';
  status.textContent = '載入人物摘要…';
  const params = new URLSearchParams(location.search);
  let summary;
  const summaryRequest = loadPersonSummary(id).then(value => {
    summary = value;
    if (ticket !== request) return;
    root.innerHTML = personSummaryCard(value);
    // This is already the requested profile page; avoid a link that reloads it.
    root.querySelector('.person-profile-button')?.remove();
    showReturn(value, params);
    document.title = `${value.heading} · 人文`;
    status.textContent = '人物摘要已載入；正在補載完整來源與家系資料…';
  }).catch(() => {});

  try {
    const personRequest = loadPerson(id);
    await summaryRequest;
    const [person, ref] = await Promise.all([personRequest, sourceRef]);
    if (ticket !== request) return;
    const family = await loadFamily(person);
    if (ticket !== request) return;
    root.innerHTML = personCard(person, true, ref, family);
    showReturn(person, params);
    document.title = `${person.label} · 人文`;
    status.textContent = '';
  } catch {
    if (ticket !== request) return;
    if (summary) {
      status.textContent = '人物摘要已載入；完整來源與家系資料暫時無法取得。';
      showReturn(summary, params);
      return;
    }
    root.innerHTML = '<h1>人物資料尚未載入</h1><p>請由 CBR 人物目錄或文獻中的人物標記進入，或稍後重試。</p><a href="cbr.html">回到 CBR 人物目錄 →</a>';
    status.textContent = '';
  }
}

window.addEventListener('hashchange', render);
render();
