import {readFileSync} from 'node:fs';
import {expandProfile, indexPassageDocument} from '../assets/passage-refs.js';

const documents = new Map();
export function storedProfile(profile) {
  return expandProfile(profile, path => {
    if (!documents.has(path)) {
      const url = new URL('../' + path, import.meta.url);
      documents.set(path, indexPassageDocument(JSON.parse(readFileSync(url, 'utf8'))));
    }
    return documents.get(path);
  });
}
