// Consume already source-validated brother namespace data; never construct a parent.
export async function explicitBrothersNamespace(person, load) {
  const row=person?.assembled_identity, g=row?.collateral_root_group, order=g?.relative_age;
  const ids=g?.root_person_ids, ns=row?.namespace_id;
  if (g?.type!=='explicit_received_brothers_parent_unidentified' || row.root_person_id!==null
      || g.status!=='contextual_provisional' || g.human_reviewed!==false
      || g.common_parent_person_id!==null || g.common_parent_name!==null
      || g.common_parent_registered!==false || g.biological_verification!==false
      || typeof ns!=='string' || !/^[a-z0-9]{3}_[a-z0-9]{3}_[a-z0-9]{3}$/.test(ns)
      || !Array.isArray(ids) || ids.length!==2 || new Set(ids).size!==2
      || ids.some(id=>typeof id!=='string'||!id.startsWith(ns+'_')||id.length!==ns.length+2)
      || order?.operator!=='lt' || order.scope!=='siblings'
      || order.older_ordinal!==null || order.younger_ordinal!==null
      || order.older_person_id===order.younger_person_id
      || !ids.includes(order.older_person_id) || !ids.includes(order.younger_person_id)
      || row.namespace_entry_person_id!==order.older_person_id
      || typeof g.brother_assertion_id!=='string' || !g.brother_assertion_id
      || !Array.isArray(g.references) || g.references.length!==1
      || g.references[0]?.assertion_id!==g.brother_assertion_id
      || typeof g.references[0]?.quote!=='string' || !g.references[0].quote
      || !Array.isArray(g.name_record_ids) || g.name_record_ids.length!==2
      || new Set(g.name_record_ids).size!==2 || g.name_record_ids.some(x=>typeof x!=='string'||!x)
      || typeof g.rationale!=='string' || !g.rationale) return null;
  const roots=await Promise.all(ids.map(async id=>{
    let data;try {data=await load(id);} catch {data=null;}
    return {id,label:data?.label||id,...(data?{person:data}:{unavailable:true}),
      role:'source_attested',inference_note:g.rationale,evidence:g.references};
  }));
  return {namespace_id:ns,entry_person_id:row.namespace_entry_person_id,roots,
    common_parent_person_id:null,namespace_kind:g.type,
    qualification:'source_attested_brothers_parent_unidentified',
    inference_note:g.rationale,evidence:g.references};
}
