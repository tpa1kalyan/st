from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By

class WebPageFetcher():
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def fetch_page(self):
        try:
            self.driver.get("https://www.btreesystems.com/selenium-with-python-training-in-chennai")
            page_source = self.driver.page_source.encode('utf-8')

            with open("result.html", "wb") as f:
                f.write(page_source)
        except Exception as e:
            print(f"An error occurred: {e}")
        

        

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    fetcher = WebPageFetcher()
    fetcher.setUp()
    fetcher.fetch_page()
    fetcher.tearDown()
