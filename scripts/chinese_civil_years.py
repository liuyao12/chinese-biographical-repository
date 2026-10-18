# coding: utf-8
"""Prototype: validate an explicitly sourced Chinese civil-year label.

This does not convert a Gregorian window into an exact Gregorian date, nor
prove the editorial judgment that the quoted events are contemporaneous.
"""
import re

def numeral(token):
    digits='一二三四五六七八九'
    if token=='元':return 1
    if token in digits and len(token)==1:return digits.index(token)+1
    if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',token or ''):
        a,b=token.split('十');return (digits.index(a)+1 if a else 1)*10+(digits.index(b)+1 if b else 0)
    return None

def civil_year_errors(event,chapters,tables):
    if not isinstance(event,dict):return ['生卒事件須為物件']
    value=event.get('chinese_civil_year');errors=[]
    if not isinstance(value,dict):return ['中國曆年須為物件']
    def check(ok,message):
        if not ok:errors.append(message)
    year,n,era=value.get('year'),value.get('era_year'),value.get('era')
    check(type(year)is int and type(n)is int and n>0 and era in ['BCE','CE'] and year==(1-n if era=='BCE' else n),'中國曆年年編號不符')
    check(value.get('calendar')=='chinese_civil' and value.get('year_numbering')=='astronomical' and value.get('precision')=='year','中國曆年須明示曆法及年度精度')
    check(value.get('status')=='editorial_provisional' and value.get('human_reviewed')is False and bool(value.get('reviewer')) and bool(value.get('rationale')),'中國曆年缺暫定判讀及覆核狀態')
    evidence=event.get('evidence',[])
    if not isinstance(evidence,list) or any(not isinstance(e,dict) for e in evidence):
        errors.append('中國曆年事件證據須為引文列表');evidence=[]
    check(value.get('evidence')==evidence and value.get('original_quote') in [e.get('quote') for e in evidence],'中國曆年須保留本筆事件原句')
    expression=value.get('source_expression');contexts=value.get('context_evidence',[])
    if not isinstance(contexts,list) or any(not isinstance(e,dict) for e in contexts):
        errors.append('中國曆年上下文須為引文列表');contexts=[]
    check(isinstance(expression,str) and bool(expression) and any(isinstance(e,dict) and expression in e.get('quote','') for e in contexts),'中國曆年缺原紀年及上下文引句')
    for e in contexts:
        c=chapters.get(e.get('chapter_id'),{});p=next((p for p in c.get('paragraphs',[]) if p['id']==e.get('paragraph_id')),None)
        check(bool(p) and bool(e.get('quote')) and e['quote'] in p['text'] and all(e.get(k)==c.get(k) for k in ['work_id','book_id','chapter_id','source_id'] if k!='chapter_id'),'中國曆年上下文來源或引文不符')
        primary=[x for x in evidence if x.get('chapter_id')==e.get('chapter_id')]
        order={x['id']:i for i,x in enumerate(c.get('paragraphs',[]))}
        check(bool(primary) and e.get('paragraph_id') in order and all(order.get(e['paragraph_id'],-1)<=order.get(x.get('paragraph_id'),-1) for x in primary),'初版中國曆年上下文須為同篇事件前文或本段')
    eq=value.get('year_equivalence',{})
    if not isinstance(eq,dict):errors.append('中國曆年對照須為物件');eq={}
    table=tables.get(eq.get('table_id'),{})
    rows=[r for f in table.get('fragments',[]) for r in f.get('rows',[])]
    cells={c['id']:(r,c) for r in rows for c in r['cells']}
    source=table.get('source',{})
    check(all(eq.get(k)==source.get(k) for k in ['work_id','book_id','chapter_id']) and eq.get('source_id')==source.get('id') and eq.get('source_revision')==source.get('revision'),'中國曆年對照須固定表格見證')
    found={}
    for stem in ['regnal_era','regnal_year','editorial_year','event']:
        hit=cells.get(eq.get(stem+'_cell_id'));found[stem]=hit
        check(bool(hit) and bool(eq.get(stem+'_quote')) and eq[stem+'_quote']==hit[1]['text'],'中國曆年表格原句不符：'+stem)
    if all(found.values()):
        row=found['regnal_year'][0]
        check(found['editorial_year'][0]['id']==row['id']==found['event'][0]['id'],'中國曆年數位對照與事件不得跨列表格')
        order={r['id']:i for i,r in enumerate(rows)}
        check(order[found['regnal_era'][0]['id']]<=order[row['id']],'中國曆年起元欄不得來自後年')
        label=row.get('year',{})
        check(label.get('era')==era and label.get('value')==n and label.get('astronomical_year')==year and found['editorial_year'][1].get('column')==0,'中國曆年數字與編者對照不符')
        token=eq.get('regnal_year_quote');tail=re.search(r'([元一二三四五六七八九十]+)年$',expression or '')
        check(bool(tail) and tail[1]==token and numeral(token)==value.get('regnal_year_number'),'中國曆年原紀年與表列年序不符')
        anchor=re.search(r'([元一二三四五六七八九十]+)年$',eq.get('regnal_era_quote',''))
        clean=lambda label:re.sub(r'(皇帝|帝)$','',label)
        check(bool(tail) and bool(anchor) and numeral(anchor[1])==1 and clean(expression[:tail.start()])==clean(eq['regnal_era_quote'][:anchor.start()]),'中國曆年原紀年與表格起元名不符')
    return errors
