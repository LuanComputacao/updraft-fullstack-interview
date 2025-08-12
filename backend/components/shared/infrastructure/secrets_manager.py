import json
from typing import Optional

from environs import EnvError

from components.shared.application.base import SecretManagerInterface
from components.shared.infrastructure import errors
from components.shared.infrastructure.logger import logger
from components.shared.infrastructure.os import env
from components.shared.infrastructure.tenant import TenantResolver


class SecretsManager(SecretManagerInterface):
    def __init__(
        self,
        tenant_resolver: Optional[TenantResolver] = None,
    ):
        self._tenant_resolver = tenant_resolver if tenant_resolver else TenantResolver()

    def _load_tenant_secrets(self, tenant):
        try:
            tenant_env_var = tenant.replace(".", "").upper()
            secret_env_var = env(tenant_env_var)
            return json.loads(secret_env_var)
        except EnvError as err:
            logger.exception(
                f"Hiding secret manager error: {err}", exc_info=err.__traceback__
            )
            raise errors.NoConfigForTenant(tenant_name=tenant)

    def get_tenant_secrets(self) -> dict:
        tenant = self._tenant_resolver.get_current_tenant()
        return self._load_tenant_secrets(tenant=tenant)

    def get_shared_secret(self, secret_key, default: any = None) -> any:
        try:
            secret = env(secret_key)
            return secret
        except EnvError:
            logger.exception(f"Could not get shared secret")
            if default is not None:
                return default
            raise


secrets_manager = SecretsManager()
