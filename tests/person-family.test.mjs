import test from 'node:test';
import assert from 'node:assert/strict';
import {traceFamily} from '../assets/person-family.js';
const relation = (subject_person_id, predicate, object_person_id) => ({subject_person_id, predicate, object_person_id, evidence: []});
test('an explicitly recorded grandfather leaves the missing father empty', async () => {
  const a={id:'a',relations:[relation('a','grandfather','g')]};
  const g={id:'g',relations:[relation('g','father','h')]};
  const h={id:'h'};
  const family=await traceFamily(a, async id => ({g,h})[id]);
  assert.deepEqual(family.ancestors.map(row=>row.map(x=>x.id)),[[],['g'],['h']]);
});
test('source JSON traversal derives three generations and separate spouses/children', async () => {
  const people = {
    a: {id:'a',label:'synthetic child',relations:[relation('a','father','b'),relation('a','mother','m'),relation('s','spouse','a'),relation('c','father','a')]},
    b: {id:'b',label:'synthetic father',relations:[relation('b','father','d')]},
    d: {id:'d',label:'synthetic grandfather',relations:[relation('d','father','e')]},
    e: {id:'e',label:'synthetic great grandfather'},
    m:{id:'m'},s:{id:'s'},c:{id:'c'},
  };
  const family = await traceFamily(people.a, async id => people[id]);
  assert.deepEqual(family.ancestors.map(row => row.map(x => x.id)), [['b'],['d'],['e']]);
  assert.deepEqual(family.mother.map(x => x.id), ['m']);
  assert.deepEqual(family.spouses.map(x => x.id), ['s']);
  assert.deepEqual(family.children.map(x => x.id), ['c']);
  assert.equal(family.children[0].spouse, undefined);
});
test('cycles stop traversal while competing source fathers remain visible', async () => {
  const a={id:'a',relations:[relation('a','father','b'),relation('a','father','c')]};
  const b={id:'b',relations:[relation('b','father','a')]};
  const c={id:'c',relations:[]};
  const family=await traceFamily(a, async id => ({a,b,c})[id]);
  assert.equal(family.ancestors[0].length,2);
  assert.equal(family.ancestors[1][0].cycle,true);
  assert.deepEqual(family.ancestors[2],[]);
});

test('non-birth maternal relations do not replace the birth mother or create biological children', async () => {
  const child={id:'child',relations:[relation('child','mother','birth'),relation('child','adoptive_mother','adoptive'),relation('child','stepmother','step')]};
  const people={birth:{id:'birth'},adoptive:{id:'adoptive',relations:child.relations},step:{id:'step'}};
  const family=await traceFamily(child,async id=>people[id]);
  assert.deepEqual(family.mother.map(x=>x.id),['birth']);
  const adopted=await traceFamily(people.adoptive,async id=>id==='child'?child:people[id]);
  assert.deepEqual(adopted.children,[]);
});

test('a separately attributed sibling assembly derives ancestors and reverse children without inventing source father', async () => {
 const connection={type:'shared_father_through_sibling',status:'contextual_provisional',rationale:'synthetic inference',references:[{quote:'synthetic sibling and father evidence'}]};
 const row={person_id:'yi',parent_person_id:'wu',assembly_id:'synthetic-family',status:'editorial_preferred',parent_connection:connection};
 const people={yi:{id:'yi',assembled_identity:row,relations:[relation('tian','brother','yi')]},wu:{id:'wu',relations:[relation('wu','father','ao')],assembled_children:[row]},ao:{id:'ao'}};
 const family=await traceFamily(people.yi,async id=>people[id]);
 assert.deepEqual(family.ancestors.map(r=>r.map(x=>x.id)),[['wu'],['ao'],[]]);
 assert.equal(family.ancestors[0][0].role,'assembly_inferred');
 assert.equal(family.ancestors[0][0].inference_note,'synthetic inference');
 assert.equal(people.yi.relations.some(r=>r.predicate==='father'),false);
 const parent=await traceFamily(people.wu,async id=>people[id]);
 assert.deepEqual(parent.children.map(x=>x.id),['yi']);
 assert.equal(parent.children[0].role,'assembly_inferred');
 const unaccepted=await traceFamily({...people.yi,assembled_identity:{...row,status:'unresolved'}},async id=>people[id]);
 assert.deepEqual(unaccepted.ancestors,[[],[],[]]);
 const wrong=await traceFamily({...people.yi,assembled_identity:{...row,person_id:'other'}},async id=>people[id]);
 assert.deepEqual(wrong.ancestors,[[],[],[]]);
});

