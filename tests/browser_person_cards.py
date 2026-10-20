"""Check that deliberate person selection survives mixed touch/mouse input.

Run with READER_URL and BROWSER_EXECUTABLE; requires Playwright.
Pointer events reproduce the browser event sequence recorded during mobile QA.
"""
import os
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

BASE = os.environ.get('READER_URL', 'http://127.0.0.1:8794/').rstrip('/') + '/'
SELECTED = 'oho_r3f_c6y'
INCIDENTAL = 'yqp_nlb_p1p_ACAA'

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=os.environ['BROWSER_EXECUTABLE'], headless=True)
    for width in (1400, 390):
        page = browser.new_page(viewport={'width': width, 'height': 1000},
                                is_mobile=width == 390, has_touch=width == 390)
        page.set_default_timeout(60000)
        expected = os.environ.get('EXPECTED_COMMIT')
        if expected:
            assert page.request.get(BASE + 'deployment.json').json()['commit'] == expected
        page.goto(BASE + 'shiji.html#' + urlencode({
            'chapter': 117, 'category': 'liezhuan', 'passage': 'c-shiji-117-xiangru:p053'}))
        selected = page.locator('[id="c-shiji-117-xiangru:m053-0001"]')
        other = page.locator('[id="c-shiji-117-xiangru:m055-0009"]')
        selected.wait_for()
        selected.scroll_into_view_if_needed()
        if width == 390:
            selected.tap()
        else:
            selected.click()
        # A compatibility mouse event can arrive after an intentional touch tap.
        other.dispatch_event('pointerover', {'pointerType': 'mouse'})
        page.wait_for_function('id => document.querySelector(".person-profile-button")?.hash === "#" + id', arg=SELECTED)
        other.dispatch_event('pointerout', {'pointerType': 'mouse', 'relatedTarget': None})
        page.wait_for_timeout(300)  # Exceed the existing hover-dismiss timer.
        assert page.locator('.table-person-card').is_visible()
        assert page.locator('.person-profile-button').get_attribute('href').endswith('#' + SELECTED)
        page.locator('.close-person-card').click()
        assert not page.locator('.table-person-card').is_visible()
        other.dispatch_event('pointerover', {'pointerType': 'mouse'})
        assert not page.locator('.table-person-card').is_visible()
        other.dispatch_event('pointermove', {'pointerType': 'mouse'})
        page.wait_for_function('id => document.querySelector(".person-profile-button")?.hash === "#" + id', arg=INCIDENTAL)
        page.keyboard.press('Escape')
        assert not page.locator('.table-person-card').is_visible()
        print(width, 'explicit selection, incidental hover, close, hover and Escape PASS', flush=True)
        page.close()
    browser.close()
print('person card mixed-input regression PASS', os.environ.get('EXPECTED_COMMIT'))
