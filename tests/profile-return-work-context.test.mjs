import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {profileSourceContext} from '../assets/corpus-reader.js';

test('a numeric non-Shiji chapter is routed by work context before Shiji volume matching', async () => {
  const source = await readFile(new URL('../assets/cbr-person-page.js', import.meta.url), 'utf8');
  const guard = source.indexOf("if (!workId || workId === 'w-shiji')");
  const shijiMatch = source.indexOf("const shijiOccurrence =", guard);
  const shijiGuardEnd = source.indexOf("\n  }\n\n  const otherSource = profileSourceContext(person, context);", shijiMatch);
  assert.ok(guard >= 0 && shijiMatch > guard && shijiGuardEnd > shijiMatch,
    'Shiji volume matching must be scoped to an absent or explicit w-shiji context');

  const person = {occurrences:[
    {work_id:'w-shiji',book_id:'b-shiji-004',chapter_id:'4',paragraph_id:'shiji-p1',number:4,category:'liezhuan'},
    {work_id:'w-songshu',book_id:'b-songshu-052',chapter_id:'52',paragraph_id:'songshu-p1',title:'王誕傳',work_title:'宋書'}
  ]};
  const back = profileSourceContext(person, new URLSearchParams({
    work:'w-songshu',book:'b-songshu-052',chapter:'52',passage:'songshu-p1'
  }));
  assert.ok(back);
  const params = new URLSearchParams(back.href.split('#')[1]);
  assert.equal(params.get('work'),'w-songshu');
  assert.equal(params.get('chapter'),'52');
});
