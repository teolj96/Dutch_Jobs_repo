import codecs
import random

from selenium import webdriver
import time
import warnings
import os

path = r'C:\Users\tljubicic\OneDrive - A1 Group\Dokumente\chromedriver.exe'
driver = webdriver.Chrome(path)
email = 'karavury@brand-app.biz'
password = 'kavabonga123'

warnings.filterwarnings('ignore')

driver.get('https://www.linkedin.com/jobs/')
driver.maximize_window()

driver.implicitly_wait(5)

try:
    driver.find_element_by_xpath('//div[@class="sign-in-form__form-input-container"]/child::div[1]/input').click()
    driver.find_element_by_xpath('//div[@class="sign-in-form__form-input-container"]/child::div[1]/input').send_keys(
        email)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//div[@class="sign-in-form__form-input-container"]/child::div[2]/input').click()
    driver.find_element_by_xpath('//div[@class="sign-in-form__form-input-container"]/child::div[2]/input').send_keys(
        password)
    driver.implicitly_wait(5)
except:
    pass

driver.find_element_by_xpath('//button[@class="sign-in-form__submit-button"]').click()
time.sleep(3)

driver.find_element_by_xpath('//ul//li//a[contains(@href,"jobs")]').click()
time.sleep(3)
driver.find_element_by_xpath('//li[contains(@class,"recent")]').click()
time.sleep(3)
driver.find_element_by_xpath(
    '//button//li-icon/following-sibling::span[text()="You are on the messaging overlay. Press enter to minimize it."]/parent::button').click()
time.sleep(3)
item_list = driver.find_elements_by_xpath('//ul[@class="scaffold-layout__list-container"]/child::li')

job_counter = 0
page_counter = 1

last_page = driver.find_element_by_xpath(
    '//div[contains(@class,"pagination")]/child::ul/li[@data-test-pagination-page-btn][last()]//span')
last_page = int(last_page.text)

while page_counter != last_page:
    for i in range(len(item_list)):
        a = driver.find_element_by_xpath(
            f'//ul[@class="scaffold-layout__list-container"]/child::li[{i + 1}]//div[contains(@class,"image")]')
        driver.execute_script("arguments[0].scrollIntoView();", a)
        a.click()
        time.sleep(3)

        n = os.path.join(r"C:\Users\tljubicic\OneDrive - A1 Group\Dokumente\html_parser", f"Job_{job_counter}.html")
        f = codecs.open(n, "w", "utf-8")
        h = driver.page_source
        f.write(h)

        job_counter = job_counter + 1
        wait_time = random.randrange(20,30)
        print(f'Number of jobs scraped: {job_counter}')
        time.sleep(wait_time)

    if page_counter != 8:
        next_page = driver.find_element_by_xpath(
            f'//div[contains(@class,"pagination")]/child::ul/li[@data-test-pagination-page-btn={page_counter + 1}]')
        driver.execute_script("arguments[0].scrollIntoView();", next_page)
        next_page.click()
        time.sleep(5)
    else:
        more_pages = driver.find_element_by_xpath(
            '//div[contains(@class,"pagination")]/child::ul/li/button/span[text()="…"]/parent::button')
        driver.execute_script("arguments[0].scrollIntoView();", more_pages)
        more_pages.click()
        time.sleep(5)


    page_counter = page_counter + 1

