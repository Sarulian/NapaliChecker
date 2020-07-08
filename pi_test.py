from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
	opts = Options()
	opts.headless = True
	driver = webdriver.Firefox(options = opts, executable_path='/usr/bin/geckodriver')
	driver.get('https://www.google.com')
	print(driver.page_source)
	driver.close()
