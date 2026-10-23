import unittest,json,hashlib,re,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];CH='corpus/weishu-weishou/058-yangbo-yangkan';CID='c-weishu-weishou-058-yangbo-yangkan'
class YangboSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/(CH+'.json')).read_text());cls.ps={p['id']:p for p in cls.c['paragraphs']};cls.reg={x['id']:x for x in json.loads((R/'registry/persons.json').read_text())['persons']};cls.a=json.loads((R/(CH+'-assertions.json')).read_text())['assertions'];cls.review=json.loads((R/cls.c['annotation'].get('identity_review_current_projection','source-evidence/weishu058-yangbo-yangkan/identity-review.json')).read_text());cls.ids={x['key']:x['person_id']for x in cls.review['new']}
 def test_full_received_units_not_summary(self):
  s=(R/self.c['source']['raw_path']).read_text();a=s.index('==楊播==');b=s.index('===弟椿===');units=[x for x in s[a:b].splitlines()if x.strip()and not x.lstrip().startswith('=')];z=s.index('史臣曰：');units.append(s[z:s.index('\n\n==校勘記==',z)]);self.assertEqual(len(units),15);self.assertEqual([re.sub(r'<ref>.*?</ref>','',x,flags=re.S)for x in units],[p['text']for p in self.c['paragraphs']]);self.assertEqual(hashlib.sha256(s.encode()).hexdigest(),self.c['source']['raw_file_sha256'])
 def test_projection_offsets_and_two_modern_collations(self):
  s=(R/self.c['source']['raw_path']).read_text()
  for p in self.c['paragraphs']:self.assertEqual(''.join(s[n]for n in p['source_position']['raw_character_offsets']),p['text'])
  reports=self.c['annotation']['modern_collation_reports'];self.assertEqual(len(reports),2)
  for x in reports:self.assertEqual(s[x['raw_start']:x['raw_end']],x['raw_text']);self.assertEqual(x['layer'],'modern_received_witness_collation_report');self.assertFalse(x['image_verified'])
 def test_parentage_and_uncle_direction_not_succession_inference(self):
  got={(x['subject_person_id'],x['predicate'],x['object_person_id'])for x in self.a}
  self.assertIn((self.ids['kan'],'father',self.ids['bo']),got);self.assertIn((self.ids['bo'],'father',self.ids['yi']),got);self.assertIn((self.ids['kan'],'paternal_uncle',self.ids['chun']),got);self.assertNotIn((self.ids['chun'],'father',self.ids['yi']),got);self.assertNotIn((self.ids['yu'],'father',self.ids['yi']),got)
 def test_uncle_reversal_rejected(self):
  from scripts.directed_uncle_roles import paternal_uncle_direction_valid
  ps={p['id']:(CID,p)for p in self.c['paragraphs']}
  for x in self.a:
   if x['predicate']=='paternal_uncle':
    self.assertTrue(paternal_uncle_direction_valid(x,ps));bad=copy.deepcopy(x);bad['subject_person_id'],bad['object_person_id']=x['object_person_id'],x['subject_person_id'];self.assertFalse(paternal_uncle_direction_valid(bad,ps))
 def test_oldest_one_and_no_other_ordinals(self):
  orders=[x for x in self.a if 'birth_order'in x['qualifiers']];self.assertEqual(len(orders),1);x=orders[0];self.assertEqual(x['subject_person_id'],self.ids['shichong']);self.assertEqual(x['qualifiers']['birth_order']['ordinal'],1);self.assertNotIn('birth_order',next(x for x in self.a if x['subject_person_id']==self.ids['chuntuo'])['qualifiers'])
 def test_anonymous_daughter_no_fabricated_spouse(self):
  self.assertIn((self.ids['daughter'],'father',self.ids['wei']),{(x['subject_person_id'],x['predicate'],x['object_person_id'])for x in self.a});self.assertFalse(any(x['predicate']=='spouse'for x in self.a));self.assertNotIn('family_path',self.reg[self.ids['daughter']])
 def test_death_year_and_no_birth_or_all_office_end(self):
  es=json.loads((R/(CH+'-life-events.json')).read_text())['events'];self.assertEqual(len(es),3);e=next(x for x in es if x['person_id']==self.ids['bo']);self.assertEqual(e['normalized_date']['year'],513);self.assertEqual(e['date_expression'],'延昌二年');self.assertTrue(all(x['event_type']=='death'for x in es));hs=json.loads((R/(CH+'-titles.json')).read_text())['holdings'];self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in hs))
 def test_ming_glyph_variants_and_source_local_context(self):
  text=''.join(p['text']for p in self.c['paragraphs']);self.assertIn('師沖',text);self.assertNotIn('師仲',text);self.assertIn('万俟醜奴',text);self.assertNotIn('萬俟醜奴',text);self.assertNotEqual(self.ids['wangji'],'7f4_2d4_c15')
 def test_all_current_reverse_occurrences_exact(self):
  for p in self.c['paragraphs']:
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
    if m['kind']=='person':
     row=self.reg[m['person_id']];self.assertIn(m['id'],[e.get('mention_id')for e in row['evidence']]);self.assertTrue(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in row['aliases']))
 def test_progress_chapter_and_existing_work_not_duplicate(self):
  ws=json.loads((R/'registry/works.json').read_text())['works'];w=[x for x in ws if x['id']=='w-weishu-weishou'];self.assertEqual(len(w),1);self.assertIn(self.c['book_id'],[b['id']for b in w[0]['books']]);entry=[x for x in json.loads((R/'corpus/progress.json').read_text())['books']if x.get('chapter_id')==CID];self.assertEqual(len(entry),1);self.assertFalse(entry[0]['complete'])

 def test_wrong_numeric_year_rejected(self):
  from scripts.validate_corpus import normalized_date_errors
  es=json.loads((R/(CH+'-life-events.json')).read_text())['events'];e=next(x for x in es if x.get('normalized_date'));d=e['normalized_date'];self.assertEqual(normalized_date_errors(d,{CID:self.c},root=R,bound_record=e,bound_role='life_event'),[]);wrong=copy.deepcopy(d);wrong['year']=wrong['era_year']=514;self.assertTrue(normalized_date_errors(wrong,{CID:self.c},root=R,bound_record=e,bound_role='life_event'))
 def test_allocator_reserves_existing_family_path(self):
  from scripts.person_ids import allocate_child_id
  chosen=allocate_child_id(self.ids['kan'],set(self.reg),root=R);self.assertNotIn(chosen,self.reg);self.assertNotIn(chosen,[self.ids['shichong'],self.ids['chuntuo']])

 def test_parent_posthumous_rank_rejects_wrong_same_paragraph_recipient(self):
  from scripts.parent_office_gift import valid
  hs=json.loads((R/(CH+'-titles.json')).read_text())['holdings'];h=hs[0];es=json.loads((R/(CH+'-life-events.json')).read_text())['events'];ps={p['id']:(CID,p)for p in self.c['paragraphs']};ms={m['id']:(CID,p['id'],m)for p in self.c['paragraphs']for m in p['mentions']};events={e['id']:e for e in es};self.assertTrue(valid(h,ps,ms,events))
  p=self.c['paragraphs'][0];ruler=next(m for m in p['mentions']if m['surface']=='高祖');bad=copy.deepcopy(h);bad['person_id']=ruler['person_id'];bad['posthumous_basis']['recipient_person_mention_id']=ruler['id']
  for e in bad['evidence']:e['person_mention_id']=ruler['id']
  for e in bad['posthumous_basis']['evidence']:e['person_mention_id']=ruler['id']
  for e in bad['effective_period']['start']['evidence']:e['person_mention_id']=ruler['id']
  for a in bad['attestations']:a['person_mention_id']=ruler['id']
  changed=copy.deepcopy(events);ev=changed[bad['posthumous_basis']['death_event_id']];ev['person_id']=ruler['person_id'];ev['evidence'][0]['person_mention_id']=ruler['id'];self.assertFalse(valid(bad,ps,ms,changed))
  wrong=copy.deepcopy(h);wrong['posthumous_basis']['grant_term']='追封'+h['title'];self.assertFalse(valid(wrong,ps,ms,events))

 def test_parent_gift_has_no_person_id_allowlist(self):
  from scripts.parent_office_gift import valid
  h=json.loads((R/(CH+'-titles.json')).read_text())['holdings'][0];events=json.loads((R/(CH+'-life-events.json')).read_text())['events'];p=copy.deepcopy(self.c['paragraphs'][0]);old={m['person_id']for m in p['mentions']if m['kind']=='person'};mapping={v:'synthetic-person-'+str(i)for i,v in enumerate(sorted(old))}
  def rewrite(v):
   if isinstance(v,str):return mapping.get(v,v)
   if isinstance(v,list):return[rewrite(x)for x in v]
   if isinstance(v,dict):return{k:rewrite(x)for k,x in v.items()}
   return v
  p=rewrite(p);h=rewrite(h);events=rewrite(events);ps={p['id']:(CID,p)};ms={m['id']:(CID,p['id'],m)for m in p['mentions']};es={e['id']:e for e in events};self.assertTrue(valid(h,ps,ms,es))
