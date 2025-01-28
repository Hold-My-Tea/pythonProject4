
from fakers import random_string


class CreateAccount:
    def __init__(self, account_type: str):
        self.name = random_string()
        self.type = account_type
        self.data = {}

        self.set_data(account_type)

    def set_data(self, account_type: str):
        if account_type == "ipmi":
            self.data = {
                "username": random_string(),
                "auth_password": random_string()
            }
        elif account_type == "snmpv3":
            self.data = {
                "username": random_string(),
                "security_level": "noauth",  # Можно изменить на другой уровень безопасности
                "context_name": "",
                "auth_password": "",
                "auth_encryption": "",
                "privacy_password": "",
                "privacy_encryption": ""
            }
        elif account_type == "snmpv2c":
            self.data = {
                "community": random_string()
            }
        else:
            raise ValueError(f"Unknown account type: {account_type}")

    def to_dict(self):
        """Преобразует объект в словарь для сериализации в JSON."""
        return {
            "name": self.name,
            "type": self.type,
            "data": self.data
        }



# if __name__ == "__main__":
#     # Создание аккаунта IPMI
#     ipmi_account = CreateAccount("ipmi")
#     print(ipmi_account.__dict__)
#
#     # Создание аккаунта SNMPv3
#     snmpv3_account = CreateAccount("snmpv3")
#     print(snmpv3_account.__dict__)
#
#     # Создание аккаунта SNMPv2c
#     snmpv2c_account = CreateAccount("snmpv2c")
#     print(snmpv2c_account.__dict__)

























