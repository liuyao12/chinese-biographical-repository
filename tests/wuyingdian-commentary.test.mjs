import test from 'node:test';import assert from 'node:assert/strict';
import {layerInfo,commentaryControls,layerParagraph} from '../assets/commentary-layers.js';
test('Wuyingdian collation keeps its own attribution and independent control',()=>{
 const w={id:'w',text_layer:'witness_appended_wuyingdian_collation'},s={id:'s',text_layer:'witness_appended_qing_siku_collation'};assert.notEqual(layerInfo(w),layerInfo(s));assert.equal(layerInfo(w)[2],'武英殿考證');assert.equal((commentaryControls({paragraphs:[w,s]}).match(/type="checkbox"/g)||[]).length,2);assert.ok(layerParagraph(w,'<p data-source-text>原文</p>').includes('data-commentary-group="wuyingdian"'));assert.ok(!layerParagraph(w,'<p data-source-text>原文</p>').includes('四庫考證'));
});
