import {escapeHTML as h} from './core.js';
import {ui} from './i18n.js';
import {groupWorks,workURL} from './corpus-discovery.js';
import {loadChapterDirectory} from './source-caption.js';
let loading;
export function loadHomeCatalog(){
  if(loading)return loading;
  loading=(async()=>{
    const [response,directory]=await Promise.all([fetch('data/corpus/works.json'),loadChapterDirectory()]);if(!response.ok)throw Error('catalog');
    const manifest=await response.json();
    const works=manifest.works.map(w=>({...w,title:directory[w.id]?.title || w.title}));
    const catalogs=await Promise.all(works.map(async w=>{
      if(!/^data\/corpus\/(?:[a-z0-9-]+\/)?index\.json$/.test(w.catalog_path))throw Error('catalog path');
      const r=await fetch(w.catalog_path);if(!r.ok)throw Error('work catalog');
      return {...w,catalog:await r.json()};
    }));
    const root=document.getElementById('home-source-catalog');
    root.innerHTML=groupWorks(catalogs).map(group=>`<section class="home-source-group" id="home-sources-${h(group.key)}"><h2>${ui(group.title)}</h2><div class="home-source-grid">${group.works.map(w=>`<article class="home-source-card"><h3><a href="${h(workURL(w))}">《${h(w.title)}》</a></h3>${w.author?`<p class="home-source-author">${h(w.author)}</p>`:''}<p class="home-source-count">${ui('{count} reading units',{count:w.catalog.chapters.length})}</p><p class="home-source-status">${ui(w.catalog.chapters.length?'Selections; review in progress':'Source text not yet imported')}</p><a class="home-source-open" href="${h(workURL(w))}">${ui(w.catalog.chapters.length?'Open source →':'Browse volume directory →')}</a></article>`).join('')}</div></section>`).join('');
    const stats=document.getElementById('home-source-total');stats.innerHTML=ui('{count} source works',{count:catalogs.length});
    const section=new URLSearchParams(location.search).get('section');if(section){const target=['early','medieval','other'].includes(section)?document.getElementById('home-sources-'+section):section==='sources'?document.getElementById('published-sources'):null;target?.scrollIntoView({block:'start'});}
  })().catch(()=>{document.getElementById('home-source-catalog').innerHTML=`<p role="status">${ui('The index could not be loaded. Please reload.')}</p><a href="reader.html">${ui('Read source texts')}</a>`;loading=null;});
  return loading;
}
