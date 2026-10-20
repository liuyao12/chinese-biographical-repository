from pathlib import Path
import json,sys,unittest,copy,hashlib,ast,tempfile
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[1];R=P;J=lambda f:json.loads(f.read_text());sys.path.insert(0,str(R))
from scripts.person_bundle import load_catalog,bundle
from scripts.occurrence_concordance import occurrence_catalog,summarize_occurrences,index_counts,validate
from scripts.export_person_bundles import index_counts as export_index_counts
CAT=load_catalog(R);RECORDS=CAT[1];D=next(r for r in RECORDS if r.get('id')=='c-sanguozhi-010-xunyu-xunyou-jiaxu');SID=D['source_id'];C=next(r for r in RECORDS if r.get('record_type')=='source_occurrence_concordance_set' and r['source']['source_id']==SID);PID='yoo_ox0_545_BA'
BASE_PARAGRAPHS={p['id']for p in J(R/'tests/fixtures/occurrence-concordance/original-anchors.json')}
def scoped_rows(b):
 return summarize_occurrences([m for m in b['mentions']if m['paragraph_id']in BASE_PARAGRAPHS],[],{D['id']:D},R,RECORDS)[0]
def getmention(d,mid):return next(m for p in d['paragraphs']for m in p['mentions']if m['id']==mid)
class Concordance(unittest.TestCase):
 def bad(self,fn):
  d,c=copy.deepcopy(D),copy.deepcopy(C);fn(d,c);records=[d if r is D else c if r is C else r for r in RECORDS]
  with self.assertRaises((ValueError,KeyError,TypeError)):occurrence_catalog(R,records)
 def test_32_person_aliases_one_collective(self):
  a,details=occurrence_catalog(R,[r for r in RECORDS if r.get('record_type')!='source_occurrence_concordance_set' or r is C]);self.assertEqual(len(a),32);self.assertEqual(len(details),32);self.assertEqual(sum(r['kind']=='unresolved_text_span_correspondence'for r in C['records']),1)
 def test_all_sources_form_disjoint_exact_alias_union(self):
  expected={SID:32,'s-houhanshu-062-xunhan-zhongchen':30};union={};all_details={}
  sets=[r for r in RECORDS if r.get('record_type')=='source_occurrence_concordance_set']
  self.assertEqual({r['source']['source_id']for r in sets},set(expected))
  for selected in sets:
   aliases,details=occurrence_catalog(R,[r for r in RECORDS if r.get('record_type')!='source_occurrence_concordance_set' or r is selected])
   self.assertEqual(len(aliases),expected[selected['source']['source_id']]);self.assertFalse(set(union)&set(aliases));union.update(aliases);all_details.update(details)
  aliases,details=occurrence_catalog(R,RECORDS);self.assertEqual(aliases,union);self.assertEqual(details,all_details);self.assertEqual(len(aliases),62)
 def test_wrong_record_type_cannot_silently_disable_dedup(self):self.bad(lambda d,c:c.update(record_type='typo'))
 def test_empty_record_id(self):self.bad(lambda d,c:c['records'][0].update(id=''))
 def test_wrong_person(self):self.bad(lambda d,c:c['records'][0].update(person_id='dad_b77_b38'))
 def test_same_label_wrong_id(self):
  def mutate(d,c):
   r=c['records'][0];getmention(d,r['canonical_mention_id'])['person_id']='same-name-fake';getmention(d,r['duplicate_mention_id'])['person_id']='same-name-fake';r['person_id']='same-name-fake'
  self.bad(mutate)
 def test_wrong_surface(self):self.bad(lambda d,c:c['records'][0].update(surface='合成'))
 def test_wrong_span(self):self.bad(lambda d,c:c['records'][0]['canonical'].update(start=0))
 def test_revision(self):self.bad(lambda d,c:c['source'].update(revision_id='0'*40))
 def test_cross_source(self):self.bad(lambda d,c:c['source'].update(source_id='s-foreign'))
 def test_raw_sha(self):self.bad(lambda d,c:c['source'].update(raw_file_sha256='0'*64))
 def test_git_blob(self):self.bad(lambda d,c:c['source'].update(source_blob_sha='0'*40))
 def test_raw_path_traversal(self):self.bad(lambda d,c:c['source'].update(raw_path='sources/witnesses/../../../foreign.txt'))
 def test_unknown_mention(self):self.bad(lambda d,c:c['records'][0].update(canonical_mention_id='missing'))
 def test_duplicate_record(self):self.bad(lambda d,c:c['records'].append(copy.deepcopy(c['records'][0])))
 def test_one_to_many(self):
  def mutate(d,c):r=copy.deepcopy(c['records'][0]);r['id']='synthetic-new';r['canonical_mention_id']=c['records'][1]['canonical_mention_id'];c['records'].append(r)
  self.bad(mutate)
 def test_cycle(self):
  def mutate(d,c):r=copy.deepcopy(c['records'][0]);r['id']='cycle';r['canonical_mention_id'],r['duplicate_mention_id']=r['duplicate_mention_id'],r['canonical_mention_id'];c['records'].append(r)
  self.bad(mutate)
 def test_chain(self):self.bad(lambda d,c:c['records'][1].update(canonical_mention_id=c['records'][0]['duplicate_mention_id']))
 def test_self_link(self):self.bad(lambda d,c:c['records'][0].update(duplicate_mention_id=c['records'][0]['canonical_mention_id']))
 def test_unresolved_collective_not_person(self):
  def mutate(d,c):next(r for r in c['records']if r['person_id']is None).update(kind='resolved_person_occurrence_alias',person_id='dkn_ge4_286_AAAAH')
  self.bad(mutate)
 def test_identical_surface_different_raw_position_rejected(self):
  def mutate(d,c):
   r=next(r for r in c['records']if r['person_id']==PID);p=next(p for p in d['paragraphs']if p['id']==r['canonical']['paragraph_id']);m=next(m for m in p['mentions']if m['person_id']==PID and m['id']!=r['canonical_mention_id']);r['canonical_mention_id']=m['id'];r['canonical'].update(start=m['start'],end=m['end']);c['records']=[r]
  self.bad(mutate)
 def test_xunyu_145_raw_143_occurrences_all_mentions_retained(self):
  b=bundle(PID,root=R,catalog=CAT,include_provisional=True);row=next(r for r in scoped_rows(b)if r['source_id']==SID);self.assertEqual((row['raw_mention_count'],row['mention_count'],row['duplicate_mention_count']),(145,143,2));self.assertEqual(len(row['mention_ids']),145);self.assertEqual(len(row['occurrence_groups']),143);self.assertIn('145個原始錨點',row['count_explanation']);self.assertIn('不',row['count_explanation']);self.assertEqual(len([g for g in row['occurrence_groups']if len(g['mention_ids'])==2]),2)
 def test_intro_not_false_duplicate(self):
  aliases,_=occurrence_catalog(R,RECORDS);intro=next(p for p in D['paragraphs']if p['id'].endswith(':intro:p001'));self.assertEqual(len(intro['mentions']),9);self.assertTrue(all(m['id']not in aliases for m in intro['mentions']));self.assertFalse(any(p['id'].endswith('full:u001')for p in D['paragraphs']))
 def test_different_version_and_same_surface_stay_separate_and_ranking(self):
  b=bundle(PID,root=R,catalog=CAT,include_provisional=True);mentions=[m for m in b['mentions']if m['chapter_id']==D['id']and m['paragraph_id']in BASE_PARAGRAPHS];foreign={'id':'foreign-chapter','source_id':'foreign-source','work_id':'foreign-work','book_id':'foreign-book','source':{'revision_id':'different'}};extra=[{'id':'other-position-'+str(i),'chapter_id':foreign['id'],'paragraph_id':'other-paragraph','surface':'彧'}for i in range(144)];rows,most=summarize_occurrences(mentions+extra,[],{D['id']:D,'foreign-chapter':foreign},R,RECORDS);self.assertEqual(most,['foreign-source']);self.assertEqual(next(r for r in rows if r['source_id']=='foreign-source')['mention_count'],144)
  rows,ties=summarize_occurrences(mentions+extra[:-1],[],{D['id']:D,'foreign-chapter':foreign},R,RECORDS);self.assertEqual(set(ties),{SID,'foreign-source'})
 def test_runtime_and_export_index_same_count_source_count_unchanged(self):
  b=bundle(PID,root=R,catalog=CAT,include_provisional=True);counts=index_counts(b);self.assertEqual(counts,export_index_counts(b));self.assertEqual(counts['raw_mention_count']-counts['mention_count'],sum(r['duplicate_mention_count']for r in b['source_mention_summary']));self.assertEqual(counts['source_count'],len(b['sources']));source=(R/'scripts/export_person_bundles.py').read_text();self.assertIn('**index_counts(result)',source);self.assertIn('原始錨點完整保留',source)
 def test_partial_export_actual_loop_and_visible_explanation(self):
  from unittest.mock import patch
  from scripts import export_person_bundles as exporter, calendar_wiring
  b=bundle(PID,root=R,catalog=CAT,include_provisional=True)
  with tempfile.TemporaryDirectory()as tmp:
   target=Path(tmp);(target/'registry').mkdir();(target/'registry/works.json').write_bytes((R/'registry/works.json').read_bytes())
   with patch.object(calendar_wiring,'export_calendar_contexts'),patch.object(exporter,'load_catalog',return_value=({PID:CAT[0][PID]},RECORDS)),patch.object(exporter,'load_assemblies',return_value=({},{})),patch.object(exporter,'bundle',return_value=b):exporter.export(target)
   row=J(target/'exports/persons/index.json')['persons'][0];self.assertEqual(row['mention_count'],index_counts(b)['mention_count']);self.assertEqual(row['raw_mention_count'],index_counts(b)['raw_mention_count']);self.assertEqual(row['source_count'],len(b['sources']));self.assertEqual(row['most_mentioned_source_ids'],b['most_mentioned_source_ids']);self.assertIn('原始錨點完整保留',(target/'exports/persons/README.md').read_text());self.assertEqual(J(target/('exports/persons/'+PID+'.json'))['mentions'],b['mentions'])
 def test_table_occurrences_not_globally_collapsed(self):
  tables=[{'id':'table1','source_id':'ts','work_id':'tw','book_id':'tb','chapter_id':'tc','table_cell_id':'cell1'},{'id':'table2','source_id':'ts','work_id':'tw','book_id':'tb','chapter_id':'tc','table_cell_id':'cell2'}];rows,most=summarize_occurrences([],tables,{},R,RECORDS);self.assertEqual(rows[0]['mention_count'],2);self.assertEqual(rows[0]['table_occurrence_count'],2)
 def test_original_source_anchors_preserved_without_freezing_registry_or_chapter_size(self):
  expected=J(R/'tests/fixtures/occurrence-concordance/original-anchors.json');by={p['id']:p for p in D['paragraphs']}
  for p in expected:
   self.assertEqual(by[p['id']]['text'],p['text']);mentions={m['id']:m for m in by[p['id']]['mentions']}
   for m in p['mentions']:self.assertEqual({k:mentions[m['id']].get(k)for k in m},m)
 def test_all_15_precise_memory_bundles(self):
  expected=J(R/'tests/fixtures/occurrence-concordance/expected-counts.json');out=[];temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);folder=Path(temp.name)
  for item in expected:
   b=bundle(item['person_id'],root=R,catalog=CAT,include_provisional=True);row=next(r for r in scoped_rows(b)if r['source_id']==SID);self.assertEqual(row['mention_count'],item['independent_occurrence_count']);self.assertEqual(row['raw_mention_count'],item['runtime_raw_summary']);f=folder/(item['person_id']+'.json');f.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n');out.append({'person_id':item['person_id'],'raw':row['raw_mention_count'],'independent':row['mention_count'],'duplicate':row['duplicate_mention_count'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'index':index_counts(b)})
  self.assertEqual(len(out),15)
if __name__=='__main__':unittest.main(verbosity=2)
