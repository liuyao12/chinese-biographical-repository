"""Editorial parent edge from a received father and its attached paternal-grandfather note."""
import json,hashlib
from pathlib import Path

def body_note_ancestor_parent_valid(member, rows, assertions, chapters, root):
    c=member.get('parent_connection')
    if not isinstance(c,dict) or c.get('type')!='parent_between_body_and_attached_note_ancestors':return False
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
