import allure
import pytest
from http import HTTPStatus
from assertions import assert_status_code, assert_contains_key, assert_equal, assert_not_equal
from accounts.account_requests import create_account_request, get_account_by_id_request, delete_account_request, \
    get_accounts_list_request, patch_account_request, account_factory, get_account_by_type


@pytest.mark.parametrize("account_type", ["ipmi", "snmpv3", "snmpv2c"])
@allure.feature('Accounts')
@allure.story('Accounts API')
class TestAccounts:
    account_responses = []  # Список для хранения ответов от POST-запросов


    @allure.title('Create account')
    def test_create_account(self, client, account_type):
        account_data = account_factory(account_type)
        response = create_account_request(client, account_data)

        assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
        json_response = response.json()

        # Проверка полей и значений ответа
        assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе
        self.account_responses.append(json_response)  # Сохраняем ответ для будущего сравнения

        for key in ["name", "type", "data"]:
            assert_equal(json_response[key], getattr(account_data, key))

    @allure.title('Get account by id')
    def test_get_account_by_id(self, client, account_type):
        # Проверяем, что есть аккаунты для проверки
        assert self.account_responses, "No accounts to check"

        account = get_account_by_type(account_type, account_responses=self.account_responses)
        post_id = account["id"]
        response = get_account_by_id_request(client, post_id)
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        get_response = response.json()

        # Сравнение ответа от GET с данными от POST
        assert_equal(get_response["id"], post_id)  # Проверяем совпадение идентификатора
        # Сравниваем остальные ключи
        for key in ["name", "type", "data"]:
            assert_equal(get_response[key], account[key])

    @allure.title('Get accounts list')
    def test_get_accounts_list(self, client, account_type):
        response = get_accounts_list_request(client)

        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        get_response = response.json()

    @allure.title('Update account')
    @pytest.mark.parametrize("new_type", ["ipmi", "snmpv3", "snmpv2c"])
    def test_update_account(self, client, account_type, new_type):
        account = get_account_by_type(account_type, account_responses=self.account_responses)
        post_id = account["id"]
        # Обновляем тип аккаунта
        account_data = account_factory(new_type)
        response = patch_account_request(client, account_data, post_id)
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        patch_response = response.json()

        for key in ["name", "type", "data"]:
            assert_equal(patch_response[key], getattr(account_data, key))

        # Сравнение ответа от GET с данными от POST
        assert_equal(patch_response["id"], post_id)  # Проверяем совпадение идентификатора
        assert_not_equal(patch_response,account)

    @allure.title('Delete account')
    def test_delete_account(self, client, account_type):
        # Проверяем, что есть аккаунты для удаления
        assert self.account_responses, "No accounts to delete"

        account = get_account_by_type(account_type, account_responses=self.account_responses)
        post_id = account["id"]
        response = delete_account_request(client, post_id)
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа

    @allure.title('Get account by id after delete')
    def test_get_account_after_delete(self, client, account_type):
        # Проверяем, что есть аккаунты для проверки после удаления
        assert self.account_responses, "No accounts to check after deletion"

        account = get_account_by_type(account_type, account_responses=self.account_responses)
        post_id = account["id"]
        response = get_account_by_id_request(client, post_id)
        assert_status_code(response, HTTPStatus.NOT_FOUND)



 ### Негативные тесты
    @pytest.mark.parametrize("field, expected_error", [
        ("name", None),  # Убираем имя
        ("type", None),  # Убираем тип
        ("data", None),  # Убираем data
    ])
    @allure.title('Create account with missing fields')
    def test_create_account_missing_fields(self, client, field, expected_error, account_type):
        account_data = account_factory(account_type)  # Создаем аккаунт с валидными данными
        setattr(account_data, field, expected_error)  # Убираем значение у указанного поля
        response = create_account_request(client, account_data)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа


    # @allure.title('Create account with invalid parameters')
    # def test_create_account_invalid_parameters(self, client):
    #     account_data = account_factory("ipmi")  # Создаем аккаунт с валидными данными
    #     account_data.type = 'invalid_type'  # Убираем имя
    #     response = create_account_request(client, account_data)
    #
    #     assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
    #
    @allure.title('Get account by non-existent id')
    def test_get_account_by_non_existent_id(self, client, account_type):
        non_existent_id = "1234567890"
        response = get_account_by_id_request(client, non_existent_id)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
    #
    @allure.title('Delete non-existent account')
    def test_delete_non_existent_account(self, client, account_type):
        non_existent_id = "00000000"
        response = delete_account_request(client, non_existent_id)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа



    # @pytest.mark.parametrize("field, expected_error", [
    #     ("name", None),  # Убираем имя
    #     ("type", None),  # Убираем тип
    #     ("data", None),  # Убираем data
    # ])
    # @allure.title('Update account with missing fields')
    # def test_update_account_missing_fields(self, client):
    #     if not self.account_responses:  # Проверяем наличие созданных аккаунтов
    #         pytest.skip("Нет аккаунтов для обновления")
    #
    #     account_data = account_factory("snmpv3")  # Создаем аккаунт с валидными данными
    #     account_id = self.account_responses[0]["id"]  # Получаем ID существующего аккаунта
    #
    #     setattr(account_data, field, expected_error)  # Убираем значение у указанного поля
    #     response = patch_account_request(client, account_data, account_id)
    #
    #     assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответ