import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {readingWitnessBadge, readingWitnessNote} from '../assets/reading-witness.js';
import {volumeModel, volumeLanding, volumeNavigation} from '../assets/volume-directory.js';

test('older data and unknown role do not acquire an invented edition label', () => {
  assert.equal(readingWitnessBadge({}), '');
  assert.equal(readingWitnessNote({reading_role:'<script>'}), '');
});

test('preferred selection has a separate edition badge and qualified rationale', () => {
  const html=readingWitnessNote({reading_role:'preferred_received_selection',
    edition_label:'合成武英殿版名',reading_preference_note:'合成選錄，仍待覆核。'});
  assert.match(html,/首選轉錄/);
  assert.match(html,/合成武英殿版名/);
  assert.match(html,/閱讀首選僅涵蓋所列選錄/);
  assert.match(html,/合成選錄，仍待覆核/);
});

test('comparison with unknown base is visibly labelled without pretending to be Siku', () => {
  const html=readingWitnessNote({reading_role:'comparison_transcription',edition_id:null});
  assert.match(html,/比較轉錄/);
  assert.match(html,/底本待核/);
  assert.doesNotMatch(html,/武英殿|四庫|首選轉錄/);
});

test('edition labels and editorial rationale are escaped', () => {
  const html=readingWitnessNote({reading_role:'preferred_received_selection',
    edition_label:'<img src=x onerror=alert(1)>',reading_preference_note:'<script>alert(1)</script>'});
  assert.doesNotMatch(html,/<img|<script/);
  assert.match(html,/&lt;img/);
  assert.match(html,/&lt;script/);
});

test('volume entries expose witness roles while the official citation title stays unchanged', () => {
  const directory={schema_version:1,works:[{work_id:'w-test',title:'合成書',books:[
    {book_id:'b-test-001',number:1,title:'卷一',citation_title:'合成篇',category:'列傳'}]}]};
  const base={work_id:'w-test',book_id:'b-test-001',chapter_id:'c-test',number:1,
    title:'合成篇',path:'data/corpus/test/001.json',available:'marked_text',text_scope:'partial_chapter'};
  const plain=volumeModel(directory,'w-test',{chapters:[base]});
  const marked=volumeModel(directory,'w-test',{chapters:[{...base,
    reading_role:'preferred_received_selection',edition_label:'合成版名',selection_label:'實際選錄範圍'}]});
  assert.equal(volumeLanding(marked,'b-test-001').title,volumeLanding(plain,'b-test-001').title);
  assert.match(volumeLanding(marked,'b-test-001').html,/合成版名/);
  assert.match(volumeLanding(marked,'b-test-001').html,/選錄範圍[^<]*<[^>]+>.*實際選錄範圍|選錄範圍.*實際選錄範圍/);
  assert.match(volumeNavigation(marked),/data-reading-role="preferred_received_selection"/);
});

test('both reader entry points use the same witness presentation', () => {
  for (const file of ['corpus-view.js','shiji-view.js']) {
    const text=fs.readFileSync(new URL('../assets/'+file,import.meta.url),'utf8');
    assert.match(text,/import \{readingWitnessNote\} from '\.\/reading-witness\.js'/);
    assert.match(text,/readingWitnessNote\((selected|entry)\)/);
  }
});
