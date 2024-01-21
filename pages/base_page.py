from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators
import time


class BasePage:
    def __init__(self, browser, url, timeout=2):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def get_text_from_element(self, by, selector):
        self.waits_for_load_response()
        return self.browser.find_element(by, selector).text
    
    def is_element_present(self, by, selector):
        try:
            self.browser.find_element(by, selector)
        except NoSuchElementException:
            return False
        return True

    def waits_for_load_response(self, timeout=5):
        for i in range(timeout):
            self.browser.implicitly_wait(0)
            # Если идет процесс загрузки, то ожидаем пока крутится спинер
            is_displayed = self.is_element_displayed(*BasePageLocators.SPINNER)
            if not is_displayed:
                break
            else:
                time.sleep(1)
        # Можно еще ожидание добавить, но не пригодилось 
        #self.browser.implicitly_wait(timeout)

    def is_element_active(self, by, selector, num):
        try:
            class_name = self.browser.find_element(by, str(selector) + f'[{num}]').get_attribute("class")
            if class_name == 'active':
                return True
            else:
                return False
        except NoSuchElementException:
            return False
    
    def is_element_displayed(self, by, selector):
        try:
            element = self.browser.find_element(by, selector)
            if element.is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def is_not_element_present(self, how, what, timeout=2):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False
