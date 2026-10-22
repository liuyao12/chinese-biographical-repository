"""Exact named father / husband / anonymous wife roles in A, B之妻父也."""
import re

def wife_father_clause_valid(a, paragraphs, chapters=None):
    try:
        q=a['qualifiers'];b=q['wife_father_context'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']}
        if (q['relationship_basis']!='named_wifes_father' or set(b)!={'kind','father_mention_id','husband_mention_id','wife_mention_id','clause_anchor','locality_prefix_anchor','human_reviewed'}
                or b['kind']!='named_wifes_father' or b['human_reviewed']is not False or q['source_term']!='妻父'
                or p.get('text_layer')!='received_chapter' or p.get('annotator')or p.get('attached_note_to_paragraph_id')
                or e['chapter_id']!=cid or e['quote']!=t):return False
        containers=[p,p.get('source_position',{})]
        if chapters is not None:
            chapter=chapters.get(cid)
            if not isinstance(chapter,dict):return False
            containers += [chapter,chapter.get('source',{})]
        if any(x.get('annotator')or x.get('attached_note_to_paragraph_id')or x.get('text_layer', 'received_chapter')!='received_chapter'or x.get('source_layer','received_chapter')not in ['received_chapter','body']for x in containers):return False
        f,h,w=[ms[b[k]]for k in ['father_mention_id','husband_mention_id','wife_mention_id']]
        if any(m.get('kind')!='person'or not m.get('person_id')or t[m['start']:m['end']]!=m['surface']for m in [f,h,w])or len({m['person_id']for m in [f,h,w]})!=3:return False
        if w['surface']!='妻' or a['subject_person_id']!=w['person_id']:return False
        if a['predicate']=='father':
            if a['object_person_id']!=f['person_id']or q.get('lineage')!='paternal':return False
        elif a['predicate']=='spouse':
            if a['object_person_id']!=h['person_id']:return False
        else:return False
        def anchor(x):return isinstance(x,dict)and set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
        c=b['clause_anchor'];prefix=b['locality_prefix_anchor']
        if not anchor(c)or prefix is not None and not anchor(prefix):return False
        lead=prefix['surface']if prefix else'';start=prefix['start']if prefix else f['start']
        if prefix and (prefix['end']!=f['start']or not re.fullmatch(r'[\u3400-\u9fff]{1,12}',lead)):return False
        expected=lead+f['surface']+'，'+h['surface']+'之妻父也'
        if c['surface']!=expected or c['start']!=start or c['end']!=w['end']+2 or f['end']+1!=h['start']or h['end']+1!=w['start']:return False
        if start>0 and t[start-1]not in '。；！？':return False
        # Outside all nested direct speech; no ignoring arbitrary embedded people.
        stack=[]
        for ch in t[:start]:
            if ch in '「『':stack.append(ch)
            elif ch in '」』':
                if not stack or (stack[-1],ch)not in [('「','」'),('『','』')]:return False
                stack.pop()
        if stack or any(ch in c['surface']for ch in '「」『』曰')or any(m['start']<c['end']and m['end']>c['start']and m['id']not in {f['id'],h['id'],w['id']}for m in p['mentions']):return False
        return c['end']==len(t)or t[c['end']]in '，。；！？'
    except (KeyError,TypeError,ValueError,StopIteration):return False
