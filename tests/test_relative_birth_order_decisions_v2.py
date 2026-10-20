import copy,hashlib,types
from pathlib import Path
from scripts.relative_birth_order_decisions import decision_errors

def base():
 p=Path(__file__).with_name('test_relative_birth_order_decisions.py');m=types.ModuleType('order_fixture_base');m.__file__=str(p);exec(compile(p.read_text(),str(p),'exec'),m.__dict__);return m.WitnessedOrderTests

class LocalAndParallelOrderTests(base()):
    def make_both_external(self):
        quote='懐敬懐肅之弟也';w=self.d['claims'][0]['witness'];p=self.root/w['path'];p.write_text(quote)
        w.update(quote=quote,start=0,end=len(quote),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),syntax='younger_older_zhidiye',
                 older_span={'start':2,'end':4,'surface':'懐肅'},younger_span={'start':0,'end':2,'surface':'懐敬'})

    def test_two_external_witnesses_cannot_skip_local_binding(self):
        self.make_both_external()
        self.assertTrue(self.errors())

    def test_two_local_witnesses_rejected(self):
        self.d['claims'][1]['witness']=copy.deepcopy(self.d['claims'][0]['witness'])
        self.assertTrue(self.errors())
