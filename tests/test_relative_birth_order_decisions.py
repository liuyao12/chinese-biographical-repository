import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.relative_birth_order_decisions import decision_errors, preferred_relation, relevant_decisions


class WitnessedOrderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        rev = 'a' * 40
        self.ch = {'id': 'c', 'source_id': 's', 'source': {}, 'annotation': {}, 'paragraphs': [
            {'id': 'p', 'text': '懷肅次弟懷敬', 'mentions': [
                {'id': 'm1', 'person_id': 'A', 'surface': '懷肅'}, {'id': 'm2', 'person_id': 'B', 'surface': '懷敬'}]}]}
        self.a = {'id': 'r', 'subject_person_id': 'B', 'object_person_id': 'A', 'predicate': 'brother',
                  'qualifiers': {'source_term': '次弟', 'relative_birth_order': {'operator': 'lt', 'scope': 'siblings', 'older_person_id': 'A', 'younger_person_id': 'B'}},
                  'evidence': [{'chapter_id': 'c', 'paragraph_id': 'p', 'quote': '懷肅次弟懷敬'}]}
        claims = []
        for i, (quote, older, younger, syntax) in enumerate([
            ('懷肅次弟懷敬', 'A', 'B', 'older_cidi_younger'), ('懐肅懐敬之弟也', 'B', 'A', 'younger_older_zhidiye')]):
            path = 'sources/x%d.txt' % i
            dest = self.root / path; dest.parent.mkdir(exist_ok=True); dest.write_text(quote)
            oldname, youngname = ('懷肅', '懷敬') if i == 0 else ('懐敬', '懐肅')
            def span(s):
                at = quote.index(s); return {'start': at, 'end': at + len(s), 'surface': s}
            witness = {'path': path, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(), 'fixed_url': 'https://example.org/' + rev,
                       'revision_id': rev, 'raw_line_range': [1, 1], 'quote': quote, 'start': 0, 'end': len(quote),
                       'older_span': span(oldname), 'younger_span': span(youngname), 'syntax': syntax}
            claims.append({'id': 'claim%d' % i, 'older_person_id': older, 'younger_person_id': younger, 'witness': witness})
        self.ch['source'] = {'raw_path': claims[0]['witness']['path'], 'raw_file_sha256': claims[0]['witness']['sha256']}
        self.d = {'id': 'd', 'assertion_id': 'r', 'person_ids': ['A', 'B'], 'source_mention_ids': ['m1', 'm2'],
                  'source_term': '懷肅次弟懷敬', 'claims': claims, 'preferred_claim_id': None,
                  'rationale': '兩部正文相反，未定。', 'reviewer': 'AI', 'human_reviewed': False, 'status': 'interpretation_disputed'}
        self.ch['annotation']['relative_birth_order_decisions'] = [self.d]

    def errors(self):
        return decision_errors(self.root, {'c': self.ch}, {'r': self.a}, {'A', 'B'})

    def test_valid_and_projection_keeps_raw(self):
        self.assertEqual([], self.errors())
        old = copy.deepcopy(self.a)
        p = preferred_relation(self.a, [self.d])
        self.assertEqual('brother', p['predicate'])
        self.assertNotIn('relative_birth_order', p['qualifiers'])
        self.assertEqual(old, self.a)
        self.assertEqual([dict(self.d, chapter_id='c', source_id='s')], relevant_decisions({'c': self.ch}, {'A'}))
        self.assertEqual(self.a, preferred_relation(self.a, []))

    def test_mutations_rejected(self):
        mutations = [
            lambda: self.d.update(assertion_id='missing'),
            lambda: self.d.update(person_ids=['A', 'C']),
            lambda: self.d.update(preferred_claim_id='claim0'),
            lambda: self.d.update(human_reviewed=True),
            lambda: self.d.update(source_mention_ids=['m1', 'missing']),
            lambda: self.d['claims'][1].update(older_person_id='A', younger_person_id='B'),
            lambda: self.d['claims'][1]['witness'].update(quote='假文'),
            lambda: self.d['claims'][1]['witness'].update(start=1),
            lambda: self.d['claims'][1]['witness'].update(sha256='0' * 64),
            lambda: self.d['claims'][1]['witness'].update(path='../outside'),
            lambda: self.d['claims'][1]['witness']['older_span'].update(surface='錯名'),
            lambda: self.d['claims'][1]['witness'].update(syntax='guess'),
            lambda: self.ch['annotation']['relative_birth_order_decisions'].append(copy.deepcopy(self.d)),
            lambda: self.a.update(predicate='father'),
            lambda: self.a['qualifiers']['relative_birth_order'].update(older_person_id='C'),
        ]
        for mutation in mutations:
            before = copy.deepcopy((self.ch, self.a))
            with self.subTest(mutation=mutation):
                mutation(); self.assertTrue(self.errors())
            self.ch, self.a = before
            self.d = self.ch['annotation']['relative_birth_order_decisions'][0]

    def test_literal_mother_clauses_preserve_unknown_birth(self):
        from scripts.song047_maternal import clause_valid
        for text,subject,obj,killer,kind in [
            ('道存出奔元凶殺其母以徇','道存','其母','元凶','named_child_killer_qimu'),
            ('髙祖產而皇妣殂','髙祖','皇妣',None,'named_child_birth_huangbi_died')]:
            def mark(mid,s,pid):
                at=text.index(s);return {'id':mid,'kind':'person','person_id':pid,'surface':s,'start':at,'end':at+len(s)}
            ms=[mark('s',subject,'child'),mark('o',obj,'mother')]
            if killer:ms.append(mark('k',killer,'killer'))
            p={'id':'p','text':text,'mentions':ms}
            a={'predicate':'maternal_role','human_reviewed':False,'status':'source_attested','subject_person_id':'child','object_person_id':'mother',
               'qualifiers':{'source_term':text,'role':'mother_unspecified','biological_mother':None,'father_person_id':None,'maternal_clause':{'kind':kind,'start':0,'end':len(text)}},
               'evidence':[{'chapter_id':'c','paragraph_id':'p','quote':text,'subject_person_mention_id':'s','object_person_mention_id':'o'}]}
            self.assertTrue(clause_valid(a,{'p':('c',p)}))
            for field,value in [('biological_mother',True),('father_person_id','killer'),('role','birth_mother')]:
                bad=copy.deepcopy(a);bad['qualifiers'][field]=value;self.assertFalse(clause_valid(bad,{'p':('c',p)}))
            bad=copy.deepcopy(a);bad['evidence'][0]['subject_person_mention_id']='o';self.assertFalse(clause_valid(bad,{'p':('c',p)}))
            bad=copy.deepcopy(a);bad['qualifiers']['maternal_clause']['start']=1;self.assertFalse(clause_valid(bad,{'p':('c',p)}))


if __name__ == '__main__':
    unittest.main()
