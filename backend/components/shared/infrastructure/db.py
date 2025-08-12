from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from components.shared.infrastructure.secrets_manager import secrets_manager


def get_postgres_uri(sm=secrets_manager) -> str:
    secrets = sm.get_tenant_secrets()
    db_secrets = secrets["database"]
    host = db_secrets["host"]
    user = db_secrets["user"]
    password = db_secrets["password"]
    port = db_secrets["port"]
    db_name = db_secrets["db_name"]

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class TenantAwareSessionFactory(sessionmaker):
    def __call__(self, **kwargs):
        # Call get_postgres_uri() to get the URI for the current tenant
        uri = get_postgres_uri()
        engine = create_engine(
            uri, isolation_level="REPEATABLE READ", poolclass=NullPool
        )

        # Bind the engine to the session's configuration
        kwargs["bind"] = engine
        return super(TenantAwareSessionFactory, self).__call__(**kwargs)


def scoped_session_factory():
    def factory():
        return scoped_session(TenantAwareSessionFactory())

    return factory


DEFAULT_SESSION_MAKER = scoped_session_factory()
