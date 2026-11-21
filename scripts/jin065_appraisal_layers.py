"""Recognize the marked historian's appraisal and praise at the end of the fixed Jin 65 source."""
import hashlib
try:from scripts.six_dynasties_inventory import received_text
except ImportError:from six_dynasties_inventory import received_text

def valid(p,ch,root):
    try:
        w=p['source_witness'];position=p['source_position'];n=w['raw_line'];prefix={120:'史臣曰：',122:'贊曰：'}[n]
        if ch['id']!='c-jinshu-065-wangdao-family' or p['text_layer']!='received_compiler_appraisal':return False
        path='source-evidence/jin065-wang-survey/jin065-ws1756144.wikitext'
        if w['raw_path']!=path or w['raw_sha256']!='98c7262170dcc4bf0f7e831fb693e46ff819e46fdd9407a484c787185901550a':return False
        fixed=(root/path).read_bytes();lines=fixed.decode().splitlines(keepends=True);a=sum(map(len,lines[:n-1]));line=lines[n-1].rstrip('\n')
        return (int(ch['source']['revision_id'])==w['revision_id']==position['revision_id']==1756144
                and hashlib.sha256(fixed).hexdigest()==w['raw_sha256'] and position['first_line']==n
                and w['section_heading_line']==118 and lines[117].strip()==w['section_heading']=='==史臣曰=='
                and [w['raw_start'],w['raw_end']]==[a,a+len(line)] and line==w['raw_quote']
                and line.startswith('　　'+prefix) and received_text(line[2:])==p['text'])
    except (KeyError,TypeError,IndexError,ValueError,OSError):return False
