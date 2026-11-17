import {sourceCitation} from './source-caption.js';
import {tableOccurrenceURL} from './cbr-person.js';
import {chapterURL, profileSourceContext} from './corpus-reader.js';

export function profileReturnLink(person, context) {
  const tableId = context.get('table');
  const tableOccurrence = tableId && (person.table_occurrences || []).find(x => x.table_id === tableId);
  if (tableOccurrence) {
    const href = tableOccurrenceURL({...tableOccurrence, cell_id:context.get('cell') || undefined,
      axis:context.get('axis') || undefined});
    if (href) return {href, text:'回到' + tableOccurrence.title + ' →'};
  }

  const workId = context.get('work');
  if (!workId || workId === 'w-shiji') {
    const chapter = Number(context.get('chapter'));
    const shijiOccurrence = (person.occurrences || []).find(x => x.number === chapter);
    if (shijiOccurrence && chapter > 0) {
      const passage = context.get('passage');
      const prefix = 'c-shiji-' + String(chapter).padStart(3, '0') + '-';
      const validPassage = passage?.startsWith(prefix) && /^[a-z0-9-]+:p\\d{3}$/.test(passage.slice(prefix.length));
      return {
        href:chapterURL(chapter, shijiOccurrence.category, validPassage ? passage : shijiOccurrence.paragraph_id),
        text:'回到' + sourceCitation({...shijiOccurrence, work_id:'w-shiji', work_title:'史記'},
          person.source_chapter_directory, person.source_work_titles) + ' →'
      };
    }
  }

  const otherSource = profileSourceContext(person, context);
  if (otherSource) return otherSource;
  return {href:'cbr.html', text:'返回 CBR 人物目錄 →'};
}
