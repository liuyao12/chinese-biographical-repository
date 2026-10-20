import unittest,copy
from scripts.houhan_text_layers import LAYERS,layer_errors
class HouhanTextLayers(unittest.TestCase):
 def paragraph(self,layer):
  a,e=LAYERS[layer];return {'source_position':{'source_layer':{'witness_appended_lixian_note':'lixian_commentary','witness_appended_liuban_collation':'liu_ban_collation','witness_appended_qing_siku_collation':'qing_siku_collation_appendix'}[layer]},'text_layer':layer,'text':'○劉攽曰案正文多一者字','layer_attribution':{'attributed_author':a,'period':e,'received_authority':'固定見證原署注','quotation_dependencies':[],'human_reviewed':False,'image_verified':False,'scope':'independent_volume_appendix'}}
 def test_three_layers(self):
  for layer in LAYERS:self.assertEqual(layer_errors(self.paragraph(layer)),[])
 def test_wrong_author_rejected(self):
  p=self.paragraph('witness_appended_lixian_note');p['layer_attribution']['attributed_author']='裴松之';self.assertTrue(layer_errors(p))
 def test_qing_not_received_body(self):
  p=self.paragraph('witness_appended_qing_siku_collation');p['layer_attribution']['scope']='received_body';self.assertTrue(layer_errors(p))
 def test_song_signature_preserved(self):
  p=self.paragraph('witness_appended_liuban_collation');p['text']='案正文多一者字';self.assertTrue(layer_errors(p))
 def test_no_false_review(self):
  p=self.paragraph('witness_appended_lixian_note');p['layer_attribution']['human_reviewed']=True;self.assertTrue(layer_errors(p))
 def test_other_tang_annotation_not_lixian(self):
  p=self.paragraph('witness_appended_lixian_note');p['source_position']['source_layer']='other_tang_annotation';self.assertTrue(layer_errors(p))
 def test_legacy_unchanged(self):self.assertEqual(layer_errors({'text_layer':'witness_appended_pei_songzhi_note'}),[])
