from .pages.start_page import StartPage
from .pages.base_page import BasePage
from .settings import host
import pytest
import numpy as np
import time

@pytest.mark.apiweb
class TestApiWeb():
    api_version = "api/"

    parametrize_list = [
        (1, "get", f'{host}{api_version}users?page=2', {}, []), (2, "get", f'{host}{api_version}users/2', {}, []),
        (3, "get", f'{host}{api_version}users/23', {}, []),     (4, "get", f'{host}{api_version}unknown', {}, []),
        (5, "get", f'{host}{api_version}unknown/2', {}, []),    (6, "get",  f'{host}{api_version}unknown/23', {}, []),
        (7, "post", f'{host}{api_version}users', {"name": "morpheus","job": "leader"}, ["name", "job"]),
        (8, "put", f'{host}{api_version}users/2', {"name": "morpheus","job": "zion resident"}, ["name", "job"]),
        (9, "patch", f'{host}{api_version}users/2', {"name": "morpheus","job": "zion resident"}, ["name", "job"]),
        (10, "delete", f'{host}{api_version}users/2', {}, []),
        (11, "post", f'{host}{api_version}register', {"email": "eve.holt@reqres.in","password": "pistol"}, ["id", "token"]),
        (12, "post", f'{host}{api_version}register', {"email": "sydney@fife"}, ["error"]),
        (13, "post", f'{host}{api_version}login', {"email": "eve.holt@reqres.in", "password": "cityslicka"}, ["token"]),
        (14, "post", f'{host}{api_version}login', {"email": "peter@klaven"}, ["error"]),   
        (15, "get", f'{host}{api_version}users?delay=3', {}, [])
    ]

    def equal_evals(self, eval_1, eval_2, keys=[]):
        """
        Args:
            params eval_1:  response from api
            params eval_2:  response from web
            params keys:    list of keys which one we must to check 
        """
        if len(eval_1.keys()) != len(eval_2.keys()):
            return False, "Len eval's not equal"

        if len(keys) != 0:
            for key in eval_1.keys():
                if eval_1[key] != eval_2[key]:
                    return False, f"Key: {key} is not equal"
            return True
        else:
            for key in keys:
                if eval_1[key] != eval_2[key]:
                    return False, f"Key: {key} is not equal"
            return True

    @pytest.mark.parametrize('num,method,url,body,keys', parametrize_list)
    def test_equal_web_and_api(self, browser, session, num, method, url, body, keys):
        page = StartPage(browser, host)
        page.open()

        page.click_on_method(num)
        page.should_be_active(num)

        response_body_web = page.get_response_body()
        response_code = page.get_response_code()

        match method:
            case "get":
                response = session.get(url)
            case "post":
                response = session.post(
                    url, data=body
                )
            case "put":
                response = session.put(
                    url, data=body
                )
            case "patch":
                response = session.patch(
                    url, data=body
                )
            case "delete":
                response  = session.delete(url)
                
        try:
            assert self.equal_evals(
                eval(response.text), eval(response_body_web), keys
                )
        except SyntaxError:
            response.text == response_body_web
            
        #assert eval(response.text) == eval(response_body_web)
        assert response.status_code == response_code
