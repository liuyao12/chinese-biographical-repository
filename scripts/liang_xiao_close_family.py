"""Source-bound near Liang Xiao family: real current rekey, never redirects.

Only exact historical endpoint values are projected; raw/MIDs/record IDs survive.
"""
import copy
import hashlib
import json
from pathlib import Path

REF='source-evidence/liang-xiao-close-family/family-source-contract.json'
SHA='a567e066707b4220c71c1da89dcc1d82540e236c7590abe0818034bd282a4d10'
KIND='fixed_liang_xiao_close_family'
NS='corpus/nanshi/006-liang-close-family.json'
NSID='c-nanshi-006-liang-close-family'
ZH='corpus/zhoushu/041-wangbao-ws2432538.json'


def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b


def expand(x,roles):
    if isinstance(x,str):return roles.get(x,x)
    if isinstance(x,list):return[expand(v,roles)for v in x]
    if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
    return x


def raw(root,rel):
    root=Path(root).resolve();p=Path(rel)
    assert not p.is_absolute()and'..'not in p.parts
    p=root/p;assert p.is_file()and not p.is_symlink()and p.resolve().is_relative_to(root)
    return p.read_bytes()


def read(root,rel):return json.loads(raw(root,rel))


def active(root):return (Path(root)/REF).is_file()


def typed_projection(x,mapping):
    """Exact equality only; never replace ID substrings inside opaque source IDs."""
    if isinstance(x,str):return mapping.get(x,x)
    if isinstance(x,list):return[typed_projection(v,mapping)for v in x]
    if isinstance(x,dict):return{mapping.get(k,k):typed_projection(v,mapping)for k,v in x.items()}
    return x


def contract(root):
    b=raw(root,REF);assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b)
    for p,h in [(c['ledger_path'],c['ledger_sha256']),(c['taizu_bridge_path'],c['taizu_bridge_sha256']),
                (c['retirement_receipt_path'],c['retirement_receipt_sha256'])]:
        assert hashlib.sha256(raw(root,p)).hexdigest()==h
    units=read(root,c['ledger_path']);us={u['id']:u for u in units}
    assert len(us)==len(units)==6
    for u in units:
        assert u['human_reviewed']is False and u['image_verified']is False
        assert u['actual_print_edition_id']is None
        assert hashlib.sha256(u['text'].encode()).hexdigest()==u['text_sha256']
        if u['capture_kind']=='web_tool_rendered_complete_paragraph_observation':assert u['original_wikitext_obtained']is False
        else:
            assert u['original_wikitext_obtained']is True
            assert ''.join(u['raw_paragraph'][i]for i in u['raw_paragraph_character_offsets'])==u['text']
    assert '姓蕭氏' in us['nanshi006-opening']['text']
    assert '道賜生皇考，諱順之' in us['nanshi006-opening']['text']
    assert '追尊皇考爲文皇帝，廟曰太祖' in us['liang002-taizu-bridge']['text']
    assert '鄱陽忠烈王恢字弘達，太祖第九子也' in us['liang022-hui-opening']['text']
    assert '太宗簡文皇帝諱綱' in us['liang004-opening']['text'] and '高祖第三子' in us['liang004-opening']['text']
    assert '高祖第七子也' in us['liang005-opening']['text'] and '高祖第八子也' in us['liang055-ji-opening']['text']
    assert us['liang004-opening']['fixed_permalink_body_read']is False
    assert us['liang055-ji-opening']['fixed_permalink_body_read']is False
    # Existing fixed witnesses are verified through their true captures, not relabelled rendered text.
    u=us['liang022-hui-opening'];fixed=raw(root,u['existing_raw_path']);assert hashlib.sha256(fixed).hexdigest()==u['existing_raw_sha256']
    assert fixed.decode()[u['raw_start']:u['raw_end']]==u['raw_paragraph']
    u=us['liang005-opening'];assert u['existing_container']=='source-evidence/nanshi033-pei-source-reading/review.json';container=read(root,u['existing_container'])
    cases=container['fixed_king_primary_witnesses'];case,=[v for v in cases if str(v['metadata']['revision_id'])=='2312810']
    assert hashlib.sha256(case['raw_wikitext'].encode()).hexdigest()==u['raw_wikitext_sha256']
    assert u['raw_paragraph']in case['raw_wikitext']
    return c


def _without_alias_mids(aliases, removed):
    result=[]
    for alias in aliases:
        assert type(alias)is dict and type(alias.get('surface'))is str and type(alias.get('mention_ids'))is list
        assert all(type(mid)is str for mid in alias['mention_ids'])
        mids=[mid for mid in alias['mention_ids']if mid not in removed]
        if mids:
            value=copy.deepcopy(alias);value['mention_ids']=mids;result.append(value)
    return result


