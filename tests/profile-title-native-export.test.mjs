import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {personCard} from '../assets/cbr-person.js';
import {profileTitlePreference} from '../assets/profile-title.js';
import {directoryDisplay} from '../assets/corpus-discovery.js';
const root=fileURLToPath(new URL('../',import.meta.url));
// Override is only for a private read-only candidate proof; normal tests use this repo.
const sourceRoot=process.env.CBR_INTEGRATION_SOURCE_ROOT||root;
let sourceCase;
function actualCase(){
 if(sourceCase)return sourceCase;
 const result=spawnSync(process.env.PYTHON||'python3',[fileURLToPath(new URL('./profile-title-native-export-case.py',import.meta.url)),sourceRoot],{cwd:sourceRoot,encoding:'utf8',timeout:240000,maxBuffer:16*1024*1024});
 assert.equal(result.error,undefined,String(result.error));assert.equal(result.status,0,result.stderr||result.stdout);
 sourceCase=JSON.parse(result.stdout.trim());return sourceCase;
}
test('actual native holding preference survives production export and full/compact person headings',()=>{
 const {decision,holding,native_default_profile_title,profile}=actualCase();
 assert.equal(decision.id,'ptp-song063-wyd-hong-taibao');assert.equal(holding.id,decision.holding_id);
 assert.equal(holding.person_id,decision.person_id);assert.equal(holding.mode,'attestation');assert.equal(holding.title,'太保');
 assert.deepEqual(profile.default_profile_title,native_default_profile_title);
 const selected=profile.titles.find(h=>h.id===decision.holding_id);assert.ok(selected);assert.equal(selected.title,'太保');
 assert.ok(profile.name_components.some(n=>n.title==='車騎將軍'));
 const before=JSON.stringify(profile);
 for(const full of[false,true]){
  const html=personCard(profile,full),tag=full?'h1':'h3',at=html.indexOf('<'+tag),heading=html.slice(at,html.indexOf('</'+tag+'>',at)).replace(/<[^>]*>/g,'').replace(/\s/g,'');
  assert.equal(heading,'太保王弘');assert.match(html,/來源用稱/);assert.match(html,/編輯選稱/);
 }
 assert.equal(JSON.stringify(profile),before);
});
test('actual generated compact directory carries the selected holding proof, not an arbitrary first title',()=>{
 const {decision,profile,directory}=actualCase();
 assert.deepEqual(directory.default_profile_title,profile.default_profile_title);
 assert.equal(profileTitlePreference(directory)?.title,'太保');
 assert.equal(directoryDisplay(directory,profile.label).title,'太保');assert.equal(directoryDisplay(directory,profile.label).name,'王弘');
 const h=directory.titles.find(h=>h.id===decision.holding_id);assert.ok(h);assert.ok(h.attestations.some(a=>a.id===decision.attestation_id));
 assert.deepEqual(directory.default_profile_title.source_ref,decision.source_ref);
 const broken=structuredClone(directory);broken.titles.find(h=>h.id===decision.holding_id).attestations=[];
 assert.equal(profileTitlePreference(broken),null);
});
