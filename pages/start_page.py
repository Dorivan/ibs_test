from .base_page import BasePage
from .locators import BasePageLocators


class StartPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(StartPage, self).__init__(*args, **kwargs)

    def click_on_method(self, num):
        """
        :param num: int position method as index in list
        """
        li_element = self.browser.find_elements(*BasePageLocators.ENDPOINT_ELEMENT)[num-1]
        li_element.click()

    def get_request_url(self):
        return self.get_text_from_element(*BasePageLocators.REQUEST_URL)

    def get_request_body(self):
        return self.get_text_from_element(*BasePageLocators.REQUEST_URL)
    
    def get_response_code(self):
        return int(self.get_text_from_element(*BasePageLocators.RESPONSE_CODE))
    
    def get_response_body(self):
        return self.get_text_from_element(*BasePageLocators.RESPONSE_BODY)
    
    def get_all_endpoints(self):
        return self.browser.find_elements(*BasePageLocators.ENDPOINT_ELEMENT)

    def get_specific_endpoint(self, num):
        """
        :param num: int position method as index in list
        """
        return self.browser.find_elements(*BasePageLocators.ENDPOINT_ELEMENT)[num]

    def should_be_active(self, num):
        """
        :param num: int position method as item in DOM
        """
        return self.is_element_active(*BasePageLocators.ENDPOINT_ELEMENT, num)

    def should_be_endpoint_list(self):
        assert self.is_element_present(*BasePageLocators.ENDPOINT_LIST), "Endpoint list is not presented"

    def should_be_request_url(self):
        assert self.is_element_present(*BasePageLocators.REQUEST_URL), "Request url is not presented"

    def should_not_displayed_request_body(self):
        assert self.is_element_displayed(*BasePageLocators.REQUEST_BODY) == False, "Request body is presented"
        
    def should_be_request_body(self):
        assert self.is_element_present(*BasePageLocators.REQUEST_BODY), "Request body is not presented"

    def should_be_response_code(self):
        assert self.is_element_present(*BasePageLocators.RESPONSE_CODE), "Response code is not presented"

    def should_be_response_body(self):
        assert self.is_element_present(*BasePageLocators.RESPONSE_BODY), "Response body is not presented"
