from http import HTTPStatus

from assertions import assert_status_code, assert_contains_key, assert_equal
from config import BASE_URL
from authentication_api import get_token
from .model_accounts import CreateAccount


def account_factory(account_type):
    return CreateAccount(account_type)

def get_account_by_type(account_type, account_responses):
    """Helper method to find an account by its type."""
    for account in account_responses:
        if account["type"] == account_type:
            return account
    return None


def create_and_return_account(client, account_type):
    """Helper method to create an account and return the response."""
    account_data = account_factory(account_type)
    response = create_account_request(client, account_data)
    assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
    json_response = response.json()

    # Проверка полей и значений ответа
    assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе

    for key in ["name", "type", "data"]:
        assert_equal(json_response[key], getattr(account_data, key))

    return json_response["id"], account_data

def create_account_request(client, account_data):
    """Создание запроса для создания аккаунта."""
    token = get_token(client)
    response = client.post(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
        json=account_data.to_dict()
    )
    return response

def patch_account_request(client, account_data, account_id):
    """Создание запроса для изменения аккаунта."""
    token = get_token(client)
    response = client.patch(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
        json=account_data.to_dict()
    )
    return response

def get_account_by_id_request(client, account_id):
    """Создание запроса для получения аккаунта по ID."""
    token = get_token(client)
    response = client.get(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
    )
    return response

def delete_account_request(client, account_id):
    """Создание запроса для удаления аккаунта по ID."""
    token = get_token(client)
    response = client.delete(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
    )
    return response

def get_accounts_list_request(client):
    """Создание запроса для получения списка аккаунтов."""
    token = get_token(client)
    response = client.get(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
    )
    return response


