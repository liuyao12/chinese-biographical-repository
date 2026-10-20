import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from witness_projection import body_positions, repository_positions
from reading_layout import validate_chapter

class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.raw='甲(注)乙丙\n丁戊己\n庚辛壬\n';self.lines=self.raw.splitlines();self.sha=hashlib.sha256(self.raw.encode()).hexdigest()
        self.data={'raw_sha256':self.sha,'units':[]};self.paragraphs=[];self.excerpts=[]
        for i,text in enumerate(('甲乙丙','丁戊己','庚辛壬'),1):
            runs=[]
            for j,ch in enumerate(text):
                a=self.lines[i-1].index(ch);runs.append({'raw_line':i,'raw_start':a,'raw_end':a+1,'start':j,'end':j+1,'surface':ch})
            self.data['units'].append({'candidate_id':str(i),'layer':'body','raw_runs':runs,'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
            self.paragraphs.append({'id':'p'+str(i),'text':text,'mentions':[],'source_position':{'raw_projection_ref':'source-evidence/p.json','unit_key':str(i),'source_layer':'body'}})
            q=self.lines[i-1]+'\n';self.excerpts.append({'proposed_paragraph_id':'a'+str(i),'source_lines':[i,i],'raw_quote':q,'raw_quote_sha256':hashlib.sha256(q.encode()).hexdigest(),'body_selection':{'start':0,'end':2,'begin_anchor':text[0],'end_anchor':text[1]}})
        self.write()
    def write(self):
        (self.root/'source-evidence').mkdir(exist_ok=True);(self.root/'source-evidence/p.json').write_text(json.dumps(self.data))
    def test_three_selected_archives(self):
        c={'source':{'normalization':{'excerpts':self.excerpts}}}
        for i,p in enumerate(self.paragraphs,1):self.assertEqual(len(body_positions(c,{'id':'a'+str(i),'text':p['text'][:2]},self.lines)),2)
    def test_exact_external(self):
        for p in self.paragraphs:self.assertEqual(len(repository_positions(self.root,p,self.lines)[0]),3)
    def test_bad_quote_sha(self):
        self.excerpts[0]['raw_quote_sha256']='bad'
        with self.assertRaises(ValueError):body_positions({'source':{'normalization':{'excerpts':self.excerpts}}},{'id':'a1','text':'甲乙'},self.lines)
    def test_two_newlines_rejected(self):
        e=self.excerpts[0];e['raw_quote']+='\n';e['raw_quote_sha256']=hashlib.sha256(e['raw_quote'].encode()).hexdigest()
        with self.assertRaises(ValueError):body_positions({'source':{'normalization':{'excerpts':self.excerpts}}},{'id':'a1','text':'甲乙'},self.lines)
    def test_bad_selection_and_anchor(self):
        for key,val in [('end',99),('start',True),('begin_anchor','錯')]:
            c={'source':{'normalization':{'excerpts':copy.deepcopy(self.excerpts)}}};c['source']['normalization']['excerpts'][0]['body_selection'][key]=val
            with self.assertRaises(ValueError):body_positions(c,{'id':'a1','text':'甲乙'},self.lines)
    def test_bad_external_variants(self):
        original=copy.deepcopy(self.data)
        for mutation in ('duplicate','offset','overlap','wrong','sha','out'):
            self.data=copy.deepcopy(original);u=self.data['units'][0];r=u['raw_runs']
            if mutation=='duplicate':self.data['units'].append(copy.deepcopy(u))
            if mutation=='offset':r[1]['start']=0
            if mutation=='overlap':r[1].update(raw_start=0,raw_end=1,surface='甲')
            if mutation=='wrong':r[0]['surface']='錯'
            if mutation=='sha':u['text_sha256']='bad'
            if mutation=='out':r[0]['raw_line']=99
            self.write()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):repository_positions(self.root,self.paragraphs[0],self.lines)
    def test_declared_unit_text_mismatch(self):
        self.data['units'][0]['text']='錯';self.write()
        with self.assertRaises(ValueError):repository_positions(self.root,self.paragraphs[0],self.lines)
    def test_symlink_outside_evidence_inside_root(self):
        other=self.root/'elsewhere';other.mkdir();target=other/'p.json';target.write_text(json.dumps(self.data))
        link=self.root/'source-evidence/link.json';link.symlink_to(target)
        p=copy.deepcopy(self.paragraphs[0]);p['source_position']['raw_projection_ref']='source-evidence/link.json'
        with self.assertRaises(ValueError):repository_positions(self.root,p,self.lines)

    def test_legacy_key_and_mixed_formats(self):
        for u in self.data['units']:
            u['key']=u.pop('candidate_id');u['text']=''.join(r['surface']for r in u['raw_runs']);u.pop('text_sha256')
        self.data['units'][1]['candidate_id']='2';self.write()
        for p in self.paragraphs:self.assertEqual(len(repository_positions(self.root,p,self.lines)[0]),3)
    def test_legacy_key_negative_cases(self):
        original=copy.deepcopy(self.data)
        for mutation in ('missingkey','mixed','duplicate','missingtextsha','windowbounds','windowruns','windowparagraph'):
            self.data=copy.deepcopy(original);u=self.data['units'][0];p=copy.deepcopy(self.paragraphs[0])
            if mutation=='missingkey':u.pop('candidate_id')
            if mutation=='mixed':u['key']='different'
            if mutation=='duplicate':self.data['units'][1]['key']='1';self.data['units'][1].pop('candidate_id')
            if mutation=='missingtextsha':u.pop('text_sha256')
            if mutation=='windowbounds':u['raw_window']=[0,99]
            if mutation=='windowruns':u['raw_window']=[2,2]
            if mutation=='windowparagraph':u['raw_window']=[1,1];p['source_position'].update(first_line=1,last_line=2)
            self.write()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):repository_positions(self.root,p,self.lines)

    def test_unsafe_path(self):
        for path in ('../p.json','/tmp/p.json','source-evidence/../p.json'):
            p=copy.deepcopy(self.paragraphs[0]);p['source_position']['raw_projection_ref']=path
            with self.assertRaises(ValueError):repository_positions(self.root,p,self.lines)
    def chapter(self):
        source={'source_id':'s','revision_id':'r','raw_file_sha256':self.sha,'source_blob_sha':hashlib.sha1(b'blob '+str(len(self.raw.encode())).encode()+b'\0'+self.raw.encode()).hexdigest(),'url':'https://example.org/fixed','raw_path':'sources/witnesses/raw.txt'}
        c={'id':'c','record_type':'marked_chapter','source_id':'s','source':{'revision_id':'r','response_sha256':self.sha,'source_blob_sha':source['source_blob_sha'],'permalink':source['url'],'normalization':{'excerpts':self.excerpts}},'paragraphs':copy.deepcopy(self.paragraphs)}
        archives=[]
        for i,p in enumerate(self.paragraphs,1):
            c['paragraphs'].append({'id':'a'+str(i),'text':p['text'][:2],'mentions':[]})
            archives.append({'paragraph_id':'a'+str(i),'default_collapsed':True,'reason':'same_fixed_witness_expanded_reading_unit','label':'舊節引','canonical_segments':[{'excerpt_start':0,'excerpt_end':2,'canonical_start':0,'canonical_end':2,'canonical_paragraph_id':p['id'],'quote':p['text'][:2]}]})
        c['reading_layout']={'version':1,'human_reviewed':False,'source':source,'concordance_path':'corpus/book/con.json','primary_paragraph_ids':[p['id']for p in self.paragraphs],'archival_excerpts':archives}
        for rel,data in [('sources/witnesses/raw.txt',self.raw),('corpus/book/con.json',json.dumps({'record_type':'source_occurrence_concordance_set','format_version':'0.2','human_reviewed':False,'source':source,'records':[]})),('registry/persons.json','{"persons":[]}')]:
            path=self.root/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data)
        return c
    def test_full_partition_three_archives(self):validate_chapter(self.chapter(),self.root)
    def test_missing_partition(self):
        c=self.chapter();c['reading_layout']['primary_paragraph_ids'].pop()
        with self.assertRaises(ValueError):validate_chapter(c,self.root)
    def test_wrong_raw_sha(self):
        c=self.chapter();self.data['raw_sha256']='bad';self.write()
        with self.assertRaises(ValueError):validate_chapter(c,self.root)
    def concordance(self):
        c=self.chapter(); source=c['reading_layout']['source'];records=[]
        for i in range(3):
            primary=c['paragraphs'][i];archive=c['paragraphs'][3+i]
            for p,prefix in ((primary,'c'),(archive,'d')):
                p['mentions']=[{'id':prefix+str(i),'start':0,'end':1,'surface':p['text'][0],'kind':'person','person_id':'person'}]
            n=i+1
            records.append({'id':'r'+str(i),'human_reviewed':False,'kind':'resolved_person_occurrence_alias','canonical_mention_id':'c'+str(i),'duplicate_mention_id':'d'+str(i),'person_id':'person','surface':primary['text'][0],'canonical':{'chapter_id':'c','paragraph_id':primary['id'],'start':0,'end':1},'duplicate':{'chapter_id':'c','paragraph_id':archive['id'],'start':0,'end':1},'canonical_projection':'repository_raw_projection_ref','duplicate_projection':'kanripo_parenthesized_commentary_body_projection','literal_character_positions':[{'line':n,'column':0}]})
        con={'record_type':'source_occurrence_concordance_set','format_version':'0.2','human_reviewed':False,'source':source,'records':records}
        (self.root/'registry/persons.json').write_text('{"persons":[{"id":"person"}]}')
        (self.root/'corpus/book/con.json').write_text(json.dumps(con))
        return c,con
    def test_occurrence_three_archives(self):
        from occurrence_concordance import occurrence_catalog
        c,con=self.concordance();aliases,_=occurrence_catalog(self.root,[c,con]);self.assertEqual(len(aliases),3);validate_chapter(c,self.root)
    def test_occurrence_one_to_many_cycle_wrong_person_position(self):
        from occurrence_concordance import occurrence_catalog
        for kind in ('repeat','self','person','position','revision'):
            c,con=self.concordance();r=con['records'][0]
            if kind=='repeat':con['records'].append(copy.deepcopy(r));con['records'][-1]['id']='other'
            if kind=='self':r['canonical_mention_id']=r['duplicate_mention_id']
            if kind=='person':r['person_id']='other'
            if kind=='position':r['literal_character_positions'][0]['column']=1
            if kind=='revision':con['source']['revision_id']='different'
            with self.subTest(kind=kind),self.assertRaises(ValueError):occurrence_catalog(self.root,[c,con])

    def test_no_layout_unchanged(self):validate_chapter({'paragraphs':[]},self.root)

if __name__=='__main__':unittest.main()
