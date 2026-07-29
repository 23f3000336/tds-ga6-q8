import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
SEEDS = range(29, 39)

NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def numbers_on_page(page):
    page.wait_for_selector("table td")
    cells = page.query_selector_all("table td")

    values = []
    for cell in cells:
        text = (cell.inner_text() or "").strip().replace(",", "")
        for match in NUMBER_RE.findall(text):
            values.append(float(match))
    return values


def main():
    grand_total = 0.0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for seed in SEEDS:
            url = BASE_URL.format(seed=seed)
            page.goto(url, wait_until="networkidle")

            values = numbers_on_page(page)
            subtotal = sum(values)
            grand_total += subtotal

            print(f"seed={seed}: found {len(values)} numbers, subtotal = {subtotal}")

        browser.close()

    if grand_total == int(grand_total):
        grand_total = int(grand_total)

    print(f"TOTAL sum of all numbers across all pages = {grand_total}")
    print(f"::notice title=Total::{grand_total}")


if __name__ == "__main__":
    main()
