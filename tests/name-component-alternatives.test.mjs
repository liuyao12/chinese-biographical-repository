import test from 'node:test';
import assert from 'node:assert/strict';
import {personCard} from '../assets/cbr-person.js';
import {setLocale} from '../assets/i18n.js';
const source={quote:'安國姓也少季名也',title:'合成測試來源',url:'https://example.com/source'};
const fixture=()=>({id:'abc_def_123',label:'安國少季',names:[],name_components:[{surname:'安國',ming:null,zi:'少季',additional_names:['字少季'],quote:'合成來源文字',note:'兩說並存。',component_alternatives:[{components:{surname:'安國',ming:'少季',zi:null},reference:source,status:'source_claim_not_selected'}]}]});
test('name components show separately cited alternative while retaining preferred heading',()=>{
 setLocale('zh-Hant');const html=personCard(fixture(),true);assert.match(html,/<h1>安國<\/h1>/);assert.match(html.replace(/<[^>]*>/g,''),/字 少季/);assert.match(html,/姓名組件另說/);assert.match(html,/安國姓也少季名也/);assert.match(html,/https:\/\/example.com\/source/);assert.match(html,/未採為預設/);
 setLocale('en');const english=personCard(fixture(),true);assert.match(english,/Name component alternative/);assert.match(english,/Not selected as default/);assert.match(english,/安國姓也少季名也/);setLocale('zh-Hant');
});
test('alternative source values are escaped and non-web links are omitted',()=>{
 const p=fixture();p.name_components[0].component_alternatives[0]={components:{ming:'<script>bad</script>'},reference:{quote:'<img src=x>',url:'javascript:bad'}};const html=personCard(p,true);assert.match(html,/&lt;script&gt;/);assert.match(html,/&lt;img src=x&gt;/);assert.doesNotMatch(html,/href="javascript:/);assert.doesNotMatch(html,/<script>/);
});
