import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import founder_generation_errors

class HanFounderGenerationEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table=json.loads((Path(__file__).resolve().parents[1] / 'data/historical-tables/hanshu-016.json').read_text());row=cls.table['fragments'][0]['rows'][0];cls.cells={c['column']:c for c in row['cells']};
        for cell in row['cells']: cell['person_mentions'] = []
        cls.ids={k:'synthetic-'+k for k in ['founder','son','grandchild','descendant']}
        def mark(col,word,pid,n):
            cell=cls.cells[col];start=cell['text'].index(word);m={'id':cell['id']+'-synthetic-'+str(n),'start':start,'end':start+len(word),'surface':word,'person_id':pid};cell['person_mentions'].append(m);return m
        cls.founder=mark(0,'蟲達',cls.ids['founder'],0);cls.son=mark(4,'捷',cls.ids['son'],0);cls.grandchild=mark(5,'皇柔',cls.ids['grandchild'],0);cls.local=mark(7,'達',cls.ids['founder'],0);cls.descendant=mark(7,'宣',cls.ids['descendant'],1)
    def evidence(self,col,who):
        source=self.table['source'];m={'son':self.son,'grandchild':self.grandchild,'descendant':self.descendant}[who];terms={4:('子',1),5:('孫',2),7:('玄孫',4)};term,generation=terms[col]
        e={'kind':'table_cell','table_id':self.table['id'],'relationship_layout':'founder_generation_column','table_cell_id':self.cells[0]['id'],'subject_table_cell_id':self.cells[col]['id'],'quote':self.cells[0]['text'],'subject_quote':self.cells[col]['text'],'object_mention_id':self.founder['id'],'subject_mention_id':m['id'],'generation_source_term':term,'generation_distance':generation}
        for k,v in [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),('source_id','id'),('source_revision','revision')]:e[k]=source[v]
        if col==7:e.update(local_ancestor_mention_id=self.local['id'],source_kinship_term='達玄孫')
        return e
    def check(self,e,who,predicate,table=None,ancestor=None):return founder_generation_errors(e,{self.table['id']:table or self.table},self.ids[who],ancestor or self.ids['founder'],predicate)
    def test_actual_child_column_supports_father_only(self):
        e=self.evidence(4,'son');self.assertEqual(self.check(e,'son','father'),[]);self.assertTrue(self.check(e,'son','grandfather'))
    def test_actual_grandchild_column_never_supplies_a_missing_father(self):
        e=self.evidence(5,'grandchild');self.assertEqual(self.check(e,'grandchild','grandfather'),[]);self.assertTrue(self.check(e,'grandchild','father'));self.assertTrue(self.check(e,'grandchild','father',ancestor=self.ids['son']))
    def test_emperor_date_anchor_before_heir_is_not_a_prior_holder(self):
        t=copy.deepcopy(self.table);cell=t['fragments'][0]['rows'][0]['cells'][4]
        cell['person_mentions'].append({'id':'emperor-date','start':0,'end':2,'surface':'孝文','person_id':'synthetic-wendi'})
        self.assertEqual(self.check(self.evidence(4,'son'),'son','father',table=t),[])
    def test_later_named_holder_is_not_the_generation_header_subject(self):
        t=copy.deepcopy(self.table);cell=t['fragments'][0]['rows'][0]['cells'][4]
        cell['text']='矦別人嗣。'+cell['text']
        for m in cell['person_mentions']:m['start']+=5;m['end']+=5
        e=self.evidence(4,'son');e['subject_quote']=cell['text']
        self.assertTrue(self.check(e,'son','father',table=t))
    def test_previous_child_cell_cannot_be_used_as_the_parent(self):
        e=self.evidence(5,'grandchild');e.update(table_cell_id=self.cells[4]['id'],object_mention_id=self.son['id'],quote=self.cells[4]['text'],generation_distance=1);self.assertTrue(self.check(e,'grandchild','father',ancestor=self.ids['son']))
    def test_explicit_xuan_preserves_four_generations_to_founder(self):
        e=self.evidence(7,'descendant');self.assertEqual(self.check(e,'descendant','ancestor'),[]);self.assertTrue(self.check(e,'descendant','father'));self.assertTrue(self.check(e,'descendant','grandfather'));self.assertTrue(self.check(e,'descendant','ancestor',ancestor=self.ids['grandchild']))
    def test_xuan_requires_actual_local_ancestor_anchor(self):
        for changes in [{'local_ancestor_mention_id':'missing'},{'source_kinship_term':'捷玄孫'},{'generation_distance':3},{'generation_source_term':'曾孫'}]:
            e=self.evidence(7,'descendant');e.update(changes);self.assertTrue(self.check(e,'descendant','ancestor'),changes)
    def test_wrong_work_or_revision_cannot_reuse_the_row(self):
        for changes in [{'work_id':'w-shiji'},{'source_revision':'1'},{'book_id':'b-shiji-016'},{'chapter_id':'table-chapter-shiji-016'}]:
            e=self.evidence(4,'son');e.update(changes);self.assertTrue(self.check(e,'son','father'),changes)
    def test_do_not_turn_native_cells_into_a_paragraph(self):
        e=self.evidence(4,'son');e['paragraph_id']='synthetic-paragraph';self.assertTrue(self.check(e,'son','father'));e=self.evidence(4,'son');e['subject_quote']='捷';self.assertTrue(self.check(e,'son','father'))
    def test_generation_bools_and_other_column_names_are_rejected(self):
        e=self.evidence(4,'son');e['generation_distance']=True;self.assertTrue(self.check(e,'son','father'));t=copy.deepcopy(self.table);t['fragments'][0]['columns'][5]['text']='承爵者';self.assertTrue(self.check(self.evidence(5,'grandchild'),'grandchild','grandfather',table=t))
    def test_different_row_cannot_supply_founder(self):
        e=self.evidence(4,'son');e['table_cell_id']='another-row-c00';self.assertTrue(self.check(e,'son','father'))
    def test_empty_generation_label_does_not_invent_a_named_greatgrandchild(self):
        e=self.evidence(5,'grandchild');e.update(subject_table_cell_id=self.cells[6]['id'],subject_quote=self.cells[6]['text'],generation_source_term='曾孫',generation_distance=3);self.assertTrue(self.check(e,'grandchild','great_grandfather'))

if __name__=='__main__':unittest.main(verbosity=2)
