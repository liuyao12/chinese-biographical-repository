// Native table source links. Source metadata is explicit; a volume number is never a work.
export function nativeTableURL(x) {
 const match=/^([a-z][a-z0-9-]*?)-(\d{3}[a-z]?)$/.exec(x?.table_id || '');
 if(!match)return '';
 const [,slug,number]=match,work='w-'+slug,book='b-'+slug+'-'+number,chapter='table-chapter-'+slug+'-'+number;
 for(const [key,value]of [['work_id',work],['book_id',book],['chapter_id',chapter]])if(x[key]!==undefined&&x[key]!==value)return '';
 if(slug!=='shiji'&&[x.work_id,x.book_id,x.chapter_id].some(v=>typeof v!=='string'||!v))return '';
 const cell=x.cell_id || x.table_cell_id || '';
 const p=slug==='shiji'?new URLSearchParams({chapter:String(Number(number)),category:'biao'}):new URLSearchParams({work,book,chapter,table:x.table_id});
 if(cell)p.set('cell',cell);
 if(['horizontal','vertical'].includes(x.axis))p.set('axis',x.axis);
 return(slug==='shiji'?'shiji.html':'reader.html')+'#'+p;
}
export function nativeProfileURL(personId,source) {
 if(!nativeTableURL(source))return '';
 const p=new URLSearchParams();
 for(const [to,from]of [['work','work_id'],['book','book_id'],['chapter','chapter_id'],['table','table_id']])if(source[from])p.set(to,source[from]);
 const cell=source.cell_id||source.table_cell_id;if(cell)p.set('cell',cell);
 if(['horizontal','vertical'].includes(source.axis))p.set('axis',source.axis);
 return'person.html?'+p+'#'+encodeURIComponent(personId);
}
export function nativeProfileReturn(person,params) {
 const matches=(person.table_occurrences||[]).filter(x=>x.work_id===params.get('work')&&x.book_id===params.get('book')&&x.chapter_id===params.get('chapter')&&x.table_id===params.get('table'));
 if(!matches.length)return null;
 const chosen=matches.find(x=>(x.cell_id||x.table_cell_id)===params.get('cell'))||matches[0];const href=nativeTableURL({...chosen,axis:params.get('axis')});
 return href?{href,text:'回到'+chosen.title+' →'}:null;
}
