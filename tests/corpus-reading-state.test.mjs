import test from 'node:test';
import assert from 'node:assert/strict';
import {captureReadingState,restoreReadingState} from '../assets/corpus-reading-state.js';
function node({id='',caseID,top=0,bottom=0,open=false,popup=false}={}){
  return {id,open,dataset:{interpretationId:caseID},hasAttribute:name=>name==='data-interpretation-id'&&caseID!==undefined,closest:()=>popup?{}:null,getBoundingClientRect:()=>({top,bottom})};
}
function fixture(details,anchors=[],chapter='chapter:1'){
  return {querySelector:()=>chapter?{dataset:{chapterId:chapter}}:null,querySelectorAll:selector=>selector==='details'?details:selector==='[data-source-text]'?anchors.filter(n=>!n.hasAttribute('data-interpretation-id')):selector==='[data-interpretation-id]'?anchors.filter(n=>n.hasAttribute('data-interpretation-id')):anchors};
}
function viewport(x=0,y=0){return {scrollX:x,scrollY:y,calls:[],scrollTo(x,y){this.calls.push([x,y]);}};}
test('same chapter restores nested disclosures and scroll after rebuilding content',()=>{
  const win=viewport(3,900);const state=captureReadingState(fixture([node({open:true}),node({open:false}),node({open:true})]),win);
  const fresh=[node(),node({open:true}),node()];restoreReadingState(fixture(fresh),state,win);
  assert.deepEqual(fresh.map(n=>n.open),[true,false,true]);assert.deepEqual(win.calls,[[3,900]]);
});
test('person popup disclosures never interfere with source disclosures',()=>{
  const state=captureReadingState(fixture([node({open:true}),node({open:true,popup:true})]),viewport());
  assert.deepEqual(state.openDetails,[true]);const fresh=node();restoreReadingState(fixture([fresh,node({popup:true})]),state,viewport());assert.equal(fresh.open,true);
});
test('reading anchor survives viewport clamping while the chapter is loading',()=>{
  const old=node({id:'chapter:1:p052',top:-35,bottom:150});const state=captureReadingState(fixture([], [old]),viewport(0,800));
  const win=viewport(0,0);const fresh=node({id:'chapter:1:p052',top:120,bottom:300});restoreReadingState(fixture([],[fresh]),state,win);assert.deepEqual(win.calls,[[0,155]]);
});
test('open referent evidence is a reading anchor and opaque keys are compared as data',()=>{
  const key='ri:source[1]';const state=captureReadingState(fixture([node({open:true})],[node({caseID:key,top:-10,bottom:200})]),viewport(0,500));
  const fresh=node({caseID:key,top:25,bottom:300});const win=viewport(0,100);restoreReadingState(fixture([node()],[fresh]),state,win);assert.deepEqual(win.calls,[[0,135]]);
});
test('changing the chapter never reapplies another chapter disclosure state',()=>{
  const state=captureReadingState(fixture([node({open:true})]),viewport(0,300));const fresh=node();const win=viewport();restoreReadingState(fixture([fresh],[],'chapter:2'),state,win);assert.equal(fresh.open,false);assert.deepEqual(win.calls,[]);
});
test('header position remains at the header and missing anchors fall back to saved scroll',()=>{
  const state=captureReadingState(fixture([],[node({id:'p1',top:0,bottom:10})]),viewport());assert.equal(state.anchor,undefined);
  const win=viewport();restoreReadingState(fixture([]),state,win);assert.deepEqual(win.calls,[[0,0]]);
  const saved=captureReadingState(fixture([],[node({id:'p1',top:-10,bottom:50})]),viewport(0,333));const later=viewport();restoreReadingState(fixture([]),saved,later);assert.deepEqual(later.calls,[[0,333]]);
});
test('a changed disclosure structure is not restored by a misleading index',()=>{
  const state=captureReadingState(fixture([node({open:true})]),viewport());const a=node(),b=node();restoreReadingState(fixture([a,b]),state,viewport());assert.deepEqual([a.open,b.open],[false,false]);
  assert.equal(captureReadingState(fixture([],[],null),viewport()),null);
});
