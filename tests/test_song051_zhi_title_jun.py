from scripts.snapshot_test_expectations import current_snapshot
from pathlib import Path
import copy,json,hashlib,unittest
from scripts.fixed_wuyingdian_song051_family_phase import source_errors
R=Path(__file__).resolve().parents[1];B='source-evidence/song051-wyd1739-zongshi/';CID='c-songshu-051-wyd1739-zongshi'
class FiveReferences(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.ch=json.loads((R/'corpus/songshu/051-wyd1739.json').read_bytes());c.ps={p['id'].split(':')[-1]:p for p in c.ch['paragraphs']};c.reg={p['id']:p for p in json.loads((R/'registry/persons.json').read_bytes())['persons']};c.ids=[('p006','m0209','長'),('p007','m0000','沙景王'),('p010','m0103','祗'),('p018','m0199','始興王濬'),('p018','m0208','濬')]
 def test_five_exact_current_ordinary_person_references(self):
  self.assertEqual(source_errors(self.ch,R),[])
  for pn,suffix,surface in self.ids:
   p=self.ps[pn];m=next(m for m in p['mentions']if m['id'].endswith(':'+suffix));self.assertEqual(m['kind'],'person');self.assertEqual(p['text'][m['start']:m['end']],surface);self.assertEqual(m['surface'],surface);person=self.reg[m['person_id']];self.assertTrue(any(a['surface']==surface and m['id']in a['mention_ids']for a in person['aliases']));self.assertTrue(any(e['mention_id']==m['id']and e['quote']==surface for e in person['evidence']))
  daolian=next(m['person_id']for m in self.ps['p001']['mentions']if m['id'].endswith(':m0000'))
  for pn,suffix in [('p006','m0209'),('p007','m0000')]:self.assertEqual(next(m['person_id']for m in self.ps[pn]['mentions']if m['id'].endswith(':'+suffix)),daolian)
  self.assertEqual(self.ps['p006']['text'][-1]+self.ps['p007']['text'][:3],'長沙景王')
 def test_prior592_marker_shapes_and_exact_six_new_mid_set(self):
  old=json.loads((R/'tests/song051-592-marker-stage.json').read_bytes());self.assertEqual(old['source_raw_sha256'],'f74728c7bbdcc282b0285671b86bfb8eb3d51b0bef5e5a0b165fde4ee9cd97c4');self.assertEqual(len(old['markers']),592);prior={m['id']:m for m in old['markers']};self.assertEqual(len(prior),592);current={m['id']:{'paragraph_id':p['id'],**{k:m[k]for k in ['id','start','end','surface','kind']}}for p in self.ch['paragraphs']for m in p['mentions']};self.assertEqual(len(current),598)
  expected={CID+':'+p+':'+mid for p,mid in [('p006','m0209'),('p007','m0000'),('p010','m0103'),('p018','m0199'),('p018','m0208'),('p019','m0004')]};self.assertEqual(set(current)-set(prior),expected);self.assertFalse(set(prior)-set(current))
  false_mid=CID+':p019:m0172'
  for mid,row in prior.items():
   target=current_snapshot(row)
   if mid==false_mid:self.assertEqual(row['kind'],'person');target['kind']='non_person'
   self.assertEqual(current[mid],target,mid)
 def test_wrong_owner_span_kind_or_missing_reference_rejected(self):
  wrong=next(m['person_id']for m in self.ps['p001']['mentions']if m['surface']=='高祖')
  for pn,suffix,_ in self.ids:
   for change in ['owner','span','kind','missing']:
    ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id'].endswith(':'+pn));m=next(m for m in p['mentions']if m['id'].endswith(':'+suffix))
    if change=='owner':m['person_id']=wrong
    elif change=='span':m['end']+=1
    elif change=='kind':m['kind']='work'
    else:p['mentions'].remove(m)
    self.assertTrue(source_errors(ch,R),(pn,suffix,change))
 def test_zhi_single_glyph_composition_and_original_stage_preserved(self):
  c=json.loads((R/(B+'zhi-glyph-image-correction.json')).read_bytes());raw=(R/(B+'transcription-columns.txt')).read_bytes();before=(R/c['before_transcription_path']).read_bytes();lines=before.decode().splitlines(keepends=True);self.assertEqual(lines[90][19],'〓');lines[90]=lines[90][:19]+'祗'+lines[90][20:];self.assertEqual(''.join(lines).encode(),raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),c['after_transcription_sha256']);self.assertEqual(self.ps['p010']['text'][103],'祗');self.assertFalse(c['human_reviewed']);self.assertFalse(c['image_verified']);self.assertEqual(c['changes'][0]['comparator']['mention_id'],CID+':p010:m0182')
  g=json.loads((R/(B+'glyph-review-qualification.json')).read_bytes());self.assertEqual(g['unresolved_glyphs'],[]);self.assertEqual(g['resolved_AI_glyphs'][0]['accepted_reading'],'祗')
 def test_jun_uses_real_foreign_mid_not_general_title_matching(self):
  seed=json.loads((R/'corpus/songshu/085-xiezhuang.json').read_bytes());p=next(p for p in seed['paragraphs']if p['id'].endswith(':p001'));s=next(m for m in p['mentions']if m['id'].endswith(':m0063'));self.assertEqual(s['surface'],'始興王濬')
  for suffix in ['m0199','m0208']:self.assertEqual(next(m['person_id']for m in self.ps['p018']['mentions']if m['id'].endswith(':'+suffix)),s['person_id'])
  self.assertIn('太祖見而異之',p['text']);self.assertIn('每為始興王濬兄弟所戲弄濬常',self.ps['p018']['text'])
 def test_source_owned_title_group_not_name_or_holding(self):
  from scripts.wyd_song051_yixin import state,validate_appellation_fragment_groups
  actual,roles,c,docs=state(R);group=c['appellation_fragment_groups'][0];self.assertEqual(group['appellation_kind'],'title');self.assertEqual(group['value'],'長沙景王');self.assertEqual(group['canonical_mention_id'],CID+':p006:m0209');self.assertNotIn('complete_component',group);self.assertNotIn('effective_period',group);validate_appellation_fragment_groups(actual,roles,c)
  for case in ['value','reverse','owner','span','anchor','kind','not_adjacent']:
   cc=copy.deepcopy(c);g=cc['appellation_fragment_groups'][0]
   if case=='value':g['value']='長沙王'
   elif case=='reverse':g['fragments'].reverse()
   elif case=='owner':g['role']='old_taizu'
   elif case=='span':g['fragments'][0]['start']-=1
   elif case=='anchor':g['complete_source_anchor']['id']=CID+':p001:m0004'
   elif case=='kind':g['appellation_kind']='ming'
   else:g['fragments'][1]['paragraph_id']=CID+':p008'
   with self.assertRaises((ValueError,StopIteration,KeyError)):validate_appellation_fragment_groups(actual,roles,cc)
  ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id'].endswith(':p006'));p['text']='字'+p['text'];p['mentions']=[dict(m,start=m['start']+1,end=m['end']+1)for m in p['mentions']];self.assertTrue(source_errors(ch,R))
 def test_prior_false_zhen_and_lu_fix_and_unusual_printed_text_preserved(self):
  p=self.ps['p019'];self.assertEqual(next(m for m in p['mentions']if m['id'].endswith(':m0172'))['kind'],'non_person');self.assertEqual(next(m for m in p['mentions']if m['id'].endswith(':m0004'))['surface'],'陸士衡');self.assertIn('元興元年',self.ps['p004']['text']);self.assertIn('寧孟龍驤',self.ps['p002']['text']);self.assertIn('昇平三年',p['text']);self.assertIn('豫章江二州',self.ps['p027']['text'])
if __name__=='__main__':unittest.main()
