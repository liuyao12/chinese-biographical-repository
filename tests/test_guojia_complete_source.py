# coding: utf-8
import unittest,json,copy,hashlib,tempfile
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/sanguozhi/014-guojia.json').read_text());PS=C['paragraphs'];REG={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
def hits(j,s):return[m for m in PS[j-1]['mentions']if m['surface']==s]
class GuojiaCompleteSource(unittest.TestCase):
 def test_full_unit_all_notes_and_raw_boundary(self):
  self.assertEqual(len(PS),20);self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in PS),10);self.assertEqual(sum(len(p['text'])for p in PS),2471);self.assertFalse(errors(C,R));self.assertIn('162–253',C['source']['extent']);self.assertIn('254董昭',C['source']['extent'])
 def test_reverse_refs_spans_and_no_overlap(self):
  for p in PS:
   prior=[]
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertTrue(all(m['start']>=b or m['end']<=a for a,b in prior));prior.append((m['start'],m['end']))
    if m['kind']=='person':self.assertTrue(any(m['id']in a['mention_ids']and a['surface']==m['surface']for a in REG[m['person_id']]['aliases']));self.assertTrue(any(e.get('mention_id')==m['id']and e['quote']==m['surface']for e in REG[m['person_id']]['evidence']))
 def test_raw_projection_co_shift_and_layer_negative(self):
  ref=C['annotation']['fixed_kanripo_projection_ref'];d=json.loads((R/ref).read_text())
  with tempfile.TemporaryDirectory()as t:
   root=Path(t)
   for rel in [ref,d['raw_file']]:p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/rel).read_bytes())
   self.assertFalse(errors(C,root));bad=copy.deepcopy(d);bad['unit']['start']+=1;(root/ref).write_text(json.dumps(bad,ensure_ascii=False));self.assertTrue(errors(C,root));(root/ref).write_text(json.dumps(d,ensure_ascii=False));cc=copy.deepcopy(C);cc['paragraphs'][1]['text_layer']='received_chapter';self.assertTrue(errors(cc,root))
 def test_author_criticism_and_different_claims_retained(self):
  self.assertIn('案魏書所云與傅子正反也',PS[5]['text']);self.assertIn('皆出自太祖此云用嘉計則為不同',PS[7]['text']);self.assertIn('今正以襲許年死此蓋事之偶合',PS[7]['text']);self.assertEqual(hits(8,'松之')[0]['person_id'],next(p['id']for p in REG.values()if p['label']=='裴松之'))
 def test_original_words_not_silent_emendation(self):
  self.assertTrue(PS[1]['text'].startswith('傳子曰'));self.assertTrue(PS[3]['text'].startswith('傅子曰'));self.assertIn('八百尸并前千户',PS[10]['text']);self.assertIn('盪定烏九',PS[11]['text']);self.assertIn('辛評',PS[2]['text'])
 def test_guoyi_is_boyi_and_other_guoyi_not_used(self):
  self.assertEqual(hits(13,'奕')[0]['person_id'],hits(14,'伯益')[0]['person_id']);old=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());m=next(m for p in old['paragraphs']for m in p['mentions']if m['surface']=='郭伯益');self.assertEqual(m['person_id'],hits(13,'奕')[0]['person_id']);other=json.loads((R/'corpus/sanguozhi/026-guohuai.json').read_text());other_id=next(m['person_id']for p in other['paragraphs']for m in p['mentions']if m['surface']=='泰業');self.assertNotEqual(m['person_id'],other_id);self.assertFalse(any(x.get('person_id')==other_id for p in PS for x in p['mentions']))
 def test_xin_source_forms_preferred_same_not_corrected(self):
  old=json.loads((R/'corpus/sanguozhi/010.json').read_text());m=next(m for p in old['paragraphs']for m in p['mentions']if m['surface']=='辛平');self.assertEqual(hits(3,'辛評')[0]['person_id'],m['person_id']);review=json.loads((R/'source-evidence/sgz014-guojia/identity-review.json').read_text());self.assertTrue(review['identities']['辛評']['source_spelling_is_not_alias']);self.assertIn('未見014另一版本',review['identities']['辛評']['rationale'])
 def test_work_title_inside_name_not_double_person(self):
  self.assertEqual(hits(5,'荀攸傳')[0]['kind'],'work');self.assertFalse(hits(5,'荀攸'));self.assertEqual(hits(14,'王昶家誡')[0]['kind'],'work');self.assertFalse(hits(14,'王昶'));self.assertEqual(hits(8,'本傳')[0]['kind'],'unresolved')
 def test_work_scope_no_fictitious_full_title_antecedent(self):
  self.assertEqual(hits(2,'傳子')[0]['work_id'],hits(4,'傅子')[0]['work_id']);self.assertEqual(hits(20,'世語')[0]['work_id'],'w-shiyu-sgz027-reference');self.assertTrue(all('work_reference_resolution'not in m for p in PS for m in p['mentions']));self.assertTrue(all(m['kind']=='work'for j,s in [(6,'魏書'),(14,'王昶家誡'),(8,'武紀')]for m in hits(j,s)))
 def test_military_bei_and_ce_not_false_people(self):
  p=PS[10]
  for word in ['設備','無備','為備']:
   st=p['text'].index(word)+word.index('備');self.assertFalse(any(m['start']==st and m['kind']=='person'for m in p['mentions']))
  st=PS[3]['text'].index('䇿得');self.assertFalse(any(m['start']==st and m['kind']=='person'for m in PS[3]['mentions']))
 def test_chang_grandfather_and_unreported_father_preserved(self):
  self.assertIn('嘉孫敞字泰中',PS[19]['text'])
  ledger_path=R/'source-evidence/sgz014-guojia/source-facts-ledger.json';ledger=json.loads(ledger_path.read_text());self.assertFalse(ledger['runtime_assertions_added']);self.assertEqual(len(ledger['items']),12)
  current=json.loads((R/'source-evidence/sgz014-guojia-typed/coverage-ledger.json').read_text());self.assertEqual(current['prior_source_only_ledger']['sha256'],hashlib.sha256(ledger_path.read_bytes()).hexdigest())
  aa=json.loads((R/'corpus/sanguozhi/014-guojia-assertions.json').read_text())['assertions'];self.assertEqual(len(aa),4)
  descendant=hits(20,'敞')[0]['person_id'];ancestor=hits(20,'嘉')[0]['person_id'];g,=[a for a in aa if a['subject_person_id']==descendant]
  self.assertEqual((g['predicate'],g['object_person_id']),('grandfather',ancestor));self.assertIsNone(g['qualifiers']['parent_person_id']);self.assertEqual(g['qualifiers']['intermediate_person_ids'],[None]);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==descendant for a in aa))
 def test_nested_quoted_wo_tracks_actual_speaker(self):
  self.assertEqual(hits(4,'吾')[0]['person_id'],hits(4,'太祖')[0]['person_id']);self.assertEqual(hits(18,'吾')[0]['person_id'],hits(1,'郭嘉')[0]['person_id']);self.assertNotEqual(hits(18,'吾')[0]['person_id'],hits(18,'太祖')[0]['person_id'])
 def test_internal_references_do_not_dangle_or_invent_chapters(self):
  works=json.loads((R/'registry/works.json').read_text())['works'];bookids={b['id']for w in works for b in w['books']};chapterids={d['id']for q in(R/'corpus').glob('*/*.json')for d in[json.loads(q.read_text())]if d.get('record_type')=='marked_chapter'}
  for p in PS:
   for m in p['mentions']:
    if 'internal_source_reference'not in m:continue
    b=m['internal_source_reference'];self.assertTrue(b['book_id']is None or b['book_id']in bookids);self.assertTrue(b['chapter_id']is None or b['chapter_id']in chapterids)
 def test_metadata_and_progress_explicitly_incomplete(self):
  meta=json.loads((R/'registry/work-provenance.json').read_text());e=meta['text_bases'][C['source_id']];self.assertIsNone(e['edition_id']);self.assertIsNone(e['earliest_extant_basis_edition_id']);p=next(p for p in json.loads((R/'corpus/progress.json').read_text())['books']if p['chapter_id']==C['id']);self.assertFalse(p['complete']);self.assertFalse(C['source']['image_verified']);self.assertFalse(C['annotation']['human_reviewed'])
if __name__=='__main__':unittest.main()
