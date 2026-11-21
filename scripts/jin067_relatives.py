"""Validate the named child roles in the two parallel tellings of the feeding account."""
def valid(a, paragraphs):
    try:
        e, = a['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        names = {m['id']:m for m in p['mentions'] if m['kind']=='person'}
        child=names[e['subject_person_mention_id']]; adult=names[e['object_person_mention_id']]
        s=p['text']; q=a['qualifiers'];role=q['reading_basis']['kind']
        if (a['status']!='source_attested' or a.get('human_reviewed') is not False or e['chapter_id']!=cid
                or e['quote']!=s or child['person_id']!=a['subject_person_id'] or adult['person_id']!=a['object_person_id']
                or child['person_id']==adult['person_id'] or child['surface']=='其' or adult['surface']=='其'):
            return False
        pairing='兄子邁、外甥周翼並小'
        if role=='jin067_contemporaneous_nephews':
            if s.count(pairing)!=1 or not s.startswith('初，鑒值永嘉喪亂') or adult['surface']!='鑒' or adult['start']!=2:
                return False
            paired=s.index(pairing)
            if a['predicate']=='paternal_uncle':
                return q['source_term']=='兄子邁' and child['surface']=='邁' and child['start']==paired+2
            if a['predicate']=='maternal_uncle':
                return (q['source_term']=='外甥周翼' and q['lineage']=='maternal'
                        and q['generation_difference']==-1 and child['surface']=='周翼' and child['start']==paired+6
                        and '鑒之薨也，翼追撫育之恩' in s)
        return False
    except (KeyError,TypeError,ValueError,IndexError,StopIteration):
        return False
