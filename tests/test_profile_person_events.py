"""Real partial profile producer with a tiny synthetic filesystem, no historical IDs."""
from pathlib import Path
import tempfile,json,copy,unittest,contextlib,io
from scripts.table_person_profiles import build

def setup(root,events_marker='missing'):
 def write(rel,obj):
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False)+'\n')
 people=[dict(id=k,label=label,identity_note='synthetic',aliases=[])for k,label in [('alpha','甲'),('beta','乙'),('untouched','丙')]]
 write('registry/persons.json',dict(persons=people));write('data/corpus/index.json',dict(chapters=[]));write('data/historical-tables/person-candidates.json',dict(persons=[]));write('exports/persons/index.json',dict(persons=[dict(person_id=p['id'])for p in people]));write('data/corpus/profiles/index.json',dict(schema_version=1,profiles=[dict(id=p['id'],label=p['label'],sentinel='keep-'+p['id'])for p in people]))
 for p in people:
  b=dict(canonical_person_id=p['id'],person_ids=[p['id']],persons=[p],passages=[],source_mention_summary=[],most_mentioned_source_ids=[],mentions=[],table_occurrences=[],title_holdings=[],address_assertions=[],sources=[],relations=[],date_normalizations=[])
  if p['id']=='alpha'and events_marker!='missing':b['person_events']=copy.deepcopy(events_marker)
  write('exports/persons/'+p['id']+'.json',b);write('data/corpus/profiles/'+p['id']+'.json',dict(sentinel='keep-'+p['id']))
 return write
class ProfilePersonEvents(unittest.TestCase):
 def run_case(self,events):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);setup(root,events);before=(root/'data/corpus/profiles/untouched.json').read_bytes();index=json.loads((root/'data/corpus/profiles/index.json').read_text());other=next(x for x in index['profiles']if x['id']=='untouched')
   with contextlib.redirect_stdout(io.StringIO()):build(root,person_ids=['alpha','beta'])
   self.assertEqual((root/'data/corpus/profiles/untouched.json').read_bytes(),before);newindex=json.loads((root/'data/corpus/profiles/index.json').read_text());self.assertEqual(next(x for x in newindex['profiles']if x['id']=='untouched'),other);self.assertEqual({x['id']for x in newindex['profiles']},{'alpha','beta','untouched'})
   a=json.loads((root/'data/corpus/profiles/alpha.json').read_text());b=json.loads((root/'data/corpus/profiles/beta.json').read_text());self.assertNotIn('person_events',b);return a
 def test_burial_and_other_events_raw_values_and_owner_filter(self):
  events=[dict(id='burial',person_id='alpha',event_type='burial',epitaph_date_parts=dict(month=3,day=5),evidence=[dict(quote='synthetic full burial evidence')]),dict(id='call',person_id='alpha',event_type='recruitment',source_term='徵',status='offered'),dict(id='foreign',person_id='beta',event_type='burial')]
  self.assertEqual(self.run_case(events)['person_events'],events[:2])
 def test_missing_not_invented(self):self.assertNotIn('person_events',self.run_case('missing'))
 def test_empty_not_invented(self):self.assertNotIn('person_events',self.run_case([]))
if __name__=='__main__':unittest.main()
