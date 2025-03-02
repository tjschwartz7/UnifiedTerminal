from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#WARNING
#More research is needed before full testing can be done with this scraper.
#Careless usage of this program can result in an IP ban from some websites. 
#Because of this, proxy networks should be used when actually performing testing,
#along with other safeguards.

# 1. Don't turn on headless mode. You'll get CAPTCHA'd.
# 2. If you get CAPTCHA'd, you been found out.
# 3. If you get CAPTCHA'd enough, you can get banned. Be careful.
# 
# I feel like I don't know what I'm doing with this yet, 
# and I won't be playing with this much until I feel that I do. 

# Set up Firefox options (optional: headless mode)
options = Options()
options.set_preference("general.useragent.override", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("webdriver.chrome.driver", "")


# options.add_argument("--headless")  # Uncomment for headless mode

# Set up the WebDriver path
service = Service()  # Replace with actual path or ensure it's in PATH

# Launch Firefox
driver = webdriver.Firefox(service=service, options=options)

# Open Google
driver.get("https://www.google.com")

# Wait until the search box is visible
# Find the search box, enter query, and submit
search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "q")))


search_box.send_keys("Selenium with Firefox")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
driver.implicitly_wait(5)

# Get the first result's title
first_result = driver.find_element(By.CSS_SELECTOR, "h3")
print("First search result:", first_result.text)

# Close the browser
driver.quit()
