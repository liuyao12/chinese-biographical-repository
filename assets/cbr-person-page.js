import {loadPerson, loadFamily, personCard, tableOccurrenceURL} from './cbr-person.js';
let request = 0;
const sourceRef = fetch('deployment.json').then(async r => {
  if (!r.ok) return 'main';
  const d = await r.json();
  return /^[a-f0-9]{40}$/.test(d.commit) ? d.commit : 'main';
}).catch(() => 'main');
async function render() {const ticket = ++request; const root = document.getElementById('cbr-profile'); try {const id = decodeURIComponent(location.hash.slice(1)); const [p, ref] = await Promise.all([loadPerson(id), sourceRef]); const family = await loadFamily(p); if (ticket !== request) return; root.innerHTML = personCard(p, true, ref, family); const back = document.getElementById('cbr-person-table-back'); const occurrences = p.table_occurrences || []; const origin = new URLSearchParams(location.search).get('table'); const occurrence = occurrences.find(x => x.table_id === origin) || occurrences[0]; back.href = occurrence ? tableOccurrenceURL(occurrence) : 'shiji.html'; back.textContent = occurrence ? '回到' + occurrence.title + ' →' : '回到《史記》 →'; document.title = p.label + ' · 人文';} catch {if (ticket === request) root.innerHTML = '<h1>人物資料尚未載入</h1><p>請由史表的人名進入，或稍後重試。</p><a href="shiji.html">回到《史記》</a>';}}
window.addEventListener('hashchange', render);
(async () => {
  const select = document.getElementById('cbr-person-select');
  try {
    const response = await fetch('data/corpus/profiles/index.json');
    if (!response.ok) throw Error('人物索引載入失敗');
    const {profiles} = await response.json();
    for (const p of profiles) {const option = document.createElement('option'); option.value = p.id; option.textContent = p.label; select.append(option);}
    select.onchange = () => {location.hash = encodeURIComponent(select.value);};
    const sync = () => {try {select.value = decodeURIComponent(location.hash.slice(1));} catch {select.value = '';}};
    window.addEventListener('hashchange', sync);
    if (!location.hash && profiles.length) location.hash = encodeURIComponent(profiles[0].id);
    sync();
  } catch {select.disabled = true;}
  render();
})();