def _external_growth(root, physical, people, expected, ownids, ownmids, records=None):
    """Conserve prior rows; independently prove every added physical source MID.

    This is reciprocal source consistency, not automatic historical identity proof.
    Scanning current marked chapters also detects a new marker whose reverse was
    entirely removed; a caller or registry ledger alone is never its authority.
    """
    works={w['id']:w for w in read(root,'registry/works.json')['works']}
    bases=read(root,'registry/work-provenance.json')['text_bases']
    prior={pid:{e['mention_id']for e in want['evidence']}for pid,want in expected.items()}
    additions={pid:{}for pid in expected};chapters={}
    for path in sorted((Path(root)/'corpus').glob('*/*.json')):
        ch=read(root,str(path.relative_to(root)))
        if type(ch)is not dict or ch.get('record_type')!='marked_chapter' or ch.get('id')in ownids:continue
        relevant=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m.get('person_id')in expected and m['id']not in prior[m['person_id']] and m['id']not in ownmids]
        if not relevant:continue
        assert ch['id']not in chapters;chapters[ch['id']]=ch
        work=works[ch['work_id']];book,=[b for b in work['books']if b['id']==ch['book_id']]
        assert ch['id']in book['chapter_ids']
        base=bases[ch['source_id']];assert base['work_id']==ch['work_id'] and base['source_id']==ch['source_id']
        allm=[m['id']for p in ch['paragraphs']for m in p['mentions']];assert len(allm)==len(set(allm))
        for par,m in relevant:
            pid=m['person_id'];assert m['kind']in('person','pronoun')
            assert type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(par['text'])
            assert par['text'][m['start']:m['end']]==m['surface'] and m['id']not in additions[pid]
            canonical=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=par['id'],mention_id=m['id'],quote=m['surface'])
            hits=[(owner,e)for owner,p in physical.items()for e in p.get('evidence',[])if e.get('mention_id')==m['id']]
            assert len(hits)==1 and hits[0][0]==pid
            evidence=hits[0][1];assert all(k in evidence for k in canonical)and same({k:evidence[k]for k in canonical},canonical)
            aliases=[(owner,a)for owner,p in physical.items()for a in p.get('aliases',[])if m['id']in a.get('mention_ids',[])]
            if m['kind']=='person':assert len(aliases)==1 and aliases[0][0]==pid and aliases[0][1]['surface']==m['surface'] and aliases[0][1]['mention_ids'].count(m['id'])==1
            else:assert not aliases
            additions[pid][m['id']]=evidence
    for pid,want in expected.items():
        actor=people[pid];assert same(actor,physical[pid])
        extra=additions[pid]
        external=[e for e in actor['evidence']if e.get('chapter_id')not in ownids]
        assert same([e for e in external if e.get('mention_id')not in extra],want['evidence'])
        assert same([e for e in external if e.get('mention_id')in extra],[extra[e['mention_id']]for e in external if e.get('mention_id')in extra])
        assert len(external)==len(want['evidence'])+len(extra)
        assert same(_without_alias_mids(actor['aliases'],set(ownmids)|set(extra)),want['aliases'])
    for ch in records or []:
        if type(ch)is not dict or ch.get('record_type')!='marked_chapter' or ch.get('id')in ownids:continue
        claimed=any(m.get('person_id')in expected and m.get('id')not in prior[m['person_id']] and m.get('id')not in ownmids for p in ch.get('paragraphs',[])for m in p.get('mentions',[]))
        if claimed:assert ch.get('id')in chapters and same(ch,chapters[ch['id']])
    return additions


