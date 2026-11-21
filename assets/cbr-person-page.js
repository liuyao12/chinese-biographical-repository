import {loadPerson, loadFamily, personCard} from './cbr-person.js';
import {profileReturnLink} from './profile-return.js';
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
  const route = profileReturnLink(person, new URLSearchParams(location.search));
  back.href = route.href;
  back.textContent = route.text;
}

function disclosures(root) {
  const occurrences = new Map();
  return Array.from(root.querySelectorAll('details'), detail => {
    const section = detail.closest('section');
    const signature = JSON.stringify([
      section?.querySelector(':scope > h4')?.textContent,
      detail.querySelector(':scope > summary')?.textContent,
      detail.querySelector('a[href]')?.getAttribute('href'),
      detail.querySelector('blockquote')?.textContent
    ]);
    const occurrence = (occurrences.get(signature) || 0) + 1;
    occurrences.set(signature, occurrence);
    return [signature + ':' + occurrence, detail];
  });
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
    const openDisclosures = new Set(disclosures(root).filter(([, detail]) => detail.open).map(([key]) => key));
    root.innerHTML = personCard(p, true, ref, family)
      + (familyResult.error ? '<p class="person-family-loading" role="status">家族資料暫時無法載入；人物及來源資料仍可閱讀。</p>' : '');
    for (const [key, detail] of disclosures(root)) {
      if (openDisclosures.has(key)) detail.open = true;
    }
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
