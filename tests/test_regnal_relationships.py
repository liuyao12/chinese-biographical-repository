# coding: utf-8
"""Mutated negative controls are synthetic; never written into source records."""
import copy,hashlib,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.regnal_relationships import regnal_spouse_errors,received_body
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'corpus/hanshu/007.json').read_text())
A=next(a for a in json.loads((ROOT/'corpus/hanshu/007-assertions.json').read_text())['assertions'] if a['id']=='a-hanshu007-004')
class RegnalRelationshipTests(unittest.TestCase):
 def test_explicitly_reviewed_interval_does_not_claim_physical_adjacency(self):
  self.assertEqual(regnal_spouse_errors(A,C),[]);self.assertGreater(C['paragraphs'][1]['source_position']['first_line'],C['paragraphs'][0]['source_position']['last_line']+1)
 def test_not_a_general_parentage_exemption(self):
  a=copy.deepcopy(A);a['predicate']='father';self.assertTrue(regnal_spouse_errors(a,C))
 def test_wrong_emperor_or_wrong_coronation_anchor_is_rejected(self):
  a=copy.deepcopy(A);a['object_person_id']='yqp_nlb_p1p_ACAA';self.assertTrue(regnal_spouse_errors(a,C))
  a=copy.deepcopy(A);a['context']['monarch_mention_id']=C['paragraphs'][0]['mentions'][0]['id'];self.assertTrue(regnal_spouse_errors(a,C))
 def test_fixed_source_and_line_coordinates_are_required(self):
  for key,value in [('source_commit','synthetic-other'),('source_blob_sha','synthetic-other'),('first_line',22),('last_line',68)]:
   a=copy.deepcopy(A);a['context']['witness_interval'][key]=value;self.assertTrue(regnal_spouse_errors(a,C))
 def test_context_cannot_suppress_an_intervening_succession(self):
  a=copy.deepcopy(A);w=a['context']['witness_interval'];lines=w['raw_quote'].splitlines();lines[10]+='改立皇帝';w['raw_quote']='\n'.join(lines);w['raw_quote_sha256']=hashlib.sha256(w['raw_quote'].encode()).hexdigest();w['body']=received_body(w['raw_quote']);self.assertTrue(regnal_spouse_errors(a,C))
 def test_full_quotes_and_raw_context_hash_must_match(self):
  a=copy.deepcopy(A);a['evidence'][1]['quote']='立皇后上官氏';self.assertTrue(regnal_spouse_errors(a,C))
  a=copy.deepcopy(A);a['context']['witness_interval']['raw_quote_sha256']='synthetic';self.assertTrue(regnal_spouse_errors(a,C))
 def test_commentary_is_not_received_regnal_narrative(self):
  c=copy.deepcopy(C);c['paragraphs'][0]['text_layer']='witness_appended_bangu_note';self.assertTrue(regnal_spouse_errors(A,c))
 def test_unattested_installation_and_invalid_review_flags_are_rejected(self):
  a=copy.deepcopy(A);a['qualifiers']['source_term']='立帝';self.assertTrue(regnal_spouse_errors(a,C))
  a=copy.deepcopy(A);a['context']['human_reviewed']=True;self.assertTrue(regnal_spouse_errors(a,C))
 def test_malformed_context_fails_without_crashing(self):
  for value in [None,False,'synthetic',[]]:
   a=copy.deepcopy(A);a['context']['witness_interval']=value;self.assertTrue(regnal_spouse_errors(a,C))
 def test_renaming_the_kind_cannot_turn_an_omitted_interval_into_adjacent_text(self):
  from scripts.validate_corpus import validate
  target=ROOT/'corpus/hanshu/007-assertions.json';original=Path.read_text;data=json.loads(original(target));record=next(a for a in data['assertions'] if a['id']==A['id']);record['context']['kind']='adjacent_paragraphs'
  def read(p,*args,**kwargs):return json.dumps(data,ensure_ascii=False) if p==target else original(p,*args,**kwargs)
  with patch.object(Path,'read_text',read):errors=validate(ROOT)
  self.assertTrue(any('省略原行' in e for e in errors),errors)
