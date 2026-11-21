"""作用域限於《南史》卷19謝瞻的三處正文，按原述主語分辨親屬與報齡。"""
import hashlib
H = {'c-nanshi-019-nan19:p002': 'cb3d219658eb2a6e1463190d4713a78fe78b37d47177fefa00230a089b08e804', 'c-nanshi-019-nan19:zhan-l042': 'b6698dd9ba2d2d3de64bd81c63ac75966a5cce249da2dd0e15cb90d9c905262b', 'c-nanshi-019-nan19:zhan-l044': 'f7801d46a856979d36cddcca1e5dcb3ee2ac36d95e1cb05c6bb22471657315d1', 'c-nanshi-019-nan19:zhan-l050': '88a531940be00f84f19133716214eca6da1384949305a78c3d7dc3f1db8c23b9'}
CH = 'c-nanshi-019-nan19'
SRC = 's-nanshi-019-nan19-ws1531762'
def fixed(p):
    key=p.get('id')
    return (key in H and hashlib.sha256(p['text'].encode()).hexdigest()==H[key]
            and p.get('text_layer')=='received_chapter' and p.get('source_position',{}).get('revision_id')==1531762)
def contains(m,p,phrase,surface):
    t=p['text']
    return (t.count(phrase)==1 and phrase.count(surface)==1 and m.get('surface')==surface
            and m.get('start')==t.index(phrase)+phrase.index(surface)
            and m.get('end')==m.get('start')+len(surface))
def kin_valid(a,paragraphs):
    q=a.get('qualifiers',{})
    def cross(e):
        hit=paragraphs.get(e.get('paragraph_id'))
        if not hit or hit[0]!=CH or e.get('chapter_id')!=CH or e.get('source_id')!=SRC:return False
        p=hit[1]
        if not fixed(p) or e.get('quote')!=p.get('text'):return False
        ms={m['id']:m for m in p['mentions']}
        left=ms.get(e.get('subject_person_mention_id'),{});right=ms.get(e.get('object_person_mention_id'),{})
        if left.get('person_id')!=a['subject_person_id'] or right.get('person_id')!=a['object_person_id'] or left.get('kind')!=right.get('kind') or left.get('kind')!='person':return False
        if a['predicate']=='agnatic_senior_kin':
            intro='瞻字宣遠' if p['id'].endswith('p002') else '瞻文章之美'
            return (q.get('source_term')=='從叔混' and q.get('kinship_structure')=={'lineage':'paternal','generation_difference':-1,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'unknown'} and contains(left,p,intro,'瞻') and contains(right,p,'與從叔混、族弟靈運','混'))
        return (a['predicate']=='raised_by' and q=={'source_term':'瞻幼孤，叔母劉撫養有恩','care_basis':'orphan_reared_by_named_uncle_wife','legal_adoption_status':'not_asserted'} and contains(left,p,q['source_term'],'瞻') and contains(right,p,q['source_term'],'劉'))
    return bool(a.get('evidence')) and all(cross(e) for e in a['evidence'])
def kin_age(age,chapter,e):
    if chapter.get('id')!=CH or chapter.get('source_id')!=SRC or e.get('source_id')!=SRC or e.get('chapter_id')!=CH:return False
    ps={p['id']:p for p in chapter['paragraphs']};p=ps.get(e.get('paragraph_id'),{})
    if not fixed(p) or p['id']!=CH+':zhan-l044' or e.get('quote')!=p['text']:return False
    key=age.get('source_reference_id')
    rows=chapter['annotation'].get('person_reference_occurrences',[])
    target=next((r for r in rows if r['id']==key and r['paragraph_id']==p['id']),{})
    prior=ps[CH+':p002']
    older=next((m for m in prior['mentions'] if contains(m,prior,'瞻字宣遠','瞻')),{})
    younger=next((m for m in prior['mentions'] if contains(m,prior,'晦次兄也','晦')),{})
    named=next((m for m in p['mentions'] if contains(m,p,'欲以瞻爲吳興郡','瞻')),{})
    return (fixed(prior) and age['source_term']=='年始三十' and age['value']==30 and age['source_number']=='三十'
            and target.get('person_id')==younger.get('person_id')==age['person_id'] and target.get('referent_role')=='third_person'
            and contains(target,p,'弟年始三十','弟') and named.get('person_id')==older.get('person_id')!=age['person_id'])
