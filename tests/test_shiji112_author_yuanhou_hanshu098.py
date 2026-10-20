# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ROOT='4w5_b4e_vf5';F=ROOT+'_A';Z=ROOT+'_AB';M='2cf_ibm_2cg';Q='pme_eis_xqi_*A*AAAAA'
def load(f):return json.loads((R/f).read_text())
def chapter(n,work='shiji'):return load('corpus/'+work+'/'+n+'.json')
def p(n,k,work='shiji'):return next(p for p in chapter(n,work)['paragraphs']if p['id'].endswith(k))
def rels():return load('corpus/hanshu/098-assertions.json')['assertions']
class AuthorYuanhouHanshu098(unittest.TestCase):
 def test_author_local_signature_not_father_or_appended_speaker(self):
  self.assertEqual(next(m for m in p('112','p028')['mentions']if m['surface']=='太史公')['person_id'],Q)
  self.assertEqual(next(m for m in p('130','p004')['mentions']if m['surface']=='太史公')['person_id'],'pme_eis_xqi_*A*AAAA')
  self.assertEqual(next(m for m in p('112','p029')['mentions']if m['surface']=='太皇太后')['person_id'],Z)
  self.assertEqual(p('112','p029')['text_layer'],'witness_appended_edict');self.assertEqual(p('112','p030')['text_layer'],'witness_appended_bangu_note')
 def test_catalogue_is_reference_not_fabricated_author_mention(self):
  d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-taishigong-author');r=next(r for r in d['references']if r['scope']=='received_work_catalogue');self.assertIn('作平津侯列傳第五十二',r['quote']);self.assertFalse(any(e['paragraph_id'].endswith('p124')for e in d['evidence']))
 def test_edict_identity_binds_received_name_and_commentary(self):
  d=next(d for d in load('corpus/shiji/112-equivalences.json')['decisions']if d['id']=='eq-shiji112-yuanhou-edict');self.assertEqual(d['person_ids'],[Z]);self.assertIn('平帝元始中王元后詔',d['references'][0]['quote']);self.assertTrue(any('生女政君即元后也'in e['quote']for e in d['evidence']));self.assertFalse(d['human_reviewed'])
 def test_partial_witness_has_fixed_revision_raw_extent_and_no_image_claim(self):
  c=chapter('098','hanshu');s=c['source'];self.assertEqual(len(c['paragraphs']),3);self.assertEqual(s['text_scope'],'partial_chapter');self.assertEqual(s['source_commit'],'683113d4baf6febecaf2ccb7913df87c4d68d454');self.assertEqual(len(s['source_blob_sha']),40);self.assertEqual(len(s['response_sha256']),64);self.assertEqual(s['response_extent'],dict(first_line=1,last_line=75,partial_file=True));self.assertFalse(s['image_verified']);self.assertEqual(s['normalization']['character_conversion'],{})
 def test_source_glyphs_omitted_commentary_and_precise_names(self):
  q=p('098','p-kin-002','hanshu');self.assertIn('不修㢘隅',q['text']);self.assertIn('譚子元崇少子商子夏',q['text']);self.assertNotIn('譚字上',q['text']);self.assertNotIn('次譚',q['text']);self.assertEqual(next(m for m in q['mentions']if m['surface']=='少子')['person_id'],ROOT+'_AH');self.assertEqual(next(m for m in q['mentions']if m['surface']=='君弟')['person_id'],ROOT+'_AD')
 def test_three_generations_come_from_independent_father_assertions(self):
  fathers={a['subject_person_id']:a['object_person_id']for a in rels()if a['predicate']=='father'};self.assertEqual(fathers[Z],F);self.assertEqual(fathers[F],ROOT);self.assertNotIn(ROOT,fathers);self.assertEqual(len([a for a in rels()if a['predicate']=='father']),13)
 def test_birth_mother_only_three_explicit_children_and_separate_spouse(self):
  rows=rels();mothers={a['subject_person_id']:a['object_person_id']for a in rows if a['predicate']=='mother'};self.assertEqual(mothers,{ROOT+'_AE':M,ROOT+'_AH':M,Z:M});self.assertTrue(any(a['predicate']=='spouse'and a['subject_person_id']==M and a['object_person_id']==F for a in rows));self.assertFalse(any(a['object_person_id']==M and a['subject_person_id']==ROOT+'_AF'for a in rows))
 def test_order_has_separate_sex_scopes_and_no_assumed_son_numbers(self):
  order={a['subject_person_id']:a['qualifiers']['birth_order']for a in rels()if 'birth_order'in a['qualifiers']};self.assertEqual(set(order),{ROOT+'_AA',Z,ROOT+'_AC',ROOT+'_AD',ROOT+'_AE',ROOT+'_AF'});self.assertEqual((order[Z]['scope'],order[Z]['ordinal']),('daughters_of_parent',2));self.assertEqual((order[ROOT+'_AE']['scope'],order[ROOT+'_AE']['ordinal']),('sons_of_parent',1))
 def test_birth_after_taichu_does_not_use_old_tenth_month_direction(self):
  e=load('corpus/hanshu/098-life-events.json')['events'][0];d=e['normalized_date_range'];self.assertEqual(e['date_expression'],'本始三年');self.assertEqual(e['person_id'],Z);self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(71,70));self.assertEqual((d['earliest']['year'],d['latest']['year']),(-70,-69));self.assertNotIn('normalized_date',e);self.assertTrue(any('以正月為歲首'in r['quote']for r in d['references']));self.assertFalse(any('後八十年'in e['quote']for e in d['evidence']))
 def test_name_components_keep_evidence_and_do_not_store_ancestors(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']==Z);self.assertEqual((n['title'],n['surname'],n['ming']),('太皇太后','王','政君'));self.assertIn('生女政君即元后也',n['quote']);self.assertTrue(any('王翁孺'in r['quote']for r in n['references']));self.assertNotIn('grandfather',n);self.assertNotIn('age',n)
 def test_family_ids_do_not_reach_claimed_ancient_ancestors(self):
  people={p['id']:p for p in load('registry/persons.json')['persons']};self.assertNotIn('family_path',people[ROOT]);self.assertEqual(people[Z]['family_path']['parent_person_id'],F);self.assertFalse(any('黄帝'in a['evidence'][0]['quote']for a in rels()))
 def test_retired_ids_have_no_registry_alias_or_person_json(self):
  people=load('registry/persons.json')['persons'];serialized=json.dumps(people,ensure_ascii=False)
  for old in ['iaf_rfl_80u','38x_hpr_ltp']:
   self.assertNotIn(old,serialized)
   for directory in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/directory/(old+'.json')).exists())
