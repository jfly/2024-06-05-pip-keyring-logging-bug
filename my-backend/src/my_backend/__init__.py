from keyring import backend, credentials
import logging

logger = logging.getLogger()


class JflyBackend(backend.KeyringBackend):
    priority = 9.9

    def get_credential(
        self,
        service: str,
        username: str | None,
    ) -> credentials.Credential | None:
        print("Hello from JflyBackend::get_credential. I'm about to log a message.")
        logger.debug("This is a debug message: %s", {"foo": 42})
        print("Successfully logged a message. Now I'm going to return a credential.")
        return credentials.SimpleCredential(
            username="fake-username",
            password="fake-password",
        )

    def get_password(self, service: str, username: str) -> str | None:
        return "fake-password"

    def set_password(self, service: str, username: str, password: str) -> None:
        raise NotImplementedError()

    def delete_password(self, service: str, username: str) -> None:
        raise NotImplementedError()
