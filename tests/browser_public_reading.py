"""Exercise public reader tasks against either a staged site or the deployed URL."""
import argparse
import os
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import expect, sync_playwright


def check_tasks(page, base, mobile, screenshots):
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))

    def check_width():
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), page.url

    def capture(name):
        check_width()
        if screenshots:
            page.screenshot(path=screenshots / f'{name}-{"mobile" if mobile else "desktop"}.png')

    page.goto(base)
    query = page.get_by_label('搜尋書名或作者')
    expect(page.locator('.home-source-card').first).to_be_visible()
    first_book = page.locator('.home-source-card h3 a').first
    assert first_book.evaluate('node => node.getBoundingClientRect().bottom <= innerHeight')
    capture('catalogue')
    query.fill('不存在的測試書名')
    expect(page.locator('#home-source-total')).to_contain_text('沒有相符')
    query.fill('陳壽')
    expect(page.locator('.home-source-card:visible')).to_have_count(1)
    page.get_by_role('link', name='《三國志》', exact=True).click()
    page.get_by_label('搜尋篇名或卷號').fill('三少帝紀')
    entry = page.locator('.volume-directory-entry').filter(has=page.locator('a[href*="c-sanguozhi-004-jin033-wangxiang"]'))
    entry.locator('.volume-entry').click()
    page.locator('[data-volume-placeholder] a[href*="c-sanguozhi-004-jin033-wangxiang"]').click()
    article = page.locator('.corpus-text')
    expect(article).to_be_visible()
    pei = page.locator('[data-commentary-toggle="pei"]')
    notes = article.locator('[data-commentary-group="pei"]')
    expect(notes.first).to_be_visible()
    quote = notes.first.text_content()
    pei.uncheck()
    expect(notes.first).to_be_hidden()
    pei.check()
    expect(notes.first).to_have_text(quote)
    capture('volume')

    page.locator('.public-nav').get_by_role('link', name='史書目錄').click()
    page.get_by_role('link', name='《史記》', exact=True).click()
    page.get_by_label('搜尋篇名或卷號').fill('秦始皇')
    page.locator('.chapter-entry').filter(has_text='秦始皇').click()
    person = page.locator('.corpus-text .cbr-person-link').first
    expect(person).to_be_visible()
    if mobile:
        assert not page.locator('#chapter-directory').evaluate('node => node.open')
        assert person.evaluate('node => node.getBoundingClientRect().top < innerHeight')
    original = person.locator('xpath=ancestor::p[1]').text_content()
    person.click()
    page.locator('.person-profile-button:visible').click()
    page.get_by_role('button', name='篇章引文').click()
    passages = page.locator('.profile-passage-citations')
    expect(passages).to_be_focused()
    citation = passages.locator('li').first
    href = citation.locator('a').get_attribute('href')
    cited_text = citation.locator('q').inner_text()
    citation.locator('a').click()
    passage = parse_qs(urlsplit(href).fragment)['passage'][0]
    expect(page.locator(f'[id="{passage}"]')).to_contain_text(cited_text)
    page.go_back()
    page.locator('#cbr-person-table-back').click()
    expect(page.locator('.corpus-text p').first).to_have_text(original)
    capture('chapter')

    page.locator('.public-nav').get_by_role('link', name='年表', exact=True).click()
    other = page.locator('.related-table a')
    other.click()
    expect(page.locator('[data-native-table] .source-cell').first).to_be_visible()
    expect(page.locator('[data-source-scope]')).to_contain_text('曲成')
    page.go_back()
    page.locator('.table-directory').get_by_role('link', name='六國年表第三').click()
    expect(page.locator('.source-cell')).to_have_count(2306)
    page.select_option('#year-select', label='西元前 207 年')
    cell = page.locator('.active-cell').get_attribute('id')
    page.locator('#axis-horizontal').click()
    expect(page.locator('.active-cell')).to_have_attribute('id', cell)
    capture('table')

    page.locator('.public-nav').get_by_role('link', name='人物索引').click()
    page.locator('#person-search').fill('王珣')
    if mobile:
        filters = page.locator('#directory-filters')
        assert not filters.evaluate('node => node.open')
        filters.locator('summary').click()
        expect(filters.locator('input[data-facet]').first).to_be_visible()
        filters.locator('summary').click()
    page.locator('.person-result-name[href*="7r6_k52_qji_ABAAAA"]').first.click()
    expect(page.locator('.person-family')).to_be_visible()
    page.get_by_role('button', name='家族親屬').click()
    expect(page.locator('.person-family')).to_be_focused()
    capture('family')
    assert not errors, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.getenv('BROWSER_EXECUTABLE'))
        static_page = browser.new_page(java_script_enabled=False)
        static_page.goto(args.url.rstrip('/') + '/')
        expect(static_page.get_by_role('link', name='《史記》', exact=True)).to_be_visible()
        expect(static_page.get_by_role('link', name='《三國志》', exact=True)).to_be_visible()
        expect(static_page.locator('.home-source-count').first).to_contain_text('130')
        static_page.close()
        for mobile in [False, True]:
            options = dict(pw.devices['iPhone 13']) if mobile else {'viewport': {'width': 1440, 'height': 900}}
            options.pop('default_browser_type', None)
            page = browser.new_page(**options)
            page.set_default_timeout(60000)
            expect.set_options(timeout=60000)
            check_tasks(page, args.url.rstrip('/') + '/', mobile, args.output)
            page.close()
            print('Mobile' if mobile else 'Desktop', 'reader tasks passed', flush=True)
        page = browser.new_page(viewport={'width': 320, 'height': 800})
        page.goto(args.url.rstrip('/') + '/reader.html')
        page.get_by_role('button', name='English', exact=True).click()
        page.locator('.public-more summary').click()
        menu = page.locator('.public-more > div')
        expect(menu).to_be_visible()
        assert menu.evaluate('node => { const r = node.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth; }')
        page.close()
        browser.close()


if __name__ == '__main__':
    main()
