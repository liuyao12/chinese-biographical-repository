from pathlib import Path
import urllib.request,json,hashlib,base64
P=Path('/Users/liuyao/.codex/visualizations/2026/10/08/01a1196e-92f4-7fd1-a99c-8be9123187ca/cbr-wangxuan-eight-wang-identity-research');repo='kanripo/KR4b0009';api='https://api.github.com/repos/'+repo
req=lambda u:json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'CBR-source-reading'}),timeout=30))
c=req(api+'/commits/master');commit=c['sha'];files=req(api+'/contents?ref='+commit);print(commit,[x['name']for x in files],flush=True)
for name in ['KR4b0009_010.txt','Readme.org']:
 item=next(x for x in files if x['name']==name);d=req(item['url']);raw=base64.b64decode(d['content']);out=P/name;out.write_bytes(raw);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==d['sha'];meta={'repository':repo,'commit':commit,'git_blob_sha1':d['sha'],'file':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'url':'https://github.com/'+repo+'/blob/'+commit+'/'+name,'api_url':item['url'],'image_verified':False,'rights':'Kanripo文字見證；原作品古籍，數位轉錄權利依庫聲明；本包僅研究文字、不存圖。'};(P/(name+'.metadata.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(meta,flush=True)
