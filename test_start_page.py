from .pages.start_page import StartPage
from .settings import host
import pytest
import numpy as np
import random

@pytest.mark.web
class TestStartPage():
    values_methods = []
    values_methods.append(pytest.param(-1, marks=pytest.mark.xfail))
    values_methods.extend(np.array(range(0, 15)).tolist())
    values_methods.append(pytest.param(16, marks=pytest.mark.xfail))

    def test_request_block(self, browser):
        page = StartPage(browser, host)
        page.open()

        page.should_not_displayed_request_body()
        page.should_be_request_url()
        
        # интересно, а тут баг в момент проверки этого условия status code = 200, а вот в Request url
        # Уже /api/unknown, а не /api/users?page=2
        assert page.get_request_url() == '/api/users?page=2' # 

    def test_response_block(self, browser):
        page = StartPage(browser, host)
        page.open()

        page.should_be_response_body()
        page.should_be_response_code()

        assert int(page.get_response_code()) == 200, "Status code is not equal, must be 200"

    def test_endpoint_block(self, browser):
        page = StartPage(browser, host)
        page.open()

        page.should_be_endpoint_list()
        page.should_be_active(1) 
    
    # Закомментировал проход по всем элементам, тк проверил в отдельном классе
    # где совместно проверял web + api
    #@pytest.mark.parametrize('num', values_methods)
    def test_endpoint_click(self, browser):
        # Возьмем случайный пример из сгенерированного списка
        num = self.values_methods[(random.randint(0, 17))]

        page = StartPage(browser, host)
        page.open()

        page.click_on_method(num)
        page.should_be_active(num)
