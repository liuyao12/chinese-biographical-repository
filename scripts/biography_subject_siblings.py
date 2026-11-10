"""Validate sibling-list anchors against the biography subject."""
def biography_subject_siblings_valid(assertion, paragraphs):
 try:
  q=assertion["qualifiers"];b=q["source_clause_binding"];e,=assertion["evidence"];cid,p=paragraphs[e["paragraph_id"]];t=p["text"];ms={m["id"]:m for m in p["mentions"]}
  if assertion.get("predicate")!="brother" or b.get("kind")!="biography_subject_named_siblings" or e.get("chapter_id")!=cid or e.get("quote")!=t:return False
  def anchor(mid):
   m=ms[mid]
   if m.get("kind")!="person" or not m.get("person_id") or type(m.get("start"))is not int or type(m.get("end"))is not int or t[m["start"]:m["end"]]!=m["surface"]:raise ValueError()
   return m
  head=anchor(b["biography_subject_person_mention_id"]);elder=anchor(b["older_brother_person_mention_id"]);mids=b["younger_brother_person_mention_ids"]
  if len(mids)!=2:return False
  young=[anchor(x)for x in mids]
  if head["start"]!=0 or head["person_id"]!=assertion["subject_person_id"]:return False
  term="兄"+elder["surface"]+"，弟"+young[0]["surface"]+"、"+young[1]["surface"];start=b["start"];end=b["end"]
  if t[start:end]!=term or q["source_term"]!=term:return False
  obj=anchor(e["object_person_mention_id"])
  if obj["person_id"]!=assertion["object_person_id"] or e.get("subject_person_mention_id")!=head["id"]:return False
  o=q["relative_birth_order"];older,younger=(obj["person_id"],head["person_id"])if obj["id"]==elder["id"]else(head["person_id"],obj["person_id"])
  return o=={"older_person_id":older,"younger_person_id":younger,"operator":"lt","older_ordinal":None,"younger_ordinal":None,"scope":"siblings"}
 except (KeyError,TypeError,ValueError,StopIteration,IndexError):return False
