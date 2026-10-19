import copy
import hashlib
import json
from pathlib import Path
import unittest
from scripts.biographical_children_lists import children_list_errors
from scripts.validate_corpus import source_age_number

ROOT = Path(__file__).resolve().parents[1]

def fixture():
    chapter=json.loads((ROOT/'corpus/jinshu/059.json').read_text())
    a=next(a for a in json.loads((ROOT/'corpus/jinshu/059-assertions.json').read_text())['assertions'] if a.get('context',{}).get('kind')=='biographical_children_list')
    return a,chapter

def errors(a,c):return children_list_errors(a,c,source_age_number)

class ChildrenListTests(unittest.TestCase):
    def test_full_fixed_biography_and_five_members(self):
        a,c=fixture();self.assertEqual(errors(a,c),[])
        for item in json.loads((ROOT/'corpus/jinshu/059-assertions.json').read_text())['assertions']:
            if item.get('context',{}).get('kind')=='biographical_children_list':
                self.assertEqual(errors(item,c),[])
    def test_wrong_father(self):
        a,c=fixture();a['object_person_id']='someone_else';self.assertTrue(errors(a,c))
    def test_wrong_father_anchor(self):
        a,c=fixture();m=next(m for m in c['paragraphs'][0]['mentions']if m['surface']=='宣帝');a['object_person_id']=m['person_id'];a['context']['parent_mention_id']=m['id'];self.assertTrue(errors(a,c))
    def test_cannot_start_from_intermediate_biography_paragraph(self):
        a,c=fixture();a['context']['paragraph_ids']=a['context']['paragraph_ids'][4:];a['evidence']=a['evidence'][4:];m=c['paragraphs'][4]['mentions'][0];a['context']['parent_mention_id']=m['id'];a['object_person_id']=m['person_id'];self.assertTrue(errors(a,c))
    def test_cannot_skip_recorded_middle_prose(self):
        a,c=fixture();a['context']['paragraph_ids'].pop(2);a['evidence'].pop(2);self.assertTrue(errors(a,c))
    def test_cannot_remove_prose_from_chapter_to_hide_gap(self):
        a,c=fixture();c['paragraphs'].pop(2);a['context']['paragraph_ids'].pop(2);a['evidence'].pop(2);self.assertTrue(errors(a,c))
    def test_prose_cannot_be_relabelled_as_blank_gap(self):
        a,c=fixture();c['paragraphs'].pop(2);a['context']['paragraph_ids'].pop(2);a['evidence'].pop(2);raw='被略正文';c['source']['normalization']['verified_blank_line_gaps'].append({'source_lines':[21,23],'raw_quote':raw,'raw_quote_sha256':hashlib.sha256(raw.encode()).hexdigest(),'revision_id':2650517});self.assertTrue(errors(a,c))
    def test_heading_cannot_conceal_prose_with_recomputed_hash(self):
        a,c=fixture();record=c['source']['normalization']['omitted_digital_paratext'][0];record['raw_quote']+='\n正文不可略';record['raw_quote_sha256']=hashlib.sha256(record['raw_quote'].encode()).hexdigest();self.assertTrue(errors(a,c))
    def test_different_revision(self):
        a,c=fixture();c['paragraphs'][2]['source_position']['revision_id']+=1;self.assertTrue(errors(a,c))
    def test_wrong_list_character_position(self):
        a,c=fixture();c['paragraphs'][5]['mentions'][0]['start']+=1;self.assertTrue(errors(a,c))
    def test_wrong_list_member_identity(self):
        a,c=fixture();a['subject_person_id']='someone_else';self.assertTrue(errors(a,c))
    def test_wrong_list_member_order(self):
        a,c=fixture();a['context']['list_member_mention_ids'].reverse();self.assertTrue(errors(a,c))
    def test_missing_list_member(self):
        a,c=fixture();a['context']['list_member_mention_ids'].pop();self.assertTrue(errors(a,c))
    def test_list_sequence_cannot_become_birth_order(self):
        a,c=fixture();a['qualifiers']['ordinal']=1;self.assertTrue(errors(a,c))
    def test_short_quotes_cannot_replace_complete_paragraphs(self):
        a,c=fixture();a['evidence'][0]['quote']='汝南文成王亮';self.assertTrue(errors(a,c))
    def test_editorial_note_is_not_received_prose(self):
        a,c=fixture();c['paragraphs'][1]['text_layer']='digital_editorial_note';self.assertTrue(errors(a,c))
    def test_cross_biography_unit(self):
        a,c=fixture();c['paragraphs'][2]['unit_id']='different_unit';self.assertTrue(errors(a,c))
    def test_edited_children_count(self):
        a,c=fixture();a['qualifiers']['source_term']='有四子';self.assertTrue(errors(a,c))
    def test_not_human_reviewed(self):
        a,c=fixture();a['context']['human_reviewed']=True;self.assertTrue(errors(a,c))

    def test_distinct_children_cannot_share_one_identity(self):
        a,c=fixture();c['paragraphs'][5]['mentions'][1]['person_id']=c['paragraphs'][5]['mentions'][0]['person_id'];self.assertTrue(errors(a,c))
