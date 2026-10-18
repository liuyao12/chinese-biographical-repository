import test from 'node:test';
import assert from 'node:assert/strict';
import {personCardPosition} from '../assets/cbr-person.js';

function check(anchor, viewport, width, height) {
  const card = personCardPosition(anchor, viewport, width, height);
  const bottom = card.top + Math.min(height, card.maxHeight);
  const right = card.left + card.width;
  assert.ok(card.left >= 16 && card.top >= 16);
  assert.ok(right <= viewport.width - 16 + 1e-6);
  assert.ok(bottom <= viewport.height - 16 + 1e-6);
  assert.ok(right <= anchor.left || card.left >= anchor.right || bottom <= anchor.top || card.top >= anchor.bottom,
    'The profile card must not cover the triggering name');
  return card;
}

test('Sima An measured name remains reachable after loading the full card', () => {
  const anchor = {left:1016.875, right:1074.484375, top:104.015625, bottom:131.015625};
  check(anchor, {width:1400, height:1000}, 432, 800.328125);
});

test('desktop and phone card placement stays visible without covering names', () => {
  for (const viewport of [{width:1400,height:1000}, {width:390,height:1000}, {width:320,height:480}]) {
    for (const x of [20, viewport.width / 2, viewport.width - 85]) {
      for (const y of [50, viewport.height / 2, viewport.height - 60]) {
        for (const height of [48, 800]) {
          check({left:x,right:x+60,top:y,bottom:y+27}, viewport, Math.min(432,viewport.width-32),height);
        }
      }
    }
  }
});

test('wrapped names and short viewports use remaining vertical space', () => {
  check({left:268,right:1130,top:84,bottom:138}, {width:1400,height:1000},432,800);
  check({left:120,right:200,top:100,bottom:127}, {width:320,height:240},288,500);
});
