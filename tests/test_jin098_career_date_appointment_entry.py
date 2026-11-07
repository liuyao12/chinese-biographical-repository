"""Exercise the actual main annotation appointment date block with physical-root source data."""
import copy,unittest
from pathlib import Path
from scripts import fixed_jin098_wangdun_career as career
from scripts import fixed_jin098_wangdun_career_dates as bridge
from scripts import validate_corpus as validator
ROOT=Path(__file__).resolve().parents[1]
def notice_block(proposal,chapters,root):
 # Compile the exact production main block, rather than replacing it with a test-only analogue.
 source=(root/'scripts/validate_corpus.py').read_text()
 start=source.index("                    jin098_outer_year_valid = False\n")
 end=source.index("                    errors.extend(normalized_date_errors(proposal['normalized_date'], chapters, root, proposal, 'appointment_notice'))",start)
 end=source.index('\n',end)
 code=source[start:end];code='\n'.join(line[20:]for line in code.splitlines())
 errors=[]
 def check(value,msg):
  if not value:errors.append(msg)
 exec(compile(code,'actual-main-appointment-block','exec'),{'proposal':proposal,'chapters':chapters,'root':root,'check':check,'errors':errors,'normalized_date_errors':validator.normalized_date_errors})
 return errors
class AppointmentEntry(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=career.read(ROOT,career.CH);cls.roles,cls.t=career.prepared(cls.ch,ROOT);cls.qs=[q for q in cls.t['annotation']['title_proposals']if q['id']in bridge.TARGETS]
 def test_all_four_real_appointment_notice(self):
  self.assertEqual(len(self.qs),4)
  for q in self.qs:
   self.assertNotEqual(q['normalized_date']['evidence'],q['evidence']);self.assertEqual(validator.normalized_date_errors(q['normalized_date'],{self.ch['id']:self.ch},ROOT,q,'appointment_notice'),[]);self.assertEqual(notice_block(q,{self.ch['id']:self.ch},ROOT),[])
 def test_wrong_person_chain_outcome_and_prior_event_rejected(self):
  for kind in ['person','chain','outcome','year','prior','source']:
   q=copy.deepcopy(self.qs[0])
   if kind=='person':q['person_id']=self.roles['dao']
   elif kind=='chain':q['normalized_date']['event_evidence_binding']['complete_chain_paragraph_ids'].pop(1)
   elif kind=='outcome':q['outcome']='not_reported'
   elif kind=='year':q['normalized_date']['year']=324
   elif kind=='prior':q['source_appointment_context']['paragraph_id']=self.ch['id']+':p011'
   else:q['normalized_date']['event_evidence_binding']['kind']='other_source_chain'
   self.assertTrue(notice_block(q,{self.ch['id']:self.ch},ROOT),kind)
 def test_original_same_clause_path_remains(self):
  q={'normalized_date':{'evidence':[],'source_expression':'年'},'evidence':[],'date_expression':'年'}
  # Same-clause remains true independently; the usual normalized-date validator still rejects malformed date.
  errs=notice_block(q,{},ROOT);self.assertNotIn('任命通知紀年須綁同一原句',errs);self.assertTrue(errs)
  q['normalized_date']['evidence']=[{'quote':'他句'}];self.assertIn('任命通知紀年須綁同一原句',notice_block(q,{},ROOT))
if __name__=='__main__':unittest.main()
