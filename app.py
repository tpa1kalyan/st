from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your Chrome driver
driver_path = 'D:/sel/chromedriver-win64/chromedriver.exe'  # Update with your actual chromedriver location

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # Go to Google and search for 'net speed test'
    driver.get('https://www.google.com/')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('net speed test')
    search_box.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 30)
    # Wait for and click 'RUN SPEED TEST' button
    run_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RUN SPEED TEST')]"))
    )
    run_btn.click()

    # Wait for Download speed result (the actual selectors may need adjustment based on webpage changes)
    download_result = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Download')]/following-sibling::div"))
    )
    upload_result = driver.find_element(
        By.XPATH, "//div[contains(text(),'Upload')]/following-sibling::div"
    )
    ping_result = driver.find_element(
        By.XPATH, "//div[contains(text(),'Latency')]/following-sibling::div"
    )
    signal_result = driver.find_element(
        By.XPATH, "//div[contains(text(),'Jitter')]/following-sibling::div"
    )

    print(f"Download Speed: {download_result.text}")
    print(f"Upload Speed: {upload_result.text}")
    print(f"Ping/Latency: {ping_result.text}")
    print(f"Signal/Jitter: {signal_result.text}")

finally:
    driver.quit()
