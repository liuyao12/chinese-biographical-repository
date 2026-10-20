import copy,unittest
from scripts.profile_occurrence_counts import profile_occurrences

def fixture():
 ms=[{'id':i,'chapter_id':'c','paragraph_id':p,'start':0,'end':1}for i,p in [('old','old-p'),('new','new-p')]]
 ps=[{'id':p,'text':'甲','work_id':'w','book_id':'b','chapter_id':'c','source_id':'s'}for p in ['old-p','new-p']]
 return {'mentions':ms,'table_occurrences':[],'passages':ps,'sources':[{'source_id':'s'}],'most_mentioned_source_ids':['s'],'source_mention_summary':[{'mention_count':1,'paragraph_occurrence_count':1,'table_occurrence_count':0,'occurrence_groups':[{'canonical_mention_id':'new','mention_ids':['old','new'],'kind':'paragraph'}]}]}
class ProfileOccurrenceCounts(unittest.TestCase):
 def test_counts_and_original_backlinks(self):
  row=profile_occurrences(fixture(),{'c':{'number':1,'title':'篇'}},{'w':'書'})[0];self.assertEqual((row['count'],row['raw_count'],row['duplicate_count']),(1,2,1));self.assertEqual(row['paragraph_id'],'new-p');self.assertEqual(row['paragraph_ids'],['new-p','old-p']);self.assertEqual(row['mention_ids'],['old','new'])
 def test_missing_membership_rejected(self):
  b=fixture();b['source_mention_summary'][0]['occurrence_groups']=[]
  with self.assertRaises(ValueError):profile_occurrences(b,{}, {})
 def test_duplicate_membership_rejected(self):
  b=fixture();b['source_mention_summary'][0]['occurrence_groups']*=2
  with self.assertRaises(ValueError):profile_occurrences(b,{}, {})
 def test_unknown_chapter_rejected(self):
  with self.assertRaises(ValueError):profile_occurrences(fixture(),{}, {})
if __name__=='__main__':unittest.main()
