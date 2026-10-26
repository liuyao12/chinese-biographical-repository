"""正式書／卷篇引用；不從編輯選錄題刪字推導題名。"""
from pathlib import Path
import json

def _title(value):
    if not isinstance(value,str) or not value.strip():
        raise ValueError('正式來源題名必須為非空字串')
    return value.strip()

def citation_index(registry,directory):
    if not isinstance(registry,dict) or not isinstance(registry.get('works'),list):
        raise ValueError('作品登記格式錯誤')
    if not isinstance(directory,dict) or directory.get('schema_version')!=1 or not isinstance(directory.get('works'),list):
        raise ValueError('正式卷目格式錯誤')
    works={};formal={}
    for work in registry['works']:
        if not isinstance(work,dict) or not isinstance(work.get('id'),str) or work['id'] in works:
            raise ValueError('作品登記重複或錯誤')
        books={}
        for book in work.get('books',[]):
            if not isinstance(book,dict) or not isinstance(book.get('id'),str) or book['id'] in books or book.get('work_id')!=work['id']:
                raise ValueError('卷登記重複或作品歸屬錯誤')
            books[book['id']]=book
        works[work['id']]={'title':_title(work.get('citation_title',work.get('title'))),'books':books}
    for work in directory['works']:
        if not isinstance(work,dict) or not isinstance(work.get('work_id'),str) or work['work_id'] in formal or not isinstance(work.get('books'),list):
            raise ValueError('正式卷目作品重複或錯誤')
        books={}
        for book in work['books']:
            if not isinstance(book,dict) or not isinstance(book.get('book_id'),str) or book['book_id'] in books:
                raise ValueError('正式卷目卷重複或錯誤')
            citation=book.get('citation_title')
            if citation is not None and not isinstance(citation,str):
                raise ValueError('正式篇題格式錯誤')
            books[book['book_id']]=_title(citation if isinstance(citation,str)and citation.strip()else book.get('title'))
        formal[work['work_id']]={'title':_title(work.get('title')),'books':books}
    return {'registered':works,'formal':formal}

def load_citation_index(root):
    root=Path(root)
    return citation_index(json.loads((root/'registry/works.json').read_text()),json.loads((root/'data/corpus/chapter-directory.json').read_text()))

def source_caption(record,index):
    """精確按 work_id/book_id；缺目錄時只用正式登記，不用 selection/source title。"""
    if not isinstance(record,dict):
        raise ValueError('來源記錄格式錯誤')
    wid,bid=record.get('work_id'),record.get('book_id')
    work=index['registered'].get(wid)
    if work is None or bid not in work['books']:
        raise ValueError('來源作品／卷不屬於正式登記')
    if wid in index['formal']:
        formal=index['formal'][wid]
        if bid not in formal['books']:
            raise ValueError('已具正式目錄的來源卷尚未登記')
        title,chapter=formal['title'],formal['books'][bid]
    else:
        title=work['title'];book=work['books'][bid]
        chapter=_title(book.get('citation_title')or book.get('title'))
    return '《'+title+'・'+chapter+'》'
