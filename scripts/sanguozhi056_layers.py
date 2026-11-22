"""卷56固定原文的版面模板與裴注，保留每個可見字的原始位置。"""
import re

def bounds(s,i):
 depth=1;j=i+2
 while depth:
  if j>=len(s):raise ValueError(s[i:i+40])
  if s.startswith('{{',j):depth+=1;j+=2
  elif s.startswith('}}',j):depth-=1;j+=2
  else:j+=1
 return j

def shown(text, offset):
 out=[];pos=[];i=0
 while i<len(text):
  if text.startswith("'''",i):i+=3;continue
  if text.startswith('{{',i):
   z=bounds(text,i);mid=text.find('|',i+2,z);kind=text[i+2:mid] if mid!=-1 else text[i+2:z-2]
   if kind=='gap' and mid==-1:i=z;continue
   assert kind in ('YL','blue','red','quote','另'),(kind,text[i:z]);e=text.find('|',mid+1,z-2) if kind in ('YL','另') else -1;e=z-2 if e==-1 else e
   a,b=shown(text[mid+1:e],offset+mid+1);out+=a;pos+=b;i=z;continue
  if text.startswith('[[',i):
   z=text.index(']]',i+2);mid=text.rfind('|',i+2,z);a=mid+1 if mid!=-1 else i+2;out+=text[a:z];pos+=range(offset+a,offset+z);i=z+2;continue
  if text.startswith('-{',i):
   z=text.index('}-',i+2);out+=text[i+2:z];pos+=range(offset+i+2,offset+z);i=z+2;continue
  out.append(text[i]);pos.append(offset+i);i+=1
 return ''.join(out),pos

def project_line(line, offset=0):
 if line.startswith('{{quote|') and line.count('{{')>line.count('}}'):
  return project_line(line[8:],offset+8)
 if line.endswith('}}') and line.count('}}')>line.count('{{'):
  return project_line(line[:-2],offset)
 i=0;lo=0;out=[];pos=[];notes=[]
 while i<len(line):
  if not line.startswith('{{',i):i+=1;continue
  z=bounds(line,i)
  if line.startswith('{{*|',i):
   a,b=shown(line[lo:i],offset+lo);out+=a;pos+=b;notes.append((i+4,z-2,len(pos)));lo=z
  i=z
 a,b=shown(line[lo:],offset+lo);out+=a;pos+=b
 return ''.join(out),pos,notes
