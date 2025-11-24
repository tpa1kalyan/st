from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By

class Count(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.google.co.in/")
        self.driver.maximize_window()

    def test_count_element(self):
        driver = self.driver
        links = driver.find_elements(By.TAG_NAME, "a")
        print("Total links are:", len(links))
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print("Total buttons are:", len(buttons))
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print("Total input elements:", len(inputs))

        

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
