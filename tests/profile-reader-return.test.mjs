import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {profileReaderURL} from '../assets/library.js';
test('profile returns to its own imported ECCP entry rather than the bare homepage',()=>{
 const p={id:'person-test',accounts:[]};
 const c={sources:[{id:'eccp-test',work:'work-eccp',subject:p.id}]};
 assert.equal(profileReaderURL(p,c),'./#eccp-test');
});
test('local source account retains its passage and person context',()=>{
 const p={id:'person-test',accounts:[{readerWitness:'qsg-test',passage:'p003'}]};
 assert.equal(profileReaderURL(p,{sources:[]}),'./?passage=p003&person=person-test#qsg-test');
});
test('unsafe or external-only accounts cannot become the reader return URL',()=>{
 const p={id:'person-test',accounts:[{readerWitness:'javascript:evil',url:'https://example.org/'}]};
 assert.equal(profileReaderURL(p,{sources:[{id:'eccp-other'}]}),'./#eccp-other');
 assert.equal(profileReaderURL(p,{sources:[]}),'./#eccp');
});
test('invalid passage is skipped rather than injected into the URL',()=>{
 const p={id:'person-test',accounts:[{readerWitness:'qsg-test',passage:'x&bad'}]};
 assert.equal(profileReaderURL(p,{sources:[{id:'eccp'}]}),'./#eccp');
});
test('production profile navigation consumes the shared source-aware return route',async()=>{
 const source=await readFile(new URL('../assets/profile-view.js',import.meta.url),'utf8');
 assert.ok(source.includes('h(profileReaderURL(p,libraryCatalog))'));
 assert.ok(!source.includes('<a href="./">${ui("Three-panel reader →")}'));
});
