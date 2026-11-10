"""Validate full texts transcribed from an institutional museum catalogue.

This records the museum's digital transcription as the working witness. It is
not an image collation, a capture of the museum's complete web page, or proof of
the oldest printed edition.
"""
import hashlib
import json
from pathlib import Path

KIND = 'institutional_museum_web_epitaph_transcription'
LAYER = 'epitaph_as_modernly_transcribed'


def errors(chapter, root, works, books):
    failures = []

    def require(ok, reason):
        if not ok:
            failures.append('機構博物館墓誌錄文見證：' + reason)

    def read(relative):
        if (not isinstance(relative, str) or not relative.startswith('source-evidence/')
                or not relative.endswith('.json')):
            raise ValueError('來源證據路徑格式')
        base = Path(root).resolve()
        path = (base / relative).resolve()
        if not path.is_relative_to(base) or not path.is_file():
            raise ValueError('來源證據缺失或越界')
        return json.loads(path.read_text(encoding='utf-8'))

    try:
        source = chapter['source']
        witness = source['transcription_witness']
        require(witness.get('kind') == KIND, '見證類型不符')
        require(source.get('revision_id') is None and not source.get('source_commit')
                and not source.get('source_blob'), '不得偽造網站修訂或 Git 版本')
        require(source.get('image_verified') is False
                and witness.get('original_stone_or_rubbing_image_verified') is False
                and witness.get('underlying_rubbing_personally_accessed') is False,
                '數位釋文不得冒稱原石或拓片校讀')
        require(witness.get('transcription_page_visually_checked') is False
                and chapter.get('annotation', {}).get('human_reviewed') is False,
                '文字頁核讀及人工覆核狀態不符')
        require(source.get('text_scope') == 'complete_work'
                and witness.get('scope') == 'complete_single_inscription_not_modern_article',
                '須僅收單方墓誌全文')
        require(source.get('license_scope') == 'classical_inscription_text_only'
                and isinstance(source.get('rights'), str) and bool(source['rights']),
                '古代碑文與現代圖片、考述權利須分開')
        require(witness.get('institution') == '河南博物院'
                and witness.get('catalogue_title') == '荀岳墓誌'
                and witness.get('accessed_on') == source.get('accessed_on'),
                '館方書目或查閱日期缺失')
        require(source.get('url') == source.get('permalink') == witness.get('institution_url'),
                '單件館藏頁網址不一致')

        work = works.get(chapter.get('work_id'), {})
        book = books.get(chapter.get('book_id'), {})
        require(work.get('work_type') == 'single_epitaph' and len(work.get('books', [])) == 1,
                '作品須為單方墓誌')
        require(book.get('unit_kind') == 'editorial_single_text_container'
                and book.get('number') is None and book.get('original_volume_number') is None
                and bool(work.get('numbering_note')), '不得偽造古代卷次')

        transcription = read(witness.get('transcription_path'))
        metadata = read(witness.get('metadata_path'))
        faces = transcription.get('normalized_text_traditional')
        hashes = transcription.get('text_sha256')
        require(transcription.get('source_url') == source.get('url')
                and transcription.get('accessed_on') == source.get('accessed_on'),
                '轉錄見證來源網址或查閱日不符')
        require(transcription.get('page_text_visually_checked') is False
                and transcription.get('original_stone_or_rubbing_image_verified') is False,
                '不得擴張館方數位文字的核讀範圍')
        require(metadata.get('source_url') == source.get('url')
                and metadata.get('image_verified') is False
                and metadata.get('images_stored_in_repository') is False,
                '館藏資訊或外部影像狀態不符')
        require(isinstance(faces, list) and len(faces) == 4
                and isinstance(hashes, list) and len(hashes) == len(faces),
                '須逐面保存四段原文及指紋')
        if isinstance(faces, list) and isinstance(hashes, list):
            require(len(chapter.get('paragraphs', [])) == len(faces), '正文分面數與館方錄文不符')
            for index, text in enumerate(faces):
                digest = hashlib.sha256(text.encode('utf-8')).hexdigest() if isinstance(text, str) else None
                require(digest == hashes[index], f'第{index + 1}面全文指紋不符')
                if index < len(chapter.get('paragraphs', [])):
                    paragraph = chapter['paragraphs'][index]
                    position = paragraph.get('source_position', {})
                    require(paragraph.get('text') == text
                            and paragraph.get('text_layer') == LAYER,
                            f'第{index + 1}面正文非原錄文')
                    require(position.get('kind') == KIND
                            and position.get('source_text_path') == witness.get('transcription_path')
                            and position.get('face') == ['題額及正面', '背面', '右側', '左側'][index]
                            and position.get('editorial_single_paragraph') is True
                            and position.get('physical_line_divisions_inferred') is False,
                            f'第{index + 1}面段落定位或行界聲明不符')
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError, AttributeError) as exc:
        failures.append('機構博物館墓誌錄文見證：格式或所據文字不可讀 ' + type(exc).__name__)
    return failures
