"""校方正注獨立引書區塊；該條數位來源以一對模板框出古注。"""
import hashlib,re
def formal_comment(p,chapter,root):
    try:
        s=chapter['source'];data=(root/s['raw_path']).read_bytes();t=data.decode();q=p['source_quote'];i,j=q['raw_start'],q['raw_end']
        if hashlib.sha256(data).hexdigest()!=s['raw_file_sha256'] or chapter['id']!='c-shishuoxinyu-005-wangdao-relatives':return False
        a=t.rfind('{{*s}}',0,i);b=t.find('{{*e}}',j)
        if a<0 or b<0 or t[a:i]!='{{*s}}《中興書》曰：「' or '\n' in t[a:b] or '{{*e}}' in t[a:j]:return False
        unmarked=re.sub(r'\{\{ProperNoun\|([^{}]+)\}\}',r'\1',q['quote'])
        return (q['quote']==t[i:j] and q['raw_line']==t[:i].count('\n')+1
                and p['text']==re.sub(r'-\{([^{}]+)\}-',r'\1',unmarked)
                and p['text_layer']=='witness_appended_liuxiaobiao_note'
                and q['source_layer']=='劉注引中興書' and p['attribution']=={'annotator':'劉孝標','quoted_work':'中興書'})
    except (KeyError,ValueError,TypeError,OSError):return False
