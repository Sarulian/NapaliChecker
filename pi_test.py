from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import time


if __name__ == '__main__':

	opts = Options()
	opts.headless = True
	driver = webdriver.Firefox(options = opts, executable_path='/usr/bin/geckodriver')
	driver.get('https://www.google.com')
	print(driver.page_source)
	driver.close()
	# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  # Optional argument, if not specified will search path.
	# driver.get('http://www.google.com/xhtml');
	# time.sleep(5) # Let the user actually see something!
	# search_box = driver.find_element_by_name('q')
	# search_box.send_keys('ChromeDriver')
	# search_box.submit()
	# time.sleep(5) # Let the user actually see something!
	# driver.quit()

