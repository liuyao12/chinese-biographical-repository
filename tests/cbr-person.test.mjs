import test from 'node:test';
import assert from 'node:assert/strict';
import {markCell, personCard, profileURL, tableOccurrenceURL, personBundleURL, bindPersonCards} from '../assets/cbr-person.js';
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
    events.get('pointerover')({type:'pointerover',pointerType:'mouse',target});assert.equal(card.hidden,false);
  } finally {dispose?.();globalThis.document=savedDocument;globalThis.fetch=savedFetch;}
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
