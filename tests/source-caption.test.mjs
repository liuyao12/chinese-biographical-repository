import test from 'node:test';
import assert from 'node:assert/strict';
import {sourceCaption} from '../assets/source-caption.js';
test('citation captions preserve plain titles and remove only exact leading work title',()=>{
 assert.equal(sourceCaption('史記','秦始皇本紀'),'《史記·秦始皇本紀》');
 assert.equal(sourceCaption('三國志','《三國志》魏書卷二十二（編輯選錄題）'),'《三國志·魏書卷二十二（編輯選錄題）》');
 assert.equal(sourceCaption('三國志','《漢書》卷二十二'),'《三國志·《漢書》卷二十二》');
 assert.equal(sourceCaption('史記','前言《史記》'),'《史記·前言《史記》》');
});
