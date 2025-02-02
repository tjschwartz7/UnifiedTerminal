from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Launch Chrome
driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

# Open a webpage
driver.get("https://www.google.com")

# Find search bar and input text
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.send_keys(Keys.RETURN)

# Close browser
driver.quit()
