import {readFileSync} from 'node:fs';
import {setLocale} from '../assets/i18n.js';
import test from 'node:test';
import assert from 'node:assert/strict';
import {markCell, personCard, profileURL, tableOccurrenceURL, personBundleURL, bindPersonCards, titleUsageHTML} from '../assets/cbr-person.js';
test('a sourced clan appellation heads the profile while zi remains separate and ming unknown',()=>{
 const name={surname:'鍾',ming:null,zi:'琰',clan_style:{value:'鍾氏'},quote:'鍾氏，字琰。',additional_names:[]};
 const html=personCard({id:'synthetic-woman',label:'Synthetic woman',name_components:[name]},true);
 assert.match(html,/<h1>鍾氏<\/h1>/);
 assert.match(html.replace(/<[^>]*>/g,''),/字 琰/);
 assert.doesNotMatch(html,/<h1>鍾琰<\/h1>/);
});
test('maternal grandfather retains the source relation with its own label',()=>{
 const p={id:'synthetic-child',label:'Synthetic child',related_people:{'synthetic-grand':'Synthetic grandfather'},relations:[{subject_person_id:'synthetic-child',predicate:'grandfather',object_person_id:'synthetic-grand',qualifiers:{lineage:'maternal',source_term:'外祖'},evidence:[]}]};
 assert.match(personCard(p,true),/外祖父/);
});
test('年表錨點保留原文並連至人物頁，拒絕錯位或交疊',()=>{
 const c={text:'張儀相。',person_mentions:[{start:0,end:2,surface:'張儀',person_id:'abc_def_123'}]};
 const html=markCell(c); assert.match(html,/張儀<\/a>相。/);assert.match(html,/person.html#abc_def_123/);
 assert.throws(()=>markCell({...c,person_mentions:[{...c.person_mentions[0],end:3}]}));
 assert.equal(markCell({text:'<楚>&'}),'&lt;楚&gt;&amp;');
});
test('人物卡片提供跨篇原文與完整人物頁，不以 JSON 代替介面',()=>{
 const p={id:'abc_def_123',label:'張儀',names:['張子'],titles:[{title:'秦相',period:'起訖未定'}],occurrences:[{number:70,category:'liezhuan',title:'張儀列傳',paragraph_id:'p1',quote:'張儀者，魏人也。',count:2}]};
 const html=personCard(p);assert.match(html,/稱號與持職/);assert.match(html,/閱讀完整人物頁/);assert.match(html,/chapter=70&amp;category=liezhuan&amp;passage=p1/);assert.doesNotMatch(html,/\.json/);
 assert.match(personCard({...p,label:'<script>'},true),/&lt;script&gt;/);
 assert.equal(profileURL('a#b'),'person.html#a%23b');
});

test('table occurrences link to their own chapter and mark names inside a cell', () => {
 for (const chapter of [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]) {
  const url=tableOccurrenceURL({table_id: 'shiji-'+String(chapter).padStart(3,'0'),cell_id:'synthetic-cell'});
  assert.match(url,new RegExp('chapter='+chapter+'&'));
 }
 assert.equal(tableOccurrenceURL({table_id:'javascript:alert(1)',cell_id:'x'}),'');
 const html=markCell({text:'甲與乙會盟。',person_mentions:[{start:0,end:1,surface:'甲',person_id:'abc_def_123'},{start:2,end:3,surface:'乙',person_id:'xyz_abc_456'}]});
 assert.equal((html.match(/class="table-person-link"/g)||[]).length,2);
 assert.match(html,/<\/a>與<a/);
 assert.match(html,/<\/a>會盟。$/);
});

test('source-local person card shows received table evidence before opening its page', () => {
  const html = personCard({id: 'abc_def_123', label: '劉成', review: 'source_local_candidate', identity_note: '杏山列，尚未跨篇合併。', table_occurrences: [{table_id: 'shiji-021', cell_id: 'shiji-021-t1-r006-c02', title: '《史記·建元以來王子侯者年表》', year: null, quote: '一。六年後九月壬戌，侯劉成元年。'}]});
  assert.match(html, /侯劉成元年/);
  assert.match(html, /杏山列/);
  assert.match(html, /chapter=21/);
});

test('person navigation retains a bounded source-table context', () => {
  assert.equal(profileURL('abc_def_123', 'shiji-021'), 'person.html?table=shiji-021#abc_def_123');
  assert.equal(profileURL('abc_def_123', 'https://example.com'), 'person.html#abc_def_123');
  assert.match(markCell({id: 'shiji-021-t1-r006-c02', text: '侯劉成元年。', person_mentions: [{start: 1, end: 3, surface: '劉成', person_id: 'abc_def_123'}]}), /person.html\?table=shiji-021#abc_def_123/);
});

test('full person page renders the checked primary passage for a table identity decision', () => {
  const html = personCard({id: 'yqp_nlb_p1p_ACAF', label: '彭祖', table_occurrences: [{table_id: 'shiji-017', cell_id: 'shiji-017-t1-r052-c17', title: '《史記·漢興以來諸侯王年表》', year: null, quote: '王彭祖元年。景帝子。', mention: {identity_evidence: [{chapter_id: 'c-shiji-059-wuzong', paragraph_id: 'c-shiji-059-wuzong:p017', quote: '趙王彭祖', source_revision: 2621125}]}}]}, true);
  assert.match(html, /人物同指的篇文證據/);
  assert.match(html, /趙王彭祖/);
  assert.match(html, /chapter=59/);
  assert.match(html, /passage=c-shiji-059-wuzong/);
  assert.match(html, /2621125/);
});

test('profile preserves alternative death years and marks the scoped provisional default', () => {
 const p={id:'abc_def_123',label:'synthetic person',dates:[{era:'BCE',era_year:252,record_id:'old',original_quote:'synthetic earlier account'},{era:'BCE',era_year:251,record_id:'new',original_quote:'synthetic other account'}],life_event_date_decisions:[{candidate_event_ids:['old','new'],preferred_event_id:'new',status:'editorial_provisional',rationale:'synthetic comparison <script>',evidence:[]}],life_events:[{event_type:'death',date_expression:'synthetic year',source_term:'synthetic death',evidence:[]}]};
 const html=personCard(p,true);
 assert.match(html,/西元前252年/);assert.match(html,/西元前251年/);
 assert.match(html,/來源異說/);assert.match(html,/本項預設/);assert.ok(html.indexOf('西元前251年') < html.indexOf('西元前252年'));
 assert.match(html,/來源所記生卒/);assert.match(html,/synthetic comparison &lt;script&gt;/);
 p.life_event_date_decisions[0].status='unresolved';p.life_event_date_decisions[0].preferred_event_id=null;
 assert.doesNotMatch(personCard(p,true),/本項預設/);assert.match(personCard(p,true),/取捨未定/);
});

test('office event counts stay separate from title duration and retain each source record', () => {
 const title={title:'synthetic office',period:'未定 → 未定',reported_office_event_counts:{departure:{value:3,source_term:'synthetic departure'},reinstatement:{value:3,source_term:'synthetic reinstatement'}}};
 const html=personCard({id:'abc_def_123',label:'synthetic person',titles:[{title:title.title,period:title.period},title]},true);
 assert.match(html,/離相 3 次/);assert.match(html,/復位 3 次/);assert.doesNotMatch(html,/各次起訖未定/);
 assert.doesNotMatch(html,/任職三年|任職3年/);
});


test('source JSON links use the deployed exact commit with a bounded fallback', () => {
 const ref = 'a'.repeat(40);
 const url = personBundleURL('abc_def_123', ref);
 assert.equal(url, 'https://github.com/liuyao12/chinese-biographical-repository/blob/'+ref+'/exports/persons/abc_def_123.json');
 assert.match(personBundleURL('a#b', 'javascript:alert(1)'), /blob\/main\/exports\/persons\/a%23b\.json$/);
 assert.match(personCard({id:'abc_def_123',label:'synthetic'},true,ref), new RegExp('blob/'+ref+'/exports/persons'));
});


test('missing fields and entire empty sections are omitted in both card and profile', () => {
 const p={id:'abc_def_123',label:'甲'};
 const family={ancestors:[[],[],[]],mother:[],spouses:[],children:[]};
 for(const full of [false,true]) {
  const html=personCard(p,full,'main',family);
  assert.doesNotMatch(html,/person-aliases|person-life-summary|person-family|person-facts|表中原文|出現篇章|未詳|尚未整理/);
 }
});
test('known grandfather survives a missing father and undated death retains source evidence', () => {
 const family={ancestors:[[],[{id:'g',label:'祖甲',evidence:[]}],[]],mother:[],spouses:[],children:[]};
 const p={id:'abc_def_123',label:'甲',life_events:[{person_id:'abc_def_123',event_type:'death',source_term:'甲卒',evidence:[{quote:'甲卒'}]}],age_assertions:[{person_id:'abc_def_123',value:70,evidence:[]}],titles:[{title:'君',period:'未定 → 未定'}]};
 const html=personCard(p,true,'main',family);
 assert.match(html,/<dt>祖<\/dt>/);assert.doesNotMatch(html,/<dt>(父|曾祖|生母|配偶|子女|生|卒)<\/dt>/);
 assert.match(html,/70 歲/);assert.match(html,/甲卒/);assert.match(html,/稱號與持職/);
 assert.doesNotMatch(html,/起訖未定|原文未明紀年|來源所記地望/);
});
test('a dated death shows its available year without an absent birth or Chinese date placeholder', () => {
 const p={id:'abc_def_123',label:'甲',life_events:[{person_id:'abc_def_123',event_type:'death',normalized_date:{era:'BCE',era_year:243},evidence:[]}]};
 for(const full of [false,true]) {
  const html=personCard(p,full);
  assert.match(html,/<dt>卒<\/dt>/);assert.match(html,/西元前243年/);
  assert.doesNotMatch(html,/<dt>(生|年齡)<\/dt>|原文未明紀年/);
 }
});

test('inferred family edges are visibly provisional and their explanation is escaped',()=>{
 const family={ancestors:[[{id:'father',label:'synthetic father',role:'assembly_inferred',inference_note:'<script>bad</script>',evidence:[]}],[],[]],mother:[],spouses:[],children:[]};
 const html=personCard({id:'child',label:'synthetic child'},true,'main',family);
 assert.match(html,/父系暫定/);assert.match(html,/&lt;script&gt;bad&lt;\/script&gt;/);assert.doesNotMatch(html,/<script>/);
});

test('place roles distinguish ancestors, residence and death without relabelling them birthplaces',()=>{
 const addresses=[['ancestral_origin','齊'],['residence','上郡'],['death_place','陽周']].map(([relation,source_name])=>({relation,place:{source_name},term:'synthetic received wording',quote:'synthetic quote',interpretation_note:'<script>synthetic</script>'}));
 const html=personCard({id:'synthetic',label:'synthetic',addresses},true);
 assert.match(html,/祖先出身：齊/);assert.match(html,/居地：上郡/);assert.match(html,/卒地：陽周/);
 assert.doesNotMatch(html,/出生地：/);assert.doesNotMatch(html,/<script>/);assert.match(html,/&lt;script&gt;synthetic&lt;\/script&gt;/);
});
test('title year evidence is shown only when available and source text stays inert',()=>{
 const p={id:'abc_def_123',label:'張敖',titles:[{title:'宣平侯',evidence:[],effective_period:{start:{normalized_date:{original_quote:'封為宣平侯',rationale:'<判斷>',references:[{title:'<年表>',quote:'九年四月',url:'https://example.org/source?x=1&y=2'},{title:'不合法網址',quote:'<script>',url:'javascript:alert(1)'}]}}}}]};
 const html=personCard(p,true);
 assert.match(html,/始年紀年依據/);assert.match(html,/九年四月/);assert.match(html,/&lt;判斷&gt;/);assert.match(html,/&lt;年表&gt;/);assert.match(html,/&lt;script&gt;/);
 assert.match(html,/https:\/\/example.org\/source\?x=1&amp;y=2/);assert.doesNotMatch(html,/href="javascript:/);assert.doesNotMatch(html,/終年紀年依據/);
 const second={...p.titles[0],effective_period:{start:{normalized_date:{original_quote:'另一授侯原語',references:[{title:'另一本來源',quote:'另一紀年引句',url:'https://example.org/other'}]}}}};
 const both=personCard({...p,titles:[p.titles[0],second]},true);assert.match(both,/九年四月/);assert.match(both,/另一紀年引句/);
 assert.doesNotMatch(personCard(p),/始年紀年依據/);
 assert.doesNotMatch(personCard({id:p.id,label:p.label,titles:[{title:'宣平侯',evidence:[]}]},true),/紀年依據/);
});
test('a dated approximate age identifies the reporting period without inventing lifespan',()=>{
 const p={id:'abc_def_123',label:'趙午',age_assertions:[{person_id:'abc_def_123',value:null,source_term:'年六十餘',date_expression:'漢七年',normalized_date:{era:'BCE',era_year:200},evidence:[]}]};
 const html=personCard(p,true);
 assert.match(html,/年六十餘/);assert.match(html,/漢七年/);assert.match(html,/西元前200年/);assert.match(html,/報齡時/);
 assert.doesNotMatch(html,/<dt>生<\/dt>|<dt>卒<\/dt>|60 歲|享年/);
 const unknown=personCard({...p,age_assertions:[{...p.age_assertions[0],date_expression:null,normalized_date:null}]},true);
 assert.doesNotMatch(unknown,/報齡時|西元|未定/);
});


test('royal scope and office jurisdiction remain readable without rewriting the title', () => {
 const p={id:'abc_def_123',label:'synthetic person',titles:[{title:'王',kind:'royal_rank',period:'',jurisdictions:[{source_name:'膠東'}]},{title:'太守',kind:'office',period:'',jurisdictions:[{source_name:'隴西'},{source_name:'<script>'}]}]};
 const html=personCard(p,true);
 assert.match(html,/<strong>王<\/strong>/);
 assert.match(html,/所王地：膠東/);
 assert.match(html,/所屬地：隴西、&lt;script&gt;/);
 assert.doesNotMatch(personCard({id:'abc_def_123',label:'synthetic person',titles:[{title:'王',period:''}]},true),/所王地|所屬地/);
});

test('same title with different territories keeps separate source assertions', () => {
 const titles=['膠東','齊'].map(source_name=>({title:'王',kind:'royal_rank',period:'',jurisdictions:[{source_name}]}));
 const html=personCard({id:'abc_def_123',label:'synthetic person',titles},true);
 assert.equal((html.match(/class="person-title"/g)||[]).length,2);
 assert.match(html,/所王地：膠東/);assert.match(html,/所王地：齊/);
});

test('full lifespan date evidence displays parallel sources and escapes external material', () => {
 const p={id:'abc_def_123',label:'synthetic person',dates:[{era:'BCE',era_year:205,original_quote:'received passage',evidence:[],rationale:'comparison <script>',references:[{quote:'calendar month',title:'checked table',url:'https://example.com/table'},{quote:'<script>',title:'unresolved note',url:'javascript:alert(1)'}]}]};
 const html=personCard(p,true);
 assert.match(html,/person-date-references/);assert.match(html,/紀年依據/);
 assert.match(html,/calendar month/);assert.match(html,/href="https:\/\/example.com\/table"/);
 assert.match(html,/comparison &lt;script&gt;/);assert.match(html,/unresolved note/);
 assert.doesNotMatch(html,/href="javascript:/);assert.doesNotMatch(html,/<script>/);
 assert.doesNotMatch(personCard(p),/person-date-references|calendar month/);
});

test('lifespan date without parallel references omits the empty evidence field', () => {
 const p={id:'abc_def_123',label:'synthetic person',dates:[{era:'BCE',era_year:205,original_quote:'received passage',evidence:[]}]};
 assert.doesNotMatch(personCard(p,true),/person-date-references|紀年依據/);
});


test('touch opens a card after the tap, while mouse hover and keyboard focus still open it', () => {
  const savedDocument=globalThis.document, savedFetch=globalThis.fetch;
  const events=new Map(), card={hidden:true,setAttribute(){},remove(){}}, root={append(){},addEventListener(k,v){events.set(k,v);},removeEventListener(){}};
  let keyboard=false, prevented=false, stopped=false;
  const node={dataset:{personId:'synthetic_touch_case'},href:'person.html#synthetic_touch_case',matches:()=>keyboard};
  const target={closest:()=>node};
  globalThis.document={createElement:()=>card};globalThis.fetch=()=>new Promise(()=>{});
  let dispose;
  try {
    dispose=bindPersonCards(root);
    events.get('pointerover')({type:'pointerover',pointerType:'touch',target});assert.equal(card.hidden,true);
    events.get('focusin')({type:'focusin',target});assert.equal(card.hidden,true);
    events.get('click')({target,preventDefault(){prevented=true;},stopPropagation(){stopped=true;}});
    assert.equal(card.hidden,false);assert.ok(prevented && stopped);
    events.get('keydown')({key:'Escape'});assert.equal(card.hidden,true);
    keyboard=true;events.get('focusin')({type:'focusin',target});assert.equal(card.hidden,false);
    events.get('keydown')({key:'Escape'});
    events.get('pointerover')({type:'pointerover',pointerType:'mouse',target});assert.equal(card.hidden,true);
    events.get('pointermove')({type:'pointermove',pointerType:'mouse',target});assert.equal(card.hidden,false);
  } finally {dispose?.();globalThis.document=savedDocument;globalThis.fetch=savedFetch;}
});

test('a clicked person remains selected through incidental mouse hover until closed or another click', async () => {
  const savedDocument=globalThis.document, savedFetch=globalThis.fetch;
  const events=new Map(), documentEvents=new Map(), closeButton={focus(){}}, profileButton={};
  const card={hidden:true,setAttribute(){},remove(){},contains(){return false;},
    querySelector(selector){return selector==='.person-profile-button'?profileButton:closeButton;}};
  const ownerDocument={createElement:()=>card,addEventListener(k,v){documentEvents.set(k,v);},removeEventListener(k){documentEvents.delete(k);}};
  const root={ownerDocument,append(){},addEventListener(k,v){events.set(k,v);},removeEventListener(){}};
  let keyboard=false;
  const node=id=>({dataset:{personId:id},href:'person.html#'+id,matches:()=>keyboard});
  const chosen=node('synthetic_pinned_chosen'), incidental=node('synthetic_pinned_incidental');
  const hover=n=>events.get('pointerover')({type:'pointerover',pointerType:'mouse',target:{closest:()=>n}});
  const click=n=>events.get('click')({target:{closest:()=>n},preventDefault(){},stopPropagation(){}});
  const settle=()=>new Promise(resolve=>setImmediate(resolve));
  globalThis.document=ownerDocument;
  globalThis.fetch=async url=>({ok:true,json:async()=>({id:decodeURIComponent(url.split('/').pop().slice(0,-5)),label:'synthetic person'})});
  let dispose;
  try {
    dispose=bindPersonCards(root);
    hover(incidental);await settle();
    click(chosen);hover(incidental);await settle();
    assert.equal(profileButton.href,chosen.href);
    events.get('pointerout')({pointerType:'mouse',relatedTarget:null});
    await new Promise(resolve=>setTimeout(resolve,280));
    assert.equal(card.hidden,false);
    click(incidental);await settle();assert.equal(profileButton.href,incidental.href);
    keyboard=true;events.get('focusin')({type:'focusin',target:{closest:()=>chosen}});
    await settle();assert.equal(profileButton.href,chosen.href);keyboard=false;
    closeButton.onclick();assert.equal(card.hidden,true);
    hover(chosen);await settle();assert.equal(card.hidden,true);
    events.get('pointermove')({type:'pointermove',pointerType:'mouse',target:{closest:()=>chosen}});
    await settle();assert.equal(profileButton.href,chosen.href);assert.equal(card.hidden,false);
    documentEvents.get('keydown')({key:'Escape'});assert.equal(card.hidden,true);
    assert.equal(events.has('keydown'),false);
  } finally {dispose?.();assert.equal(documentEvents.size,0);globalThis.document=savedDocument;globalThis.fetch=savedFetch;}
});


test('unresolved identities expose candidates and source references on the full profile safely', () => {
 const p={id:'synthetic_one',label:'測試人物',related_people:{synthetic_one:'甲',synthetic_two:'乙'},unresolved_identity_cases:[{note:'<script>不可執行</script>',candidate_person_ids:['synthetic_one','synthetic_two'],paragraph_ids:['c-shiji-095-fankuang:p021'],references:[{title:'史料',quote:'另號孫公主。',url:'https://example.com/source'},{quote:'<img src=x>',url:'javascript:alert(1)'}]}]};
 const html=personCard(p,true);
 assert.match(html,/身份待考/);assert.match(html,/person.html#synthetic_two/);assert.match(html,/https:\/\/example.com\/source/);assert.match(html,/另號孫公主/);
 assert.match(html,/&lt;script&gt;/);assert.doesNotMatch(html,/<script>|javascript:|<img/);
 assert.doesNotMatch(personCard(p),/person-identity-cases/);
 assert.doesNotMatch(personCard({id:'synthetic_none',label:'無未決案'},true),/身份待考/);
});


test('same wording retains office and honorific types without labelling every ordinary title', () => {
 const p={id:'synthetic_teng',label:'測試人物',titles:[{title:'滕公',kind:'office',period:'未定 → 未定'},{title:'滕公',kind:'honorific',period:'未定 → 未定'}]};
 const html=personCard(p,true);assert.match(html,/person-title-kind">官稱/);assert.match(html,/person-title-kind">尊稱/);
 assert.equal((html.match(/class="person-title"/g)||[]).length,2);
 assert.doesNotMatch(personCard({...p,titles:[p.titles[0]]},true),/person-title-kind/);
});

test('name and place reading evidence is readable on the full profile and escapes sources', () => {
 const p={id:'synthetic_general',label:'雍將軍',reading_decisions:[{rationale:'<script>bad</script>',evidence:[{paragraph_id:'c-shiji-095-fankuang:p012'}],references:[{title:'古注',quote:'縣名。',url:'https://example.com/source'},{quote:'<img>',url:'javascript:alert(1)'}]}]};
 const html=personCard(p,true);assert.match(html,/名物辨讀/);assert.match(html,/縣名/);assert.match(html,/https:\/\/example.com\/source/);assert.match(html,/來源原文/);
 assert.doesNotMatch(html,/<script>|<img>|javascript:/);assert.doesNotMatch(personCard(p),/person-reading-evidence/);
});


test('unenacted proposals remain separate from held titles and only appear on the full profile', () => {
 const p={id:'synthetic_proposed',label:'測試人物',title_proposals:[{title:'太子',outcome:'not_enacted',interpretation_note:'<script>提議未行</script>',evidence:[{chapter_id:'c-shiji-096-zhang',paragraph_id:'c-shiji-096-zhang:p005',quote:'<img>欲立而止'}]}]};
 const html=personCard(p,true);assert.match(html,/擬議而未授的稱號/);assert.match(html,/未實行提議/);assert.match(html,/來源原文/);
 assert.doesNotMatch(html,/<script>|<img>|class="person-title"/);
 assert.doesNotMatch(personCard(p),/person-title-proposals/);
 assert.doesNotMatch(personCard({id:'synthetic_none',label:'無提議'},true),/擬議而未授/);
});

test('life summary retains explicit year ranges, source age and reference safety', () => {
 const evidence=[{chapter_id:'c-shiji-096-zhang',paragraph_id:'c-shiji-096-zhang:p014',quote:'孝景前五年，蒼卒。'}];
 const range={earliest:{era:'BCE',era_year:153,year:-152},latest:{era:'BCE',era_year:152,year:-151},references:[{url:'https://example.com/calendar',title:'曆法',quote:'十月為歲首'},{url:'javascript:alert(1)',quote:'<script>bad</script>'}]};
 const p={id:'synthetic_cang',label:'測試人物',life_events:[{person_id:'synthetic_cang',event_type:'death',date_expression:'孝景前五年',normalized_date_range:range,evidence}],age_assertions:[{person_id:'synthetic_cang',value:null,source_term:'百有餘歲',bounds:{lower:100,lower_inclusive:false,upper:null},evidence}]};
 const html=personCard(p,true);assert.match(html,/西元前153至152年（暫定範圍）/);assert.match(html,/孝景前五年/);assert.match(html,/百有餘歲/);assert.match(html,/https:\/\/example.com\/calendar/);
 assert.doesNotMatch(html,/100 歲|享年|<strong>西元前152年<\/strong>|javascript:|<script>/);
});
test('傳說分類在卡片與人物頁明示，缺資料時省略',()=>{
 const p={id:'synthetic_legend',label:'合成傳說人物',historicity:'legendary_tradition'};
 for(const full of [false,true]){
  assert.match(personCard(p,full),/class="person-historicity">傳說敘事人物/);
  assert.doesNotMatch(personCard({...p,historicity:undefined},full),/person-historicity/);
  assert.doesNotMatch(personCard({...p,historicity:'historical_tradition'},full),/person-historicity/);
 }
});
test('未窮盡候選明示於人物頁，不把缺旗標當作完整名單',()=>{
 const c={candidate_person_ids:['synthetic_candidate'],paragraph_ids:[],note:'合成未決案例',candidate_list_exhaustive:false};
 const p={id:'synthetic_reference',label:'合成稱呼',unresolved_identity_cases:[c]};
 assert.match(personCard(p,true),/已列候選人物（未窮盡）/);
 assert.doesNotMatch(personCard({...p,unresolved_identity_cases:[{...c,candidate_list_exhaustive:undefined}]},true),/未窮盡/);
});
test('親屬表格來源回到原格，不冒作正文段落',()=>{
 const e={kind:'table_cell',table_id:'shiji-016',table_cell_id:'shiji-016-t2-r033-c04',quote:'合成表格親屬引文'};
 const p={id:'synthetic_child',label:'合成子',relations:[{subject_person_id:'synthetic_child',object_person_id:'synthetic_parent',predicate:'father',qualifiers:{source_term:'合成關係原詞'},evidence:[e]}]};
 const html=personCard(p,true);
 assert.match(html,/來源表格 →/);
 assert.match(html,/shiji\.html#chapter=16&amp;category=biao&amp;cell=shiji-016-t2-r033-c04/);
 assert.doesNotMatch(html,/passage=undefined|passage=shiji-016/);
 assert.doesNotMatch(personCard({...p,relations:[{...p.relations[0],evidence:[{...e,table_id:'javascript:synthetic'}]}]},true),/href="javascript:/);
});
test('其他作品的主要來源、親屬引用及出現篇章使用實際書名',()=>{
 const e={work_id:'w-hanshu',book_id:'b-hanshu-041',chapter_id:'c-hanshu-041-synthetic',paragraph_id:'synthetic-p',quote:'合成原句'};
 const p={id:'synthetic_person',label:'合成人物',occurrences:[{...e,work_title:'漢書',title:'合成篇',count:2}],relations:[{subject_person_id:'synthetic_person',object_person_id:'synthetic_parent',predicate:'father',evidence:[e]}]};
 const html=personCard(p,true);
 assert.match(html,/《漢書·合成篇》/);assert.match(html,/reader\.html#work=w-hanshu/);
 assert.doesNotMatch(html,/《史記·合成篇》|shiji\.html#chapter=41/);
});
test('稱號首選校讀與來源原字分列，不改其他持職字面',()=>{
 const title={id:'synthetic_holding',title:'合成原字',kind:'noble_rank',evidence:[],effective_period:{start:{status:'unknown'},end:{status:'unknown'}}};
 const p={id:'synthetic_person',label:'合成人物',titles:[title],preferred_title_readings:[{holding_id:'synthetic_holding',source_title:'合成原字',preferred_title:'合成校讀'}]};
 const html=personCard(p,true);
 assert.match(html,/<strong>合成校讀<\/strong>/);assert.match(html,/來源原字：合成原字/);
 assert.equal(title.title,'合成原字');
 assert.match(personCard({...p,preferred_title_readings:[]},true),/<strong>合成原字<\/strong>/);
});

test('稱號時長顯示來源數字與古注，不當生卒或授官年',()=>{
 const title={id:'synthetic-holding',title:'齊相國',period:'起訖未定',evidence:[{quote:'五歲為齊相國。'}],reported_duration:{value:5,unit:'title_year',source_term:'五歲為齊相國'},interpretation_note:'來源持職五歲，起訖未知。',references:[{title:'正義',quote:'爲齊悼惠王劉肥相五歲也。',url:'https://example.org/source'}]};
 const html=personCard({id:'abc_def_123',label:'甲',titles:[title]},true);
 assert.match(html,/原記時長：<strong>5年<\/strong>/);
 assert.match(html,/五歲為齊相國/);assert.match(html,/爲齊悼惠王劉肥相五歲也/);
 assert.doesNotMatch(html,/始於|西元.*5年|年齡/);
});
test('不把時長約數或餘月轉成零或確定時長，跨稱號不重複計數',()=>{
 const t={title:'相',period:'起訖未定',evidence:[],reported_duration:{value:null,unit:'title_month',source_term:'十餘月'},duration_scope:{kind:'multiple_holdings'}};
 const html=personCard({id:'abc_def_123',label:'甲',titles:[t]});
 assert.match(html,/十餘月/);assert.match(html,/涵蓋多項稱號/);assert.doesNotMatch(html,/<strong>0月/);
});
test('同號同起訖的不同來源時長各自保留',()=>{
 const t={title:'相',period:'起訖未定',evidence:[]};
 const html=personCard({id:'abc_def_123',label:'甲',titles:[{...t,reported_duration:{value:5,unit:'title_year',source_term:'相五歲'}},{...t,reported_duration:{value:6,unit:'title_year',source_term:'相六年'}}]});
 assert.match(html,/>5年</);assert.match(html,/>6年</);
});

test('同年數的跨書稱號時長合併呈現，保留兩份原句',()=>{
 const duration={value:5,unit:'title_year',source_number:'五',source_term:'五歲為齊相國',counting:'unspecified_source_years',status:'source_attested'};
 const t={title:'齊相國',period:'起訖未定'};
 const html=personCard({id:'abc_def_123',label:'甲',titles:[{...t,evidence:[{quote:'甲書原句'}],reported_duration:{...duration,evidence:[{quote:'甲書原句'}]}},{...t,evidence:[{quote:'乙書原句'}],reported_duration:{evidence:[{quote:'乙書原句'}],...Object.fromEntries(Object.entries(duration).reverse())}}]},true);
 assert.equal((html.match(/class="person-title-duration"/g)||[]).length,1);assert.match(html,/甲書原句/);assert.match(html,/乙書原句/);
});
test('嗣位依明示前任持職ID解析，不捏造嗣字是爵名，也不繼承官職',()=>{
 const p={id:'child',label:'乙',relations:[{subject_person_id:'child',predicate:'father',object_person_id:'parent',qualifiers:{succession:{source_term:'子乙嗣',predecessor_person_id:'parent',predecessor_holding_id:'source-holding',status:'contextual_provisional',rationale:'明示嗣前爵。'}},evidence:[{quote:'子乙嗣'}]}]};
 const parent={id:'parent',titles:[{id:'source-holding',title:'甲侯',kind:'noble_rank'}]};
 const family={ancestors:[[{id:'parent',label:'甲',person:parent,evidence:[]}],[],[]],mother:[],spouses:[],children:[]};
 const html=personCard(p,true,'main',family);assert.match(html,/來源所記承襲/);assert.match(html,/甲侯/);assert.match(html,/子乙嗣/);
 parent.titles[0].kind='office';assert.doesNotMatch(personCard(p,true,'main',family),/來源所記承襲/);
 assert.equal(p.titles,undefined);
});
test('曾孫來源的反向關係標示曾祖父，不顛倒成曾孫',()=>{
 const html=personCard({id:'child',label:'乙',related_people:{parent:'甲'},relations:[{subject_person_id:'child',predicate:'great_grandfather',object_person_id:'parent',qualifiers:{source_term:'曾孫'},evidence:[]}]},true);
 assert.match(html,/曾祖父/);assert.doesNotMatch(html,/· 曾孫/);
});

test('teaching has a separate linked source section and is excluded from kinship',()=>{
 const p={id:'student',label:'合成學生',related_people:{student:'合成學生',master:'合成老師'},relations:[{subject_person_id:'student',predicate:'teacher',object_person_id:'master',qualifiers:{relationship_basis:'teaching',source_term:'學於合成老師'},evidence:[{quote:'合成學生學於合成老師。'}]}]};
 const html=personCard(p,true);assert.match(html,/class="person-teaching"/);assert.match(html,/受業於/);assert.match(html,/person.html#master/);assert.match(html,/合成學生學於合成老師/);assert.doesNotMatch(html,/來源所記親屬/);
 assert.doesNotMatch(personCard(p),/person-teaching/);
});

test('table name components render known ming, omit unknown surname and link original cell',()=>{
 const html=personCard({id:'synthetic-person',label:'合成人物',name_components:[{title:'合成侯',surname:null,ming:'甲',additional_names:[],kind:'table_cell',table_id:'shiji-018',table_cell_id:'synthetic-name-cell',quote:'合成甲原文',note:'合成測試資料'}]},true);
 assert.match(html,/<h1>合成侯 甲<\/h1>/);assert.match(html,/姓名依據/);assert.match(html,/chapter=18&amp;category=biao&amp;cell=synthetic-name-cell/);assert.doesNotMatch(html,/null甲|undefined甲/);
});

test('reported age shows its editorial year window without a birth year',()=>{
 const p={id:'abc_def_123',label:'測試人物',age_assertions:[{person_id:'abc_def_123',value:62,date_expression:'七國之發',normalized_date_range:{earliest:{era:'BCE',era_year:155,year:-154},latest:{era:'BCE',era_year:154,year:-153}},evidence:[]}]};
 const html=personCard(p,true);assert.match(html,/西元前155至154年/);assert.match(html,/報齡時/);assert.match(html,/七國之發/);assert.doesNotMatch(html,/<dt>生<\/dt>/);
});

test('received kinship people link directly to profiles and retain literal source evidence',()=>{
 const p={id:'abc_def_123',label:'張羽',related_people:{abc_def_123:'張羽',xyz_abc_456:'張尚'},relations:[{subject_person_id:'abc_def_123',predicate:'brother',object_person_id:'xyz_abc_456',qualifiers:{source_term:'楚死事相弟張羽'},evidence:[{quote:'楚死事相弟張羽'}]}]};
 const html=personCard(p,true);assert.match(html,/<a class="person-kinship-link" href="person.html#xyz_abc_456">張尚<\/a>/);assert.match(html,/<a class="person-kinship-link" href="person.html#abc_def_123">張羽<\/a>/);assert.match(html,/楚死事相弟張羽/);assert.doesNotMatch(personCard(p,false),/person-kinship-link/);
});

test('compact title summary shows attested periods while full profile retains undated sources',()=>{
 const p={id:'abc_def_123',label:'測試人物',titles:[{title:'吳王',kind:'royal_rank',period:'未定 → 未定',evidence:[]},{title:'沛侯',kind:'noble_rank',period:'未定 → 未定',evidence:[]},{title:'吳王',kind:'royal_rank',period:'西元前196至195年（暫定範圍） → 未定',evidence:[]}]};
 const compact=personCard(p,false),full=personCard(p,true);assert.match(compact,/西元前196至195年/);assert.equal((compact.match(/<strong>吳王<\/strong>/g)||[]).length,1);assert.equal((full.match(/<strong>吳王<\/strong>/g)||[]).length,2);assert.match(compact,/沛侯/);
});

test('生卒首選與異說範圍保留並展示古注依據',()=>{
 setLocale('zh-Hant',{persist:false});
 const p=JSON.parse(readFileSync(new URL('../data/corpus/profiles/nuf_tb9_fjs_A.json',import.meta.url),'utf8'));const html=personCard(p,true);
 assert.match(html,/data-event-id="le-hanshu006-003" data-choice="preferred"/);assert.match(html,/data-event-id="le-shiji107-003" data-choice="alternative"/);assert.match(html,/西元前132至131年/);assert.match(html,/西元前131至130年/);assert.match(html,/按：五年者，誤也。/);assert.match(html,/oldid=2514777/);
});
test('紀年狀態可切英文，取捨參考拒絕腳本連結並轉義引文',()=>{
 const p=JSON.parse(readFileSync(new URL('../data/corpus/profiles/nuf_tb9_fjs_A.json',import.meta.url),'utf8'));const d=p.life_event_date_decisions.find(d=>d.id==='ld-shiji107-death-001');d.references=[{url:'javascript:alert(1)',quote:'<script>synthetic</script>',title:'synthetic'}];setLocale('en',{persist:false});let html=personCard(p,true);assert.match(html,/Provisional preferred date/);assert.doesNotMatch(html,/href="javascript:/);assert.match(html,/&lt;script&gt;synthetic&lt;\/script&gt;/);d.status='unresolved';d.preferred_event_id=null;html=personCard(p,true);assert.match(html,/Date choice unresolved/);setLocale('zh-Hant',{persist:false});
});

test('distinct people retain separate profile links and escaped source evidence',()=>{
 const p={id:'abc_def_123',label:'王恢',names:[],person_ids:['abc_def_123'],related_people:{xyz_abc_456:'另一王恢<script>'},identity_distinctions:[{id:'d',person_ids:['abc_def_123','xyz_abc_456'],rationale:'不同人<理由>',evidence:[{chapter_id:'c-shiji-108-han',paragraph_id:'c-shiji-108-han:p010',quote:'王恢自殺<script>'}]}]};
 setLocale('zh-Hant');const html=personCard(p,true);assert.match(html,/同名異人/);assert.match(html,/person.html#xyz_abc_456/);assert.match(html,/另一王恢&lt;script&gt;/);assert.match(html,/王恢自殺&lt;script&gt;/);assert.match(html,/chapter=108/);assert.doesNotMatch(html,/<script>/);assert.doesNotMatch(personCard(p),/person-identity-distinctions/);
 setLocale('en');assert.match(personCard(p,true),/Distinct people/);setLocale('zh-Hant');
});
test('people without distinction data omit the section',()=>{
 assert.doesNotMatch(personCard({id:'abc_def_123',label:'某人',names:[]},true),/person-identity-distinctions/);
 assert.doesNotMatch(personCard({id:'abc_def_123',label:'某人',names:[],identity_distinctions:[]},true),/person-identity-distinctions/);
});

test('native table profile links only the matching fixed witness and rejects unsafe URLs', () => {
 const evidence={kind:'table_cell',table_id:'shiji-022',table_cell_id:'synthetic-cell',work_id:'w-shiji',book_id:'b-shiji-022',chapter_id:'table-chapter-shiji-022',source_id:'synthetic-witness',source_revision:'42',quote:'synthetic quotation'};
 const witness={work_id:evidence.work_id,book_id:evidence.book_id,chapter_id:evidence.chapter_id,source_id:evidence.source_id,source:{revision:'42',revision_url:'https://example.com/?oldid=42'}};
 const profile={id:'abc_def_123',label:'synthetic person',name_components:[{...evidence,title:'synthetic rank',ming:'synthetic name'}],sources:[witness]};
 setLocale('zh-Hant');assert.match(personCard(profile,true),/person-fixed-table-source/);assert.match(personCard(profile,true),/固定來源版本/);
 setLocale('en');assert.match(personCard(profile,true),/Fixed source revision/);setLocale('zh-Hant');
 for(const change of [{source:{...witness.source,revision:'43'}},{chapter_id:'different-chapter'},{source:{revision:'42',revision_url:'javascript:alert(1)'}}]){
  assert.doesNotMatch(personCard({...profile,sources:[{...witness,...change}]},true),/class="person-fixed-table-source"/);
 }
});

test('cross-cell family evidence keeps parent label and child name as separate quotations and links', () => {
 const e={kind:'table_cell',table_id:'shiji-021',table_cell_id:'synthetic-parent-cell',subject_table_cell_id:'synthetic-child-cell',quote:'synthetic parent label <tag>',subject_quote:'synthetic child name <tag>'};
 const family={ancestors:[[{id:'xyz_abc_456',label:'synthetic father',evidence:[e]}],[],[]],mother:[],spouses:[],children:[]};
 const profile={id:'abc_def_123',label:'synthetic child'};
 setLocale('zh-Hant');const html=personCard(profile,true,'main',family);
 assert.match(html,/synthetic parent label &lt;tag&gt;/);assert.match(html,/class="person-table-subject-quote"/);assert.match(html,/synthetic child name &lt;tag&gt;/);assert.match(html,/cell=synthetic-parent-cell/);assert.match(html,/cell=synthetic-child-cell/);assert.match(html,/同列姓名/);assert.doesNotMatch(html,/<tag>/);
 setLocale('en');assert.match(personCard(profile,true,'main',family),/Name in same row/);setLocale('zh-Hant');
});

test('name evidence displays the chosen source as well as the separately marked alternative', () => {
 const n={title:'synthetic title',ming:'synthetic name',quote:'synthetic received sentence',note:'synthetic preference reason',references:[{quote:'chosen component quote <tag>',title:'chosen source',url:'https://example.com/chosen'},{quote:'unsafe source quote',url:'javascript:alert(1)'}],component_alternatives:[{components:{surname:'synthetic surname',ming:'synthetic alternative'},reference:{quote:'alternative component quote',title:'alternative source',url:'https://example.com/alternative'}}]};
 const html=personCard({id:'abc_def_123',label:'synthetic person',name_components:[n]},true);
 assert.match(html,/chosen component quote &lt;tag&gt;/);assert.match(html,/href="https:\/\/example.com\/chosen"/);assert.match(html,/alternative component quote/);assert.match(html,/未採為預設/);assert.doesNotMatch(html,/href="javascript:|<tag>/);
});

// Synthetic title-use records: they do not assert historical facts.
test('source title use shows a date window without inventing effective tenure', () => {
 const a={date_expression:'元封二年',normalized_date_range:{earliest:{era:'BCE',era_year:110},latest:{era:'BCE',era_year:109}}};
 const html=titleUsageHTML([{attestation:a}]);assert.match(html,/來源用稱/);assert.match(html,/元封二年/);assert.match(html,/110至109/);assert.doesNotMatch(html,/始於|止於|用稱紀年依據/);
 assert.equal(titleUsageHTML([{attestation:{}}]),'');
});
test('source title use deduplicates matching evidence and escapes untrusted text and links', () => {
 const u={attestation:{date_expression:'<img>',normalized_date:{era:'BCE',era_year:109,references:[{quote:'<script>',url:'javascript:alert(1)',title:'unsafe'}]}},evidence:[{quote:'<svg>',chapter_id:'c-shiji-115-chaoxian',paragraph_id:'c-shiji-115-chaoxian:p003'}]};
 const html=titleUsageHTML([u,u],true);assert.equal((html.match(/class="person-title-usage"/g)||[]).length,1);assert.match(html,/&lt;img&gt;/);assert.match(html,/&lt;svg&gt;/);assert.match(html,/&lt;script&gt;/);assert.doesNotMatch(html,/href="javascript:/);assert.match(html,/chapter=115/);
});
test('grouped titles preserve each source use and keep grant records separate', () => {
 const title=expression=>({title:'測試官',kind:'office',mode:'attestation',period:'未定 → 未定',attestations:[{date_expression:expression}],evidence:[]});
 const p={id:'abc_def_123',label:'測試人物',titles:[title('甲年'),title('乙年')]};
 const html=personCard(p,true);assert.match(html,/來源用稱：甲年/);assert.match(html,/來源用稱：乙年/);assert.doesNotMatch(html,/始於|止於/);
 assert.doesNotMatch(personCard({...p,titles:[{...title('甲年'),mode:'grant'}]},true),/來源用稱/);
});

test('source title use keeps fixed table witness links on the full profile', () => {
 const source={source_id:'synthetic-table-source',work_id:'w-shiji',source:{revision:123,revision_url:'https://example.org/fixed-table?oldid=123'}};
 const evidence={kind:'table_cell',table_id:'shiji-020',table_cell_id:'synthetic-cell',source_id:source.source_id,work_id:'w-shiji',source_revision:123,quote:'合成用稱原文'};
 const p={id:'abc_def_123',label:'合成人物',sources:[source],titles:[{title:'合成稱號',mode:'attestation',period:'未定 → 未定',attestations:[{date_expression:'合成年'}],evidence:[evidence]}]};
 const html=personCard(p,true);assert.match(html,/來源用稱：合成年/);assert.match(html,/class="person-fixed-table-source" href="https:\/\/example.org\/fixed-table\?oldid=123"/);
});

test('agreed appointment with unreported outcome is shown separately from actual titles', () => {
 const proposal={title:'令',proposal_kind:'agreed_appointment',outcome:'not_reported',interpretation_note:'合成安排，不推履任。',evidence:[{quote:'合成約定使其子為令',chapter_id:'c-shiji-116-xinanyi',paragraph_id:'c-shiji-116-xinanyi:p003'}]};
 const p={id:'abc_def_123',label:'合成未名者',title_proposals:[proposal]};const html=personCard(p,true);
 assert.match(html,/person-appointment-arrangements/);assert.match(html,/實行情況未載/);assert.match(html,/合成約定使其子為令/);assert.match(html,/chapter=116/);assert.doesNotMatch(html,/class="person-title"|擬議而未授/);
 assert.doesNotMatch(personCard(p),/person-appointment-arrangements/);assert.doesNotMatch(personCard({...p,title_proposals:[]},true),/person-appointment-arrangements/);
});
test('agreed appointment evidence and notes are escaped', () => {
 const html=personCard({id:'abc_def_123',label:'合成人物',title_proposals:[{title:'<img>',proposal_kind:'agreed_appointment',outcome:'not_reported',interpretation_note:'<script>',evidence:[{quote:'<svg>'}]}]},true);
 assert.match(html,/&lt;img&gt;/);assert.match(html,/&lt;script&gt;/);assert.match(html,/&lt;svg&gt;/);assert.doesNotMatch(html,/<script>|<svg>|<img>/);
});
test('textual variant study references retain scope and do not invent dates', () => {
 const v={received_reading:'甲',reported_reading:'乙',commentator:'合成注家',quote:'合成引句',url:'https://example.org/primary',study_references:[{display_title:'合成考證',display_author:'合成作者',url:'https://example.org/study',publication_year:null,reviewed_scope:'只讀摘頁',opinion_validation:'not_attempted'}]};
 const p={id:'abc_def_123',label:'合成人物',reported_variants:[v]};const html=personCard(p,true);assert.match(html,/person-study-references/);assert.match(html,/合成考證/);assert.match(html,/只讀摘頁/);assert.match(html,/研究意見未獨立驗證/);assert.doesNotMatch(html,/（null）/);
 v.study_references=[{display_title:'<svg>',url:'javascript:alert(1)',reference_note:'<script>'}];const safe=personCard(p,true);assert.match(safe,/&lt;svg&gt;/);assert.match(safe,/&lt;script&gt;/);assert.doesNotMatch(safe,/href="javascript:/);
});
test('courtesy and early given names have typed labels and retain source characters in both languages', () => {
 const n={title:null,surname:'司馬',ming:'相如',zi:'長卿',former_ming:'犬子',additional_names:['長卿','犬子']};const p={id:'abc_def_123',label:'合成測試',name_components:[n]};
 try {
  setLocale('zh-Hant');const zh=personCard(p,true);assert.match(zh,/<h1>司馬相如<\/h1>/);assert.match(zh,/data-i18n="Courtesy name">字/);assert.match(zh,/data-i18n="Former given name">初名/);assert.match(zh,/長卿/);assert.match(zh,/犬子/);
  setLocale('en');const en=personCard(p,true);assert.match(en,/Courtesy name/);assert.match(en,/Former given name/);assert.match(en,/<h1>司馬相如<\/h1>/);assert.match(en,/長卿/);assert.match(en,/犬子/);assert.equal(n.additional_names[0],'長卿');
 } finally {setLocale('zh-Hant');}
});
test('an untyped alias does not invent courtesy or earlier-name labels and remains escaped', () => {
 const html=personCard({id:'abc_def_123',label:'合成人物',name_components:[{surname:null,ming:'某',additional_names:['<img>']} ]},true);assert.match(html,/&lt;img&gt;/);assert.doesNotMatch(html,/<img>|data-i18n="Courtesy name"|data-i18n="Former given name"/);
});

test('unrelated pointer exits and stale hide timers cannot close a newly hovered person', async()=>{
  const saved={document:globalThis.document,fetch:globalThis.fetch,setTimeout:globalThis.setTimeout,clearTimeout:globalThis.clearTimeout};
  const events=new Map(),pending=new Map();let sequence=0;
  const button={focus(){}},profile={};
  const card={hidden:true,setAttribute(){},remove(){},contains(n){return n===this;},querySelector(s){return s==='.person-profile-button'?profile:button;}};
  const root={append(){},addEventListener(k,v){events.set(k,v);},removeEventListener(){}};
  const node=id=>({dataset:{personId:id},href:'person.html#'+id,matches:()=>false});
  const first=node('synthetic_timer_first'),next=node('synthetic_timer_next');
  const hover=n=>events.get('pointerover')({type:'pointerover',pointerType:'mouse',target:{closest:()=>n}});
  const exit=n=>events.get('pointerout')({pointerType:'mouse',target:{closest:()=>n},relatedTarget:null});
  const settle=()=>new Promise(resolve=>setImmediate(resolve));
  let dispose;
  globalThis.document={createElement:()=>card};globalThis.fetch=async url=>({ok:true,json:async()=>({id:decodeURIComponent(url.split('/').pop().slice(0,-5)),label:'synthetic person'})});
  globalThis.setTimeout=callback=>{const id=++sequence;pending.set(id,callback);return id;};globalThis.clearTimeout=id=>pending.delete(id);
  try {
    dispose=bindPersonCards(root);
    exit(null);exit(null);assert.equal(pending.size,0,'summary exits must not start person-card timers');
    hover(first);await settle();exit(first);exit(first);assert.equal(pending.size,1,'successive exits share one cancellable timer');
    hover(next);await settle();for(const callback of pending.values())callback();
    assert.equal(card.hidden,false);assert.equal(profile.href,next.href);
  } finally {dispose?.();Object.assign(globalThis,saved);}
});

test('approximate source ages are labelled as approximations in both interface languages',()=>{
 const p={id:'synthetic-person',label:'合成人',age_assertions:[{person_id:'synthetic-person',value:null,source_number:'七八',source_term:'皆七八歲',approximation:{kind:'adjacent_age_numbers',numbers:[7,8]},evidence:[{paragraph_id:'synthetic-paragraph',quote:'合成測試：皆七八歲'}]}]};const before=JSON.stringify(p);
 try {
  for(const full of [false,true]){
   setLocale('zh-Hant');let html=personCard(p,full);assert.match(html,/七八歲（<span[^>]*data-i18n="Source age approximation"[^>]*>來源約數/);assert.match(html,/合成測試：皆七八歲/);assert.doesNotMatch(html,/7[–-]8|享年|出生年/);
   setLocale('en');html=personCard(p,full);assert.match(html,/Source age approximation/);assert.match(html,/七八歲/);
  }
 }finally{setLocale('zh-Hant');}
 assert.equal(JSON.stringify(p),before);
});

test('unsegmented source names render whole with original spelling below, without invented components',()=>{
 const p={id:'synthetic-person',label:'合成舊標籤',name_components:[{full_name:'合成姓名',surname:null,ming:null,title:null,additional_names:['合成異文'],quote:'合成史料引句',references:[],note:'不拆姓與名'}]};const before=JSON.stringify(p);
 for(const full of [false,true]){const html=personCard(p,full);assert.match(html,new RegExp('<h'+(full?1:3)+'>合成姓名</h'));assert.match(html,/person-aliases/);assert.match(html,/合成異文/);assert.doesNotMatch(html,/null|undefined/);}
 assert.equal(JSON.stringify(p),before);
});

test('acting office is explicit and kept separate from an undifferentiated office',()=>{
 const source=JSON.parse(readFileSync(new URL('../corpus/shiji/118-titles.json',import.meta.url),'utf8'));
 const acting=source.holdings.find(h=>h.id==='th-shiji118-fengjing-acting-yushi');const regular={...acting,id:'synthetic-regular',appointment_role:undefined,punctuation_attribution:undefined};
 const p={id:'synthetic-person',label:'合成測試',titles:[acting,regular]};const html=personCard(p,true);assert.equal((html.match(/class="person-title"/g)||[]).length,2);assert.match(html,/person-acting-office/);assert.match(html,/代理任事/);assert.match(html,/官職句讀判讀/);assert.match(html,/典客臣馮敬行御史大夫事、宗正臣逸/);assert.match(html,/683113d4baf6febecaf2ccb7913df87c4d68d454/);
 assert.doesNotMatch(personCard(p),/person-office-attribution/);
});
test('office punctuation evidence escapes text and refuses script URLs',()=>{
 const a={received_segment:'<script>bad</script>',preferred_segmentation:'<img>',rationale:'<b>',references:[{url:'javascript:alert(1)',quote:'<svg>',title:'<i>'}]};const html=personCard({id:'synthetic-person',label:'合成測試',titles:[{title:'合成官',appointment_role:'acting',punctuation_attribution:a,evidence:[]}]},true);assert.match(html,/&lt;script&gt;/);assert.match(html,/&lt;svg&gt;/);assert.doesNotMatch(html,/href="javascript:|<img>|<svg>/);
});
test('acting label changes language without translating source office wording',()=>{
 try{setLocale('en');const html=personCard({id:'synthetic-person',label:'合成測試',titles:[{title:'御史大夫',appointment_role:'acting'}]});assert.match(html,/Acting appointment/);assert.match(html,/御史大夫/);}finally{setLocale('zh-Hant');}
});

test('title chronology retains a readable alternative chapter and fixed primary evidence',()=>{
 const data=JSON.parse(readFileSync(new URL('../corpus/shiji/118-titles.json',import.meta.url),'utf8'));const h=data.holdings.find(h=>h.id==='th-shiji118-xi-chengyang-return');const p={id:'synthetic-person',label:'合成測試',titles:[h]};const html=personCard(p,true);assert.match(html,/稱號紀年來源判讀/);assert.match(html,/孝文十六年/);assert.match(html,/四年，復還王城陽/);assert.match(html,/chapter=52/);assert.match(html,/KR2a0007_038/);assert.doesNotMatch(personCard(p),/person-title-chronology-choice/);
});
test('title chronology escapes source alternatives and rejects executable links',()=>{
 const c={preferred_source_expression:'<x>',alternative_source_term:'<img>',alternative_evidence:{quote:'<svg>'},rationale:'<script>',references:[{quote:'<iframe>',url:'javascript:alert(1)',title:'bad'}]};const html=personCard({id:'synthetic-person',label:'合成測試',titles:[{title:'王',evidence:[],chronology_source_choice:c}]},true);assert.match(html,/&lt;img&gt;/);assert.match(html,/&lt;iframe&gt;/);assert.doesNotMatch(html,/href="javascript:|<svg>|<img>/);
});

test('unadopted distant ancestry remains readable as a source claim on the full profile',()=>{
 const p={id:'synthetic-child',label:'Synthetic child',related_people:{'synthetic-ancestor':'Synthetic remote ancestor'},relations:[{subject_person_id:'synthetic-child',object_person_id:'synthetic-ancestor',predicate:'ancestor',qualifiers:{adopted_for_family_tree:false,source_term:'Synthetic received genealogy claim'},evidence:[{quote:'Synthetic received genealogy claim'}]}]};
 const html=personCard(p,true);
 assert.match(html,/person-unadopted-ancestry/);
 assert.match(html,/Synthetic remote ancestor/);
 assert.match(html,/Synthetic received genealogy claim/);
 assert.doesNotMatch(html,/class="person-family"/);
});
