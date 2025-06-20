# pip3 install selenium
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Class
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import time

import json
import math

# XPATH

FORM_CARD_XPATH     = '/html/body/app-root/vertical-layout/div/content/div/app-classinfo/div[2]'

# Specifier
SEARCH_BUTTON_XPATH = f'{FORM_CARD_XPATH}/div/div[2]/div[5]/button'
FACULTY_XPATH       = f'{FORM_CARD_XPATH}/div/div[2]/div[1]/ng-select/div/div/div[2]/input'
DEPARTMENT_XPATH    = f'{FORM_CARD_XPATH}/div/div[2]/div[2]/ng-select/div/div/div[2]/input'
SEMESTER_XPATH      = f'{FORM_CARD_XPATH}/div/div[1]/div[2]/div/div'
COURSE_XPATH        = f'{FORM_CARD_XPATH}/div/div[2]/div[3]/input'
YEAR_XPATH          = f'{FORM_CARD_XPATH}/div/div[1]/div[1]/div/ng-select/div/div/div[3]/input'

# Element
LOADING_XPATH       = '/html/body/app-root/vertical-layout/div/content/div/app-classinfo/ngx-loading/div'
TOTAL_RESULT_XPATH  = '/html/body/app-root/vertical-layout/div/content/div/app-classinfo/div[2]/ngx-datatable/div/datatable-footer/div/div'
DATATABLE_XPATH     = '/html/body/app-root/vertical-layout/div/content/div/app-classinfo/div[2]/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller'

# Nevigate
PAGE_NEVIGATE_XPATH = '/html/body/app-root/vertical-layout/div/content/div/app-classinfo/div[2]/ngx-datatable/div/datatable-footer/div/datatable-pager/ul'

LANG_MENU_XPATH   = '//*[@id="dropdown-flag"]'
LANG_DROPDOWN_XPATH = '/html/body/app-root/vertical-layout/app-navbar/div/ul[2]/li[1]/div'

DAY_MAP = {
    'จ.': 'จันทร์', 
    'อ.': 'อังคาร', 
    'พ.': 'พุธ', 
    'พฤ.': 'พฤหัส', 
    'ศ.': 'ศุกร์', 
    'ส.': 'เสาร์', 
    'อา.': 'อาทิตย์',
    'MON' : 'MON',
    'TUE' : 'TUE',
    'WED' : 'WED',
    'THU' : 'THU',
    'FRI' : 'FRI',
    'SAT' : 'SAT',
    'SUN' : 'SUN',
}

LANG = 'th'

def main():
    # instantiate options for Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    # instantiate Chrome WebDriver with options
    driver = webdriver.Chrome(options=options)

    # URL of the web page to scrape
    url = "https://reg2.kmutnb.ac.th/registrar/classinfo"

    # open the specified URL in the browser
    driver.get(url)

    reg_change_lang(driver, lang=2)

    result = reg_scrape(driver, course_id='080303701')

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    driver.quit()