test('shared ancestor through a sibling leaves father empty and traces the next generation', async () => {
  const connection={type:'shared_ancestor_through_sibling',status:'contextual_provisional',rationale:'Two source relations.',references:[{quote:'Sibling and grandfather evidence.'}]};
  const a={id:'a',assembled_identity:{person_id:'a',assembly_id:'family',status:'editorial_preferred',connection:'grandfather',parent_person_id:null,ancestor_person_id:'g',ancestor_connection:connection},relations:[]};
  const g={id:'g',relations:[relation('g','father','h')]};
  const h={id:'h'};
  const family=await traceFamily(a,async id=>({g,h})[id]);
  assert.deepEqual(family.ancestors.map(row=>row.map(x=>x.id)),[[],['g'],['h']]);
  assert.equal(family.ancestors[1][0].role,'assembly_inferred');
  assert.equal(family.ancestors[1][0].inference_note,connection.rationale);
  const grandfather=await traceFamily(g,async id=>({a,h})[id]);
  assert.deepEqual(grandfather.children,[]);
});
test('unreviewed shape or missing evidence does not create a shared ancestor edge', async () => {
  for (const connection of [{type:'other',status:'contextual_provisional',rationale:'x',references:[{quote:'x'}]},
                            {type:'shared_ancestor_through_sibling',status:'contextual_provisional',rationale:'x',references:[]}]) {
    const a={id:'a',assembled_identity:{person_id:'a',assembly_id:'family',status:'editorial_preferred',connection:'grandfather',ancestor_person_id:'g',ancestor_connection:connection}};
    const family=await traceFamily(a,async()=>({id:'g'}));
    assert.deepEqual(family.ancestors,[[],[],[]]);
  }
});

test('teaching in either direction does not create parents, ancestors, spouse or children', async () => {
 const p={id:'student',relations:[relation('student','teacher','master'),relation('pupil','teacher','student')]};
 const family=await traceFamily(p, async () => {throw Error('teaching must not trigger family loading');});
 assert.deepEqual(family,{ancestors:[[],[],[]],mother:[],spouses:[],children:[]});
});

test('consecutive ancestral evidence supplies separately labelled intermediate parents and reverse children', async () => {
  const proof={type:'parent_between_consecutive_ancestors',status:'contextual_provisional',human_reviewed:false,
    chain_subject_person_id:'descendant',nearer_ancestor_assertion_id:'near',farther_ancestor_assertion_id:'far',
    rationale:'Synthetic consecutive paternal ancestor statements.',references:[{quote:'Synthetic source passage.',chapter_id:'c',paragraph_id:'p'}]};
  const row=(id,parent)=>({person_id:id,parent_person_id:parent,assembly_id:'synthetic',status:'editorial_preferred',parent_connection:proof});
  const people={descendant:{id:'descendant',relations:[relation('descendant','father','father'),{...relation('descendant','grandfather','grand'),evidence:[{quote:'Direct grandfather statement.'}]},{...relation('descendant','great_grandfather','great'),evidence:[{quote:'Direct great-grandfather statement.'}]}]},
    father:{id:'father',assembled_identity:row('father','grand')},grand:{id:'grand',assembled_identity:row('grand','great'),assembled_children:[row('father','grand')]},great:{id:'great'}};
  const family=await traceFamily(people.descendant,async id=>people[id]);
  assert.deepEqual(family.ancestors.map(g=>g.map(p=>p.id)),[['father'],['grand'],['great']]);
  assert.notEqual(family.ancestors[1][0].role,'assembly_inferred');
  assert.notEqual(family.ancestors[2][0].role,'assembly_inferred');
  assert.equal(family.ancestors[1][0].explicitAncestor,true);
  assert(family.ancestors[1][0].evidence.some(e=>e.quote==='Direct grandfather statement.'));
  assert(family.ancestors[1][0].evidence.some(e=>e.quote==='Synthetic source passage.'));
  const father=await traceFamily(people.father,async id=>people[id]);
  assert.deepEqual(father.ancestors.map(g=>g.map(p=>p.id)),[['grand'],['great'],[]]);
  assert.equal(father.ancestors[0][0].role,'assembly_inferred');
  assert.equal(father.ancestors[0][0].inference_note,proof.rationale);
  const grandfather=await traceFamily(people.grand,async id=>people[id]);
  assert.deepEqual(grandfather.children.map(p=>p.id),['father']);
  assert.equal(people.father.relations,undefined);
  const unaccepted=await traceFamily({...people.father,assembled_identity:{...row('father','grand'),status:'unresolved'}},async id=>people[id]);
  assert.deepEqual(unaccepted.ancestors,[[],[],[]]);
});

test('unadopted source claims remain in the payload without becoming family edges', async()=>{
 const claim={...relation('child','grandfather','remote'),qualifiers:{adopted_for_family_tree:false}};
 const child={id:'child',relations:[claim]};
 const family=await traceFamily(child,async id=>({id}));
 assert.deepEqual(family.ancestors,[[],[],[]]);
 assert.equal(child.relations[0],claim);
 const relative=await traceFamily({id:'remote',relations:[claim]},async id=>({id}));
 assert.deepEqual(relative.children,[]);
});
