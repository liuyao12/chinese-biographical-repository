# coding: utf-8
"""Editorial parent edge from a received father and its attached paternal-grandfather note."""
import json,hashlib
from pathlib import Path

def body_note_ancestor_parent_valid(member, rows, assertions, chapters, root):
    c=member.get('parent_connection')
    if not isinstance(c,dict) or c.get('type')!='parent_between_body_and_attached_note_ancestors':return False
    if c.get('interpretation_basis') is not None:
        return _body_grandfather_note_father_valid(member, rows, assertions, chapters, root)
    if c.get('status')!='contextual_provisional' or c.get('human_reviewed')is not False or not c.get('rationale') or member.get('source_assertion_id')is not None:return False
    near=assertions.get(c.get('nearer_ancestor_assertion_id'));far=assertions.get(c.get('farther_ancestor_assertion_id'));witness=rows.get(c.get('chain_subject_person_id'));parent=rows.get(member.get('parent_person_id'))
    if not all([near,far,witness,parent]):return False
    if near.get('predicate')!='father' or far.get('predicate')!='grandfather' or any(a.get('status')!='source_attested'or a.get('qualifiers',{}).get('lineage')!='paternal'for a in [near,far]):return False
    sub=near.get('subject_person_id')
    if sub!=far.get('subject_person_id') or witness.get('source_person_ids')!=[sub] or member.get('source_person_ids')!=[near.get('object_person_id')] or parent.get('source_person_ids')!=[far.get('object_person_id')]:return False
    if len({sub,near['object_person_id'],far['object_person_id']})!=3 or near.get('qualifiers',{}).get('source_term')not in ['父','喪父']:return False
    if any(a.get('predicate')=='father'and a.get('subject_person_id')in member['source_person_ids']and a.get('object_person_id')not in parent['source_person_ids']for a in assertions.values()):return False
    seen={member['person_id']};node=parent
    while node:
        if node['person_id']in seen:return False
        seen.add(node['person_id']);node=rows.get(node.get('parent_person_id'))
    refs=c.get('references')
    if not isinstance(refs,list)or len(refs)!=2 or {r.get('assertion_id')for r in refs if isinstance(r,dict)}!={near['id'],far['id']}:return False
    pairs=[]
    for a in [near,far]:
        ref=next((r for r in refs if r.get('assertion_id')==a['id']),{})
        chapter=chapters.get(ref.get('chapter_id'),{});p=next((p for p in chapter.get('paragraphs',[])if p['id']==ref.get('paragraph_id')),None)
        if not p or not ref.get('scope') or ref.get('quote')!=p['text'] or ref.get('source_id')!=chapter.get('source_id') or ref.get('url')not in [chapter.get('source',{}).get('url'),chapter.get('source',{}).get('permalink')]:return False
        if not any(all(e.get(k)==ref.get(k)for k in ['chapter_id','paragraph_id','source_id','quote'])for e in a.get('evidence',[])):return False
        pairs.append((chapter,p,ref))
    chapter,b,br=pairs[0];ch2,n,nr=pairs[1]
    if chapter is not ch2 or b.get('text_layer')!='received_chapter' or n.get('text_layer')!='witness_appended_pei_songzhi_note':return False
    bp=b.get('source_position',{});np=n.get('source_position',{});revision=chapter.get('source',{}).get('revision_id')
    if not revision or c.get('source_revision')!=revision or any(p.get('revision_id')!=revision for p in [bp,np]):return False
    if not bp.get('source_unit_id') or bp.get('source_unit_id')!=np.get('source_unit_id') or bp.get('biography_subject_person_id')!=sub or np.get('biography_subject_person_id')!=sub or np.get('attached_note_to_paragraph_id')!=b['id'] or np.get('annotator')!='裴松之' or not np.get('cited_work'):return False
    ps=chapter['paragraphs'];bi=next(i for i,p in enumerate(ps)if p['id']==b['id']);ni=next(i for i,p in enumerate(ps)if p['id']==n['id'])
    if ni!=bi+1 or bp.get('projected_end')!=np.get('projected_start'):return False
    refpath=bp.get('raw_projection_ref')
    if not isinstance(refpath,str)or not refpath.startswith('source-evidence/')or '..'in Path(refpath).parts or np.get('raw_projection_ref')!=refpath:return False
    try:
        projection=json.loads((Path(root)/refpath).read_text());rawpath=Path(root)/refpath;rawfile=projection['raw_file']
        if not isinstance(rawfile,str)or Path(rawfile).name!=rawfile:return False
        raw=(rawpath.parent/rawfile).read_bytes();digest=hashlib.sha256(raw).hexdigest()
        if digest!=projection['source_sha256']or digest!=chapter['source']['raw_sha256']or projection['full_context']['source_revision']!=revision:return False
        first,last=projection['source_lines'];projected=''.join(q.removesuffix('¶')for q in raw.decode().splitlines()[first-1:last]if not q.startswith('<pb:'))
        if projected!=projection['full_context']['projected_text']:return False
        units={u['paragraph_id']:u for u in projection['units']}
        for p,pos in [(b,bp),(n,np)]:
            u=units[p['id']]
            if u['start']!=pos['projected_start']or u['end']!=pos['projected_end']or u['text']!=p['text']:return False
            if ''.join(x['character']for x in u['character_projection'])!=p['text']or any(projected[x['projected_offset']]!=x['character']for x in u['character_projection']):return False
    except(KeyError,ValueError,TypeError,OSError):return False
    anchors=[('nearer_subject_mention_id',b,sub),('farther_subject_mention_id',n,sub),('nearer_ancestor_mention_id',b,near['object_person_id']),('farther_ancestor_mention_id',n,far['object_person_id'])];found=[]
    for key,p,pid in anchors:
        m=next((m for m in p['mentions']if m['id']==c.get(key)),None)
        if not m or m.get('kind')!='person' or m.get('person_id')!=pid or m.get('status')=='unresolved' or m.get('candidate_person_ids') or p['text'][m['start']:m['end']]!=m['surface']:return False
        found.append(m)
    if found[2]['surface']!='父' or found[3]['surface']!='祖父' or found[0]['start']>=found[2]['start'] or found[1]['end']!=found[3]['start']:return False
    if n['text'][max(0,found[3]['start']-1):found[3]['end']].startswith('母'):return False
    return True

