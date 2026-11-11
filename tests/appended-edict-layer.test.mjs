import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import test from 'node:test';
import {commentaryControls, layerInfo, layerParagraph} from '../assets/commentary-layers.js';

const chapter = JSON.parse(await readFile(new URL('../corpus/shiji/112.json', import.meta.url), 'utf8'));
const edict = chapter.paragraphs.find(paragraph => paragraph.text_layer === 'witness_appended_edict');

test('後附詔書作為來源附層呈現，正文逐字不改', () => {
  assert.ok(edict, 'fixture contains the source-recorded appended edict');
  assert.equal(layerInfo(edict)?.[0], 'edict');
  const rendered = layerParagraph(edict, `<p data-source-text>${edict.text}</p>`);
  assert.match(rendered, /data-commentary-group="edict"/);
  assert.match(rendered, /見證附載詔書|Appended edict \(source witness\)/);
  assert.ok(rendered.includes(`<p data-source-text>${edict.text}</p>`));
  assert.match(commentaryControls({paragraphs: [edict]}), /data-commentary-toggle="edict"/);
});

