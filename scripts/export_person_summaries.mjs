import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL, fileURLToPath} from 'node:url';
const CODE_ROOT = fileURLToPath(new URL('..', import.meta.url));
const safe=id=>typeof id==='string'&&id.length>0&&id!=='.'&&id!=='..'&&!/[\\/\u0000-\u001f]/.test(id);
export async function activeIds(root) {
  const index=JSON.parse(await fs.readFile(path.join(root,'data/corpus/profiles/index.json'),'utf8'));
  if(!Array.isArray(index.profiles))throw Error('invalid profile index');
  const ids=index.profiles.map(p=>p.id);
  if(ids.some(id=>!safe(id))||new Set(ids).size!==ids.length)throw Error('unsafe/duplicate profile ID');
  return ids;
}
export async function generator(root) {
 const active = new Set(await activeIds(root));
 const mod=async name=>import(pathToFileURL(path.join(CODE_ROOT,'assets',name)).href);
 const [
   {traceFamily},
   {summarizeNameComponents, nameAliases},
   {summarizeLife, ageLabel, lifeYearLabel, sourceDateLabel}
 ] = await Promise.all(
   ['person-family.js', 'name-components.js', 'person-life.js'].map(mod)
 );
 let profileTitlePreference=()=>null;
 let titleHelperExists=true;
  try{await fs.access(path.join(CODE_ROOT,'assets/profile-title.js'));
  }catch(e){if(e.code==='ENOENT')titleHelperExists=false;
  else throw e;
}
 if(titleHelperExists)profileTitlePreference=(await mod('profile-title.js')).profileTitlePreference;
 const cache=new Map();
 async function load(id) {
if(!safe(id))throw Error('unsafe profile ID');
if(!active.has(id))throw Error('inactive profile ID: '+id);
if(!cache.has(id))cache.set(id,fs.readFile(path.join(root,'data/corpus/profiles',id+'.json'),'utf8').then(JSON.parse));
return cache.get(id);
}
 const pick=(o,keys)=>Object.fromEntries(keys.filter(k=>o?.[k]!==undefined).map(k=>[k,structuredClone(o[k])]));
 function familyEntry(x) {
   const entry = pick(x, ['id', 'label', 'role', 'inference_note', 'cycle', 'unavailable', 'marriage_status']);
   if (x.ancestry_paths?.length) {
     entry.route_qualification = [...new Set(x.ancestry_paths.map(p => p.qualification))];
     entry.ancestry_cycle = x.ancestry_paths.some(p => p.cycle);
     entry.ancestry_unavailable = x.ancestry_paths.some(p => p.unavailable);
   }
   return entry;
 }
 async function project(p) {
  const name = summarizeNameComponents(p.name_components, p.preferred_name_component_readings);
  const title = profileTitlePreference(p);
  const life = summarizeLife(p);
  const traced = await traceFamily(p, load);
  // traceFamily deliberately catches loader errors for missing data. An inactive
  // endpoint is different: never export a clickable retired identity.
  function assertActiveFamily(value, key = '') {
    if (Array.isArray(value)) {
      for (const child of value) assertActiveFamily(child, key);
    } else if (value && typeof value === 'object') {
      if (typeof value.id === 'string' && !active.has(value.id)
          && ('label' in value || 'person' in value)) {
        throw Error('inactive family endpoint: ' + value.id);
      }
      for (const [field, child] of Object.entries(value)) {
        if (['candidate_person_ids', 'root_person_ids'].includes(field)
            && child.some(id => !active.has(id))) {
          throw Error('inactive family candidate');
        }
        if (field !== 'evidence' && field !== 'references' && field !== 'person') {
          assertActiveFamily(child, field);
        }
      }
    }
  }
  assertActiveFamily(traced);

  const family={ancestors:traced.ancestors.map(xs=>xs.map(familyEntry))};
  for(const k of ['mother','spouses','children','adoptive_father','adopted_children'])if(traced[k]?.length)family[k]=traced[k].map(familyEntry);
  if(traced.child_order_conflicts?.length)family.child_order_conflicts=traced.child_order_conflicts.map(x=>Array.isArray(x)?[...x]:pick(x,['kind','type','message','reason','person_ids','older_person_id','younger_person_id']));
  if(traced.unresolved_spouse_groups?.length)family.unresolved_spouse_groups=traced.unresolved_spouse_groups.map(x=>pick(x,['id','status','rationale','same_person','distinct_people','common_person_id','candidate_person_ids']));
  if(traced.family_namespace)family.family_namespace={...pick(traced.family_namespace,['namespace_kind','qualification','inference_note','common_parent_person_id']),roots:traced.family_namespace.roots.map(familyEntry)};
  const event=e=>{const d=(p.life_event_date_decisions||[]).find(x=>x.candidate_event_ids.includes(e.id));
return {year_label:lifeYearLabel(e),date_expression:sourceDateLabel(e),...(d?{choice:d.status==='unresolved'?'unresolved':d.preferred_event_id===e.id?'preferred':'alternative'}:{}),...pick(e,['status','reporting_status','prospective'])};
};
  const out={
 schema_version:1,
 record_type:'derived_person_summary',
 id:p.id,
 label:p.label,
 full_profile_path:'data/corpus/profiles/'+encodeURIComponent(p.id)+'.json',
 additional_names:name.names?nameAliases(name.names):[],...(title?{title_preference:pick(title,['title','mode','status'])}:{}),
 life_summary:{birth:life.birth.map(event),death:life.death.map(event),ages:life.ages.map(x=>({...event(x),label:ageLabel(x),approximate:['adjacent_age_numbers','quoted_kin_age_designation'].includes(x.approximation?.kind),...pick(x,['counting','reporting_status']),...(x.age_context?{context:x.age_context.kind}:{})}))},
 family
 };
  if(p.historicity)out.historicity=typeof p.historicity==='string'?p.historicity:pick(p.historicity,['status','kind','classification','label','note']);
  if(p.unresolved_identity_cases?.length)out.identity_unresolved=true;
  if(p.identity_distinctions?.length)out.identity_distinctions_present=true;
  if(p.addresses?.length)out.addresses=p.addresses.map(x=>pick(x,['kind','place','place_name','source_term','label','status','interpretation_note']));
  const names=name.names,partial=Boolean(names&&!names.clan_style?.value&&!names.full_name&&names.ming&&!names.surname&&p.label?.endsWith(names.ming)&&p.label.length>names.ming.length),personal=names?.clan_style?.value||names?.full_name||(names?`${names.surname||''}${names.ming||''}`:'');
  out.heading=title&&names&&name.canHead&&!partial&&personal?`${title.title} ${personal}`:partial?p.label:names&&name.canHead?`${names.title||''} ${personal}`.trim()||p.label:p.label;
  out.aliases=out.additional_names;
delete out.additional_names;
  out.jiguan=[...new Set((p.addresses||[]).filter(a=>(p.person_ids||[p.id]).includes(a.person_id)&&['biographical_origin','native_place'].includes(a.relation)).map(a=>a.place?.source_name).filter(Boolean))];
delete out.addresses;
  out.life=out.life_summary;
delete out.life_summary;
for(const rows of [out.life.birth,out.life.death,out.life.ages])for(const row of rows){row.source_date=row.date_expression;
delete row.date_expression;
}
  out.qualifications=[];
if(name.coreConflict)out.qualifications.push('姓名異說');
if(out.identity_unresolved)out.qualifications.push('身份未決');
if(p.relative_birth_order_decisions?.length)out.qualifications.push('排行有異說');
if(p.review==='source_local_candidate')out.qualifications.push('來源局部候選');
  delete out.identity_unresolved;
delete out.identity_distinctions_present;
  const own = new Set(p.person_ids || [p.id]);
  for (const address of p.addresses || []) {
    if (!own.has(address.person_id) || address.status !== 'source_attested'
        || !['birth_place', 'death_place'].includes(address.relation)
        || !address.normalized_date) continue;
    const year = lifeYearLabel(address);
    if (!year) continue;
    const row = event(address);
    row.source_date = row.date_expression;
    delete row.date_expression;
    out.life[address.relation === 'birth_place' ? 'birth' : 'death'].push(row);
  }
  function compactDates(rows) {
    const visible = rows.filter(row => row.year_label || row.source_date);
    const dated = visible.some(row => row.year_label);
    const groups = new Map();
    for (const row of visible) {
      if (dated && !row.year_label) continue;
      const key = JSON.stringify([row.year_label || '', row.choice || '']);
      if (!groups.has(key)) groups.set(key, {...row, source_date: []});
      const target = groups.get(key);
      if (row.source_date && !target.source_date.includes(row.source_date)) {
        target.source_date.push(row.source_date);
      }
    }
    return [...groups.values()].map(row => ({...row, source_date:row.source_date.join('／')}));
  }
  out.life.birth = compactDates(out.life.birth);
  out.life.death = compactDates(out.life.death);


out.life.ages=out.life.ages.filter(e=>e.label);
  return out;
 }
 return {load,project};
}
export async function plan(root, ids = undefined) {
  ids??=await activeIds(root);
  if(ids.some(id=>!safe(id))||new Set(ids).size!==ids.length)throw Error('unsafe/duplicate ID');
  const g=await generator(root),out=new Map();
  for(const id of ids){const p=await g.load(id);
  if(p.id!==id)throw Error('profile ID differs from index');
  out.set('data/corpus/summaries/'+id+'.json',JSON.stringify(await g.project(p))+'\n');
  }return out;
}
export async function write(root) {
  const outputs=await plan(root),directory=path.join(root,'data/corpus/summaries');
  await fs.mkdir(directory,{recursive:true});
  for(const[relative,text]of outputs)await fs.writeFile(path.join(root,relative),text);
  const active=new Set([...outputs.keys()].map(x=>path.basename(x)));
  for(const filename of await fs.readdir(directory))if(filename.endsWith('.json')&&!active.has(filename))await fs.unlink(path.join(directory,filename));
  return {summaries:outputs.size};
}
export async function check(root) {
  const expected = await plan(root);
  const directory = path.join(root, 'data/corpus/summaries');
  const actual = (await fs.readdir(directory)).filter(name => name.endsWith('.json'));
  const names = new Set([...expected.keys()].map(name => path.basename(name)));
  if (actual.length !== names.size || actual.some(name => !names.has(name)))
    throw Error('person summary index differs from current profiles');
  for (const [relative, text] of expected) {
    if (await fs.readFile(path.join(root, relative), 'utf8') !== text)
      throw Error('stale person summary: ' + relative);
  }
  return {summaries: expected.size};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const checking = process.argv[2] === '--check';
  const root = path.resolve(process.argv[checking ? 3 : 2] || '.');
  console.log(JSON.stringify(await (checking ? check(root) : write(root))));
}
