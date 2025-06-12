import time

from azure.identity import DefaultAzureCredential
from django.db.backends.postgresql import base


class DatabaseWrapper(base.DatabaseWrapper):
    """
    Wrap the Postgres engine to support Azure passwordless login
    https://learn.microsoft.com/en-us/azure/developer/intro/passwordless-overview

    This involves fetching a token at runtime to use as the database password.

    The consequence of this is our database credentials aren't static - they
    expire. We therefore need to ensure that every new connection
    checks the expiry date, and fetches a new one if necessary.

    Unless you disable persistent connections, each thread will maintain its own
    connection.
    Since Django 5.1 it is possible to configure a connection pool
    instead of using persistent connections, but that would require us to
    fix the credentials.
    See https://docs.djangoproject.com/en/5.2/ref/databases/#persistent-connections
    for more details of how this works.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = None
        self.azure_credential = None

    def _get_azure_connection_password(self) -> str:
        self.azure_credential = self.azure_credential or DefaultAzureCredential()

        if not self.access_token or self.access_token.expires_on - 300 < time.time():
            self.access_token = self.azure_credential.get_token(
                "https://ossrdbms-aad.database.windows.net/.default"
            )

        return self.access_token.token

    def get_connection_params(self) -> dict:
        params = super().get_connection_params()
        if params.get("host", "").endswith(".database.azure.com"):
            params["password"] = self._get_azure_connection_password()
        return params
