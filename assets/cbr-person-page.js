import {loadPerson, personCard} from './cbr-person.js';
let request = 0;
async function render() {const ticket = ++request; const root = document.getElementById('cbr-profile'); try {const id = decodeURIComponent(location.hash.slice(1)); const p = await loadPerson(id); if (ticket !== request) return; root.innerHTML = personCard(p, true); document.title = p.label + ' · 人文';} catch {if (ticket === request) root.innerHTML = '<h1>人物資料尚未載入</h1><p>請由年表的人名進入，或稍後重試。</p><a href="shiji.html#chapter=15&category=biao">回到六國年表</a>';}}
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
