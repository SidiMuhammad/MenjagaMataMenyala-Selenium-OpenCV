from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import imageio

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)


def click(element_css):
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, element_css)))
    driver.find_element(By.CSS_SELECTOR, element_css).click()


driver.get('https://kkn-upnyk.com')
click('#topbar > div > div:nth-child(2) > a')
driver.find_element(By.CSS_SELECTOR, '#ni').send_keys('NIM')
driver.find_element(By.CSS_SELECTOR, '#password').send_keys('password')
click('#app > section > div > div > div > div.card.card-success.card-login > div.card-body > form > div:nth-child(5) > button')
click('#sidebar-wrapper > ul > li:nth-child(4) > a')
click('#sidebar-wrapper > ul > li.dropdown.active > ul > li:nth-child(2) > a')


def download(x):
    click('#table-1 > tbody > tr:nth-child(' +
          str(x)+') > td:nth-child(3) > center > a')
    src = driver.find_element(
        By.CSS_SELECTOR, '#berkas').get_attribute('src')
    save_image = imageio.imread(src)
    imageio.imwrite(str(x)+'.jpg', save_image)
    click('#view-berkas > div > div > div.modal-header > button')


for x in range(1, 63):
    try:
        download(x)
    except:
        click('#view-berkas > div > div > div.modal-header > button')
        download(x)
