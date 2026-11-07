import unittest,json,copy
from pathlib import Path
from scripts import fixed_jin098_wangdun_comparison as s
from scripts.parallel_context_identity import valid
from tests import test_jin098_wangdun_roles as role_test
ROOT=role_test.ROOT;CH=role_test.CH;EP=role_test.EP
class Jin098Legal(unittest.TestCase):
 def context(self,root=ROOT):
  spec=json.loads((root/EP/'ner-roles.json').read_bytes());files={CH}|{x['native_path']for x in spec['existing_seeds'].values()}|{x['native_path']for x in spec.get('comparison_seeds',{}).values()};chapters={}
  files.add(json.loads((root/EP/'ner-legal-precedent.json').read_bytes())['parallel']['native_path'])
  for f in files:
   c=json.loads((root/f).read_bytes());chapters[c['id']]=c
  people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']};d=next(x for x in json.loads((root/'corpus/jinshu/098-wangdun-comparison-identities.json').read_bytes())['decisions']if x['id']=='d-jin098-wangling');return d,chapters,people
 def mini(self):return role_test.Jin098Roles().mini()
 def test_ordinary_dispatch_exact_reading_and_no_alias(self):
  d,c,p=self.context();self.assertTrue(valid(d,c,p,ROOT));r=d['parallel_context_reading'];self.assertTrue(r['source_spelling_is_not_alias']);self.assertNotIn('王浚',d['surfaces']);self.assertNotIn('王浚',{a['surface']for a in p[d['person_id']]['aliases']});local=c['c-jinshu-098-wangdun-comparison']['paragraphs'][35];a=next(m for m in local['mentions']if m['start']==44);b=next(m for m in local['mentions']if m['start']==134);self.assertEqual((a['surface'],b['surface']),('王浚','王淩'));self.assertEqual(a['person_id'],b['person_id'])
 def test_wrong_candidate_or_changed_qualifications(self):
  d,c,p=self.context()
  for mutation in['candidate','kind','status','alias','human']:
   x=copy.deepcopy(d);r=x['parallel_context_reading']
   if mutation=='candidate':x['person_id']=next(pid for pid in r['candidate_person_ids']if pid!=x['person_id'])
   elif mutation=='kind':r['kind']='two_candidates_same_event_parallel_context'
   elif mutation=='status':r['status']='source_attested'
   elif mutation=='alias':r['source_spelling_is_not_alias']=False
   else:x['human_reviewed']=True
   self.assertFalse(valid(x,c,p,ROOT),mutation)
 def test_wrong_parallel_case_and_dimension_use_actual_root(self):
  for mutation in['clause','work','revision','raw']:
   t,r=self.mini()
   try:
    ref=json.loads((r/EP/'ner-legal-precedent.json').read_bytes())['parallel'];q=r/ref['native_path'];c=json.loads(q.read_bytes())
    if mutation=='clause':next(p for p in c['paragraphs']if p['id']==ref['paragraph_id'])['text']='另一刑例'
    elif mutation=='work':c['work_id']='w-jinshu'
    elif mutation=='revision':c['source']['revision_id']='wrong'
    else:(r/ref['raw_path']).write_bytes((r/ref['raw_path']).read_bytes()+b'\n')
    q.write_text(json.dumps(c,ensure_ascii=False));d,cs,ps=self.context(r);self.assertFalse(valid(d,cs,ps,r),mutation)
   finally:t.cleanup()
 def test_later_named_ling_cannot_be_deleted_or_moved(self):
  t,r=self.mini()
  try:
   q=r/CH;c=json.loads(q.read_bytes());p=c['paragraphs'][35];p['text']=p['text'].replace('王淩儭土','某人儭土');q.write_text(json.dumps(c,ensure_ascii=False));d,cs,ps=self.context(r);self.assertFalse(valid(d,cs,ps,r))
  finally:t.cleanup()
 def test_no_pollution_of_names_or_true_aliases(self):
  d,cs,ps=self.context();p=copy.deepcopy(ps);p[d['person_id']]['aliases'].append({'surface':'王浚','mention_ids':[d['parallel_context_reading']['person_mention_id']]});self.assertFalse(valid(d,cs,p,ROOT))
  from scripts.person_bundle import validate_full_name
  n=dict(id='unreviewed-name',person_id=d['person_id'],chapter_id='c-jinshu-098-wangdun-comparison',paragraph_id='c-jinshu-098-wangdun-comparison:p036',person_mention_id=d['parallel_context_reading']['person_mention_id'],surname='王',ming='浚',quote=cs['c-jinshu-098-wangdun-comparison']['paragraphs'][35]['text'],status='source_attested',human_reviewed=False)
  self.assertFalse(s.name_record_valid(n,ROOT))
  with self.assertRaises(ValueError):validate_full_name(n,cs['c-jinshu-098-wangdun-comparison']['paragraphs'][35],chapter=cs['c-jinshu-098-wangdun-comparison'],root=ROOT)
 def test_preferred_uid_consistent_rekey_uses_mid_not_whitelist(self):
  t,r=self.mini()
  try:
   d,_,people=self.context(r);old=d['person_id'];new='8xz_42h_y1c';self.assertNotIn(new,people)
   def replace(x):
    if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
    if isinstance(x,list):return[replace(v)for v in x]
    return new if x==old else x
   # Only actual mutable native JSON has literal PID endpoints; fixed templates are symbolic.
   for q in sorted(r.rglob('*.json')):
    x=json.loads(q.read_bytes());y=replace(x)
    if y!=x:q.write_text(json.dumps(y,ensure_ascii=False))
   d,cs,ps=self.context(r);self.assertEqual(d['person_id'],new);self.assertTrue(valid(d,cs,ps,r))
   ch=cs['c-jinshu-098-wangdun-comparison'];next(m for m in ch['paragraphs'][35]['mentions']if m['start']==44)['person_id']=old
   self.assertFalse(valid(d,cs,ps,r))
  finally:t.cleanup()
if __name__=='__main__':unittest.main()
