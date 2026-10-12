"""在真實 HTTP 檢查首頁、分類原文、人物資料與可轉置連續年表。"""
import argparse
import json
import os
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
report = {'url': args.url, 'mockedNetwork': False, 'errors': [], 'failedRequests': []}
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=os.environ.get('BROWSER_EXECUTABLE'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.set_default_timeout(45000)
    page.on('pageerror', lambda e: report['errors'].append(str(e)))
    page.on('requestfailed', lambda r: report['failedRequests'].append(r.url))
    def goto(path):
        response = page.goto(urljoin(args.url, path), wait_until='networkidle', timeout=120000)
        assert response is None or response.status == 200
    try:
        goto('')
        expect(page.locator('#home-library')).to_be_visible()
        expect(page.locator('#workspace')).to_be_hidden()
        page.screenshot(path=str(args.output / 'home.png'), full_page=True)
        page.get_by_role('link', name='閱讀《史記》').click()
        expect(page.locator('.chapter-entry')).to_have_count(130)
        for category, count in [('本紀', 12), ('表', 10), ('書', 8), ('世家', 30), ('列傳', 70)]:
            page.locator('#shiji-categories').get_by_role('link', name=category, exact=True).click()
            expect(page.locator('.chapter-entry')).to_have_count(count)
        page.locator('#shiji-categories').get_by_role('link', name='本紀', exact=True).click()
        page.locator('.chapter-entry').filter(has_text='秦始皇').click()
        expect(page.locator('.corpus-text > p')).to_have_count(127)
        first = page.locator('.cbr-person-link').first
        first.hover()
        expect(page.locator('#person-preview')).to_be_visible()
        expect(page.locator('#person-preview')).to_contain_text('秦始皇帝')
        page.screenshot(path=str(args.output / 'shiji.png'))
        first.click()
        expect(page.locator('#corpus-person-dialog')).to_be_visible()
        expect(page.locator('#corpus-person-details blockquote')).to_contain_text('秦始皇帝者')
        expect(page.locator('#corpus-person-details a').filter(has_text='完整人物 JSON')).to_have_attribute('href', 'https://raw.githubusercontent.com/liuyao12/chinese-biographical-repository/main/exports/persons/ao3_0fy_d45_AAA.json')
        page.locator('#corpus-person-dialog button').click()
        goto('shiji.html#category=biao')
        page.locator('.chapter-entry').filter(has_text='六國年表').click()
        expect(page.locator('#chapter-table-reader .source-cell')).to_have_count(2306)
        assert 'shiji.html' in page.url and 'chapter=15' in page.url
        assert page.locator('iframe').count() == 0
        page.locator('.chapter-entry').filter(has_text='十二諸侯年表').click()
        expect(page.locator('#chapter-table-reader .source-cell')).to_have_count(5840)
        page.locator('.chapter-entry').filter(has_text='六國年表').click()
        expect(page.locator('#chapter-table-reader .source-cell')).to_have_count(2306)
        goto('tables.html#table=shiji-015&axis=vertical')
        page.wait_for_selector('.source-cell')
        assert 'shiji.html' in page.url and 'chapter=15' in page.url
        count = page.locator('.source-cell').count()
        page.select_option('#year-select', label='西元前 207 年')
        expect(page.locator('.active-cell')).to_contain_text('207')
        cell_id = page.locator('.active-cell').get_attribute('id')
        page.click('#axis-horizontal')
        expect(page.locator('#table-grid')).to_have_class('historical-grid horizontal')
        expect(page.locator('.source-cell')).to_have_count(count)
        expect(page.locator('#table-grid .year-cell')).to_have_count(270)
        expect(page.locator('#table-grid .axis-heading')).to_have_count(0)
        expect(page.locator('#table-grid .corner-heading')).to_contain_text('編輯補充 · 第零列')
        assert page.locator('#table-grid [data-source-text].year-cell').count() == 0
        assert page.locator('#table-grid .year-cell').evaluate_all("nodes => nodes.every(n => n.style.gridRow.startsWith('1 /'))")
        expect(page.locator('.active-cell')).to_have_attribute('id', cell_id)
        merged = page.locator('[id="shiji-015-r270-c01"]')
        expect(merged).to_have_attribute('style', 'grid-column:271 / span 1;grid-row:2 / span 8')
        page.fill('#table-search', '子嬰')
        page.click('#search-next')
        expect(page.locator('.active-cell')).to_contain_text('子嬰')
        page.select_option('#year-select', label='西元前 207 年')
        merged.click()
        expect(page.locator('#cell-dialog')).to_be_visible()
        expect(page.locator('#cell-details')).to_contain_text('來源合併範圍：1 列、8 欄')
        page.locator('#cell-dialog button').click()
        page.screenshot(path=str(args.output / 'table-horizontal.png'))
        goto('tables.html#table=shiji-014&axis=vertical')
        expect(page.locator('.source-cell')).to_have_count(5840)
        page.select_option('#year-select', label='西元前 477 年')
        expect(page.locator('.active-cell')).to_contain_text('477')
        page.click('[data-set-locale="en"]')
        expect(page.locator('#table-title')).to_contain_text('十二諸侯年表')
        expect(page.locator('.active-cell')).to_contain_text('477 BCE')
        page.click('[data-set-locale="zh-Hant"]')
        page.set_viewport_size({'width': 390, 'height': 844})
        goto('shiji.html#chapter=6&category=benji')
        expect(page.locator('.corpus-text > p')).to_have_count(127)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        page.screenshot(path=str(args.output / 'shiji-mobile.png'), full_page=True)
        goto('tables.html#table=shiji-015&axis=horizontal')
        page.wait_for_selector('.source-cell')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        page.select_option('#year-select', label='西元前 207 年')
        expect(page.locator('.active-cell')).to_contain_text('207')
        page.screenshot(path=str(args.output / 'table-mobile.png'))
        page.set_viewport_size({'width': 1440, 'height': 1000})
        goto('#eccp-zeng-guofan')
        page.wait_for_selector('#reader p[id]')
        expect(page.locator('#home-library')).to_be_hidden()
        expect(page.locator('#workspace')).to_be_visible()
        assert not report['errors'], report['errors']
        assert not report['failedRequests'], report['failedRequests']
        report['passed'] = True
    finally:
        (args.output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        browser.close()
