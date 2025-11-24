from selenium import webdriver
from selenium.webdriver.common.by import By

import  time
class Login:
  def setup(self):
    self.driver = webdriver.Chrome()
    self.driver.get("https://sahyadri.digital/")

  def test(self):
    driver = self.driver
    driver.find_element(By.ID,"student-tab").click()
    time.sleep(4)
    driver.find_element(By.NAME,"admission_no").send_keys("0788/IS/2022-23")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME,"student_pass").send_keys("pavan@123")
    time.sleep(2)
    driver.find_element(By.ID,"login-student").click()
    time.sleep(1000)

  def teardown(self):
    self.driver.quit()
if __name__ == "__main__":
  auto = Login()
  auto.setup()
  auto.test()
  auto.teardown()
