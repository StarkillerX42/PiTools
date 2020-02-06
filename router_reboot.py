from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
now = datetime.datetime.now()
print("Router Reboot started at {}".format(now))
driver = webdriver.Chrome()
time.sleep(1)
driver.get("http://10.0.0.1")
elem = driver.find_element_by_name("username")
elem.clear()
elem.send_keys("admin")
elem = driver.find_element_by_name("password")
elem.clear()
elem.send_keys("password1")
elem.send_keys(Keys.RETURN)
#Alert(driver).dismiss()
elem = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "nav-troubleshooting")))
elem.click()
elem = driver.find_element_by_class_name("nav-restore-reboot")
elem.click()
elem = driver.find_element_by_id("btn2")
elem.click()
elem = driver.find_element_by_id("popup_ok")
elem.click()
driver.quit()

