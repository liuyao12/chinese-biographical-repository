"""Independent synthetic source assertions for missing-parent ancestry assembly."""
import copy
import unittest
try:from scripts.ancestor_through_uncle import valid
except ImportError:from ancestor_through_uncle import valid

def fixture():
    chapter={'id':'chapter-test','source_id':'source-test','work_id':'work-test','book_id':'book-test','source':{'url':'https://example.org/fixed'},'paragraphs':[]}
    def evidence(pid,text,subject,object):
        marks=[{'id':pid+':s','kind':'person','person_id':subject},{'id':pid+':o','kind':'person','person_id':object}]
        chapter['paragraphs'].append({'id':pid,'text':text,'text_layer':'received_chapter','mentions':marks})
        return {'chapter_id':chapter['id'],'source_id':chapter['source_id'],'work_id':chapter['work_id'],'book_id':chapter['book_id'],'paragraph_id':pid,'quote':text,'subject_person_mention_id':pid+':s','object_person_mention_id':pid+':o'}
    ue=evidence('p-child','Nephew is the elder brother\'s son of Tutor.','child','uncle')
    fe=evidence('p-uncle','Tutor is the son of Elder.','uncle','grand')
    u={'id':'u','subject_person_id':'child','object_person_id':'uncle','predicate':'paternal_uncle','status':'source_attested','qualifiers':{'lineage':'paternal','generation_difference':-1,'father_person_id':None},'evidence':[ue]}
    f={'id':'f','subject_person_id':'uncle','object_person_id':'grand','predicate':'father','status':'source_attested','qualifiers':{},'evidence':[fe]}
    rows={'child':{'person_id':'child','source_person_ids':['child'],'parent_person_id':None,'source_assertion_id':None,'ancestor_person_id':'grand','connection':'grandfather','generation_distance':2,'intermediate_person_ids':[None]},'uncle':{'person_id':'uncle','source_person_ids':['uncle'],'parent_person_id':'grand','source_assertion_id':'f'},'grand':{'person_id':'grand','source_person_ids':['grand'],'parent_person_id':None}}
    c={'type':'ancestor_through_paternal_uncle','status':'contextual_provisional','human_reviewed':False,'rationale':'Explicit uncle and his explicit father, missing intervening parent retained.','uncle_person_id':'uncle','paternal_uncle_assertion_id':'u','uncle_father_assertion_id':'f','references':[]}
    for a in (u,f):
        for e in a['evidence']:c['references'].append(dict({k:v for k,v in e.items() if k not in ('subject_person_mention_id','object_person_mention_id')},assertion_id=a['id'],scope='whole source context',url=chapter['source']['url']))
    rows['child']['ancestor_connection']=c
    return rows['child'],rows,{'u':u,'f':f},{chapter['id']:chapter}
class AncestorThroughUncle(unittest.TestCase):
    def test_positive(self):self.assertTrue(valid(*fixture()))
    def reject(self,mutate):
        args=fixture();mutate(*args);self.assertFalse(valid(*args))
    def test_reversed_uncle(self):self.reject(lambda m,r,a,c:a['u'].update(subject_person_id='uncle',object_person_id='child'))
    def test_maternal_uncle(self):self.reject(lambda m,r,a,c:a['u']['qualifiers'].update(lineage='maternal'))
    def test_cousin(self):self.reject(lambda m,r,a,c:a['u'].update(predicate='agnatic_cousin'))
    def test_adoptive_father(self):self.reject(lambda m,r,a,c:a['f'].update(predicate='adoptive_father'))
    def test_named_father_not_hidden(self):self.reject(lambda m,r,a,c:a['u']['qualifiers'].update(father_person_id='someone'))
    def test_add_known_father(self):self.reject(lambda m,r,a,c:a.update(extra={'predicate':'father','subject_person_id':'child','object_person_id':'known','status':'source_attested'}))
    def test_wrong_uncle_father(self):self.reject(lambda m,r,a,c:a['f'].update(object_person_id='other'))
    def test_wrong_member_father(self):self.reject(lambda m,r,a,c:m.update(parent_person_id='someone'))
    def test_wrong_generation(self):self.reject(lambda m,r,a,c:m.update(generation_distance=3))
    def test_named_intermediate(self):self.reject(lambda m,r,a,c:m.update(intermediate_person_ids=['someone']))
    def test_cycle(self):self.reject(lambda m,r,a,c:r['grand'].update(source_person_ids=['child']))
    def test_wrong_chapter_source(self):self.reject(lambda m,r,a,c:c['chapter-test'].update(source_id='other'))
    def test_wrong_subject_anchor(self):self.reject(lambda m,r,a,c:c['chapter-test']['paragraphs'][0]['mentions'][0].update(person_id='other'))
    def test_cropped_quote(self):self.reject(lambda m,r,a,c:m['ancestor_connection']['references'][0].update(quote='Nephew'))
    def test_missing_context(self):self.reject(lambda m,r,a,c:m['ancestor_connection']['references'].pop())
    def test_wrong_url(self):self.reject(lambda m,r,a,c:m['ancestor_connection']['references'][0].update(url='https://example.org/unread'))
    def test_source_explicit_not_inferred(self):self.reject(lambda m,r,a,c:m['ancestor_connection'].update(status='source_attested'))
    def test_human_review_claim(self):self.reject(lambda m,r,a,c:m['ancestor_connection'].update(human_reviewed=True))
if __name__=='__main__':unittest.main()
