"""Keep the sovereign reply in the reference layer while reusing the scoped gift proof."""
from copy import deepcopy
try:
    from scripts.explicit_topic_gifts import explicit_topic_gift_valid
except ImportError:
    from explicit_topic_gifts import explicit_topic_gift_valid


def valid(h, chapter, paragraphs, mentions, events):
    if not chapter or chapter.get('id') != 'c-songshu-042-wanghong' or chapter['source'].get('revision_id') != 1478172:
        return False
    try:
        trial=deepcopy(h);b=trial['posthumous_basis'];reply,=b['sovereign_replies'];refs=chapter['annotation']['person_reference_occurrences']
        if b['kind'] != 'explicit_topic_scoped_gift_with_sovereign_reference' or set(reply)!={'person_reference_id','clause_anchor'}:
            return False
        row,=(r for r in refs if r['id']==reply['person_reference_id']);cid,p=paragraphs[row['paragraph_id']];a=reply['clause_anchor']
        if (row['person_id']!='3bh_k4m_fg4' or row['referent_role']!='third_person' or row['surface']!='上' or row['start']!=a['start'] or row['end']!=a['start']+1
            or row['paragraph_id']!=a['paragraph_id'] or p['source_position']['first_line']!=87 or cid!=chapter['id'] or a['surface']!='上輒優詔不許'
            or not p['text'].startswith('其後弘寢疾，弘表屢乞骸骨，'+a['surface']+'。') or row['id'] in mentions):return False
        bridge={**mentions,row['id']:(cid,p['id'],row)};reply['person_mention_id']=reply.pop('person_reference_id');b['kind']='explicit_topic_scoped_gift'
        return explicit_topic_gift_valid(trial,paragraphs,bridge,events)
    except (KeyError,TypeError,ValueError):
        return False
