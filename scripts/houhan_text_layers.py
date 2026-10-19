"""後漢書見證附載三層資格；不把轉引當獨立原著。"""
LAYERS={
 'witness_appended_lixian_note':('李賢','唐'),
 'witness_appended_liuban_collation':('劉攽','宋'),
 'witness_appended_qing_siku_collation':('四庫館臣','清')}
def layer_errors(p):
 layer=p.get('text_layer')
 if layer not in LAYERS:return []
 meta=p.get('layer_attribution',{});author,era=LAYERS[layer];errors=[]
 expected={'witness_appended_lixian_note':'lixian_commentary','witness_appended_liuban_collation':'liu_ban_collation','witness_appended_qing_siku_collation':'qing_siku_collation_appendix'}[layer]
 if p.get('source_position',{}).get('source_layer')!=expected:errors.append('史料層與固定投影歸屬不符')
 if meta.get('attributed_author')!=author or meta.get('period')!=era:errors.append('史料層作者／時代不符')
 if meta.get('human_reviewed') is not False or meta.get('image_verified') is not False:errors.append('史料層覆核資格不得冒填')
 if not meta.get('received_authority') or not isinstance(meta.get('quotation_dependencies'),list):errors.append('史料層署注／轉引範圍缺失')
 if layer=='witness_appended_liuban_collation' and not p.get('text','').startswith('○劉攽曰'):errors.append('劉攽層須保留原署名')
 if layer=='witness_appended_qing_siku_collation' and meta.get('scope')!='independent_volume_appendix':errors.append('清考證不得冒傳文')
 return errors
