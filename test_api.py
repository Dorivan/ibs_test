from .settings import GET_DICT, POST_DICT, UPDATE_DICT, ERROR_DICT, host

import requests
import pytest

@pytest.mark.api
class TestApiv1:
    api_version = "api/"


    test_uesrs = [
        ("Toran", "ds"),
        (5, "ds"),
        ("Toran", 5),
        (5, 5)
        # Эти тесты падают, из-за того, что можно создать пользователя 
        # с именем и работой в цифровом виде)
        # ("Toran", pytest.param(5, marks=pytest.mark.xfail)),
        # (pytest.param(5, marks=pytest.mark.xfail), "ds")
    ]


    @pytest.mark.get
    @pytest.mark.parametrize('dict_keys', GET_DICT.keys())
    def test_get_api(self, session, dict_keys):
        url = f'{host}{self.api_version}{GET_DICT[dict_keys]["end_point"]}'
        response = session.get(url)
        assert eval(response.text) == GET_DICT[dict_keys]['response']
        assert response.status_code == GET_DICT[dict_keys]['status_code']

    @pytest.mark.post
    @pytest.mark.parametrize('dict_keys', POST_DICT.keys())
    def test_post_api(self, session, dict_keys):
        url = f'{host}{self.api_version}{POST_DICT[dict_keys]["end_point"]}'
        response = session.post(
            url, data=POST_DICT[dict_keys]["body"]
        )
        assert eval(response.text) == POST_DICT[dict_keys]['response']
        assert response.status_code == POST_DICT[dict_keys]['status_code']

    @pytest.mark.post
    @pytest.mark.parametrize('name,job', test_uesrs)
    def test_create_user(self, session, name, job):
        user_dict = {
            "status_code": 201,
            "body": {
                "name": name, "job": job
                },
            "end_point": f"{self.api_version}users"
        }

        url = f'{host}{self.api_version}{user_dict["end_point"]}'
        response = session.post(
            url, data=user_dict["body"]
        )

        # Преобразование к str необходимо тк со стороны reqres.in при создании юзера
        # происходит преобразование всех данных к str, даже если отправить туда число
        assert eval(response.text)['name'] == str(user_dict['body']['name']) 
        assert eval(response.text)['job'] == str(user_dict['body']['job'])
        
        assert response.status_code == user_dict['status_code']
        assert response.reason == 'Created'

    @pytest.mark.update
    @pytest.mark.parametrize('dict_keys', UPDATE_DICT.keys())
    def test_update_data(self, session, dict_keys):
        url = f'{host}{self.api_version}{UPDATE_DICT[dict_keys]["end_point"]}'
        if UPDATE_DICT[dict_keys]["method"] == "put":
            response = session.put(
                url, data=UPDATE_DICT[dict_keys]["body"]
            )
        elif UPDATE_DICT[dict_keys]["method"] == "patch":
            response = session.patch(
                url, data=UPDATE_DICT[dict_keys]["body"]
            )
        if UPDATE_DICT[dict_keys]["updated_fields"] == "all":
            assert eval(response.text)['name'] == UPDATE_DICT[dict_keys]['body']['name']
            assert eval(response.text)['job'] == UPDATE_DICT[dict_keys]['body']['job']
        else:
            for field in UPDATE_DICT[dict_keys]["updated_fields"]:
                assert eval(response.text)[field] == UPDATE_DICT[dict_keys]['body'][field]

        assert response.status_code == UPDATE_DICT[dict_keys]['status_code']
        assert response.reason == 'OK'

    @pytest.mark.delete
    def test_delete(self, session):
        url = f'{host}{self.api_version}users/2'
        response = session.delete(url)
        assert response.status_code == 204
        assert response.text == ''


    @pytest.mark.xfail(reason="Error request about 'Missing email'")
    @pytest.mark.parametrize('dict_keys', ERROR_DICT.keys())
    def test_response_fails(self, session, dict_keys):
        url = f'{host}{self.api_version}{POST_DICT[dict_keys]["end_point"]}'
        response = session.post(
            url, data=POST_DICT[dict_keys]["body"]
        )
        assert eval(response.text) == POST_DICT[dict_keys]['response']
        assert response.status_code == POST_DICT[dict_keys]['status_code']
