import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {canonicalProfiles,searchPeople} from './corpus-discovery.js';
const PAGE_SIZE=48;
document.querySelector('.person-search').addEventListener('submit',event=>event.preventDefault());
const requestedPage=Number(new URLSearchParams(location.search).get('page') || 1);
let people=[],page=Number.isSafeInteger(requestedPage)&&requestedPage>0?requestedPage-1:0;
const query=document.getElementById('person-search'),results=document.getElementById('person-results');
function render(){
  const matches=searchPeople(people,query.value),pages=Math.max(1,Math.ceil(matches.length/PAGE_SIZE));page=Math.min(page,pages-1);
  const from=page*PAGE_SIZE,to=Math.min(matches.length,from+PAGE_SIZE);
  document.getElementById('person-result-count').innerHTML=ui('{count} matching people',{count:matches.length});
  document.getElementById('person-page-position').innerHTML=matches.length?ui('Showing {start}–{end} of {count}',{start:from+1,end:to,count:matches.length}):'';
  results.innerHTML=matches.length?matches.slice(from,to).map(p=>{
    const other=p.names.filter(n=>n!==p.label).slice(0,4);
    return `<li><a class="person-result-name" href="person.html#${encodeURIComponent(p.id)}">${h(p.label)}<span aria-hidden="true"> →</span></a>${other.length?`<p class="person-result-forms"><span class="sr-only">${ui('Other attested forms')}: </span>${other.map(h).join(' · ')}</p>`:''}<code>${h(p.id)}</code></li>`;
  }).join(''):`<li class="person-search-empty">${ui('No matching person. Try a shorter name or another attested form.')}</li>`;
  document.getElementById('person-prev').disabled=page===0;document.getElementById('person-next').disabled=to>=matches.length;
  const url=new URL(location.href);if(query.value.trim())url.searchParams.set('q',query.value.trim());else url.searchParams.delete('q');if(page)url.searchParams.set('page',String(page+1));else url.searchParams.delete('page');history.replaceState(null,'',url);
}
query.value=new URLSearchParams(location.search).get('q')?.slice(0,200)||'';
query.addEventListener('input',()=>{page=0;render();});
document.getElementById('person-clear').addEventListener('click',()=>{query.value='';query.dispatchEvent(new Event('input'));query.focus();});
document.getElementById('person-prev').addEventListener('click',()=>{page--;render();results.scrollIntoView({block:'start'});});
document.getElementById('person-next').addEventListener('click',()=>{page++;render();results.scrollIntoView({block:'start'});});
window.addEventListener('renwen:languagechange',()=>{if(people.length)render();});
(async()=>{
  try{
    const responses=await Promise.all([fetch('data/corpus/persons.json'),fetch('data/corpus/profiles/index.json')]);
    if(responses.some(r=>!r.ok))throw Error('person index');
    const [registry,index]=await Promise.all(responses.map(r=>r.json()));people=canonicalProfiles(registry,index);
    if(people.length!==Object.keys(registry).length)throw Error('incomplete profile index');
    document.getElementById('person-total').innerHTML=ui('{count} people in this published version',{count:people.length});query.disabled=false;render();
  }catch{results.innerHTML=`<li role="status">${ui('The index could not be loaded. Please reload.')}</li>`;}
})();
