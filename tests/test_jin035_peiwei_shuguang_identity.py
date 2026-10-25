"""Permanent exact-source identity checks; canonical ID follows actual Shiji seed."""
from pathlib import Path
import copy,hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1];BASE='source-evidence/jin035-peiwei-shuguang-prince';TARGET='c-jinshu-035-peiwei:p006:m0273';SEED='c-shiji-096-zhang:m027-0093';DID='d-jin035-peiwei-shuguang-prince'
J=lambda p:json.loads(p.read_text())
def marker(ch,mid):return next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==mid)
def canonical_pair(ch,seed,people):
 a=marker(ch,TARGET);b=marker(seed,SEED)
 assert a['kind']==b['kind']=='person' and a['surface']=='太子'and b['surface']=='孝元帝'and a['person_id']==b['person_id']and a['person_id']in people
 owner=people[a['person_id']]
 assert all(any(e.get('mention_id')==mid for e in owner['evidence'])for mid in (TARGET,SEED))
 return a['person_id']
class ShuguangHistoricalPrince(unittest.TestCase):
 def setUp(self):
  self.c=J(ROOT/'corpus/jinshu/035-peiwei.json');self.s=J(ROOT/'corpus/shiji/096.json');self.people={p['id']:p for p in J(ROOT/'registry/persons.json')['persons']};self.r=J(ROOT/BASE/'review.json')
 def test_current_native_decision_and_reverse_anchor(self):
  pid=canonical_pair(self.c,self.s,self.people);d=next(d for d in J(ROOT/'corpus/jinshu/035-peiwei-identities.json')['decisions']if d['id']==DID)
  self.assertEqual(d['person_id'],pid);self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(d['human_reviewed']);self.assertEqual(d['external_reference_file'],BASE+'/review.json')
  self.assertEqual({e['mention_id']for e in d['evidence']},{TARGET,SEED});self.assertEqual([a['surface']for a in self.people[pid]['aliases']if TARGET in a['mention_ids']],['太子'])
 def test_fixed_han_complete_units(self):
  pins={'071':('be32afadfff3f8b983ce5148a790230d54f48b4d891f9c74231cd3a78010396a',1160,2004,7904576),'009':('e68afd3fb1097ccd7ee077ec75f2305a174110fbda9bfb4c667f2d93f240739c',153,466,2315084)}
  self.assertEqual({u['external_volume']for u in self.r['external_primary_units']},set(pins))
  for u in self.r['external_primary_units']:
   sha,a,z,rev=pins[u['external_volume']];f=ROOT/u['raw_file'];b=f.read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),sha);self.assertEqual((u['raw_start'],u['raw_end'],u['revision_id']),(a,z,rev));self.assertEqual(b.decode()[a:z],u['raw_quote']);self.assertEqual(u['work_id'],'w-hanshu');self.assertTrue(u['complete_selected_natural_unit']);self.assertFalse(u['native_book_or_chapter_id_created']);self.assertFalse(u['image_verified'])
  a,b=[next(u['raw_quote']for u in self.r['external_primary_units']if u['external_volume']==k)for k in ('071','009')]
  self.assertTrue(all(x in a for x in ['疏廣字仲翁','太子外祖父特進平恩侯許伯','不宜獨親外家許氏','皆以壽終']));self.assertTrue(all(x in b for x in ['孝元皇帝，宣帝太子也','黃龍元年','太子即皇帝位']))
 def test_received_summary_is_not_verbatim_han_quote(self):
  p=next(p for p in self.c['paragraphs']if p['id']=='c-jinshu-035-peiwei:p006');self.assertEqual(p['text'],self.r['source_quote']);self.assertEqual(p['text'][270:281],'疏廣戒太子以舅氏為官屬');self.assertIn('不宣稱逐字同引',self.r['source_wording_qualification']);self.assertTrue(self.r['personal_name_shi_not_added_from_these_witnesses'])
 def test_other_taizi_marks_preserved(self):
  baseline=J(ROOT/BASE/'other-taizi-baseline.json');allmarks=[m for p in self.c['paragraphs']for m in p['mentions']if'太子'in m['surface']and m['id']!=TARGET];self.assertEqual({m['id']for m in allmarks},{x['id']for x in baseline['marks']});jin=marker(self.c,baseline['seed_mention_id'])['person_id'];han=marker(self.s,SEED)['person_id'];self.assertNotEqual(jin,han)
  for e in baseline['marks']:
   m=marker(self.c,e['id']);self.assertEqual({k:m[k]for k in ('id','start','end','surface','kind')},{k:e[k]for k in ('id','start','end','surface','kind')});self.assertEqual(m['person_id'],jin)
 def test_no_same_name_jin_identity(self):
  pid=canonical_pair(self.c,self.s,self.people);self.assertFalse(any(e.get('mention_id')=='c-jinshu-073-yu-yi-bing-tiao:line113:m0211'for e in self.people[pid]['evidence']))
 def test_rekey_does_not_require_a_fixed_person_id(self):
  c=copy.deepcopy(self.c);s=copy.deepcopy(self.s);people=copy.deepcopy(self.people);old=canonical_pair(c,s,people);new='synthetic-current-canonical';people[new]=people.pop(old);people[new]['id']=new;marker(c,TARGET)['person_id']=marker(s,SEED)['person_id']=new;self.assertEqual(canonical_pair(c,s,people),new)
if __name__=='__main__':unittest.main()
