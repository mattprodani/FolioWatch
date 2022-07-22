import requests
from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync


class SeekingAlpha():
    def __init__(self, **kwargs):
        self.delay = kwargs.get("delay", 0)
        self.session = requests.Session()
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch(
            headless=kwargs.get("headless", True)
            )
        self.page = self.browser.new_page(
            user_agent=kwargs.get("user_agent"),
            viewport=kwargs.get("viewport")
        )
        stealth_sync(self.page)
   
    def delay_nav(self):
        self.page.wait_for_timeout(self.delay)

    def login(self, username, password):
        """
            Login to SeekingAlpha
        """
        with self.page.expect_navigation():
            self.page.goto("https://seekingalpha.com/account/login")
        self.page.wait_for_load_state("domcontentloaded")
        # self.page.wait_for_timeout(2000)
        self.delay_nav()
        self.page.wait_for_selector('input[name="email"]')

        self.page.click('input[name="email"]')
        self.page.fill('input[name="email"]', username)

        self.page.press('input[name="password"]', "Tab")
        self.page.fill('input[name="password"]', password)
        self.page.press('[data-test-id="sign-in-button"]', "Enter")

        self.page.wait_for_load_state("domcontentloaded")
        return True

    def get_top_stocks(self):
        """
            Returns a dictionary of analyst ratings where the key is the ticker
        """

        self.page.wait_for_timeout(2000)
        self.page.locator('[data-test-id = "top-stocks"]').click()
        self.page.wait_for_load_state("networkidle")
        # self.page.waitForLoadState('networkidle') 

        self.page.locator('[data-test-id = "screener-link"]', has_text = "Top Rated Stocks").click()

        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector("table")
        html = self.page.locator('table').inner_html()
        html = f'<table>{html}</table>'
        return html

