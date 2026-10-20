// Display-only consensus. Original records and every source stay intact.
const text = value => typeof value === 'string' && value.trim() ? value.trim() : null;
export function summarizeNameComponents(value) {
  const records = Array.isArray(value) ? value.filter(x => x && typeof x === 'object' && !Array.isArray(x)) : [];
  if (!records.length) return {names:null, records, conflicts:[], coreConflict:false, canHead:false};
  const names = {}, conflicts = [];
  const fields = ['surname','ming','zi','xiaozhi','hao','former_ming','full_name'];
  for (const field of fields) {
    const values = [...new Set(records.map(x => text(x[field])).filter(Boolean))];
    if (values.length === 1) names[field] = values[0];
    else if (values.length > 1) conflicts.push({field, values});
  }
  const clans = [...new Set(records.map(x => text(x.clan_style?.value)).filter(Boolean))];
  if (clans.length === 1) names.clan_style = {value:clans[0]};
  else if (clans.length > 1) conflicts.push({field:'clan_style', values:clans});
  // Individually non-conflicting fields must not combine into a different full name.
  const derived = names.surname && names.ming ? names.surname + names.ming : null;
  if (names.full_name && derived && names.full_name !== derived) {
    conflicts.push({field:'full_name', values:[names.full_name, derived]});
    delete names.full_name;
  }
  if (names.clan_style && names.surname && names.clan_style.value !== names.surname + '氏') {
    conflicts.push({field:'clan_style', values:[names.clan_style.value, names.surname + '氏']});
    delete names.clan_style;
  }
  const coreConflict = conflicts.some(x => ['surname','ming','full_name','clan_style'].includes(x.field));
  const additional = records.flatMap(x => Array.isArray(x.additional_names) ? x.additional_names : []).map(text).filter(Boolean);
  // Only an explicitly typed courtesy name justifies this exact display deduplication.
  names.additional_names = [...new Set(additional.filter(x => (!names.zi || x !== '字' + names.zi) && (!names.xiaozhi || x !== '小字' + names.xiaozhi)))];
  // Preserve the established single-source title display; never promote multi-source
  // titles (possibly from different periods) into a generic name/title consensus.
  if (records.length === 1 && text(records[0].title)) names.title = text(records[0].title);
  const canHead = !coreConflict && (records.length === 1 || Boolean(names.ming || names.full_name || names.clan_style?.value));
  return {names, records, conflicts, coreConflict, canHead};
}

// Generic source forms are not promoted to personal aliases. Only the explicit
// additional_names and typed personal-name fields enter the main alias row.
export function nameAliases(names) {
  if (!names) return [];
  const typed = ['zi','xiaozhi','hao','former_ming'].filter(kind => text(names[kind])).map(kind => ({kind, value:text(names[kind])}));
  const typedValues = new Set(typed.map(x => x.value));
  const raw = (names.additional_names || []).filter(value => !typedValues.has(value)).map(value => ({kind:null,value}));
  const result = [], seen = new Set();
  for (const item of [...raw,...typed]) {
    const key = JSON.stringify([item.kind,item.value]);
    if (!seen.has(key)) {seen.add(key);result.push(item);}
  }
  return result;
}
