"""Verify named or titled family roles against an exact span of the fixed witness."""
from hashlib import sha256

# Chapter, clause and predicate determine both endpoints in their source order.
CASES = {('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'mother', 'iwn_c2g_zvh'): ('廢帝', '憲嫄', 'iwn_c2g_zvh', '7r6_k52_qji_ABAACAABA'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'iwn_c2g_zvh'): ('廢帝', '世祖', 'iwn_c2g_zvh', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'y7i_swu_xgh'): ('子尚', '世祖', 'y7i_swu_xgh', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'hx8_st4_jdd_C'): ('楚玉', '世祖', 'hx8_st4_jdd_C', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'hx8_st4_jdd_D'): ('楚佩', '世祖', 'hx8_st4_jdd_D', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'hx8_st4_jdd_E'): ('楚琇', '世祖', 'hx8_st4_jdd_E', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '孝武文穆王皇后諱憲嫄，琅邪臨沂人。元嘉二十年，拜武陵王妃。生廢帝、豫章王子尚、山陰公主楚玉、臨淮康哀公主楚佩、皇女楚琇、康樂公主脩明。世祖', 'father', 'hx8_st4_jdd_F'): ('脩明', '世祖', 'hx8_st4_jdd_F', 'hx8_st4_jdd'), ('c-songshu-041-wangxianyuan-family', '后父偃', 'father', '7r6_k52_qji_ABAACAABA'): ('后', '偃', '7r6_k52_qji_ABAACAABA', '7r6_k52_qji_ABAACAAB'), ('c-songshu-041-wangxianyuan-family', '偃，字子游，晉丞相導玄孫，尚書嘏之子也。母晉孝武帝女鄱陽公主', 'mother', '7r6_k52_qji_ABAACAAB'): ('偃', '鄱陽公主', '7r6_k52_qji_ABAACAAB', '9c8_5fa_bea'), ('c-songshu-041-wangxianyuan-family', '母晉孝武帝女鄱陽公主', 'father', '9c8_5fa_bea'): ('鄱陽公主', '晉孝武帝', '9c8_5fa_bea', 'uke_dff_yrf'), ('c-songshu-041-wangxianyuan-family', '偃尚高祖第二女吳興長公主諱榮男', 'father', '3qs_nqa_ioa_AAAA'): ('榮男', '高祖', '3qs_nqa_ioa_AAAA', '3qs_nqa_ioa_AAA'), ('c-songshu-041-wangxianyuan-family', '尚太祖第六女臨川長公主諱英媛', 'father', '3bh_k4m_fg4_B'): ('英媛', '太祖', '3bh_k4m_fg4_B', '3bh_k4m_fg4'), ('c-songshu-041-wangxianyuan-family', '臨川長公主上表曰：「妾遭隨奇薄，絕於王氏，私庭囂戾，致此分異。今孤疾煢然，假息朝夕，情寄所鍾，唯在一子。契闊荼炭，持兼憐愍，否泰枯榮，繫以為命。實願申其門釁，還為母子。推遷僶俛，未及自聞。先朝慈愛，鑑妾丹衷。若賜使息徹', 'mother', 'yvy_7f7_tgk'): ('徹', '臨川長公主', 'yvy_7f7_tgk', '3bh_k4m_fg4_B')}
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
