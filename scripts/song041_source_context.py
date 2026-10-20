# coding: utf-8
"""Source-bound 041 temporal context and unresolved kin references; never parentage from a title."""
import re

def _bound(item,chapters,people):
    es=item.get('evidence');a=item.get('source_anchor');pid=item.get('person_id')
    if not isinstance(es,list)or len(es)!=1 or not isinstance(a,dict)or set(a)!={'paragraph_id','start','end','surface'}:raise ValueError('source shape')
    e=es[0];c=chapters[e['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);ms={m['id']:m for m in p['mentions']};m=ms[e['person_mention_id']];s,t=a['start'],a['end']
    if (pid not in people or m.get('person_id')!=pid or m.get('kind')!='person'or e['quote']!=p['text']or a['paragraph_id']!=p['id']
        or any(e[k]!=c[k]for k in('work_id','book_id','source_id'))or type(s)is not int or type(t)is not int or not 0<=s<t<=len(p['text'])
        or p['text'][s:t]!=a['surface']or a['surface']!=item['source_term']or item.get('human_reviewed')is not False or not item.get('reviewer')):raise ValueError('unbound source')
    return c,p,ms

def temporal_errors(record,chapters,people,normalize,events=None):
    errors=[];seen=set();rows=record.get('records',[]);byid={x.get('id'):x for x in rows}
    if record.get('record_type')!='source_temporal_attestation_set'or record.get('chapter_id')not in chapters:return['來源時間集格式或篇不存在']
    for r in rows:
        try:
            c,p,ms=_bound(r,chapters,people);kind=r['kind'];d=r['normalized_date'];duration=r['duration'];term=r['source_term']
            required={'id','person_id','source_term','source_anchor','event_context','date_role','status','evidence','kind','normalized_date','duration','prospective','human_reviewed','reviewer','model'}
            if kind=='elapsed_since_death':required.add('reference_life_event_id')
            if set(r)!=required or not isinstance(r['event_context'],str)or not r['event_context']:raise ValueError('explicit temporal contract')
            if (r['id']in seen or c['id']!=record['chapter_id']or r['status']!='source_attested'or r['date_role']!='source_context_not_title_boundary'
                or kind not in('calendar_context','reported_duration','elapsed_since_death','prospective_formula')or type(r['prospective'])is not bool):raise ValueError('temporal role')
            seen.add(r['id'])
            if d is not None:
                if kind!='calendar_context'or r['prospective']or duration is not None or d['evidence']!=r['evidence']:raise ValueError('date is not source calendar context')
                errs=normalize(d,chapters)
                if errs:raise ValueError(';'.join(errs))
                expression=d['source_expression'];at=p['text'].index(expression)
                if expression not in term:
                    if term=='其年又詔曰':
                        previous=next(x for x in rows if x['source_term']=='永初二年')
                        if previous['source_anchor']['end']>r['source_anchor']['start']or previous['person_id']!=r['person_id']or previous['normalized_date']['year']!=d['year']:raise ValueError('same year antecedent')
                    elif term in('高祖踐阼','及即大位'):
                        if d['source_expression']!='元熙二年'or not p['text'][at:r['source_anchor']['start']].startswith('元熙二年入朝因受晉禪')or'少帝即位'in p['text'][at:r['source_anchor']['start']]:raise ValueError('accession referent')
                    else:raise ValueError('unbound event calendar')
            if kind=='calendar_context':
                if duration is not None or r['prospective']:raise ValueError('calendar duration')
            elif kind=='reported_duration':
                if term!='在外凡五年'or d is not None or duration!={'value':5,'unit':'source_residence_years','source_number':'五','operator':'eq','counting':'unspecified_source_years'}or r['prospective']:raise ValueError('residence duration')
            elif kind=='elapsed_since_death':
                if term!='孝皇背世五十餘年'or d is not None or duration!={'value':50,'unit':'source_elapsed_years','source_number':'五十','operator':'gt','counting':'unspecified_source_years'}or r['prospective']or r.get('reference_life_event_id')!='le-song041-qiao-death':raise ValueError('elapsed years not death year')
                event=(events or {}).get(r['reference_life_event_id'],{})
                if event.get('event_type')!='death'or event.get('person_id')!=r['person_id']or event.get('status')!='source_attested'or not any(e.get('paragraph_id')==r['evidence'][0]['paragraph_id']for e in event.get('evidence',[])):raise ValueError('elapsed reference must be the same person/source death')
            else:
                if term!='太后百嵗後'or d is not None or duration is not None or not r['prospective']:raise ValueError('prospective not age')
        except(KeyError,TypeError,ValueError,StopIteration)as ex:errors.append('來源時間上下文未逐字綁定或冒作任期／實際事件：'+str(ex))
    return errors

def unresolved_kin_errors(r,chapters,people):
    try:
        c,p,ms=_bound(r,chapters,people)
        if (r['status']!='unresolved'or r['source_term']!='無子以弟孫襲之繼宣之紹封'or r['source_kin_term']!='弟孫'
            or len(r['reference_person_candidates'])!=2 or len(set(r['reference_person_candidates']))!=2
            or not set(r['reference_person_candidates']).issubset(people)
            or any(r.get(k)is not None for k in('preferred_reference_person_id','father_person_id','common_ancestor_person_id','generation_difference','exact_distance'))
            or not r.get('rationale')):return['弟孫未決不得補父、祖先或選定關係']
        keys={'id','person_id','reference_person_candidates','source_term','source_kin_term','source_anchor','evidence','status','preferred_reference_person_id','father_person_id','common_ancestor_person_id','generation_difference','exact_distance','rationale','human_reviewed','reviewer','model'}
        if set(r)!=keys:return['弟孫未決欄位未知']
        start=r['source_anchor']['start'];pre=p['text'].rfind('裔長子',0,start)
        yi=next(m for m in p['mentions']if m['start']==pre and m['surface']=='裔')
        xuanzhi=next(m for m in p['mentions']if m['start']==start+8 and m['surface']=='宣之')
        if set(r['reference_person_candidates'])!={yi['person_id'],xuanzhi['person_id']}:return['弟孫候選不符本句裔／宣之指涉']
        selected=next(m for m in p['mentions']if m['start']==r['source_anchor']['start']+5)
        if selected.get('person_id')!=r['person_id']or selected['surface']!='襲之':return['弟孫襲之錨點不符']
        if not all(any(m.get('person_id')==pid for m in p['mentions'])for pid in r['reference_person_candidates']):return['弟孫候選缺本段原證']
        return[]
    except(KeyError,TypeError,ValueError,StopIteration):return['弟孫未決來源不完整']

def kin_clause_valid(a,paragraphs,assertions):
    try:
        e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']];q=a['qualifiers'];text=p['text'];term=q['source_term']
        if e['chapter_id']!=cid or e['quote']!=text or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or a['human_reviewed']is not False:return False
        if q.get('succession_kind')=='ji_named_predecessor':
            b=q['source_clause_binding'];return(set(q)=={'source_term','succession_kind','legal_adoption_status','parentage_inference','source_clause_binding'}and a['predicate']=='ritual_successor_of'and q['legal_adoption_status']=='not_stated'and q['parentage_inference']=='not_inferred'
             and b['kind']=='named_successor_ji_named_predecessor'and text[b['start']:b['end']]==term==s['surface']+'繼'+o['surface']and s['start']==b['start']and o['end']==b['end'])
        if q.get('kinship_basis')=='stepfamily_grandparent_appellation':
            refs={x['id']:x for x in assertions};father,spouse=[refs[i]for i in q['basis_assertion_ids']];mother=q['stepfamily_mother_person_id']
            return(a['predicate']=='kinship_unspecified'and term=='外祖趙光祿蕭光祿'and term in text
                and q['biological_lineage']is None and q['connecting_biological_parent_person_id']is None
                and father['predicate']=='father'and father['subject_person_id']==mother and father['object_person_id']==o['person_id']
                and spouse['predicate']=='spouse'and spouse['subject_person_id']==mother and spouse['qualifiers']['marriage_stage']=='successive_wife'
                and any('聘后為繼室'in x['quote']for x in spouse['evidence'])and o['surface']=='蕭光祿')
        return False
    except(KeyError,TypeError,ValueError,StopIteration):return False

def same_year_birth_day_conflict_valid(decision,selected,windows):
    if decision.get('comparison_scope')!='source_calendar_day'or decision.get('status')!='unresolved'or decision.get('preferred_event_id')is not None:return False
    if len(selected)!=2 or len(set(windows))!=1 or None in windows or not all(e.get('event_type')=='birth'for e in selected):return False
    expected={'三月壬寅','四月二日'};found=set()
    for event in selected:
        text=event.get('source_term','')
        hit=re.search(r'([一二三四五六七八九十]+月(?:[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]|[一二三四五六七八九十]+日))',text)
        if not hit or not all(text in e.get('quote','')for e in event.get('evidence',[])):return False
        found.add(hit[1])
    return found==expected

def marital_birth_context_valid(a,paragraphs,assertions):
    try:
        e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};child=ms[e['subject_person_mention_id']];father=ms[e['object_person_mention_id']];q=a['qualifiers'];term=q['source_term'];start=p['text'].index(term)
        if (a['predicate']!='father'or q['parentage_basis']!='marital_biographical_birth_context'or q['interpretation_status']!='editorial_provisional'
            or term!='孝皇帝聘后為繼室生長沙景王道憐臨川烈武王道規'or e['chapter_id']!=cid or e['quote']!=p['text']
            or child['person_id']!=a['subject_person_id']or father['person_id']!=a['object_person_id']or father['start']!=start
            or father['surface']!='孝皇帝'or child['surface']not in('長沙景王道憐','臨川烈武王道規')or not start<=child['start']<child['end']<=start+len(term)):return False
        mother=next(m for m in p['mentions']if m['start']==father['end']+1 and m['surface']=='后')
        return (any(r['predicate']=='mother'and r['subject_person_id']==child['person_id']and r['object_person_id']==mother['person_id']and r['qualifiers'].get('parentage_basis')=='explicit_sheng'for r in assertions)
         and any(r['predicate']=='spouse'and r['subject_person_id']==mother['person_id']and r['object_person_id']==father['person_id']and r['qualifiers'].get('marriage_stage')=='successive_wife'for r in assertions))
    except(KeyError,TypeError,ValueError,StopIteration):return False
