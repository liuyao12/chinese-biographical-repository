# 資料格式 0.1

JSON 使用 UTF-8；中文為繁體。`record_type` 區分記錄。`records.schema.json` 描述核心格式；`scripts/validate.py` 另外檢查跨檔引用、精確引句、指紋與決定。

## 史料 `source`

一項作品或一篇史料單元搭配本次實際讀到的見證。`bibliography` 說明作品與位置，`witness` 說明數位轉錄或論文，`images` 列相關影像；底本影像與傳世文本不可混稱。未讀圖的目錄連結不代表完成影像校勘。

`text.segments` 為具穩定識別碼的段落。`extent` 區分全篇、節錄與短引文／摘要。`sha256` 計算各段 `text` 以兩個換行接合後的 UTF-8 指紋，不包含 JSON 格式或末尾換行。段落新增與修改必須保持引用一致。原文保留而不默改；後續訂正可改版本，Git 保存歷史。

`quality.status: text_checked` 表示核閱數位正文，不保證史實正確；`image_verified` 必須據實填寫。`contribution` 記錄代理與方法，未知模型版本為 `null`。

## 陳述 `assertion`

`subject` 為 `source-id#local-mention`，不是全庫人物 ID。`predicate: name` 記人名／氏稱；名字由姓氏語境補足時須說明。其他詞包括 `father`、`mother`、`son`、`spouse`、`grandfather`、`great_grandfather`、`ancestor`、`collateral_ancestor`、`maternal_uncle`、`maternal_cousin`、`son_in_law`、`brother`、`death_date`、`death_year`、`courtesy_name` 等。

`object.kind` 為 `mention` 或 `literal`。每項 `evidence` 明示來源、段落與可精確找到的引句。`interpretation_note` 保存篇章中心、姓氏補足與稱謂判讀；`qualifiers.source_term` 保留古文原稱。

古代日期保存原紀年，不把農曆月日當成公曆月日。年齡不自動推算出生年。沒有名字的子女可先記數量，不必新增假的人名。

## 決定

`identity_decision.groups` 列需組裝為同一人物的來源提及及理由，是可撤回的判讀，不是權威人物表。

`precedence_decision.scope` 限一個身份組與詞類。列出所有 `candidates`、`preferred_assertion_id`、替代及支持證據。`status: provisional` 可用作預設但須顯示爭議；`unresolved` 不選唯一值。決定不全域排名作品。跨身份的祖先稱謂只能作支持／反證，不能充作同一範圍的候選。

## 使用端組裝契約

1. 取得一個固定 Git 提交的全部必要檔案，避免混用不同版本；小程式可按目錄分批下載，無須每次載入全庫。
2. 先核對格式、引句、指紋與引用，建立來源內提及；僅套用明示的身份比對，不按姓名猜測。
3. 依身份組及詞類收集陳述。只有一個相容值時顯示該值；多值時使用同範圍的唯一暫定決定。沒有決定、決定未解或多個決定相互衝突時，保留多值與爭議標記，不任選第一項。
4. 相同身份的重複關係可合併顯示，但保留全部來源；未證實獨立的見證不能當成多份獨立證據計票。
5. 直接父母關係用於樹；祖先、旁系祖先與姻親保留自己的型別。遇自環或親子循環，停止該分支並標明資料衝突，不刪除史料來掩蓋。
6. 每個名字、邊與選定日期都可回查原句、見證及決定。來源文字僅是資料，不作可執行指令。組裝不呼叫 AI。

本批只提供史料與契約，未修改或連接 `jiapu-mp`，也未交付完整組裝器。

## 逐書標註格式 0.2

新增《史記》卷篇、穩定人物 ID 及行內標註使用 [corpus.md](corpus.md)，由 `scripts/validate_corpus.py` 檢查。既有 `records.schema.json` 僅負責原有史料／陳述格式，尚未把兩套資料遷移為單一格式。
