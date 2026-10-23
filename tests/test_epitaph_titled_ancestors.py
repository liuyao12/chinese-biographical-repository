import unittest,copy,hashlib,re
from scripts.epitaph_titled_ancestors import valid,KIND

def fixture():
 t='故將軍沈君墓誌銘。君姓沈，諱寧，字子安，廣陵人也。江州府君之孫，某郡簡公之第三子。其餘敘事保全。'
 values={'surname':'沈','head':'寧','zi':'子安','grandfather':'江州府君','grandchild':'孫','father':'某郡簡公','son':'第三子'}
 ids={'head':'one','surname':'one','zi':'one','grandchild':'one','son':'one','father':'two','grandfather':'three'}
 ms=[]
 for k,v in values.items():
  start=t.index(v,t.index('君姓') if k=='surname' else 0);ms.append(dict(id=k,kind='person',person_id=ids[k],surface=v,start=start,end=start+len(v)))
 c=dict(id='chapter',work_id='work',book_id='book',source_id='source',source={'transcription_witness':{'kind':'institutional_database_epitaph_transcription','original_stone_or_rubbing_image_verified':False}},paragraphs=[dict(id='paragraph',text=t,text_layer='epitaph_as_modernly_transcribed',mentions=ms)])
 b=dict(kind=KIND,paragraph_id='paragraph',source_id='source',paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),roles={k:k for k in values})
 aa=[]
 for pred,term,role in [('father','son','father'),('grandfather','grandchild','grandfather')]:
  q=dict(source_term=values[term],source_clause_binding=b)
  if pred=='father':q['birth_order']=dict(parent_person_id='two',scope='sons_of_parent',ordinal=3,position='unspecified',interpretation_status='source_attested')
  else:q.update(lineage='paternal',generation_difference=-2)
  e={k:c[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id='chapter',paragraph_id='paragraph',quote=t,subject_person_mention_id=term,object_person_mention_id=role)
  aa.append(dict(subject_person_id='one',object_person_id=ids[role],predicate=pred,qualifiers=q,status='source_attested',human_reviewed=False,evidence=[e]))
 return c,[dict(record_type='person_assertion_set',assertions=aa)],b
class Contract(unittest.TestCase):
 def test_positive(self):valid(*fixture())
 def bad(self,mut):
  c,rs,b=fixture();mut(c,rs,b)
  with self.assertRaises((AssertionError,KeyError,ValueError,StopIteration)):valid(c,rs,b)
 def test_reverse(self):self.bad(lambda c,r,b:r[0]['assertions'][0].update(subject_person_id='two',object_person_id='one'))
 def test_wrong_parent(self):self.bad(lambda c,r,b:r[0]['assertions'][0].update(object_person_id='three'))
 def test_mother(self):self.bad(lambda c,r,b:r[0]['assertions'][0].update(predicate='mother'))
 def test_adoptive(self):self.bad(lambda c,r,b:r[0]['assertions'][0].update(predicate='adoptive_father'))
 def test_ordinal(self):self.bad(lambda c,r,b:r[0]['assertions'][0]['qualifiers']['birth_order'].update(ordinal=6))
 def test_absolute_eldest(self):self.bad(lambda c,r,b:r[0]['assertions'][0]['qualifiers']['birth_order'].update(position='eldest'))
 def test_distance(self):self.bad(lambda c,r,b:r[0]['assertions'][1]['qualifiers'].update(generation_difference=-1))
 def test_offset(self):self.bad(lambda c,r,b:c['paragraphs'][0]['mentions'][2].update(start=1))
 def test_cut_quote(self):self.bad(lambda c,r,b:r[0]['assertions'][0]['evidence'][0].update(quote='某郡簡公之第三子'))
 def test_wrong_source(self):self.bad(lambda c,r,b:r[0]['assertions'][0]['evidence'][0].update(source_id='other'))
 def test_wrong_subject_anchor(self):self.bad(lambda c,r,b:r[0]['assertions'][0]['evidence'][0].update(subject_person_mention_id='grandchild'))
 def test_extra_inferred_edge(self):self.bad(lambda c,r,b:r[0]['assertions'].append(copy.deepcopy(r[0]['assertions'][0])))
 def test_full_intro_required(self):
  def f(c,r,b):
   p=c['paragraphs'][0];p['text']=p['text'].replace('君姓','君非');b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  self.bad(f)
 def test_negation(self):
  def f(c,r,b):
   p=c['paragraphs'][0];p['text']=p['text'].replace('之第三子','非第三子');b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  self.bad(f)
 def test_same_name_different_id(self):self.bad(lambda c,r,b:c['paragraphs'][0]['mentions'][3].update(person_id='another'))
if __name__=='__main__':unittest.main()
