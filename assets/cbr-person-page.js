import {sourceCitation} from './source-caption.js';
import {loadPerson, loadFamily, personCard, tableOccurrenceURL} from './cbr-person.js';
import {chapterURL,profileSourceContext} from './corpus-reader.js';
import {escapeHTML} from './core.js';

let request = 0;
const sourceRef = fetch('deployment.json').then(async r => {
  if (!r.ok) return 'main';
  const d = await r.json();
  return /^[a-f0-9]{40}$/.test(d.commit) ? d.commit : 'main';
}).catch(() => 'main');

function setReturnLink(person) {
  const back = document.getElementById('cbr-person-table-back');
  if (!back) return;
  const context = new URLSearchParams(location.search);
  const tableId = context.get('table');
  const occurrence = tableId && (person.table_occurrences || []).find(x => x.table_id === tableId);
  if (occurrence) {
    const href = tableOccurrenceURL({...occurrence, cell_id:context.get('cell') || undefined,
      axis:context.get('axis') || undefined});
    if (href) {
      back.href = href;
      back.textContent = '回到' + occurrence.title + ' →';
      return;
    }
  }

  const workId = context.get('work');
  if (!workId || workId === 'w-shiji') {
    const chapter = Number(context.get('chapter'));
    const shijiOccurrence = (person.occurrences || []).find(x => x.number === chapter);
    if (shijiOccurrence && chapter > 0) {
      const passage = context.get('passage');
      const prefix = 'c-shiji-' + String(chapter).padStart(3, '0') + '-';
      const validPassage = passage?.startsWith(prefix) && /^[a-z0-9-]+:p\d{3}$/.test(passage.slice(prefix.length));
      back.href = chapterURL(chapter, shijiOccurrence.category, validPassage ? passage : shijiOccurrence.paragraph_id);
      back.textContent = '回到' + sourceCitation({...shijiOccurrence, work_id:'w-shiji', work_title:'史記'}, person.source_chapter_directory, person.source_work_titles) + ' →';
      return;
    }
  }

  const otherSource = profileSourceContext(person, context);
  if (otherSource) {
    back.href = otherSource.href;
    back.textContent = otherSource.text;
    return;
  }

  back.href = 'cbr.html';
  back.textContent = '返回 CBR 人物目錄 →';
}

async function render() {
  const ticket = ++request;
  const root = document.getElementById('cbr-profile');
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = ''; }
  if (!id) {
    root.innerHTML = '<h1>請指定一位人物</h1><p>人物資料依據原文提及與來源連結；可從文獻的人名標記，或 <a href="cbr.html">CBR 人物目錄</a> 開啟。</p>';
    document.title = '人物資料 · 人文';
    return;
  }

  try {
    const response = await fetch('data/corpus/profiles/' + encodeURIComponent(id) + '.json');
    if (!response.ok) throw Error('人物資料尚未載入');
    const preview = await response.json();
    if (preview.id !== id) throw Error('人物資料 ID 不符');
    if (ticket !== request) return;
    setReturnLink(preview);
    root.innerHTML = personCard(preview, true, 'main', null)
      + '<p class="person-family-loading" role="status">正在載入家族關係…</p>';
    document.title = preview.label + ' · 人文';

    const [p, ref, familyResult] = await Promise.all([
      loadPerson(id, preview).catch(() => preview),
      sourceRef,
      loadFamily(preview).then(family => ({family}), error => ({error}))
    ]);
    if (ticket !== request) return;
    const family = familyResult.family || null;
    const scrollY = window.scrollY;
    const focusId = document.activeElement?.id;
    root.innerHTML = personCard(p, true, ref, family)
      + (familyResult.error ? '<p class="person-family-loading" role="status">家族資料暫時無法載入；人物及來源資料仍可閱讀。</p>' : '');
    if (focusId) document.getElementById(focusId)?.focus({preventScroll:true});
    window.scrollTo({top:scrollY, behavior:'auto'});
  } catch (error) {
    if (ticket === request) {
      root.innerHTML = '<h1>人物資料無法載入</h1><p role="alert">' + escapeHTML(error?.message || '載入失敗') + '</p><p>可返回 <a href="cbr.html">CBR 人物目錄</a>，再從來源中的人名進入。</p>';
      document.title = '人物資料 · 人文';
    }
  }
}

window.addEventListener('hashchange', render);
render();