def proof(root,people=None,records=None):
    c=contract(root)
    physical={p['id']:p for p in read(root,'registry/persons.json')['persons']}
    if people is None:people=physical
    roles={}
    for role,s in c['source_role_seeds'].items():
        ch=read(root,s['path']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']]
        m,=[m for m in p['mentions']if m['id']==s['marker']['id']]
        assert p['text']==s['text']and same({k:v for k,v in m.items()if k!='person_id'},s['marker'])and m['kind']=='person'
        pid=m['person_id'];assert pid in people;roles['$'+role]=pid
        assert [e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[s['reverse']]
        assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[pid]['aliases'])
    for role,s in c['new_role_mids'].items():
        ch=read(root,s['path']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['mid']]
        assert m['kind']=='person'and m['person_id']in people;roles['$'+role]=m['person_id']
    assert len(set(roles.values()))==8
    r=roles['$daoci'];assert len(r)==11
    try:from scripts.person_ids import valid_person_id, family_path_errors
    except ImportError:from person_ids import valid_person_id, family_path_errors
    assert valid_person_id(r)
    parents={'shunzhi':'daoci','liangwu':'shunzhi','hui':'shunzhi','liangjian':'liangwu','yuan':'liangwu','ji':'liangwu','daqi':'liangjian'}
    assert all(not family_path_errors(roles['$'+child],{'connection':'father','parent_person_id':roles['$'+parent]}) for child,parent in parents.items())
    mapping={old:roles['$'+role]for old,role in c['historical_old_id_role_map'].items()}
    try:from scripts import source_primary_reference_resolutions as primary_refs
    except ImportError:import source_primary_reference_resolutions as primary_refs
    reference_state=primary_refs.resolve(root,ZH,people)
    assert not set(mapping)&set(people)
    # Other source owners retain their own independent coherent-rekey authority.
    # Derive only exact endpoint correspondences from unchanged opaque MIDs; this
    # family guard does not freeze unrelated people to historical numeric values.
    for archive in c['archives']:
        if archive['kind'] != 'current_source' or not archive['path'].endswith('.json'):continue
        prior=read(root,archive['before_capture'])
        if prior.get('record_type') != 'marked_chapter':continue
        current=read(root,archive['path'])
        if archive['path']==ZH:
            try:from scripts.zhou041_sizong_resolution import project_prior as project_sizong
            except ImportError:from zhou041_sizong_resolution import project_prior as project_sizong
            prior=project_sizong(prior,root,people)
        prior_view=primary_refs.semantic_view(prior,reference_state,prior=True)
        current_view=primary_refs.semantic_view(current,reference_state)
        oldm={m['id']:m for p in prior_view['paragraphs']for m in p['mentions']}
        newm={m['id']:m for p in current_view['paragraphs']for m in p['mentions']}
        assert oldm.keys()==newm.keys()
        for mid,om in oldm.items():
            nm=newm[mid]
            assert all(same(om.get(k),nm.get(k))for k in ('id','start','end','surface','kind','source_role'))
            if om.get('kind')in('person','pronoun'):
                old,new=om['person_id'],nm['person_id'];assert new in people
                if old in mapping:assert mapping[old]==new
                else:mapping[old]=new
    for p in people.values():assert not set(p.get('id_aliases',[]))&set(mapping)
    for rel,h in c['immutable_prior_capture_hashes'].items():assert hashlib.sha256(raw(root,rel)).hexdigest()==h
    for a in c['archives']:
        b=raw(root,a['before_capture']);assert hashlib.sha256(b).hexdigest()==a['before_sha256']
        if a['kind']=='registry':continue
        if a['path'].endswith('.json'):
            expected=typed_projection(json.loads(b),mapping)
            if a['path']=='tests/fixtures/nanqi033-wangsengqian/person-ids.json':
                try:from scripts.sima_liang_jinwu_fixture import project_jinwu_fixture
                except ImportError:from sima_liang_jinwu_fixture import project_jinwu_fixture
                expected=project_jinwu_fixture(expected,a['path'],root,people)
                try:from scripts.current_source_fixture_roles import project_fixture_roles
                except ImportError:from current_source_fixture_roles import project_fixture_roles
                expected=project_fixture_roles(expected,a['path'],root,people)
            if a['path']in (ZH,'corpus/zhoushu/041-wangbao-ws2432538-identities.json'):expected=project_sizong(expected,root,people)
            if a['path']==ZH:
                amendment=c['source_title_metadata_successor']
                assert amendment['path']==ZH and amendment['pointer']=='/source/title'
                assert expected['source']['title']==amendment['before']
                expected['source']['title']=amendment['after']
            assert same(primary_refs.semantic_view(read(root,a['path']),reference_state),primary_refs.semantic_view(expected,reference_state,prior=True))
        else:
            expected_xml=b.decode()
            for old,new in mapping.items():expected_xml=expected_xml.replace('ref="'+old+'"','ref="'+new+'"')
            if a['path']=='corpus/zhoushu/041-wangbao-ws2432538.xml':
                try:from scripts.zhou041_sizong_resolution import project_prior_xml
                except ImportError:from zhou041_sizong_resolution import project_prior_xml
                expected_xml=project_prior_xml(expected_xml,root,people)
            assert primary_refs.xml_view(raw(root,a['path']).decode(),reference_state)==primary_refs.xml_view(expected_xml,reference_state,prior=True)
    sources={p:expand(v,roles)for p,v in c['source_templates'].items()}
    sidecars={p:expand(v,roles)for p,v in c['sidecar_templates'].items()}
    names=expand(c['name_set_template'],roles)
    for rel,x in {**sources,**sidecars,c['name_path']:names}.items():assert same(read(root,rel),x)
    ownids={v['id']for v in sources.values()};midmap={m['id']:(ch,p,m)for ch in sources.values()for p in ch['paragraphs']for m in p['mentions']}
    base_reg=json.loads(raw(root,next(a['before_capture']for a in c['archives']if a['kind']=='registry')))
    byold={p['id']:p for p in base_reg['persons']}
    expected={}
    for old,role in c['historical_old_id_role_map'].items():
        want=typed_projection(byold[old],mapping);p=people[roles['$'+role]]
        assert same({k:v for k,v in p.items()if k not in('aliases','evidence','family_path')},{k:v for k,v in want.items()if k not in('aliases','evidence','family_path')})
        expected[p['id']]=want
    for role,t in c['new_people_templates'].items():
        want=expand(t,roles);p=people[roles['$'+role]]
        assert same({k:v for k,v in p.items()if k not in('aliases','evidence')},{k:v for k,v in want.items()if k not in('aliases','evidence')})
        expected[p['id']]=dict(want,evidence=[e for e in want['evidence']if e.get('chapter_id')not in ownids],aliases=_without_alias_mids(want['aliases'],set(midmap)))
    _external_growth(root,physical,people,expected,ownids,midmap,records)
    for role,t in c['family_path_templates'].items():assert same(people[roles['$'+role]].get('family_path'),expand(t,roles))
    for pid,p in people.items():
        wanted=[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=par['id'],mention_id=m['id'],quote=m['surface'])for ch,par,m in midmap.values()if m['person_id']==pid]
        assert same([e for e in p['evidence']if e.get('chapter_id')in ownids],wanted)
        aliases={}
        for ch,par,m in midmap.values():
            if m['person_id']==pid:aliases.setdefault(m['surface'],[]).append(m['id'])
        actual={a['surface']:[m for m in a['mention_ids']if m in midmap]for a in p['aliases']if any(m in midmap for m in a['mention_ids'])}
        assert same(actual,aliases)
    if records is not None:
        for want in [*sources.values(),*sidecars.values(),names]:assert sum(same(x,want)for x in records)==1
    return c,roles,sources,sidecars,names


