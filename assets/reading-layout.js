/** Explicit layout only: never infer an archive from similar text. */
export function chapterReadingLayout(chapter) {
  if (!chapter.reading_layout) return {primary:chapter.paragraphs,archival:[]};
  const layout=chapter.reading_layout, by=new Map(chapter.paragraphs.map(p=>[p.id,p]));
  const ids=[...layout.primary_paragraph_ids,...layout.archival_excerpts.map(a=>a.paragraph_id)];
  if(layout.version!==1 || by.size!==chapter.paragraphs.length || ids.length!==by.size || new Set(ids).size!==ids.length || ids.some(id=>!by.has(id))) throw Error('閱讀版面段落分割無效');
  return {primary:layout.primary_paragraph_ids.map(id=>by.get(id)),archival:layout.archival_excerpts.map(entry=>({entry,paragraph:by.get(entry.paragraph_id)}))};
}
export function revealSourceTarget(root,chapter,params) {
  const paragraphs=new Map(chapter.paragraphs.map(p=>[p.id,p]));
  const mentions=new Map(chapter.paragraphs.flatMap(p=>p.mentions.map(m=>[m.id,p.id])));
  let passage=params.get('passage'),mention=params.get('mention');
  if (!mention && mentions.has(passage)) {mention=passage;passage=mentions.get(mention);}
  if (mention && (!mentions.has(mention) || (passage && passage!==mentions.get(mention)))) return null;
  if (mention) passage=mentions.get(mention);
  if (!paragraphs.has(passage)) return null;
  const id=mention || passage;
  const node=[...root.querySelectorAll('[id]')].find(n=>n.id===id);
  if(!node)return null;
  for(let parent=node.parentElement;parent && parent!==root;parent=parent.parentElement) if(parent.tagName==='DETAILS')parent.open=true;
  node.scrollIntoView();
  return node;
}
