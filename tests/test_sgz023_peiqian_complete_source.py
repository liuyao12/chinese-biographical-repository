import copy,json,hashlib,shutil,tempfile,unittest
from pathlib import Path
from scripts.fixed_kanripo_projection import errors as body_errors
from scripts.fixed_kanripo_collation import errors as qing_errors,CID,SHA,RAW,REF
R=Path(__file__).resolve().parents[1]
class PeiqianSource(unittest.TestCase):
 def setUp(self):
  self.body=json.loads((R/'corpus/sanguozhi/023-peiqian.json').read_text());self.q=json.loads((R/'corpus/sanguozhi/023-qing-collation.json').read_text());self.people={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']};self.works={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']}
 def test_complete_body_notes_four_supplements_and_author_assessment(self):
  self.assertEqual(body_errors(self.body,R),[]);self.assertEqual(len(self.body['paragraphs']),21)
  text=''.join(p['text']for p in self.body['paragraphs'])
  for s in ['裴潛字文行','文章敘錄曰','荀綽冀州記曰','臣松之案','魏略列傳以','嚴幹字公仲','韓宣字景然','黃朗字文達','魚豢曰','評曰和洽']:self.assertIn(s,text)
  self.assertEqual(self.body['source']['text_scope'],'partial_chapter');self.assertEqual(self.body['annotation']['status'],'in_progress')
 def test_distinct_qing_source_pinned_complete_and_not_pei(self):
  self.assertEqual(qing_errors(self.q,R),[]);p=self.q['paragraphs'][0];self.assertEqual(p['text_layer'],'witness_appended_qing_siku_collation');self.assertEqual(p['layer_attribution']['scope'],'independent_volume_appendix');self.assertEqual(self.q['book_id'],self.body['book_id']);self.assertNotEqual(self.q['source_id'],self.body['source_id'])
 def test_source_layer_truncation_and_pin_co_move_rejected(self):
  for change in ['layer','truncate','author','scope','ref']:
   d=copy.deepcopy(self.q)
   if change=='layer':d['paragraphs'][0]['text_layer']='witness_appended_pei_songzhi_note'
   if change=='truncate':d['paragraphs'][0]['text']=d['paragraphs'][0]['text'][:-1]
   if change=='author':d['paragraphs'][0]['layer_attribution']['attributed_author']='裴松之'
   if change=='scope':d['paragraphs'][0]['layer_attribution']['scope']='received_body'
   if change=='ref':d['annotation'].pop('fixed_kanripo_collation_ref')
   self.assertTrue(qing_errors(d,R),change)
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)
   for rel in [RAW,REF,'scripts/fixed_kanripo_collation_pins.json']:
    out=root/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy(R/rel,out)
   raw=(root/RAW).read_bytes()+b'X';(root/RAW).write_bytes(raw);sha=hashlib.sha256(raw).hexdigest();d=copy.deepcopy(self.q);d['source']['response_sha256']=sha
   pin=json.loads((root/'scripts/fixed_kanripo_collation_pins.json').read_text());pin['bindings'][CID]['raw_sha256']=sha;(root/'scripts/fixed_kanripo_collation_pins.json').write_text(json.dumps(pin));self.assertTrue(qing_errors(d,root))
 def test_all_person_and_work_anchors_reverse_cited(self):
  for c in[self.body,self.q]:
   for p in c['paragraphs']:
    last=0
    for m in p['mentions']:
     self.assertGreaterEqual(m['start'],last);last=m['end'];self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
     if m['kind']=='person':
      row=self.people[m['person_id']];self.assertTrue(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in row['aliases']));self.assertTrue(any(e.get('mention_id')==m['id']and e.get('source_id')==c['source_id']for e in row['evidence']))
     elif m['kind']=='work':self.assertIn({'chapter_id':c['id'],'source_id':c['source_id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':p['text']},self.works[m['work_id']]['reference_attestations'])
 def test_work_title_is_not_person_and_full_title_resolutions(self):
  p=self.q['paragraphs'][0];titles=[m for m in p['mentions']if m['surface']=='曹休傳'];self.assertEqual(len(titles),1);self.assertEqual(titles[0]['kind'],'work');self.assertTrue(any(m['surface']=='曹休'and m['kind']=='person'for m in p['mentions']))
  for m in p['mentions']:
   if m['surface']=='通鑑':self.assertEqual(m['work_id'],'w-zizhitongjian')
   if m['surface']=='先賢傳':self.assertEqual(self.works[m['work_id']]['citation_title'],'汝南先賢傳')
 def test_xu_fu_not_qin_fangshi_and_retired_hui_not_revived(self):
  ms=[m for p in self.body['paragraphs']for m in p['mentions']];xs=[m['person_id']for m in ms if m['surface']=='徐福'];self.assertTrue(xs);self.assertNotIn('9nc_i02_15v',xs);self.assertNotIn('047_850_e7d',self.people)
  hui=[m['person_id']for m in ms if m['surface']in['徽','文季']];self.assertEqual(set(hui),{'4ni_4t1_4o9_B'})
 def test_two_xu_xu_and_qiao_xuan_are_not_collapsed_by_short_names(self):
  p=self.q['paragraphs'][0];xs=[m for m in p['mentions']if m['surface']=='許栩'];self.assertEqual(len(xs),2);self.assertNotEqual(xs[0]['person_id'],xs[1]['person_id']);end=p['text'].index('代玄為司徒');x=next(m for m in p['mentions']if m['start']==end-2);g=next(m for m in p['mentions']if m['start']==end+1);self.assertEqual(x['person_id'],xs[1]['person_id']);full=next(m for m in p['mentions']if m['surface']=='橋玄');self.assertEqual(g['person_id'],full['person_id'])
 def test_critical_xu_you_exclusion_preserves_two_people(self):
  p=self.q['paragraphs'][0];xs=[m for m in p['mentions']if m['surface']=='許攸'];self.assertEqual(len(xs),2);self.assertNotEqual(xs[0]['person_id'],xs[1]['person_id']);alt=next(m for m in p['mentions']if m['surface']=='許遊');self.assertEqual(alt['person_id'],xs[0]['person_id'])
 def test_cefu_single_full_title_and_qualified_composition_years(self):
  meta=json.loads((R/'registry/work-provenance.json').read_text());w=self.works['w-cefu-yuangui'];self.assertEqual(w['citation_title'],'冊府元龜');self.assertNotIn('w-cefu-sgz023-critical-reference',self.works)
  dates=meta['works']['w-cefu-yuangui']['composition'];self.assertEqual(dates['status'],'reported');self.assertEqual([(a['event_kind'],a['date']['start_year'])for a in dates['assertions']],[('commission',1005),('completion',1013)])
  self.assertEqual(meta['works']['w-cefu-yuangui']['earliest_extant_edition']['assertions'],[])
  for a in dates['assertions']:self.assertIn('清四庫提要報告',a['qualification']);self.assertTrue(a['source_expression']);self.assertEqual(len(a['reference_ids']),2)
 def test_era_kang_is_not_a_person_and_reverse_marker_is_absent(self):
  p=self.body['paragraphs'][6];i=p['text'].index('元康');self.assertFalse(any(m['kind']=='person' and m['start']<i+2 and m['end']>i for m in p['mentions']))
  self.assertTrue(any(m['kind']=='person'and m['surface']=='康'for m in self.body['paragraphs'][9]['mentions']))
  badmid='c-sanguozhi-023-peiqian:p007:m0038'
  for r in self.people.values():
   self.assertFalse(any(badmid in a.get('mention_ids',[])for a in r.get('aliases',[])))
   self.assertFalse(any(e.get('mention_id')==badmid for e in r.get('evidence',[])))
 def test_explicit_parallel_identity_roles_and_original_variants(self):
  roles=[(1,'靈帝','0wg_vtn_yqb'),(10,'王戎','ehx_cqg_nfx_AA'),(10,'鍾㑹','a6a_4c2_670'),(15,'高幹','e06_e9f_c30'),(15,'郭援','715_4e6_890'),(15,'馬超','50b_399_d54'),(15,'超','50b_399_d54')]
  for pi,surface,pid in roles:
   ms=[m for m in self.body['paragraphs'][pi]['mentions']if m['surface']==surface];self.assertTrue(ms,(pi,surface));self.assertTrue(all(m['kind']=='person'and m['person_id']==pid for m in ms),(pi,surface))
 def test_chang_shi_and_jing_remain_source_local_names(self):
  p=self.q['paragraphs'][0];shi=next(m for m in p['mentions']if m['surface']=='峕');jing=next(m for m in p['mentions']if m['surface']=='靜');self.assertNotEqual(shi['person_id'],jing['person_id']);self.assertIn('峕弟靜紹封',p['text']);self.assertIn('峕弟',self.people[jing['person_id']]['label'])
 def test_local_title_references_and_allusive_xibo(self):
  p=self.q['paragraphs'][0]
  for surface,pid in [('明帝','932_46f_026'),('靈帝','0wg_vtn_yqb')]:self.assertTrue(any(m['surface']==surface and m.get('person_id')==pid for m in p['mentions']))
  i=p['text'].index('飛書與仁')+3;self.assertTrue(any(m['start']==i and m['kind']=='person'for m in p['mentions']))
  p=self.body['paragraphs'][2];m=next(m for m in p['mentions']if m['surface']=='西伯');self.assertEqual(m['person_id'],'y4i_pjk_4gn_A');self.assertIn('引古',m['resolution_note'])
if __name__=='__main__':unittest.main()
