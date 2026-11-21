"""按固定原始碼位覆核 梁書卷二十一王份家傳。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-liangshu-021-wangfen', 'c-nanshi-012-zhang-shangrou-yixing', 'c-liangshu-027-luxiang-wangqian', 'c-liangshu-055-xiaoji-wangqian', 'c-nanshi-023-wangqian-mothers')
F='source-evidence/liang021-wangfen-family/frames.json'
FS='8698ffa61ca0bb0c438e9cf77b22d463433fd6890b88f863d30211c38e4b678c'
R='source-evidence/liang021-wangfen-family/reading-4.json'
RS='631180bfed8b3d47c83df33c61192d0b0c428b881391660ec990b0e17263b741'
PROPOSALS={'tp-liang021-wangfen-family-fen-huangmen': ('c-liangshu-021-wangfen:p002', '1227e4e4393ad5f1c0863a8de0941cac7803d04b6fb1690b46ed11210e4dbce7', '1ba0c579c8b12aa1befce60c0e4dca43626834c17612d69f54b5cb12f6e2f110'), 'tp-liang021-wangfen-family-xi-給事黃門侍郎': ('c-liangshu-021-wangfen:p010', '7f4558ff842283bc63255a8a980fd5fb1406d45b7d84e89141da14e54a87a3f7', '017b28332c56caa2aea610e8337816d9231708f9a61895a95f66ebbcfd94df88'), 'tp-liang021-wangfen-family-xi-尚書吏部郎中': ('c-liangshu-021-wangfen:p010', '7f4558ff842283bc63255a8a980fd5fb1406d45b7d84e89141da14e54a87a3f7', 'e508fe87428ee1d3e1b63c49357312f5267b97950248217b993408f5843c7a62'), 'tp-liang021-wangfen-family-qian-wei': ('c-liangshu-021-wangfen:p012', 'a1d340dc8cdb941c692d94c0492eaebccc019f39a19f9e2bf0a55a42ad7ecc4e', '7c16f8f6e93092859aed9ec1b60aeecaeaf0e6a3a11076ba754ad0a9d5eff756'), 'tp-liang021-wangfen-family-qian-shixing': ('c-liangshu-021-wangfen:p012', 'a1d340dc8cdb941c692d94c0492eaebccc019f39a19f9e2bf0a55a42ad7ecc4e', 'f4249b4156e497d39c2394bf0a2faee7310a851a2e0ab3853a5747f8c4ec2196'), 'tp-liang021-wangfen-family-qian-anxi': ('c-liangshu-021-wangfen:p012', 'a1d340dc8cdb941c692d94c0492eaebccc019f39a19f9e2bf0a55a42ad7ecc4e', '2d969a23bab5ab43cc2f495ba83cfbc78a4c6d12c0b779f049650b408c0e7bbc'), 'tp-liang021-wangfen-family-qian-shu': ('c-liangshu-021-wangfen:p012', 'a1d340dc8cdb941c692d94c0492eaebccc019f39a19f9e2bf0a55a42ad7ecc4e', '4ba1a11fc67ce87f529e309bbc0c550b96e7c4c16ea3fda39975b888dd58a4f1')}

def h(x):return hashlib.sha256(x.encode()).hexdigest()
def hd(v):return h(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def source(root,relative,digest):
    root=Path(root).resolve();p=root/relative
    if p!=p.resolve() or not p.is_relative_to(root):raise ValueError('來源路徑')
    s=p.read_text()
    if h(s)!=digest:raise ValueError('校本指紋')
    return s

def frame(ch,root):return json.loads(source(root,F,FS))[ch['id']]

def errors(ch,root):
    if ch['id']not in CIDS:return []
    try:
        u=frame(ch,root);s=ch['source'];ps=ch['paragraphs'];raw=source(root,u['source_path'],u['raw_sha256']);ls=raw.splitlines(keepends=True)
        if (ch['source_id'],s['raw_path'],s['raw_file_sha256'],s['revision_id'],s['image_verified'])!=(u['source_id'],u['source_path'],u['raw_sha256'],u['revision_id'],False):raise ValueError('底本')
        if hd([p['source_position']for p in ps])!=u['positions_sha256']:raise ValueError('段落選取')
        for i,p in enumerate(ps,1):
            pos=p['source_position'];ix=pos['raw_character_offsets'];n=pos['first_line'];base=sum(map(len,ls[:n-1]));
            if p['id']!=u['paragraph_ids'][i-1] or n!=pos['last_line'] or pos['raw_start']!=base+pos['line_start'] or pos['raw_end']!=base+pos['line_end'] or hd(ix)!=pos['projection_sha256'] or ix!=sorted(set(ix)) or ''.join(raw[v]for v in ix)!=p['text']:raise ValueError('原字')
        if h('\n\n'.join(p['text']for p in ps))!=u['body_sha256'] or ch['text_sha256']!=u['body_sha256'] or hd(ch['annotation'])!=u['annotation_sha256'] or hd([p['mentions']for p in ps])!=u['mentions_sha256']:raise ValueError('姓名、引語及官次')
        for r,d in [('source-evidence/liang021-wangfen-family/reading-1.json', '0d3584649533f98875e59f59d17c002bcd68fd72cd96d53a5800eddc5b2a498b'), ('source-evidence/liang021-wangfen-family/reading-2.json', '747fa7f8eda252373e957672dace82d31c2aedf2385ee2a2f5bfd2c186141583'), ('source-evidence/liang021-wangfen-family/reading-3.json', 'f10c1b36df17fcaa2ac320257c0b567ccbb68268483b9e8f1782d31a0e01d921'), ('source-evidence/liang021-wangfen-family/reading-4.json', '631180bfed8b3d47c83df33c61192d0b0c428b881391660ec990b0e17263b741')]:
          for v in json.loads(source(root,r,d))['comparisons']:
            l=source(root,v['fixed_path'],v['sha256']).splitlines()[v['source_line']-1]
            if l[v['start']:v['end']]!=v['quote']:raise ValueError('旁證')
        return []
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['梁書卷二十一王份家傳 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['梁書卷二十一王份家傳 的親屬、職序或身後事與所據原句不合']

def proposal_valid(q,ch):
    try:
        pid,body,record=PROPOSALS[q['id']];p,=[p for p in ch['paragraphs']if p['id']==pid]
        if ch['id']not in CIDS or h(p['text'])!=body or hd(q)!=record:return False
        for f in ('appointment_anchor','role_anchor','non_assumption_anchor'):
            a=q[f]
            if a['paragraph_id']!=pid or p['text'][a['start']:a['end']]!=a['surface']:return False
        e,=q['evidence'];np=p
        if e.get('context'):
            try:from scripts.subject_continuation import prior_subject_valid
            except ImportError:from subject_continuation import prior_subject_valid
            if not prior_subject_valid(e['context'],e,q['person_id'],ch):return False
            np=next(op for op in ch['paragraphs']if op['id']==e['context']['paragraph_id'])
        m,=[m for m in np['mentions']if m['id']==q['person_mention_id']]
        return m['person_id']==q['person_id'] and m['kind']=='person' and e['quote']==p['text'] and q['title']==q['role_anchor']['surface'] and q['outcome']=='not_assumed'
    except (KeyError,TypeError,IndexError,ValueError):return False

XI_HOLDINGS={'th-liang021-wangfen-family-xi-6-17': 'e98f48821bc7010aa50dc9a5eadb80ed557c8f5ef4771faa371ad5c4847de9e9', 'th-liang021-wangfen-family-xi-6-36': '00c5d6136978903a64db1e74e5b2b29954126c9da8d00104e5654e4a259cc745'}
SPECIAL_AGES={'age-liang021-wangfen-family-fen-14': 'da730a9f5f0c98760ea0713171bd7c4b7c7a8dc409d927f875ea0afbb258826c', 'age-liang021-wangfen-family-xi-7-8': 'ac59f9b69dde22fde4d6e089642e67faaa7f15edb5123303f20124588b0db229', 'age-liang021-wangfen-family-xi-12': '99b009171976c6394735ff1f05a1ef7c79df04a87bf284b2beb16b319d32f4e0', 'age-liang021-wangfen-family-xi-14': 'fc1ea084a4fc91007c8a5d80007ec6e24bda3bac0860d46f6e9d7f8128f4a52b'}
XI_PARAGRAPHS={9: '08e703a71e84dbb1dc6d5a4f4f464431a7f8cb196c37bc30635dfbab02a8483b', 10: '7f4558ff842283bc63255a8a980fd5fb1406d45b7d84e89141da14e54a87a3f7', 6: '64f991369a87351da996f7013f57c2b5aee90c562f9ef3db8d170543cf8c95b0'}
def age_valid(a,ch,root):
    try:
        if hd(a)!=SPECIAL_AGES[a['id']] or errors(ch,root):return False
        e,=a['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);b=a['source_anchor']
        m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
        return e['quote']==p['text'] and a['person_id']==m['person_id'] and p['text'][b['start']:b['end']]==a['source_term']==b['surface']
    except (KeyError,TypeError,ValueError,IndexError,StopIteration):return False

def xi_end_title(att,h0,ch):
    try:
        if ch['id']!='c-liangshu-021-wangfen' or h0['person_id']!='q7m_r8k_2vn_ABAB' or hd(h0)!=XI_HOLDINGS[h0['id']] or att not in h0['attestations']:return False
        three=[p for p in ch['paragraphs']if int(p['id'][-3:]) in XI_PARAGRAPHS]
        if [int(p['id'][-3:])for p in three]!=[9,10,6] or any(h(p['text'])!=XI_PARAGRAPHS[int(p['id'][-3:])]for p in three):return False
        start,mid,end=three
        ctx=att['context'];e,=h0['evidence'];m=next(m for m in start['mentions']if m['id']==ctx['person_mention_id'])
        return m['person_id']==h0['person_id'] and ctx['intervening_paragraph_ids']==[mid['id']] and e['quote']==end['text'] and end['text'][att['start']:att['end']]==h0['title']==att['surface']
    except (KeyError,IndexError,ValueError,TypeError,StopIteration):return False
