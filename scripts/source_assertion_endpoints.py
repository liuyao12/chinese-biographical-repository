"""Ordinary assertion source/endpoint checks shared by native and graph names.

This validates references, not the editor's historical/linguistic judgment.
"""
try:from scripts.person_mentions import is_person_reference
except ImportError:from person_mentions import is_person_reference

def conditions(assertion,evidence,paragraphs,chapters,chapter_id):
 hit=paragraphs.get(evidence['paragraph_id'])
 source_ok=bool(hit) and hit[0]==chapter_id==evidence['chapter_id'] and evidence['quote'] in hit[1]['text']
 sid_ok=chapters.get(evidence['chapter_id'],{}).get('source_id')==evidence['source_id']
 local={m['person_id']for m in hit[1]['mentions']if is_person_reference(m)}if hit else set()
 endpoints_ok=assertion['subject_person_id']in local and assertion['object_person_id']in local
 return ((source_ok,'人物陳述引句與所屬篇不符'),(sid_ok,'人物陳述來源 ID 不符'),(endpoints_ok,'人物陳述端點未見於證據段落'))
