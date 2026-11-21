"""Verify named or titled family roles against an exact span of the fixed witness."""
from hashlib import sha256

# Chapter, clause and predicate determine both endpoints in their source order.
CASES = {('c-songshu-041-wangzhenfeng', '明恭王皇后諱貞風，琅邪臨沂人也。元嘉二十五年，拜淮陽王妃。太宗改封，又為湘東王妃。生晉陵長公主伯姒、建安長公主伯媛', 'father', 'cti_o52_4nz_B'): ('伯姒', '太宗', 'cti_o52_4nz_B', 'cti_o52_4nz'), ('c-songshu-041-wangzhenfeng', '明恭王皇后諱貞風，琅邪臨沂人也。元嘉二十五年，拜淮陽王妃。太宗改封，又為湘東王妃。生晉陵長公主伯姒、建安長公主伯媛', 'father', 'cti_o52_4nz_C'): ('伯媛', '太宗', 'cti_o52_4nz_C', 'cti_o52_4nz'), ('c-songshu-041-wangzhenfeng', '太后與帝遜于東邸，因遷居丹陽宮，拜汝陰王太妃。順帝殂於丹陽，更立第京邑。建元元年，薨于第，時年四十四。追加號諡，葬以宋后禮。父僧朗，事別見景文傳。', 'father', 'q7m_r8k_2vn_B'): ('太后', '僧朗', 'q7m_r8k_2vn_B', 'q7m_r8k_2vn'), ('c-songshu-041-wangzhenfeng', '后兄揚州刺史景文', 'brother', 'q7m_r8k_2vn_B'): ('后', '景文', 'q7m_r8k_2vn_B', '1tc_q18_x7v'), ('c-songshu-041-wangzhenfeng', '貞風，琅邪臨沂人也。元嘉二十五年，拜淮陽王妃。太宗', 'spouse', 'q7m_r8k_2vn_B'): ('貞風', '太宗', 'q7m_r8k_2vn_B', 'cti_o52_4nz')}
REVISIONS={'b-songshu-041':2634831}

def valid(claim, evidence, chapter, root):
    try:
        qualifiers = claim['qualifiers']
        basis = qualifiers['reading_basis']
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        source = chapter['source']
        raw = (root / source['raw_path']).read_bytes()
        decoded = raw.decode()
        revision = REVISIONS[chapter['book_id']]
        text = paragraph['text']
        frame = basis['source_quote']
        start, end = basis['start'], basis['end']
        if (revision != source['revision_id'] or sha256(raw).hexdigest() != source['raw_file_sha256']
                or paragraph['source_position']['revision_id'] != revision
                or text != ''.join(decoded[i] for i in paragraph['source_position']['raw_character_offsets'])
                or evidence['quote'] != text or evidence['chapter_id'] != chapter['id']
                or text.count(frame) != 1 or text[start:end] != frame or qualifiers['source_term'] not in frame
                or claim['subject_person_id'] == claim['object_person_id']):
            return False
        marks = {r['id']:r for r in chapter['annotation']['person_reference_occurrences'] if r['paragraph_id'] == paragraph['id']}
        marks.update({m['id']:m for m in paragraph['mentions'] if m['kind'] == 'person'})
        words = CASES[(chapter['id'],frame,claim['predicate'],claim['subject_person_id'])]
        for idx,(side,word) in enumerate(zip(('subject','object'),words[:2])):
            if claim[side+'_person_id'] != words[idx+2]: return False
            mention = marks[basis[side + '_anchor_id']]
            if (mention['person_id'] != claim[side+'_person_id'] or mention['surface'] != word
                    or not start <= mention['start'] < mention['end'] <= end
                    or text[mention['start']:mention['end']] != word):
                return False
        return True
    except (KeyError, ValueError, TypeError, IndexError, StopIteration):
        return False
