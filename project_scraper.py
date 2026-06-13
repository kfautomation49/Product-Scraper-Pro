from playwright.sync_api import sync_playwright
import re

from urllib.parse import urljoin


class ProductScraper:

    def __init__(self):

        self.products = []
        self.seen_links = set()

        self.stop_requested = False

        self.base_url = ""

        self.search_keyword = ""

        self.log_callback = None
        self.progress_callback = None
        self.product_callback = None

    # ---------------------------------
    # CALLBACK HELPERS
    # ---------------------------------

    def log(self, msg):

        print(msg)

        if self.log_callback:
            self.log_callback(msg)

    def progress(self, value):

        if self.progress_callback:
            self.progress_callback(value)

    # ---------------------------------
    # STOP
    # ---------------------------------

    def stop(self):

        self.stop_requested = True

    # ---------------------------------
    # TEXT HELPERS
    # ---------------------------------

    def clean_text(self, text):

        if not text:
            return ""

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_price(self, text):

        if not text:
            return ""

        patterns = [

            r'৳\s?[\d,]+',

            r'\$\s?[\d,]+',

            r'€\s?[\d,]+',

            r'£\s?[\d,]+',

            r'USD\s?[\d,]+',

            r'BDT\s?[\d,]+'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.I
            )

            if match:
                return match.group()

        return ""

    # ---------------------------------
    # PRODUCT CARD DETECTORS
    # ---------------------------------

    PRODUCT_SELECTORS = [
        '[data-qa-locator="product-item"]'
        '[data-product-id]',
        '[data-component-type="s-search-result"]',
        '.product',
        '.product-item',
        '.product-card',
        '.product-grid-item',
        '.grid-product',
        '.item-product',
        '.product-inner',
        '.product-layout',
        '.product-box',
        '.card',
        'article',
        'li.product',
        '.item'
    ]

    NAME_SELECTORS = [
        ".RfADt",

        ".title--wFj93",
        
        "h1",

        "h2",

        "h3",

        ".product-title",

        ".title",

        ".name",

        ".product-name",

        ".woocommerce-loop-product__title",

        "a"
    ]

    PRICE_SELECTORS = [
        ".price",

        ".amount",

        ".product-price",

        ".sale-price",

        ".current-price",

        ".special-price",

        "[class*='price']",

        "[id*='price']"
    ]

    # ---------------------------------
    # EXTRACT PRODUCTS
    # ---------------------------------

    def extract_products(self, page):

        found_cards = None

        for selector in self.PRODUCT_SELECTORS:

            locator = page.locator(selector)

            try:

                count = locator.count()

                if count > 0:

                    found_cards = locator

                    self.log(
                        f"Using selector: {selector}"
                    )

                    break

            except:
                pass

        if not found_cards:

            self.log(
                "Selector failed. Using AUTO DETECT mode..."
            )

            links = page.locator("a")

            count = links.count()

            self.log(
                f"Scanning {count} links..."
            )

            for i in range(count):

                try:

                    link = links.nth(i)

                    text = self.clean_text(
                        link.inner_text()
                    )

                    href = link.get_attribute(
                        "href"
                    )

                    if not text:
                        continue

                    if not href:
                        continue

                    if len(text) < 5:
                        continue

                    if self.search_keyword:
                        if self.search_keyword not in text.lower():
                            continue

                    junk_words = [
                        "login",
                        "sign in",
                        "logout",
                        "contact",
                        "help center",
                        "wishlist",
                        "my orders",
                        "my account",
                        "search",
                        "home",
                        "seller",
                        "returns",
                        "refunds"
                    ]

                    if any(
                        word in text.lower()
                        for word in junk_words
                    ):
                        continue

                    full_link = urljoin(
                        self.base_url,
                        href
                    )

                    # Product URL filter
                    if not any(
                        word in full_link.lower()
                        for word in [
                            "/product/",
                            "/products/",
                            "/item/",
                            "-i",
                            ".html"
                        ]
                    ):
                        continue

                    if full_link in self.seen_links:
                        continue

                    parent_text = ""

                    try:

                        parent_text = link.locator(
                            "xpath=.."
                        ).inner_text()

                    except:
                        pass

                    price = self.extract_price(
                        parent_text
                    )

                    self.seen_links.add(
                        full_link
                    )

                    self.log(
                        f"FOUND => {text}"
                    )

                    self.products.append(
                        {
                            "Product Name": text,
                            "Price": price,
                            "Link": full_link
                        }
                    )

                    if hasattr(self, "product_callback"):
                        self.product_callback(
                            {
                                "Product Name": text,
                                "Price": price,
                                "Link": full_link
                            }
                        )

                    if self.product_callback:

                        self.product_callback(
                            {
                                "Product Name": text,
                                "Price": price,
                                "Link": full_link
                            }
                        )

                    self.log(
                        f"TOTAL NOW => {len(self.products)}"
                    )

                except:
                    pass

            return

        total_cards = found_cards.count()

        self.log(
            f"Cards found: {total_cards}"
        )

        # Safety Limit
        if total_cards > 200:

            total_cards = 200

            self.log(
                "Card limit applied: 200"
            )

        for i in range(min(total_cards, 200)):

            if self.stop_requested:
                return

            try:

                card = found_cards.nth(i)

                try:
                    self.log(
                        card.inner_text()[:300]
                    )

                except:
                    pass

                name = ""

                for selector in self.NAME_SELECTORS:

                    try:

                        value = card.locator(
                            selector
                        ).first.text_content(
                            timeout=2000
                        )

                        if value:

                            name = self.clean_text(value)

                            break

                    except:
                        pass

                price = ""

                for selector in self.PRICE_SELECTORS:

                    try:

                        value = card.locator(
                            selector
                        ).first.inner_text()

                        if value:

                            price = self.extract_price(
                                value
                            )

                            if not price:
                                price = self.clean_text(
                                    value
                                )

                            break

                    except:
                        pass

                link = ""

                try:

                    link = card.locator(
                        "a"
                    ).first.get_attribute("href")

                except:
                    pass

                if not name:

                    self.log(
                        f"NO NAME CARD {i}"
                    )

                    continue

                if self.search_keyword:
                    if self.search_keyword not in name.lower():
                        continue

                if not link:
                    self.log(
                        f"NO LINK CARD {i}"
                    )

                    continue

                if link in self.seen_links:
                    continue

                if len(name) < 3:
                    continue

                if len(name) > 250:
                    continue

                self.seen_links.add(link)

                full_link = urljoin(
                    self.base_url,
                    link
                )

                self.log(
                    f"FOUND => {name} | {price}"
                )

                self.products.append(
                    {
                        "Product Name": name,
                        "Price": price,
                        "Link": full_link
                    }
                )

                if self.product_callback:

                    self.product_callback(
                        {
                            "Product Name": name,
                            "Price": price,
                            "Link": full_link
                        }
                    )

            except Exception as e:

                self.log(
                    f"Card Error: {e}"
                )

    # ---------------------------------
    # PAGINATION
    # ---------------------------------

    def goto_next_page(self, page):

        selectors = [

            "a.next",

            ".next",

            "li.next a",

            ".pagination-next",

            "a[rel='next']",

            ".page-next",

            ".next-page"
        ]

        for selector in selectors:

            try:

                btn = page.locator(
                    selector
                ).first

                if btn.count() > 0:

                    btn.click()

                    page.wait_for_load_state(
                        "networkidle"
                    )

                    page.wait_for_timeout(
                        500
                    )

                    return True

            except:
                pass

        return False

    # ---------------------------------
    # MAIN SCRAPER
    # ---------------------------------

    def scrape(
        self,
        url,
        max_pages=5,
        keyword=""
    ):

        self.products.clear()
        self.seen_links.clear()

        self.stop_requested = False

        self.search_keyword = (
            keyword.lower().strip()
        )

        with sync_playwright() as p:

            browser = None

            try:

                browser = p.chromium.launch(
                    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    headless=False
                )

                context = browser.new_context()

                page = context.new_page()

                self.log(
                    f"Opening: {url}"
                )

                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                self.base_url = page.url

                page.wait_for_timeout(
                    500
                )

                for current_page in range(
                    1,
                    max_pages + 1
                ):

                    if self.stop_requested:
                        break

                    self.log(
                        f"Page {current_page}"
                    )

                    self.extract_products(
                        page
                    )

                    progress = (
                        current_page
                        / max_pages
                    )

                    self.progress(
                        progress
                    )

                    if current_page == max_pages:
                        break

                    has_next = (
                        self.goto_next_page(
                            page
                        )
                    )

                    if not has_next:

                        self.log(
                            "No next page."
                        )

                        break

            except Exception as e:

                import traceback

                print(traceback.format_exc())

                self.log(
                    f"SCRAPER ERROR: {e}"
                )

                raise

            finally:

                if browser:

                    try:

                        context.close()

                    except:
                        pass

                    try:

                        browser.close()

                    except:
                        pass
                    

        self.log(
            f"Total Products: {len(self.products)}"
        )

        self.log(
            f"SCRAPER FINISHED. PRODUCTS={len(self.products)}"
        )

        return self.products
