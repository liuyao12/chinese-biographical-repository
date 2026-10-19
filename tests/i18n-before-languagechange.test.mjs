import test from 'node:test';
import assert from 'node:assert/strict';
const {setLocale}=await import(process.env.TEST_MODULE_URL||'../assets/i18n.js');
test('beforelanguagechange captures old DOM before language chrome is changed',()=>{
 const previous={document:globalThis.document,window:globalThis.window,CustomEvent:globalThis.CustomEvent};
 const events=[];setLocale('zh-Hant');
 try{
  globalThis.document={documentElement:{lang:'zh-Hant'},querySelectorAll:()=>[]};
  globalThis.CustomEvent=class{constructor(type,options){this.type=type;this.detail=options.detail;}};
  globalThis.window={dispatchEvent:e=>events.push({type:e.type,lang:document.documentElement.lang,next:e.detail.locale})};
  setLocale('en',{persist:false});
  assert.deepEqual(events,[{type:'renwen:beforelanguagechange',lang:'zh-Hant',next:'en'},{type:'renwen:languagechange',lang:'en',next:'en'}]);
  events.length=0;setLocale('en',{persist:false});assert.deepEqual(events,[]);
  setLocale('zh-Hant',{persist:false});assert.deepEqual(events,[{type:'renwen:beforelanguagechange',lang:'en',next:'zh-Hant'},{type:'renwen:languagechange',lang:'zh-Hant',next:'zh-Hant'}]);
 }finally{for(const[k,v]of Object.entries(previous)){if(v===undefined)delete globalThis[k];else globalThis[k]=v;}setLocale('zh-Hant');}
});
