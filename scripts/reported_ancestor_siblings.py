"""Bind a reported ancestor's following sibling list without moving it to the biography subject."""

def reported_ancestor_siblings_valid(assertion, paragraphs, assertions, parse_number):
    try:
        q=assertion['qualifiers'];b=q['source_clause_binding'];e,=assertion['evidence']
        cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
        position=p.get('source_position',{})
        if not isinstance(position,dict):return False
        if position.get('source_layer') not in (None,'received_text','received_body','received_biography'):return False
        if p.get('text_layer') not in (None,'received_chapter') or position.get('text_layer') not in (None,'received_chapter'):return False
        for metadata in (p,position):
            if 'annotator' in metadata or 'attached_note_to_paragraph_id' in metadata:return False
        if p.get('source_layer','received_text')!='received_text' or e.get('source_layer','received_text')!='received_text':return False
        if (assertion.get('predicate')!='brother' or assertion.get('status')!='source_attested'
                or type(assertion.get('human_reviewed'))is not bool
                or set(q)!={'source_term','relative_birth_order','source_clause_binding'}
                or set(b)!={'kind','start','end','ancestry_assertion_id','descendant_person_mention_id','antecedent_person_mention_id','older_brother_person_mention_id','younger_brother_person_mention_ids'}
                or b['kind']!='reported_ancestor_then_named_siblings'
                or e['chapter_id']!=cid or e['quote']!=t):return False
        def anchor(mid):
            m=ms[mid]
            if (m.get('kind')!='person' or not m.get('person_id')
                    or type(m['start'])is not int or type(m['end'])is not int
                    or not 0<=m['start']<m['end']<=len(t)or t[m['start']:m['end']]!=m['surface']):raise ValueError('bad anchor')
            return m
        head=anchor(b['descendant_person_mention_id']);ante=anchor(b['antecedent_person_mention_id']);elder=anchor(b['older_brother_person_mention_id'])
        mids=b['younger_brother_person_mention_ids']
        if not isinstance(mids,list)or len(mids)!=2 or len(set(mids))!=2:return False
        younger=[anchor(mid)for mid in mids]
        if len({x['person_id']for x in [head,ante,elder]+younger})!=5:return False
        source=next(x for x in assertions if x['id']==b['ancestry_assertion_id']);sq=source['qualifiers'];se,=source['evidence']
        if (source['predicate']!='ancestor' or source['status']!='source_attested'
                or source['subject_person_id']!=head['person_id'] or source['object_person_id']!=ante['person_id']
                or se.get('subject_person_mention_id')!=head['id']or se.get('object_person_mention_id')!=ante['id']
                or se.get('paragraph_id')!=p['id']or se.get('chapter_id')!=cid or se.get('source_id')!=e.get('source_id')
                or se.get('quote')!=t or head['start']!=0
                or set(sq)!={'source_term','generation_distance','adopted_for_family_tree','source_number','reported_generation_number'}
                or sq['generation_distance']is not None or sq['adopted_for_family_tree']is not False
                or type(sq['reported_generation_number'])is not int or parse_number(sq['source_number'])!=sq['reported_generation_number']
                or sq['source_term']!=ante['surface']+sq['source_number']+'世孫'
                or t[ante['end']:elder['start']]!=sq['source_number']+'世孫。兄'):return False
        start,end=b['start'],b['end'];term='兄'+elder['surface']+'，弟'+younger[0]['surface']+'、'+younger[1]['surface']
        if (type(start)is not int or type(end)is not int or t[start:end]!=term or q['source_term']!=term
                or start!=elder['start']-1 or end!=younger[1]['end']
                or younger[0]['start']!=elder['end']+2 or younger[1]['start']!=younger[0]['end']+1):return False
        subj=anchor(e['subject_person_mention_id']);obj=anchor(e['object_person_mention_id'])
        if subj['id']!=ante['id'] or subj['person_id']!=assertion['subject_person_id'] or obj['person_id']!=assertion['object_person_id']:return False
        if obj['id']==elder['id']:older,younger_id=obj['person_id'],subj['person_id']
        elif obj['id']in mids:older,younger_id=subj['person_id'],obj['person_id']
        else:return False
        return q['relative_birth_order']=={'older_person_id':older,'younger_person_id':younger_id,'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}
    except (KeyError,TypeError,ValueError,StopIteration,IndexError):
        return False
