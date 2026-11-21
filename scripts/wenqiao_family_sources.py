"""Check named and unnamed endpoints against the family clauses in the Wen Jiao sources."""

def family_valid(a, e, ch):
    try:
        q = a['qualifiers']; p, = [p for p in ch['paragraphs'] if p['id'] == e['paragraph_id']]
        text = p['text']; kind = q['source_clause_binding']['kind']; assert a['human_reviewed'] is False
        assert a['status'] == 'source_attested' and e['quote'] == text and e['chapter_id'] == ch['id'] and e['source_id'] == ch['source_id']
        refs = {r['id']: r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id'] == p['id']}
        names = {m['id']: m for m in p['mentions'] if m['kind'] == 'person'}
        if kind == 'jin067_liukun_wife_wen_maternal_aunt':
            assert text.startswith('平北大將軍劉琨妻，嶠之從母也。') and ch['source']['revision_id'] == 2592755
            sub, obj = names[e['subject_person_mention_id']], refs[e['object_reference_id']]
            assert (sub['person_id'], obj['person_id']) == (a['subject_person_id'], a['object_person_id'])
            if a['predicate'] == 'spouse': assert q['source_term'] == '劉琨妻' and sub['surface'] == '劉琨' and obj['surface'] == '妻'
            else:
                assert a['predicate'] == 'maternal_aunt' and q['source_term'] == '嶠之從母也' and sub['surface'] == '嶠' and obj['surface'] == '從母'
                mother, = [m for pp in ch['paragraphs'] if '其母崔氏固止之' in pp['text'] for m in pp['mentions'] if m['surface']=='崔氏' and m['start']==pp['text'].index('其母崔氏')+2]
                assert q['mother_person_id']==mother['person_id'] and q['generation_difference']==-1 and q['lineage']=='maternal'
            assert sub['start'] == text.index(sub['surface']) and obj['start'] == text.index(obj['surface'])
        elif kind == 'jin067_emperor_yuliang_yuanjiu':
            assert ch['source']['revision_id']==2592755 and a['predicate']=='maternal_uncle'
            sub,obj=refs[e['subject_reference_id']],names[e['object_person_mention_id']]
            assert (sub['person_id'],obj['person_id'])==(a['subject_person_id'],a['object_person_id']) and q['source_term']=='帝之元舅'
            assert text.count('護軍庾公，帝之元舅')==1 and sub['start']==text.index('帝之元舅') and obj['start']==text.index('護軍庾公')+2
            assert q['lineage']=='maternal' and q['generation_difference']==-1 and q['mother_person_id'] is None
            report,=[r for pp in ch['paragraphs'] if '即日護軍庾亮至' in pp['text'] for r in pp['mentions'] if r['surface']=='庾亮' and r['start']==pp['text'].index('即日護軍庾亮至')+4]
            assert report['person_id']==obj['person_id']
        elif kind == 'liuzhu_wenshi_pu_named_daughter':
            assert p['attribution'] == {'annotator':'劉孝標','quoted_work':'溫氏譜'} and p['source_quote']['source_layer'] == '劉注引溫氏譜'
            sub, obj = refs[e['subject_reference_id']], names[e['object_person_mention_id']]
            assert sub['surface'] == '女' and (sub['person_id'],obj['person_id']) == (a['subject_person_id'],a['object_person_id'])
            if text == '嶠父襜，娶清河崔參女。':
                assert ch['source']['revision_id']==1500491; source='崔參女'; spouse='襜'; marriage='襜，娶清河崔參女'
            else:
                assert text == '嶠初取高平李暅女，中取琅琊王詡女，後取廬江何邃女。' and ch['source']['revision_id']==1500502
                marriage, = [part for part in ('初取高平李暅女','中取琅琊王詡女','後取廬江何邃女') if text.index(part)+len(part)-1==sub['start']];source=marriage[-3:];spouse='嶠'
            assert sub['start']==text.index(source)+len(source)-1
            if a['predicate']=='father':assert obj['surface']==source[:-1] and q['source_term']==source and obj['start']==text.index(source)
            else:assert a['predicate']=='spouse' and obj['surface']==spouse and q['source_term']==marriage and obj['start']==text.index(spouse)
        else: return False
        return True
    except (KeyError, AssertionError, IndexError, ValueError, TypeError): return False


def situ_valid(a, paragraphs):
    try:
        e, = a['evidence']; cid,p=paragraphs[e['paragraph_id']];text=p['text'];prefix='溫嶠，字太真，司徒羨弟之子也。父憺，河東太守。';assert text.startswith(prefix)
        names={m['id']:m for m in p['mentions']}; child,uncle=names[e['subject_person_mention_id']],names[e['object_person_mention_id']]
        return (a['status']=='source_attested' and a['human_reviewed'] is False and e['chapter_id']==cid and e['quote']==text
                and a['qualifiers']['source_term']=='司徒羨弟之子也' and a['predicate']=='paternal_uncle'
                and (child['surface'],child['start'],child['person_id'])==('溫嶠',0,a['subject_person_id']) and (uncle['surface'],uncle['start'],uncle['person_id'])==('羨',text.index('司徒羨')+2,a['object_person_id']))
    except (KeyError, AssertionError, IndexError, ValueError, TypeError):return False
