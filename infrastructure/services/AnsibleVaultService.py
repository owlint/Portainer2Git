from ansible_vault import Vault


class AnsibleVaultService:
    def __init__(self, password: str):
        self.__vault = Vault(password)

    def encrypt(self, data: str):
        return self.__vault.dump(data)