# coding: utf-8

def _body_grandfather_note_father_valid(member, rows, assertions, chapters, root):
    """One named father between one child's body grandfather and attached-note father.

    The source assertions remain distinct. This edge is editorial only.
    """
    import re
    try:
        c=member['parent_connection'];near=assertions[c['nearer_ancestor_assertion_id']];far=assertions[c['farther_ancestor_assertion_id']]
        sub=c['chain_subject_person_id'];mid=near['object_person_id'];gid=far['object_person_id']
        if (c['interpretation_basis']!='body_grandfather_attached_note_father'
            or c.get('type')!='parent_between_body_and_attached_note_ancestors'
            or c.get('status')!='contextual_provisional' or c.get('human_reviewed')is not False
            or not c.get('rationale') or member.get('source_assertion_id')is not None
            or near.get('predicate')!='father' or far.get('predicate')!='grandfather'
            or near.get('subject_person_id')!=sub or far.get('subject_person_id')!=sub
            or any(a.get('status')!='source_attested' or a.get('qualifiers',{}).get('lineage')!='paternal' for a in [near,far])
            or len({sub,mid,gid})!=3 or member.get('source_person_ids')!=[mid]
            or rows[c['chain_subject_person_id']].get('source_person_ids')!=[sub]
            or rows[member['parent_person_id']].get('source_person_ids')!=[gid]):return False
        if any(a.get('predicate')=='father'and a.get('subject_person_id')==mid and a.get('object_person_id')!=gid for a in assertions.values()):return False
        seen={member['person_id']};cursor=member.get('parent_person_id')
        while cursor is not None:
            if cursor in seen or cursor not in rows:return False
            seen.add(cursor);cursor=rows[cursor].get('parent_person_id')
        refs=c['references']
        if not isinstance(refs,list)or len(refs)!=2 or {r.get('assertion_id')for r in refs}!={near['id'],far['id']}:return False
        proofs={near['id']:near,far['id']:far};pars={};chapter=None
        for ref in refs:
            a=proofs[ref['assertion_id']];ch=chapters[ref['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==ref['paragraph_id'])
            if (chapter is not None and ch is not chapter):return False
            chapter=ch
            if (not ref.get('scope') or ref.get('quote')!=p['text']
                or any(ref.get(k)!=ch.get(k if k!='chapter_id'else'id')for k in ['work_id','book_id','chapter_id','source_id'])
                or ref.get('url')not in [ch['source'].get('url'),ch['source'].get('permalink')]
                or not any(all(e.get(k)==ref.get(k)for k in ['work_id','book_id','chapter_id','source_id','paragraph_id','quote'])for e in a['evidence'])):return False
            pars[a['predicate']]=p
        body,note=pars['grandfather'],pars['father'];order=[p['id']for p in chapter['paragraphs']];i=order.index(body['id'])
        binding=c['witness_binding'];following=chapter['paragraphs'][i+2]
        if (order[i+1]!=note['id']or binding.get('body_paragraph_id')!=body['id']or binding.get('note_paragraph_id')!=note['id']or binding.get('following_body_paragraph_id')!=following['id']
            or body.get('text_layer')!='received_chapter'or note.get('text_layer')!='witness_appended_pei_songzhi_note'or following.get('text_layer')!='received_chapter'):return False
        revision=chapter['source']['revision_id']
        if binding.get('source_revision')!=revision or not revision or chapter['source'].get('source_commit')not in[None,revision]:return False
        for p in [body,note,following]:
            pos=p['source_position']
            if pos.get('source_commit',pos.get('revision_id'))!=revision or any(pos.get(k)not in[None,revision]for k in['source_commit','revision_id']):return False
            if p is not note:
                if any(k in d for d in [p,pos]for k in ['annotator','attached_note_to_paragraph_id']):return False
                if any(d.get('source_layer')not in [None,'received_body','received_text','received_biography','received_chapter']for d in [p,pos]):return False
            else:
                if any(d.get('annotator')not in [None,'裴松之']or d.get('attached_note_to_paragraph_id')not in [None,body['id']]or d.get('source_layer')not in [None,'ancient_commentary','witness_appended_pei_songzhi_note']for d in [p,pos]):return False
            if pos.get('text_layer')not in [None,p['text_layer']]:return False
        rootpath=Path(root).resolve();relative=binding['raw_file']
        if not isinstance(relative,str)or Path(relative).is_absolute()or Path(relative).parts[0]!='sources'or '..'in Path(relative).parts:return False
        rawpath=(rootpath/relative).resolve()
        if rootpath not in rawpath.parents or not rawpath.is_file():return False
        raw=rawpath.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        if binding.get('raw_file_sha256')!=digest or chapter['source'].get('response_sha256')!=digest:return False
        if chapter['source'].get('raw_sha256')not in [None,digest]:return False
        if chapter['source'].get('source_blob_sha') and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=chapter['source']['source_blob_sha']:return False
        text=raw.decode('utf8');lines=text.splitlines(keepends=True);offsets=[];count=0
        for line in lines:offsets.append(count);count+=len(line)
        intervals={}
        for p in [body,note,following]:
            pieces=[];points=[];fragments=p['witness_fragments']
            if not fragments:return False
            for f in fragments:
                li=f['line'];a=f['raw_line_start'];b=f['raw_line_end']
                if type(li)is not int or type(a)is not int or type(b)is not int or li<1 or li>len(lines)or a<0 or b<=a or b>len(lines[li-1].rstrip('\r\n')):return False
                actual=lines[li-1][a:b]
                if actual!=f['raw_fragment']:return False
                if p is note:
                    if not actual.startswith('(')or not actual.endswith(')'):return False
                    display=actual[1:-1]
                else:
                    if '('in actual or ')'in actual:return False
                    display=actual
                if display!=f['text']:return False
                pieces.append(display);points.append((offsets[li-1]+a,offsets[li-1]+b))
            if ''.join(pieces)!=p['text']:return False
            for left,right in zip(points,points[1:]):
                gap=text[left[1]:right[0]]
                if left[1]>right[0]or re.fullmatch(r'(?:¶?\r?\n|<pb:[^>\r\n]+>¶?\r?\n)*',gap)is None:return False
            intervals[p['id']]=(points[0][0],points[-1][1])
        if intervals[body['id']][1]!=intervals[note['id']][0]or intervals[note['id']][1]!=intervals[following['id']][0]:return False
        def marker(p,key,pid):
            m=next(m for m in p['mentions']if m['id']==c[key])
            if (m.get('kind')!='person'or m.get('person_id')!=pid or m.get('status')=='unresolved'or m.get('candidate_person_ids')or p['text'][m['start']:m['end']]!=m['surface']):raise ValueError('Role marker')
            return m
        bs=marker(body,'body_subject_mention_id',sub);bg=marker(body,'body_ancestor_mention_id',gid);ns=marker(note,'note_subject_mention_id',sub);nf=marker(note,'note_ancestor_mention_id',mid)
        if bs['start']!=0 or bg['start']<bs['end']or body['text'][bg['start']-2:bg['start']]!='祖父':return False
        # Bind the inherited body subject through the complete literal intro,
        # rather than ignoring all intervening people or accepting a topic switch.
        courtesy=next(m for m in body['mentions']if m.get('kind')=='person'and m.get('person_id')==sub and m.get('start')==bs['end']+1)
        if courtesy.get('status')=='unresolved'or courtesy.get('candidate_person_ids')or body['text'][bs['end']:courtesy['start']]!='字'or body['text'][courtesy['start']:courtesy['end']]!=courtesy['surface']:return False
        cursor=courtesy['end'];role_start=bg['start']-2
        if cursor!=role_start:
            collateral=next(m for m in body['mentions']if m.get('kind')=='person'and m.get('start')==cursor and m.get('person_id')!=sub)
            if collateral.get('status')=='unresolved'or collateral.get('candidate_person_ids')or body['text'][collateral['start']:collateral['end']]!=collateral['surface']or body['text'][collateral['end']:role_start]!='從子也':return False
        if any(x in body['text'][bs['end']:bg['end']]for x in ['非','未','不','曰','「','」','『','』']):return False
        if ns['end']+1!=nf['start']or note['text'][ns['end']:nf['start']]!='父':return False
        clause=c['role_clause'];start,end=clause['start'],clause['end']
        if clause.get('kind')!='attributed_genealogical_report'or start!=ns['start']or end!=nf['end']or note['text'][start:end]!=ns['surface']+'父'+nf['surface']:return False
        layer=next(layer for layer in note['received_text_layers']if layer['start']==clause['attribution_start']and layer['end']==clause['attribution_end'])
        if layer.get('layer')!='ancient_quoted_text'or layer.get('authority')!=clause.get('authority')or layer['quote']!=note['text'][layer['start']:layer['end']]or not layer['start']<=start<end<=layer['end']:return False
        wm=next(m for m in note['mentions']if m['id']==clause['work_mention_id'])
        if wm.get('kind')!='work'or wm.get('work_id')!=clause.get('cited_work_id')or not layer['start']<=wm['start']<wm['end']<=start or note['text'][wm['start']:wm['end']]!=wm['surface']:return False
        lead=note['text'][wm['end']:start]
        if lead.startswith(('曰','稱')):lead=lead[1:]
        if any(ch in lead for ch in '曰云言「」『』“”')or any(ch in note['text'][start:end]for ch in '非未不或曰「」『』'):return False
        if not near['qualifiers']['source_term'].endswith(ns['surface']+'父'+nf['surface'])or not far['qualifiers']['source_term'].endswith('祖父'+bg['surface']):return False
        return True
    except (KeyError,TypeError,ValueError,StopIteration,IndexError,OSError,UnicodeError):
        return False
