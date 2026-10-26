/** Display metadata only. Never derive a chapter title by trimming a source/selection title. */
const text = value => typeof value === 'string' ? value.trim() : '';
export function sourceCaption(workTitle, chapterTitle = '') {
 const work=text(workTitle), chapter=text(chapterTitle);
 return work ? `《${work}${chapter?'・'+chapter:''}》` : '來源';
}
export function chapterDirectoryMap(index) {
 if(index?.schema_version!==1 || !Array.isArray(index.works))throw Error('Invalid chapter directory');
 const result=Object.create(null);
 for(const work of index.works){
  if(!/^w-[a-z0-9-]+$/.test(work.work_id) || !text(work.title) || !Array.isArray(work.books) || Object.hasOwn(result,work.work_id))throw Error('Invalid directory work');
  const books=Object.create(null);
  for(const book of work.books){
   if(!/^b-[a-z0-9-]+$/.test(book.book_id) || Object.hasOwn(books,book.book_id) || (book.citation_title!=null && typeof book.citation_title!=='string') || (book.title!=null && typeof book.title!=='string'))throw Error('Invalid directory book');
   books[book.book_id]={citation_title:text(book.citation_title),title:text(book.title)};
  }
  result[work.work_id]={title:text(work.title),books};
 }
 return result;
}
export async function loadChapterDirectory(fetcher=globalThis.fetch){
 try{const response=await fetcher('data/corpus/chapter-directory.json');return response.ok?chapterDirectoryMap(await response.json()):Object.create(null);}catch{return Object.create(null);}
}
const directoryWork=(record,directory)=>record?.work_id && Object.hasOwn(directory || {},record.work_id)?directory[record.work_id]:null;
const directoryBook=(record,directory)=>{const work=directoryWork(record,directory);return work?.books && Object.hasOwn(work.books,record.book_id)?work.books[record.book_id]:null;};
export function sourceChapterTitle(record,directory={}) {
 const book=directoryBook(record,directory);
 return book?.citation_title || book?.title || text(record?.book_title) || (Number.isInteger(record?.number)&&record.number>0?`卷${record.number}`:'');
}
export function sourceCitation(record,directory={},workTitles={}) {
 const work=directoryWork(record,directory),book=directoryBook(record,directory);
 const registered=record?.work_id && Object.hasOwn(workTitles,record.work_id)?workTitles[record.work_id]:null;
 const workTitle=work?.title || text(typeof registered==='string'?registered:registered?.title) || text(record?.work_title);
 const locator=book?.title || text(record?.book_title) || (Number.isInteger(record?.number)&&record.number>0?`卷${record.number}`:'');
 return sourceCaption(workTitle,book?.citation_title)+(locator?' · '+locator:'');
}
