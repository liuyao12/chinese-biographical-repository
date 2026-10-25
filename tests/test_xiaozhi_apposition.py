"""小字 is not 小名. Exact new apposition; unchanged two legacy grammars."""
from pathlib import Path
import copy,json,unittest
try:
    from scripts.name_childhood import validate_childhood_name
    from scripts.name_xiaoming import validate_xiaoming
except ImportError:
    from name_childhood import validate_childhood_name
    from name_xiaoming import validate_xiaoming
ROOT=Path(__file__).resolve().parents[1]

def synthetic(kind):
    text='阿衡者季明小字也' if kind=='explicit_xiaozhi_statement' else '季明又小字阿衡'
    if kind=='explicit_xiaozhi_statement':v,s,k=(0,2),(3,5),(5,7)
    else:v,s,k=(5,7),(0,2),(3,5)
    pid='unrelated_synthetic_identity';para='synthetic:paragraph'
    def anchor(span,mid=None):
        a={'paragraph_id':para,'start':span[0],'end':span[1],'surface':text[slice(*span)]}
        if mid:a['person_mention_id']=mid
        return a
    va,sa,ka=anchor(v,'value'),anchor(s,'subject'),anchor(k)
    # The legacy 者 branch accepts kindless mentions. The existing 又 branch
    # already requires kind:person; preserve both distinct contracts.
    p={'id':para,'text':text,'mentions':[{'id':a['person_mention_id'],'person_id':pid,**{key:a[key]for key in ('start','end','surface')}}for a in (va,sa)]}
    if kind=='explicit_subject_xiaozhi':
        for m in p['mentions']:m['kind']='person'
    n={'person_id':pid,'paragraph_id':para,'quote':text,'xiaozhi':'阿衡','xiaozhi_basis':{'kind':kind,'source_term':text,'value_anchor':va,'subject_anchor':sa,'marker_anchor':ka,'status':'source_attested','human_reviewed':False,'rationale':'independent synthetic grammar'}}
    return n,p

class XiaozhiAppositionTests(unittest.TestCase):
    def setUp(self):
        c=json.loads((ROOT/'corpus/songshu/052-xiejingren.json').read_text())
        self.p=next(p for p in c['paragraphs']if p['id']=='c-songshu-052-xiejingren:p015')
        rows=json.loads((ROOT/'corpus/songshu/052-xiejingren-name-components.json').read_text())['records']
        self.n=copy.deepcopy(next(n for n in rows if n['id']=='name-song052-literal-039'))
    def reject(self,n=None,p=None):
        with self.assertRaises(ValueError):validate_childhood_name(n if n is not None else self.n,p if p is not None else self.p)
    def test_real_source_value_subject_marker(self):
        before=copy.deepcopy((self.n,self.p));validate_childhood_name(self.n,self.p)
        self.assertEqual(self.n['xiaozhi'],'道兒');self.assertNotIn('xiaoming',self.n);self.assertEqual(before,(self.n,self.p))
    def test_different_person(self):
        p=copy.deepcopy(self.p);mid=self.n['xiaozhi_basis']['subject_anchor']['person_mention_id'];next(m for m in p['mentions']if m['id']==mid)['person_id']='other';self.reject(p=p)
    def test_wrong_kind_still_requires_zhe(self):
        n=copy.deepcopy(self.n);n['xiaozhi_basis']['kind']='explicit_xiaozhi_statement';self.reject(n=n)
    def test_wrong_value(self):
        n=copy.deepcopy(self.n);n['xiaozhi']='別字';self.reject(n=n)
    def test_xiaoming_is_not_xiaozhi(self):
        n=copy.deepcopy(self.n);n['xiaoming']=n.pop('xiaozhi');self.reject(n=n)
        with self.assertRaises(ValueError):validate_xiaoming(n,self.p)
    def test_missing_ye_even_with_quote_cochanged(self):
        n=copy.deepcopy(self.n);p=copy.deepcopy(self.p);end=n['xiaozhi_basis']['marker_anchor']['end'];p['text']=p['text'][:end]+p['text'][end+1:];n['quote']=p['text'];n['xiaozhi_basis']['source_term']=n['xiaozhi_basis']['source_term'][:-1];self.reject(n=n,p=p)
    def test_shifted_value_anchor(self):
        n=copy.deepcopy(self.n);n['xiaozhi_basis']['value_anchor']['start']+=1;self.reject(n=n)
    def test_old_two_grammars_keep_original_anchor_rules(self):
        for kind in ('explicit_xiaozhi_statement','explicit_subject_xiaozhi'):
            n,p=synthetic(kind);validate_childhood_name(n,p)
        n,p=synthetic('explicit_xiaozhi_statement');p['text']=p['text'].replace('者','');n['quote']=p['text'];self.reject(n=n,p=p)
    def test_dual_anchors_must_be_distinct(self):
        n=copy.deepcopy(self.n);n['xiaozhi_basis']['subject_anchor']=copy.deepcopy(n['xiaozhi_basis']['value_anchor']);self.reject(n=n)

if __name__=='__main__':unittest.main()
