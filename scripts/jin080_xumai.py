"""真胄世譜許邁妻孫氏的父女關係以女的指代及其父名為證。"""
def wife_father_valid(row, chapters):
    try:
        e,=row['evidence'];c=chapters[e['chapter_id']];p,=[p for p in c['paragraphs']if p['id']==e['paragraph_id']]
        child,=[r for r in c['annotation']['person_reference_occurrences'] if r['id']==e['subject_reference_id']]
        father,=[m for m in p['mentions']if m['id']==e['object_person_mention_id']];t=p['text']
        return (p['id']=='c-zhengao-020-jin080-xumai:sun' and e['quote']==t and p['text_layer']=='received_chapter'
                and row['predicate']=='father' and row['qualifiers']['source_term']=='娶吳郡孫宏，字彥達女'
                and t.startswith(row['qualifiers']['source_term']) and father['start']==3 and father['end']==5
                and t[3:5]==father['surface']=='孫宏' and child['start']==9 and t[9:10]==child['surface']=='女'
                and child['paragraph_id']==p['id'] and child['person_id']==row['subject_person_id']
                and father['person_id']==row['object_person_id'] and child['person_id']!=father['person_id'])
    except (KeyError,TypeError,ValueError,IndexError):
        return False

def appraisal_valid(p,chapter,root):
    import hashlib
    try:
        source=chapter['source'];raw=(root/source['raw_path']).read_bytes();lines=raw.decode().splitlines()
        return (chapter['id']=='c-jinshu-080-wangxizhi-family' and p['id']==chapter['id']+':line126'
                and source['revision_id']==2603570 and source['raw_file_sha256']==hashlib.sha256(raw).hexdigest()
                and lines[123]=='==贊==' and p['source_position']['first_line']==126
                and p['text_layer']=='received_compiler_appraisal' and lines[125]=='　　'+p['text']
                and p['text'].startswith('贊曰：書契之興') and p['text'].endswith('何足論哉！'))
    except (KeyError,TypeError,ValueError,OSError,IndexError):
        return False
