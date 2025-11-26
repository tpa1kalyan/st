https://github.com/tpa1kalyan/wealth-compass.git
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
class Google:
    def setup(self):
        self.driver =webdriver.Chrome()
        
    def search_loacction(self):
        g_link=("https://www.google.com/maps")
        ip_link='//*[@id="searchboxinput"]'
        direction_xpath= '//*[@id="searchbox-searchbutton"]'
        self.driver.get(g_link)
        time.sleep(2)
        name =str(input("Enter location name: "))
        self.driver.find_element(By.XPATH,ip_link).send_keys(name)
        self.driver.find_element(By.XPATH,direction_xpath).click()
        time.sleep(5)
    
    def teardown(self):
        self.driver.quit()
if __name__ == "__main__":
    g=Google()
    g.setup()
    g.search_loacction()
    g.teardown()
