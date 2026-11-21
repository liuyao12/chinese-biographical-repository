"""Bind two distinct obituary clauses in the closing paragraph of Wang Zhenfeng's biography."""
from hashlib import sha256


def valid(row, evidence, chapter, root, age=False):
    if chapter.get('id') != 'c-songshu-041-wangzhenfeng' or evidence['chapter_id'] != chapter['id']:
        return False
    para = chapter['paragraphs'][-1]
    if evidence.get('paragraph_id') != para['id'] or evidence.get('quote') != para['text']:
        return False
    raw = (root/chapter['source']['raw_path']).read_bytes()
    if (chapter['source']['revision_id'] != 2634831 or sha256(raw).hexdigest() != chapter['source']['raw_file_sha256']
            or ''.join(raw.decode()[i] for i in para['source_position']['raw_character_offsets']) != para['text']):
        return False
    empress = 'q7m_r8k_2vn_B'
    emperor = '6y2_apj_l05'
    person = row.get('person_id')
    if person not in (empress,emperor) or (age and person != empress):
        return False
    if not para['text'].endswith('順帝禪位，太后與帝遜于東邸，因遷居丹陽宮，拜汝陰王太妃。順帝殂於丹陽，更立第京邑。建元元年，薨于第，時年四十四。追加號諡，葬以宋后禮。父僧朗，事別見景文傳。'):
        return False
    mark = next((r for r in chapter['annotation']['person_reference_occurrences'] if r['id']==evidence.get('person_reference_id')),None)
    term,anchor,frame = ('薨','太后','太后與帝遜于東邸') if person==empress else ('殂','順帝','順帝殂於丹陽')
    if (not mark or mark.get('person_id')!=person or mark.get('paragraph_id')!=para['id'] or mark['surface']!=anchor
            or mark['start']!=para['text'].index(frame) or mark['end']!=mark['start']+len(anchor)):
        return False
    if age:
        return (row['source_term']=='時年四十四' and row['value']==44 and row['age_context']['kind']=='at_death'
                and row['age_context']['life_event_id']=='le-song041-wangzhenfeng-278-'+str(para['text'].index('薨于第')))
    position=para['text'].index('薨于第' if person==empress else '殂於丹陽')
    return (row.get('event_type')=='death' and row['source_term']==term and row['source_anchor']=={
        'paragraph_id':para['id'],'start':position,'end':position+1,'surface':term})
