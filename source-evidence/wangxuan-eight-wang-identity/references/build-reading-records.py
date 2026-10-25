from pathlib import Path
import json,hashlib,shutil
R=Path('/private/tmp/cbr-medieval-facts-next-20261022');P=Path('/Users/liuyao/.codex/visualizations/2026/10/08/01a1196e-92f4-7fd1-a99c-8be9123187ca/cbr-wangxuan-eight-wang-identity-research');J=lambda x:json.dumps(x,ensure_ascii=False,indent=2)+'\n';readings=[]
def unit(key,file,start,end,url,layer,note):
 raw=(P/file).read_text();a=raw.index(start);z=raw.index(end,a+len(start));q=raw[a:z];v={'id':key,'file':file,'file_sha256':hashlib.sha256((P/file).read_bytes()).hexdigest(),'start':a,'end':z,'first_line':raw.count('\n',0,a)+1,'last_line':raw.count('\n',0,z)+1,'raw':q,'raw_quote_sha256':hashlib.sha256(q.encode()).hexdigest(),'url':url,'layer':layer,'read_scope':note,'image_verified':False};assert raw[a:z]==v['raw'];readings.append(v)
for rel,pid,key in [('corpus/jinshu/035-pei-family.json','c-jinshu-035-peikai-family:p019','jin035-eight'),('corpus/jinshu/043-wangyan.json','c-jinshu-043-wangyan:p010','jin043-xuan')]:
 c=json.loads((R/rel).read_text());p=next(p for p in c['paragraphs']if p['id']==pid);readings.append({'id':key,'existing_I_path':rel,'chapter_id':c['id'],'paragraph_id':p['id'],'quote':p['text'],'quote_sha256':hashlib.sha256(p['text'].encode()).hexdigest(),'url':c['source']['permalink'],'source_revision':c['source']['revision_id'],'file_sha256':c['source']['wikitext_sha256'],'layer':'received_dynastic_history_body','image_verified':False,'read_scope':'完整自然段；035並重讀前3附敘以分永嘉/東海王越語境，043十段已於前批完整讀。'})
commit='c6c870dd30b16e97405e0fb9d3b42c47f48c52d6';ss=lambda n:'https://github.com/kanripo/KR3l0002/blob/'+commit+'/KR3l0002_'+n+'.txt'
unit('ssxy-pinzao-six','ssxy-pinzao-ws1532655.wikitext','#正始中，人士比論','#冀州刺史楊淮','https://zh.wikisource.org/w/index.php?title=世說新語/品藻&oldid=1532655','received_body_with_Liu_annotation','完整第6自然條，保五荀/五陳與又以八裴八王及全部古注；不取正始總起為八王共同年份。')
unit('ssxy-pinzao-six-SBCK','ssxy-SBCK-003.txt','正始中人士比論','冀州剌史楊淮',ss('003'),'received_body_with_two_line_ancient_notes','完整第6自然條，SBCK逐行含pb/雙行注，不聲稱已核影像。')
unit('ssxy-shijian-twelve','ssxy-SBCK-002.txt','王平子素不知眉子','王大將軍始下',ss('002'),'body_plus_Liu_note_quoting_Jinzhugongzan','完整識鑒第12，注轉引晉諸公贊，未親見被引原書。')
unit('ssxy-shangyu-thirtyfive-thirtysix','ssxy-shangyu-ws1532652.wikitext','#庾太尉少為王眉子','#王公目太尉','https://zh.wikisource.org/w/index.php?title=世說新語/賞譽&oldid=1532652','body_plus_Liu_notes','完整賞譽35及36，含晉諸公贊/八王故事/王隱晉書等古注；只取同指與人際年代語境，不移入人物新官職或親屬。')
unit('ssxy-shangyu-peimiao','ssxy-shangyu-ws1532652.wikitext','#太傅府有三才','#林下諸賢','https://zh.wikisource.org/w/index.php?title=世說新語/賞譽&oldid=1532652','body_plus_Liu_notes','完整賞譽28，裴景聲正文與注裴邈分層；只佐東海王府品評圈，不判裴邈字景聲/景初正誤。')
meta=json.loads((P/'KR4b0009_010.txt.metadata.json').read_text());unit('taoji-eight-roster','KR4b0009_010.txt','裴徽字文秀','魏司空王昶',meta['url'],'transmitted_qunfulu_roster_plus_commentary','完整八裴八王自然群組與前後邊界；正文名單與括號小注分層，無作者成書先後推定。卷10完整檔已讀，非全陶集。')
raw=(P/'KR4b0009_010.txt').read_text();a=raw.index('王玄字眉子');z=raw.index('　　右河東八裴',a);readings.append({'id':'taoji-wangxuan-base-and-note','file':'KR4b0009_010.txt','file_sha256':meta['sha256'],'start':a,'end':z,'raw':raw[a:z],'base_exact_surface':'王玄字眉子','editorial_reading_of_parenthetical_note':'衍子；陳留内史','note_reading_status':'reading_from_preserved_line_split_note_not_image_collation','layer_separation':'王玄字眉子為收到名單本文；衍子/陳留内史為該箋註本小字，不冒作陶潛本文。','url':meta['url'],'image_verified':False})
(P/'selected-readings.json').write_text(J(readings))
comparison={'source_person_id':'duy_kcy_44o','preferred_same_person_candidate':'35b_mo3_adg','recommendation':'contextual_preferred_same_person','confidence':'high_but_editorial_provisional','adopted':False,'human_reviewed':False,'I_written':False,'reasons':[
 {'kind':'same_finite_comparison_group','evidence':['jin035-eight','ssxy-pinzao-six','taoji-eight-roster'],'reason':'035與世說的八對名單相同；箋註陶集另列同一8裴/8王集合，明王玄字眉子。群輔錄次序不同，只比集合與姓名，不重新配八對。'},
 {'kind':'courtesy_and_parent_role_bridge','evidence':['taoji-wangxuan-base-and-note','jin043-xuan','ssxy-shijian-twelve'],'reason':'名單王玄明字眉子；箋注衍子與識鑒注夷甫子，對043王衍本傳子玄字眉子的具體角色一致，非只同名。'},
 {'kind':'office_and_death_narrative_compatibility','evidence':['jin043-xuan','ssxy-shijian-twelve','ssxy-shangyu-thirtyfive-thirtysix'],'reason':'陳留職與眉子/王衍子同時出現，塢人所害/盜所害及慕簡曠均有具體敘事對應；不將不同來源太守/內史名號裁成同一授任或靜改字。'},
 {'kind':'time_and_reputation_network','evidence':['ssxy-shangyu-peimiao','ssxy-shijian-twelve','ssxy-shangyu-thirtyfive-thirtysix'],'reason':'裴邈與眉子都見東海王越府/永嘉渡江前後名士品評圈；王眉子與庾亮/謝鯤以及叔平子、王敦交涉背景相容，不主張共時聚會或精確年份。'}],
 'counterevidence_and_limits':[
 {'issue':'正始中總起','assessment':'品藻第6先五荀五陳，再又以八裴八王；035明魏晉之世。此是跨代名族比較，不能以總起正始斷王玄活於曹魏正始或因此另造人；也不把收到條文改掉。'},
 {'issue':'同組不同世代','assessment':'名單含父子輩和更早王祥，八王不是八位同齡者或同次集會，更不是宗室八王之亂；這不構成兩玄異人的反證。'},
 {'issue':'注與本傳依存可能','assessment':'箋註小字可能取材晉書/世說，同一史料傳承不能重複算獨立證實；但明名單中王玄=字眉子/衍子的傳世釋名，足作有資格指稱首選。未核群輔錄作者與實際撰作層次，不宣稱陶潛本人早期獨立記載。'},
 {'issue':'內史/太守名異','assessment':'收錄本小注稱陳留内史，043與世說注太守；保來源稱異，不能憑兩字自動分人，也不能本次替改官名或生成新任期。'},
 {'issue':'沒有035本身直接父字','assessment':'035只名字比較，不能單靠同名硬合；本次已有同組名單、字眉子、衍子等多層橋，缺本傳或未接父不另充反證。'},
 {'issue':'雲原字與未決資料','assessment':'035王玄61:63範圍與後雲結語照舊；本研究不改existing候選、別名、ID、家族或來源記錄。'}],
 'not_adopted_facts':['不填王玄生卒年或精確死年313','不增東海王府官職或陳留內史任職記錄','不改裴邈景初/景聲的來源字號','不一併接合035王澄或其他八王人物','不將群輔錄郡望語機械生成人物籍貫或共同父祖','不將八王故事書名誤當八名王氏比較組之書']}
