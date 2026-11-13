import {escapeHTML as h} from './core.js';
import {ui,t} from './i18n.js';
import {canonicalProfiles,filterPeople,facetCounts} from './corpus-discovery.js';
const PAGE_SIZE=48;
const dimensions=[['dynasty','Dynasty'],['surname','Surname'],['jiguan','Native place']];
const parameters=new URLSearchParams(location.search);
const selection=Object.fromEntries(dimensions.map(([key])=>[key,[...new Set(parameters.getAll(key))]]));
const facetSearch={dynasty:'',surname:'',jiguan:''};
const facetRoot=document.getElementById('person-facets');
document.querySelector('.person-search').addEventListener('submit',event=>event.preventDefault());
const requestedPage=Number(parameters.get('page') || 1);
let people=[],page=Number.isSafeInteger(requestedPage)&&requestedPage>0?requestedPage-1:0;
const query=document.getElementById('person-search'),results=document.getElementById('person-results');
const facetLabel=value=>value==='__unknown__'?ui('Not recorded'):h(value);
function renderFacets(){
  const counts=facetCounts(people,query.value,selection);
  const active=document.activeElement;
  const focus=active?.dataset.facet?{key:active.dataset.facet,value:active.value}:null;
  facetRoot.innerHTML=dimensions.map(([key,label])=>{
    const options=counts[key] || [];
    const values=new Map(options.map(item=>[item.value,item.count]));
    for(const value of selection[key])if(!values.has(value))values.set(value,0);
    return `<fieldset class="person-facet"><legend>${ui(label)}${selection[key].length?` <small>(${selection[key].length})</small>`:''}</legend>${(values.size>12 || facetSearch[key])?`<label class="facet-search-label">${ui('Find a filter')}<input type="search" data-facet-search="${key}" value="${h(facetSearch[key])}" autocomplete="off"></label>`:''}<div class="person-facet-options">${[...values].map(([value,count],index)=>`<label class="person-facet-option"${facetSearch[key]&&!String(value==='__unknown__'?t('Not recorded'):value).toLocaleLowerCase().includes(facetSearch[key].toLocaleLowerCase())?' hidden':''}><input type="checkbox" data-facet="${key}" value="${h(value)}" id="facet-${key}-${index}"${selection[key].includes(value)?' checked':''}${!count&&!selection[key].includes(value)?' disabled':''}><span>${facetLabel(value)}</span><small class="facet-count">${count}</small></label>`).join('')}</div></fieldset>`;
  }).join('');
  if(focus)[...facetRoot.querySelectorAll('input[data-facet]')].find(input=>input.dataset.facet===focus.key&&input.value===focus.value)?.focus({preventScroll:true});
  document.getElementById('person-filter-clear').disabled=!dimensions.some(([key])=>selection[key].length);
}
function personName(p){
  const d=p.display || {},name=d.name || p.label;
  const main=[d.title?`<span class="directory-title${!d.jiguan?' title-name-gap':''}">${h(d.title)}</span>`:'',d.jiguan?`<span class="directory-jiguan">〔${h(d.jiguan)}〕</span>`:'',`<span class="directory-name">${h(name)}</span>`].join('');
  const additional=(d.additional || []).filter(Boolean);
  return `<span class="directory-identity">${main}${additional.length?`<small class="directory-additional">（${additional.map(h).join('；')}）</small>`:''}</span>`;
}
function render(){
  const matches=filterPeople(people,query.value,selection),pages=Math.max(1,Math.ceil(matches.length/PAGE_SIZE));page=Math.min(Math.max(page,0),pages-1);
  const from=page*PAGE_SIZE,to=Math.min(matches.length,from+PAGE_SIZE);
  renderFacets();
  document.getElementById('person-result-count').innerHTML=ui('{count} matching people',{count:matches.length});
  document.getElementById('person-page-position').innerHTML=matches.length?ui('Showing {start}–{end} of {count}',{start:from+1,end:to,count:matches.length}):'';
  results.innerHTML=matches.length?matches.slice(from,to).map(p=>`<li><a class="person-result-name" href="person.html#${encodeURIComponent(p.id)}">${personName(p)}<span class="person-result-arrow" aria-hidden="true">→</span></a><code>${h(p.id)}</code></li>`).join(''):`<li class="person-search-empty">${ui('No matching person. Try a shorter name or another attested form.')}</li>`;
  document.getElementById('person-prev').disabled=page===0;document.getElementById('person-next').disabled=to>=matches.length;
  const url=new URL(location.href);
  if(query.value.trim())url.searchParams.set('q',query.value.trim());else url.searchParams.delete('q');
  for(const [key] of dimensions){url.searchParams.delete(key);for(const value of selection[key])url.searchParams.append(key,value);}
  if(page)url.searchParams.set('page',String(page+1));else url.searchParams.delete('page');history.replaceState(null,'',url);
}
query.value=parameters.get('q')?.slice(0,200)||'';
query.addEventListener('input',()=>{page=0;render();});
document.getElementById('person-clear').addEventListener('click',()=>{query.value='';query.dispatchEvent(new Event('input'));query.focus();});
facetRoot.addEventListener('change',event=>{const input=event.target,key=input.dataset.facet;if(!dimensions.some(([k])=>k===key))return;selection[key]=input.checked?[...new Set([...selection[key],input.value])]:selection[key].filter(v=>v!==input.value);page=0;render();});
facetRoot.addEventListener('input',event=>{const input=event.target,key=input.dataset.facetSearch;if(!dimensions.some(([k])=>k===key))return;facetSearch[key]=input.value;for(const row of input.closest('fieldset').querySelectorAll('.person-facet-option'))row.hidden=!row.querySelector('span').textContent.toLocaleLowerCase().includes(input.value.toLocaleLowerCase());});
document.getElementById('person-filter-clear').addEventListener('click',()=>{for(const [key] of dimensions){selection[key]=[];facetSearch[key]='';}page=0;render();});
document.getElementById('person-prev').addEventListener('click',()=>{page--;render();results.scrollIntoView({block:'start'});});
document.getElementById('person-next').addEventListener('click',()=>{page++;render();results.scrollIntoView({block:'start'});});
window.addEventListener('renwen:languagechange',()=>{if(people.length)render();});
(async()=>{
  try{
    const responses=await Promise.all([fetch('data/corpus/persons.json'),fetch('data/corpus/profiles/index.json'),fetch('data/corpus/person-directory.json')]);
    if(responses.some(r=>!r.ok))throw Error('person index');
    const [registry,index,directory]=await Promise.all(responses.map(r=>r.json()));
    if(directory?.schema_version!==1 || !directory.persons || Object.keys(registry).some(id=>!Object.hasOwn(directory.persons,id)))throw Error('incomplete directory metadata');
    people=canonicalProfiles(registry,index,directory);
    if(people.length!==Object.keys(registry).length)throw Error('incomplete profile index');
    document.getElementById('person-total').innerHTML=ui('{count} people in this published version',{count:people.length});query.disabled=false;render();
  }catch{results.innerHTML=`<li role="status">${ui('The index could not be loaded. Please reload.')}</li>`;}
})();
