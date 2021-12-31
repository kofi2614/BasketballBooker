from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from credential import passwordTxt, usernameTxt
import sys
import time

book_month = str(sys.argv[1])
book_year = str(sys.argv[2])
print(book_month)
print(book_year)
time_list = ['19:00  to 20:00', '20:00  to 21:00', '21:00  to 22:00']
month_day = {"01": 31, "02": 28, "03": 31, "04": 30, "05": 31,
             "06": 30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31}

driver = webdriver.Chrome('../chromedriver')

driver.get('https://aquarius.iconconnect.ca/')

username = driver.find_element_by_xpath(
    '''//*[@id="app"]/div/div[3]/form/div/div[2]/div/input''')

password = driver.find_element_by_xpath(
    '''//*[@id="app"]/div/div[3]/form/div/div[4]/div/input''')
username.clear()
password.clear()
username.send_keys(usernameTxt)
password.send_keys(passwordTxt)
driver.find_element_by_css_selector(
    'button.ui.black.huge.basic.button').click()
time.sleep(2)
driver.find_element_by_css_selector(
    'button.ui.basic.primary.button').click()
driver.get('https://aquarius.iconconnect.ca/resident/booking/130/83')

for date in range(10, month_day[book_month]+1):
    if date < 10:
        date = f'0{date}'
    for timeselect in time_list:
        driver.refresh()
        try:
            driver.find_element_by_css_selector(
                'button.ui.basic.primary.button').click()
        except NoSuchElementException:
            driver.refresh()
            time.sleep(3)
            driver.find_element_by_css_selector(
                'button.ui.basic.primary.button').click()
        book_date = driver.find_element_by_name("bookingDate")
        textarea = driver.find_element_by_css_selector('textarea')
        book_date.click()                      # Focus input field
        book_date.send_keys(Keys.CONTROL, "a")
        book_date.send_keys(Keys.BACKSPACE)
        book_date.send_keys(f"{date}-{book_month}-{book_year}")
        textarea.click()
        time.sleep(0.5)
        book_time = driver.find_element_by_id('form-select-control-gender')
        book_time.click()
        book_time.send_keys(Keys.CONTROL, "a")
        book_time.send_keys(Keys.BACKSPACE)
        book_time.send_keys(timeselect)
        textarea.click()
        if driver.find_element_by_css_selector('p').text:
            break
        next = driver.find_elements_by_css_selector(
            'button.ui.basic.primary.button')[-1]
        driver.execute_script("arguments[0].click();", next)
        try:
            driver.find_element_by_css_selector('h4')
            confirm = driver.find_elements_by_css_selector(
                'button.ui.basic.primary.button')[-1]
            driver.execute_script("arguments[0].click();", confirm)
            time.sleep(3)
        except NoSuchElementException:
            continue
        try:
            driver.find_element_by_css_selector('div.label')
            continue
        except:
            break
driver.quit()
