"""Check that opening a source during family loading survives the profile update."""

import argparse
import os
import shutil
from urllib.parse import urljoin

from playwright.sync_api import expect, sync_playwright


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--url", required=True)
    base = cli.parse_args().url.rstrip("/") + "/"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=os.environ.get("BROWSER_EXECUTABLE") or shutil.which("chromium")
        )
        for width in (390, 1440):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.add_init_script("""
                const fetchNormally = window.fetch.bind(window);
                const familyGate = new Promise(resolve => { window.releaseTestFamily = resolve; });
                window.heldTestFamily = false;
                window.fetch = async (input, options) => {
                    const pathname = new URL(input, location.href).pathname;
                    if (pathname.includes('/data/corpus/profiles/') &&
                        !pathname.endsWith('/7r6_k52_qji_ABAAAA.json')) {
                        window.heldTestFamily = true;
                        await familyGate;
                    }
                    return fetchNormally(input, options);
                };
            """)
            page.goto(urljoin(base, "person.html#7r6_k52_qji_ABAAAA"))
            page.wait_for_function("window.heldTestFamily")
            loading = page.get_by_text("正在載入家族關係…", exact=True)
            expect(loading).to_be_visible()
            source = 'a[href*="c-jinshu-010-wangxun-longan4"]'
            evidence = page.locator(".person-life-summary details").filter(has=page.locator(source)).first
            link = evidence.locator(source)
            evidence.locator("summary").click()
            expect(link).to_be_visible()
            page.evaluate("window.releaseTestFamily()")
            expect(loading).to_have_count(0)
            expect(link).to_be_visible()
            link.click()
            expect(page.locator('[id="c-jinshu-010-wangxun-longan4:p001"]')).to_contain_text("東亭侯王珣卒")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
