from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

import undetected_chromedriver as uc

from time import sleep
import os

from core.models import Product

def path_for_file_saving(dir, file):
    return os.path.join(dir, file)

def selenium_get(url, next_page, html_content_1='', html_content_2=''):
    driver = None
    html_content = ''

    try:
        current_app_dir = os.getcwd() # app
        current_dir = os.path.dirname(os.path.abspath(__file__)) # app/testparser
        static_dir = os.path.join(current_dir, 'static') # app/testparser/static

        with open(path_for_file_saving(static_dir, 'blank.html'), 'w') as f:
            f.write(f'<a href="{url}" target="_blank">link</a>')

        driver = uc.Chrome(
                headless=False,
                use_subprocess=False,
                driver_executable_path='/usr/lib/chromium/chromedriver'
                )
        driver.get(f'file://{static_dir}/blank.html')

        sleep(10)
        driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_connection1.png'))

        # and then you can click to the link and open your target URL
        links = driver.find_elements(By.XPATH, "//a[@href]")
        if links:
            links[0].click()

            # after opening the URL, we need to sleep during cloudflare chacking the browser
            sleep(15)
            driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_connection2.png'))

            # and last step: switch the driver to second tab in the browser
            # it's need for managing page by the driver
            driver.switch_to.window(driver.window_handles[1])

            # take a screenshot to /app dir
            driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_connection3.png'))

        driver.get(url)

        # element = driver.find_element(By.CLASS_NAME, "oe7")
        element = driver.find_element(By.XPATH, "//*[@id='layoutPage']/div[1]/div[5]/div/div/div[2]/div[3]")

        action = ActionChains(driver)
        action.scroll_to_element(element).perform()
        sleep(4)
        html_content_1 = element.get_attribute('innerHTML')

        with open(path_for_file_saving(static_dir, 'html_content.html'), 'w') as file:
            file.write(html_content_1)
        driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_page1.png'))

        if next_page == True:
            # element = driver.find_element(By.XPATH, "//a[@class='eo' and text()='2']")
            element = driver.find_element(By.XPATH, "//*[@id='layoutPage']/div[1]/div[5]/div/div/div[2]/div[3]/div[2]/div/div/div/a[2]")

            action.click(element).perform()
            sleep(4)
            # element = driver.find_element(By.CLASS_NAME, "eo7")
            element = driver.find_element(By.XPATH, "//*[@id='layoutPage']/div[1]/div[5]/div/div/div[2]/div[3]")
            action.scroll_to_element(element).perform()
            sleep(4)
            html_content_2 = element.get_attribute('innerHTML')

            with open(path_for_file_saving(static_dir, 'html_content2.html'), 'w') as file:
                file.write(html_content_2)
            driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_page2.png'))

        html_content = html_content_1 + html_content_2

    except (TimeoutException, WebDriverException):
        driver.save_screenshot(path_for_file_saving(static_dir, 'ozon_error.png'))
        for entry in driver.get_log('browser'):
            print(f"Browser Log: {entry}")
    finally:
        if driver:
            driver.quit()
        if not html_content:
            raise ('Html content пуст! Проверь не поменялись ли теги и посмотри скриншоты!')
        return html_content


def data_save_db(data_list):
    products = []

    for data_dict in data_list:
        product = Product(
            name=data_dict['name'],
            price=data_dict['price'],
            description=data_dict['description'],
            image_url=data_dict['image_url'],
            discount=data_dict['discount']
        )
        products.append(product)

    objects = Product.objects.bulk_create(products)
    return objects

