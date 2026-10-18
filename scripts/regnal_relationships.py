# coding: utf-8
"""Validate explicit editorial reign context; never infer relationships at runtime."""
import hashlib
import re


def received_body(raw):
    """Remove separately attributed parenthetical notes and layout, preserving glyphs."""
    if not isinstance(raw, str):
        raise ValueError('原始見證必須是文字')
    result=[];depth=0;i=0
    while i<len(raw):
        if not depth and raw.startswith('<pb:',i):
            end=raw.find('>',i)
            if end<0:raise ValueError('頁標未閉合')
            i=end+1;continue
        c=raw[i]
        if c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth<0:raise ValueError('古注括號未配對')
        elif not depth and c not in '\n\r¶ \t　':result.append(c)
        i+=1
    if depth:raise ValueError('古注未閉合')
    return ''.join(result)


def regnal_spouse_errors(assertion,chapter):
    errors=[]
    def check(ok,message):
        if not ok:errors.append('帝紀配偶承接：'+message)
    try:
        c=assertion.get('context');check(isinstance(c,dict),'缺少承接記錄')
        if not isinstance(c,dict):return errors
        ids=c.get('paragraph_ids');ps={p['id']:p for p in chapter.get('paragraphs',[])};order=list(ps)
        check(c.get('kind')=='regnal_empress_context' and assertion.get('predicate')=='spouse','只適用明書冊立皇后的配偶關係')
        check(isinstance(ids,list) and len(ids)==2 and all(isinstance(x,str) and x in ps for x in ids),'須有同篇兩段')
        if not isinstance(ids,list) or len(ids)!=2 or not all(isinstance(x,str) and x in ps for x in ids):return errors
        first,last=(ps[x] for x in ids);check(order.index(ids[0])<order.index(ids[1]),'即位段須先於冊后段')
        check(all(p.get('text_layer')=='received_chapter' for p in [first,last]),'附注不可冒作正文在位語境')
        check(bool(re.search('本紀|帝紀',chapter.get('title',''))),'須為帝紀而非泛傳記')
        check(c.get('status')=='contextual_provisional' and c.get('human_reviewed') is False and bool(c.get('reviewer')) and bool(c.get('rationale')),'缺少編者判讀及未人工覆核狀態')
        evidence=assertion.get('evidence',[])
        check(len(evidence)==2 and [e.get('paragraph_id') for e in evidence]==ids and all(e.get('quote')==p['text'] for e,p in zip(evidence,[first,last])),'兩段引文及順序須完整相符')
        monarch=next((m for m in first.get('mentions',[]) if m['id']==c.get('monarch_mention_id')),None)
        empress=next((m for m in last.get('mentions',[]) if m['id']==c.get('empress_mention_id')),None)
        accession=c.get('accession_term');installation=assertion.get('qualifiers',{}).get('source_term')
        check(isinstance(accession,str) and accession in first['text'] and any(t in accession for t in ['即皇帝位','即天子位','即位']),'即位原詞不符')
        check(isinstance(installation,str) and installation in last['text'] and installation.startswith('立皇后'),'冊后原詞不符')
        for m,pid,p,term in [(monarch,assertion.get('object_person_id'),first,accession),(empress,assertion.get('subject_person_id'),last,installation)]:
            check(bool(m) and m.get('kind')=='person' and m.get('person_id')==pid and isinstance(term,str) and any(i<=m['start']<m['end']<=i+len(term) for i in range(len(p['text'])) if p['text'].startswith(term,i)),'即位者或皇后錨點須在相應原詞內')
        w=c.get('witness_interval');check(isinstance(w,dict),'須保存含省略部分的固定見證區間')
        if not isinstance(w,dict):return errors
        src=chapter['source'];a=w.get('first_line');b=w.get('last_line');raw=w.get('raw_quote');body=received_body(raw)
        check(type(a)is int and type(b)is int and a>0 and b>=a and len(raw.splitlines())==b-a+1,'原始行範圍不符')
        check(w.get('source_commit')==src.get('source_commit') and w.get('source_blob_sha')==src.get('source_blob_sha'),'固定提交或blob不符')
        check(w.get('raw_quote_sha256')==hashlib.sha256(raw.encode()).hexdigest() and w.get('body')==body,'原始區間指紋或正文分層不符')
        excerpts=src.get('normalization',{}).get('excerpts',[])
        for p in [first,last]:
            pos=p.get('source_position',{});x=pos.get('first_line');y=pos.get('last_line')
            valid=type(a)is int and type(b)is int and type(x)is int and type(y)is int and a<=x<=y<=b and pos.get('source_commit')==w.get('source_commit')
            check(valid,'兩段原始行須包含在完整區間內')
            if valid:
                snippet='\n'.join(raw.splitlines()[x-a:y-a+1]);record=next((e for e in excerpts if e.get('proposed_paragraph_id')==p['id']),{})
                check(snippet==record.get('raw_quote') and p['text'] in received_body(snippet),'區間與已登記選錄不符')
        if isinstance(accession,str) and isinstance(installation,str) and body.count(accession)==1 and body.count(installation)==1:
            start=body.index(accession)+len(accession);stop=body.index(installation);check(start<=stop,'冊后不得早於即位')
            between=body[start:stop];check(not any(t in between for t in ['即皇帝位','即天子位','即位','崩','廢帝','改立皇帝']),'區間有君主更替用語，須另核不得默套')
        else:check(False,'區間缺少唯一即位及冊后原詞')
    except (KeyError,TypeError,ValueError,AttributeError,StopIteration) as exc:
        errors.append('帝紀配偶承接：結構或原始見證無效：'+str(exc))
    return errors
