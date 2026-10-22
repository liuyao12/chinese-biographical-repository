# coding: utf-8
"""Synthetic received-source declarations; these fixtures are not historical data."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.congzhongbiao import valid


class CongzhongbiaoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def fixture(self, text='乙氏有盛名。甲氏於乙氏為從中表，獨不至。', sub='甲氏', obj='乙氏'):
        sid, oid = 'synthetic-subject', 'synthetic-object'
        start = text.index(sub); other = text.index(obj, text.index('於', start) + 1)
        term = text.index('從中表', other)
        p = {'id': 'synthetic-p', 'text': text, 'mentions': [
            {'id': 's', 'start': start, 'end': start + len(sub), 'surface': sub, 'kind': 'person', 'person_id': sid},
            {'id': 'o', 'start': other, 'end': other + len(obj), 'surface': obj, 'kind': 'person', 'person_id': oid}]}
        raw = 'synthetic header\n　　' + text + '\n';path = self.root/'sources/synthetic/raw.txt';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(raw)
        raw_start = raw.index('　　');raw_end = raw.index('\n', raw_start)
        p['source_position'] = {'start':raw_start,'end':raw_end,'raw':raw[raw_start:raw_end],'raw_path':'sources/synthetic/raw.txt'}
        raw_sha = hashlib.sha256(raw.encode()).hexdigest();text_sha=hashlib.sha256(text.encode()).hexdigest()
        c={'id':'synthetic-c','work_id':'synthetic-w','book_id':'synthetic-b','source_id':'synthetic-source','paragraphs':[p],'text_sha256':text_sha,'source':{'revision_id':777,'raw_file_sha256':raw_sha,'raw_sha256':raw_sha,'raw_path':'sources/synthetic/raw.txt'}}
        def anchor(a,b):return {'paragraph_id':p['id'],'start':a,'end':b,'surface':text[a:b]}
        a={'id':'synthetic-a','predicate':'kinship_unspecified','subject_person_id':sid,'object_person_id':oid,'status':'source_attested','human_reviewed':False,'evidence':[{'work_id':'synthetic-w','book_id':'synthetic-b','chapter_id':'synthetic-c','source_id':'synthetic-source','paragraph_id':'synthetic-p','quote':text,'subject_person_mention_id':'s','object_person_mention_id':'o'}],'qualifiers':{'source_term':'從中表','kinship_basis':'congzhongbiao_named_pair','relationship_class':'biao_kinship','source_modifier':'從','lineage':'unspecified','generation_difference':None,'exact_distance':None,'common_ancestor_person_id':None,'connecting_person_ids':None,'subject_relative_age':'unknown','source_clause_binding':{'kind':'named_subject_yu_named_object_congzhongbiao','clause_anchor':anchor(start,term+3),'relationship_anchor':anchor(term,term+3),'source_fingerprint':{'source_id':'synthetic-source','revision_id':777,'raw_sha256':raw_sha,'text_sha256':text_sha}}}}
        return a, {'synthetic-p':('synthetic-c',p)}, {'synthetic-c':c}, self.root

    def test_literal_two_glyphs_and_alternate_people_are_accepted(self):
        self.assertTrue(valid(*self.fixture()))
        self.assertTrue(valid(*self.fixture('乙氏有盛名。甲氏於乙氏爲從中表，獨不至。')))
        self.assertTrue(valid(*self.fixture('他傳記敘。丙於丁為從中表，獨不至。', '丙', '丁')))

    def test_unknowns_cannot_be_filled_or_converted_to_first_cousins(self):
        for key,value in [('generation_difference',0),('generation_difference',-1),('exact_distance',2),('lineage','maternal'),('lineage','paternal'),('common_ancestor_person_id','synthetic-grandparent'),('connecting_person_ids',[]),('connecting_person_ids',['synthetic-parent']),('subject_relative_age','older'),('adopted_for_family_tree',True),('relationship_class','maternal_cousin'),('source_modifier','')]:
            args=self.fixture();args[0]['qualifiers'][key]=value;self.assertFalse(valid(*args),(key,value))
        args=self.fixture();args[0]['qualifiers']['kinship_structure']={'distance':2};self.assertFalse(valid(*args))

    def test_direction_and_person_binding_not_nearest_matching_name(self):
        for mode in ('reverse','wrong_subject','wrong_object','self','wrong_subject_mention','wrong_object_mention'):
            args=self.fixture();a=args[0]
            if mode=='reverse':a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];a['evidence'][0]['subject_person_mention_id'],a['evidence'][0]['object_person_mention_id']='o','s'
            elif mode=='wrong_subject':a['subject_person_id']='different'
            elif mode=='wrong_object':a['object_person_id']='different'
            elif mode=='self':a['object_person_id']=a['subject_person_id']
            elif mode=='wrong_subject_mention':a['evidence'][0]['subject_person_mention_id']='o'
            else:a['evidence'][0]['object_person_mention_id']='s'
            self.assertFalse(valid(*args),mode)

    def test_quotes_and_negative_context_rejected_after_all_hashes_are_consistent(self):
        for text in ['人曰：「舊事。甲氏於乙氏為從中表，獨不至。」','人云："舊事。甲氏於乙氏為從中表，獨不至。"',"人云：'舊事。甲氏於乙氏為從中表，獨不至。'",'乙氏有盛名。非甲氏於乙氏為從中表，獨不至。']:
            self.assertFalse(valid(*self.fixture(text)),text)

    def test_quote_opened_in_previous_paragraph_is_not_direct_narration(self):
        args=self.fixture('乙氏有盛名。甲氏於乙氏為從中表，獨不至。」')
        a,paragraphs,chapters,root=args;c=chapters['synthetic-c'];p=c['paragraphs'][0]
        prefix='人曰：「';file=root/'sources/synthetic/raw.txt';raw=file.read_text().replace('synthetic header\n','synthetic header\n'+prefix+'\n\n');file.write_text(raw)
        added=len(prefix)+2;p['source_position']['start']+=added;p['source_position']['end']+=added
        c['paragraphs'].insert(0,{'id':'synthetic-prefix','text':prefix,'mentions':[]})
        sha=hashlib.sha256(raw.encode()).hexdigest();c['source'].update(raw_file_sha256=sha,raw_sha256=sha)
        text_sha=hashlib.sha256('\n\n'.join(x['text'] for x in c['paragraphs']).encode()).hexdigest();c['text_sha256']=text_sha
        a['qualifiers']['source_clause_binding']['source_fingerprint'].update(raw_sha256=sha,text_sha256=text_sha)
        self.assertFalse(valid(*args))

    def test_wrong_connector_term_or_missing_modifier_not_general_kinship(self):
        for key,value in [('source_term','有親'),('source_term','中表'),('source_term','表兄弟'),('kinship_basis','external_clan_affiliation')]:
            args=self.fixture();args[0]['qualifiers'][key]=value;self.assertFalse(valid(*args))
        args=self.fixture();p=args[1]['synthetic-p'][1];p['text']=p['text'].replace('於','與');self.assertFalse(valid(*args))

    def test_received_layers_at_all_four_levels_and_notes_rejected(self):
        for which in ('chapter','source','paragraph','position'):
            for field,value in [('text_layer','peisongzhi_annotation'),('source_layer','attached_note'),('annotator','synthetic commentator'),('attached_note',{'text':'later note'})]:
                args=self.fixture();p=args[1]['synthetic-p'][1];c=args[2]['synthetic-c'];obj={'chapter':c,'source':c['source'],'paragraph':p,'position':p['source_position']}[which];obj[field]=value;self.assertFalse(valid(*args),(which,field))

    def test_full_evidence_and_source_fingerprint_required(self):
        for field in ('work_id','book_id','chapter_id','source_id','paragraph_id'):
            args=self.fixture();args[0]['evidence'][0][field]='wrong';self.assertFalse(valid(*args),field)
        args=self.fixture();args[0]['evidence'][0]['quote']='甲氏於乙氏為從中表';self.assertFalse(valid(*args))
        for field in ('source_id','revision_id','raw_sha256','text_sha256'):
            args=self.fixture();args[0]['qualifiers']['source_clause_binding']['source_fingerprint'][field]='wrong';self.assertFalse(valid(*args),field)

    def test_exact_anchors_and_competing_person_in_clause_rejected(self):
        for field in ('clause_anchor','relationship_anchor'):
            args=self.fixture();args[0]['qualifiers']['source_clause_binding'][field]['start']+=1;self.assertFalse(valid(*args),field)
        args=self.fixture();p=args[1]['synthetic-p'][1];s=p['mentions'][0];p['mentions'].append(dict(s,id='competing',person_id='other-person'));self.assertFalse(valid(*args))

    def test_absolute_raw_position_coshift_and_changed_bytes_rejected(self):
        args=self.fixture();pos=args[1]['synthetic-p'][1]['source_position'];pos['start']+=1;pos['end']+=1;self.assertFalse(valid(*args))
        args=self.fixture();file=args[3]/'sources/synthetic/raw.txt';file.write_bytes(file.read_bytes()+b'changed');self.assertFalse(valid(*args))
        args=self.fixture();(args[3]/'sources/synthetic/raw.txt').write_bytes(b'\xff');self.assertFalse(valid(*args))

    def test_raw_path_escape_and_symlink_rejected(self):
        args=self.fixture();args[2]['synthetic-c']['source']['raw_path']='../outside.txt';self.assertFalse(valid(*args))
        args=self.fixture();path=args[3]/'sources/synthetic/raw.txt';other=args[3]/'other.txt';other.write_bytes(path.read_bytes());path.unlink();path.symlink_to(other);self.assertFalse(valid(*args))

    def test_assertion_status_and_no_extra_evidence(self):
        args=self.fixture();args[0]['status']='proposed';self.assertFalse(valid(*args))
        args=self.fixture();args[0]['human_reviewed']=True;self.assertFalse(valid(*args))
        args=self.fixture();args[0]['evidence'].append(copy.deepcopy(args[0]['evidence'][0]));self.assertFalse(valid(*args))

if __name__=='__main__':unittest.main()
