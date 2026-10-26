"""Three different speakers/occasions of source age in fixed WYD044."""
CID='c-songshu-044-wyd1739-xiehui'

def records(ch):
    if ch.get('id')!=CID:
        raise ValueError('報齡卷篇不符')
    ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']}
    def mention(p,key):
        return next(m for m in p['mentions']if m['id']==p['id']+':'+key)
    def row(key,p,m,value,number,term,context,note):
        if m['kind']!='person' or term not in p['text']:
            raise ValueError('報齡須有相符人物與原詞')
        return {'id':'age-song044-wyd-'+key,'person_id':m['person_id'],'value':value,
                'source_number':number,'source_term':term,'unit':'source_age_years',
                'counting':'unspecified_source_age','birth_year':None,'status':'source_attested',
                'date_expression':None,'evidence':[{**{k:ch[k]for k in('work_id','book_id','source_id')},
                'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':m['id']}],
                'age_context':context,'interpretation_note':note,'reviewer':'Codex（AI代理）',
                'human_reviewed':False,'model':None}
    p=ps['p003'];question=mention(p,'m0146');answer=mention(p,'m0148');asker=mention(p,'m0144')
    if (question['person_id']!=answer['person_id']or asker['person_id']==answer['person_id']
            or p['text'][asker['start']:answer['end']+5]!='澹問晦年晦答曰三十三'):
        raise ValueError('年齡問答須分詢問者與回答者，不借同段荀中郎之齡')
    a=row('hui-answer',p,answer,33,'三十三','晦答曰三十三',{'kind':'during_life'},
          '澹問晦年，晦本人回答三十三；保存問答原詞，不虛造年三十三或當卒齡，不倒算生年。')
    a['source_age_answer_binding']={'kind':'wyd_song044_named_age_answer',
        'question_person_mention_id':question['id'],'answer_person_mention_id':answer['id'],
        'asker_person_mention_id':asker['id'],'clause':{'paragraph_id':p['id'],
        'start':asker['start'],'end':answer['end']+5,'surface':'澹問晦年晦答曰三十三'}}
    m=mention(p,'m0158')
    if m['surface']!='荀中郎'or p['text'][m['start']:m['end']+4]!='荀中郎年二十七':
        raise ValueError('二十七屬荀中郎而非晦或澹')
    b=row('xun-recollection',p,m,27,'二十七','年二十七',{'kind':'during_life'},
          '謝澹引述荀中郎任北府都督時的往事，非謝晦本人的年齡；不由此補年份或出生年。')
    p=ps['p016'];m=mention(p,'m0365')
    if m['surface']!='晦'or p['text'][m['start']:m['end']+6]!='晦死時年三十七':
        raise ValueError('卒齡須有晦死時年三十七原句')
    c=row('hui-death',p,m,37,'三十七','年三十七',{'kind':'at_death','life_event_id':'le-song044-wyd-hui'},
          '本源明言晦死時年三十七，連到同人同段死亡記載；不把生前答齡當享年或倒算生年。')
    return [a,b,c]

def answer_valid(age,ch,root):
    try:
        try:from .wyd_song044_formal_roles import source_errors
        except ImportError:from wyd_song044_formal_roles import source_errors
        return not source_errors(ch,root) and age==records(ch)[0]
    except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):
        return False


def base_annotation(ch):
    """Separate only these validated additions from the original role contract."""
    annotation=dict(ch['annotation'])
    if 'age_assertions' in annotation:
        if annotation.pop('age_assertions')!=records(ch):
            raise ValueError('報齡主語或問答原詞漂移')
    return annotation
