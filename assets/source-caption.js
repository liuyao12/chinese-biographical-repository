/** Readable citation only: stored source titles stay untouched. */
export function sourceCaption(workTitle, chapterTitle) {
 const work=typeof workTitle==='string'&&workTitle?workTitle:'史記';
 const original=typeof chapterTitle==='string'?chapterTitle:'';
 const prefix=`《${work}》`;
 const chapter=original.startsWith(prefix)?original.slice(prefix.length):original;
 return chapter?`《${work}·${chapter}》`:`《${work}》`;
}