def errors(root):
    if not active(root):return[]
    try:proof(root);return[]
    except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return['梁蕭近世來源/皇考太祖身份/實體父系重鍵/有限current投影及反查不符；不得改原capture或留舊PID替身']


def family_applies(a):return a.get('qualifiers',{}).get('source_clause_binding',{}).get('kind')==KIND


def family_valid(a,paragraphs,root):
    if not family_applies(a):return False
    try:
        _,_,sources,sidecars,_=proof(root)
        assert sum(same(a,v)for s in sidecars.values()for v in s['assertions'])==1
        e,=a['evidence'];_,p=paragraphs[e['paragraph_id']]
        assert same(p,next(p for s in sources.values()for p in s['paragraphs']if p['id']==e['paragraph_id']))
        return True
    except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False


def validate_surname(name,names,chapters,assertions,root=None):
    assert root is not None
    _,_,sources,_,ns=proof(root)
    assert sum(same(name,n)for n in ns['records'])==1
    assert sum(same(name,n)for n in names)==1
    assert same(chapters[NSID],sources[NS])
    return None


def guard_bundle(root,pid,people,records):
    if not active(root):return
    # True current source anchors own the guard, even when caller reverse is stripped.
    owned={m['person_id']for p in read(root,NS)['paragraphs']for m in p['mentions']}
    owned.update(m['person_id']for p in read(root,ZH)['paragraphs']for m in p['mentions']if m.get('source_role')in('liangwu','liangjian','liangyuan','hui','ji','daqi')and m.get('kind')=='person')
    if pid not in owned:return
    proof(root,people=people,records=records)


def project_prior_contract(root,captured,path):
    """Two immutable Liang041 contracts get a current endpoint view, never new bytes."""
    if not active(root):return captured
    assert path in ('source-evidence/liang041-wanggui-ws1512987/complete-unit-contract.json',
                    'source-evidence/liang041-wanggui-ws1512987/taoshiheng-identity-successor.json')
    assert same(captured,read(root,path))
    c,roles,*_=proof(root)
    mapping={old:roles['$'+role]for old,role in c['historical_old_id_role_map'].items()}
    return typed_projection(captured,mapping)


def family_paths_valid(root,paths):
    """Validate one call's paths against one complete proof; retain no state."""
    paths=tuple(paths)
    if not paths:return True
    if not active(root):return False
    try:
        c,roles,*_=proof(root)
        return all(any(roles['$'+role]==pid and same(path,expand(t,roles))
                       for role,t in c['family_path_templates'].items())
                   for pid,path in paths)
    except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False


def family_path_valid(root,pid,path):
    return family_paths_valid(root,((pid,path),))