(P/'identity-recommendation.json').write_text(J(comparison))
(P/'source-availability.json').write_text(J({'new_fixed_text':meta,'new_fixed_readme':json.loads((P/'Readme.org.metadata.json').read_text()),'reused_sources':'詳reused-reference-paths，原庫SBCK commit c6c870d與WS固定1532655/1532652','web_readable_primary':[{'url':'https://www.shidianguji.com/zh/book/HY0599/chapter/1kjifp8gsxk4b','scope':'實開集聖賢群輔錄下整頁，重點41–43行；含原字，不存HTML。'},{'url':'https://zh.wikisource.org/wiki/世說新語/品藻','scope':'實開第6完整條；固定原文另用已存1532655。'},{'url':'https://zh.wikisource.org/wiki/世說新語/識鑒','scope':'實開第12完整條及劉注；固定原文另用已存SBCK。'},{'url':'https://zh.wikisource.org/wiki/世說新語/賞譽','scope':'實開28、35、36完整條；固定原文另用已存1532652/SBCK。'}],'not_readable':[{'url':'https://ctext.org/wiki.pl?chapter=152874&if=gb','result':'403，不用搜尋OCR冒全文。'},{'url':'https://www.kanripo.org/text/KR4b0009/010','result':'web不可讀；改讀獨立公開GitHub固定文字，非繞過該站權限。'},{'url':'https://zh.wikisource.org/wiki/箋註陶淵明集_(四部叢刊本)/卷10','result':'web不可讀，不聲稱已讀此站該頁。'}],'rights_qualification':'古籍文字與數位見證原歸屬保留；Kanripo標SBCK不代表親核原版，Wikisource轉錄沿CC BY-SA來源聲明；沒有下載圖像/PDF/HTML二進位。','modern_search_results_used_only_as_leads':True,'modern_research_authority_relied_on':False}))
shutil.copyfile('/private/tmp/fetch-taoji-reference.log',P/'new-reference-fetch.log');shutil.copyfile('/private/tmp/fetch-taoji-reference.py',P/'fetch-new-public-reference.py')
print(len(readings))
