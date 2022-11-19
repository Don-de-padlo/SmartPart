from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent

def get_driver(driver_path):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent="+ UserAgent().opera)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('window-size=1920x1080')
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options = options)
    driver.set_window_position(-10000, 0)
    return driver


