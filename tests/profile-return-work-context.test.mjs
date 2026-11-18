import test from 'node:test';
import assert from 'node:assert/strict';
import {profileReturnLink} from '../assets/profile-return.js';

const person = {
  occurrences:[
    {number:4,category:'liezhuan',paragraph_id:'c-shiji-004-some:p001'},
    {work_id:'w-songshu',book_id:'b-songshu-052',chapter_id:'4',
      paragraph_id:'songshu-p1',paragraph_ids:['songshu-p1'],title:'王誕傳',work_title:'宋書'}
  ]
};

test('numeric chapter from another work never routes to a matching Shiji volume', () => {
  const route = profileReturnLink(person, new URLSearchParams({
    work:'w-songshu',book:'b-songshu-052',chapter:'4',passage:'songshu-p1'
  }));
  assert.match(route.href,/^reader\.html#/);
  const params = new URLSearchParams(route.href.split('#')[1]);
  assert.equal(params.get('work'),'w-songshu');
  assert.equal(params.get('book'),'b-songshu-052');
  assert.equal(params.get('chapter'),'4');
  assert.equal(params.get('passage'),'songshu-p1');
});

test('explicit Shiji context still routes to its Shiji chapter', () => {
  const route = profileReturnLink(person, new URLSearchParams({
    work:'w-shiji',chapter:'4',passage:'c-shiji-004-some:p001'
  }));
  assert.match(route.href,/^shiji\.html#/);
  const params = new URLSearchParams(route.href.split('#')[1]);
  assert.equal(params.get('chapter'),'4');
  assert.equal(params.get('passage'),'c-shiji-004-some:p001');
});

test('empty source context returns to the CBR directory despite other occurrences', () => {
  assert.deepEqual(profileReturnLink(person,new URLSearchParams()),{
    href:'cbr.html',text:'返回 CBR 人物目錄 →'
  });
});

test('no valid source context returns to the CBR person directory', () => {
  assert.deepEqual(profileReturnLink(person,new URLSearchParams({work:'w-weishu',chapter:'12'})),{
    href:'cbr.html',text:'返回 CBR 人物目錄 →'
  });
});
