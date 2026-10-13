import test from 'node:test';
import assert from 'node:assert/strict';
import {sectionMarkup} from '../assets/historical-table-sections.js';
import {continuousRows} from '../assets/historical-tables.js';
const cell={id:'synthetic-cell',column:0,rowspan:1,colspan:1,text:'甲與乙',person_mentions:[{start:0,end:1,surface:'甲',person_id:'abc_def_123'},{start:2,end:3,surface:'乙',person_id:'xyz_abc_456'}]};
const fragment=(id,label)=>({id,source_id:'synthetic-source',columns:[{text:label,kind:'source_column'}],source_header:[label],rows:[{id:id+'-row',year:null,cells:[{...cell,id:id+'-cell'}]}]});
const table={title:'synthetic',independent_sections:true,source:{id:'synthetic-source'},fragments:[fragment('a','lineage'),fragment('b','office')]};
test('unlike sections remain separate and each person is an inline link in both orientations',()=>{
 assert.equal(continuousRows(table).length,2);
 for(const horizontal of [false,true]){
  const html=sectionMarkup(table,horizontal);
  assert.equal((html.match(/role="table"/g)||[]).length,2);
  assert.equal((html.match(/class="table-person-link"/g)||[]).length,4);
  assert.match(html,/<\/a>與<a/);
  assert.doesNotMatch(html,/data-editorial-year/);
  assert.match(html,/lineage/);assert.match(html,/office/);
 }
});
