# Explicit 小字 apposition

`xiaozhi_basis.kind: explicit_xiaozhi_apposition` accepts exactly value + subject + 小字 + 也. Both value and subject have distinct, same-canonical `kind: person` mentions with exact paragraph offsets. Marker has its own exact slice. `quote` must equal the full received paragraph; `source_term` must equal the full contiguous clause. Status is source_attested and human_reviewed is false. This is 小字, never 小名 or 字.

The existing explicit_xiaozhi_statement still requires 者; explicit_subject_xiaozhi still requires 又 and its established ending rule. Their function bodies remain unchanged except the new opt-in dispatcher. Legacy synthetic mention objects without kind retain their previous behavior. The new grammar alone requires kind:person.

Native all_name_records processing invokes the same validator only for dictionary records carrying xiaozhi or xiaozhi_basis, resolving the full chapter_id + paragraph_id and collecting ValueError. It does not infer name types, modify source, or scan the whole catalog per person.