def reg_scrape(driver: WebDriver, faculty_id=None, department_id=None, course_id=None, semester=None, year=None) -> list:

    if year != None:
        reg_select_year(driver, year)

    if faculty_id != None:
        reg_select_faculty(driver, faculty_id)

    if department_id != None:
        reg_select_department(driver, department_id)

    if semester != None:
        reg_select_semester(driver, semester)
    
    if course_id != None:
        reg_select_course(driver, course_id)

    reg_search(driver)

    print("Loading")

    reg_wait_loading(driver)

    print("Loaded")

    total_result = reg_get_total_result(driver)

    if total_result == 0: return

    print(f'{total_result} total result!')

    datas = []

    for _ in range(max(1, total_result//10)):

        datatable_rows = driver.find_elements(By.XPATH, f'{DATATABLE_XPATH}/*')

        for i, datatable_row in enumerate(datatable_rows):
            #test = datatable_row.find_elements(By.XPATH, './/*[@class="datatable-row-group"]')
            datatable_row = datatable_row.find_element(By.XPATH, './datatable-body-row/div[2]')

            data = reg_extract_data_from_row(datatable_row)

            datas.append(data)

            print(" ")
        
        if total_result > 10:
            reg_next_page(driver)
        
        reg_wait_loading(driver)

    return datas

def reg_wait_loading(driver):
    WebDriverWait(driver, 10).until(
        expected_conditions.none_of(
            expected_conditions.presence_of_element_located((By.XPATH, LOADING_XPATH))
        )
    )


def reg_change_lang(driver: WebDriver, lang=1):
    lang_button = driver.find_element(By.XPATH, LANG_MENU_XPATH)
    lang_button.click()

    drowdrop = driver.find_element(By.XPATH, f'{LANG_DROPDOWN_XPATH}/a[{lang}]')
    drowdrop.click()

    reg_wait_loading(driver)
    
def reg_select_year(driver: WebDriver, year):
    year_field = driver.find_element(By.XPATH, YEAR_XPATH)

    if year_field == None: return

    year_field.click()
    year_field.send_keys(year)
    year_field.send_keys(Keys.ENTER)
    

def reg_extract_data_from_row(row: WebElement):
    row_elements = row.find_elements(By.XPATH, './*')

    course_id   = row_elements[0].text

    course_name = row_elements[1].text.split('\n')[0]
    instuctors  = row_elements[1].text.split('\n')[1:]

    credits_raw = row_elements[2].text

    credits     = int(credits_raw.split('(')[0])
    section     = int(row_elements[3].text)

    total_seats     = int(row_elements[4].text)
    enrolled_seats  = int(row_elements[5].text)
        
    level = row_elements[8].text
    course_status = row_elements[9].text

    class_schedule_raw  = row_elements[6].text
    
    exam_date_raw       = row_elements[7].text

    print(course_id)
    print(course_name)
    print(instuctors)
    print(credits)
    print(section)

    print(total_seats)
    print(enrolled_seats)
    print(class_schedule_raw)
    print(exam_date_raw)
    print(level)
    print(course_status)

    class_schedule_raw_splited  = class_schedule_raw.split('\n')

    class_schedule = []

    if len(class_schedule_raw) != 0:
        for i in range(0, len(class_schedule_raw_splited), 2):

            class_schedule_date = class_schedule_raw_splited[i].split(' ')

            class_schedule.append({
                "room": class_schedule_raw_splited[i+1].split(' ')[1],
                "day": DAY_MAP[class_schedule_date[1]],
                "from"  : class_schedule_date[2].split('-')[0],
                "until" : class_schedule_date[2].split('-')[1]
            })

    # print(class_schedule)

    exam_date_raw_midterm   = exam_date_raw.split('\n')[1].split(' ')
    exam_date_raw_final     = exam_date_raw.split('\n')[3].split(' ')

    exam_date = {
        'midterm': None,
        'final': None,
    }

    if len(exam_date_raw_midterm) != 1:
        exam_date['midterm'] =  {
            "date": exam_date_raw_midterm[0],
            "from"  : exam_date_raw_midterm[1].split('-')[0],
            "until"  : exam_date_raw_midterm[1].split('-')[1]
        }
    
    if len(exam_date_raw_final) != 1:
        exam_date['final'] = {
            "date": exam_date_raw_final[0],
            "from"  : exam_date_raw_final[1].split('-')[0],
            "until"  : exam_date_raw_final[1].split('-')[1]
        }

    # print(exam_date)

    data = {
        "course_id": course_id,
        "course_name": course_name,
        "instuctors": instuctors,
        "credits": credits,
        "section": section,
        "total_seats": total_seats,
        "enrolled_seats": enrolled_seats,
        "class_schedule": class_schedule,
        "exam_date": exam_date
    }

    return data

def reg_prev_page(driver: WebDriver):
    prev_button = driver.find_element(By.XPATH, '//a[@aria-label="go to previous page"]')

    if prev_button == None: return

    prev_button.click()

def reg_next_page(driver: WebDriver):
    next_button = driver.find_element(By.XPATH, '//a[@aria-label="go to next page"]')

    if next_button == None: return

    next_button.click()

def reg_get_total_result(driver: WebDriver):
    total_result_raw = driver.find_element(By.XPATH, TOTAL_RESULT_XPATH).text

    total_result = int(total_result_raw.split(' ')[0].replace(',', ''))

    return total_result

def reg_select_course(driver: WebDriver, course_id):
    course_field = driver.find_element(By.XPATH, COURSE_XPATH)

    if course_field == None: return

    course_field.click()
    course_field.send_keys(course_id)
    course_field.send_keys(Keys.ENTER)

def reg_select_semester(driver: WebDriver, semester):
    semester_button = driver.find_element(By.XPATH, f'{SEMESTER_XPATH}/label[{semester}]')

    if semester_button == None: return

    semester_button.click();

def reg_select_faculty(driver: WebDriver, faculty_id):
    faculty_field = driver.find_element(By.XPATH, FACULTY_XPATH)

    if faculty_field == None: return

    faculty_field.click()
    faculty_field.send_keys(faculty_id)
    faculty_field.send_keys(Keys.ENTER)

def reg_select_department(driver: WebDriver, department_id):
    department_field = driver.find_element(By.XPATH, DEPARTMENT_XPATH)

    if department_field == None: return

    department_field.click()
    department_field.send_keys(department_id)
    department_field.send_keys(Keys.ENTER)

def reg_search(driver):
    # List all buttons present on the page
    button = driver.find_element(By.XPATH, SEARCH_BUTTON_XPATH)

    if button == None:
        print("Search button is not found!")
        return;

    button.click()

if __name__ == "__main__":
    main()

