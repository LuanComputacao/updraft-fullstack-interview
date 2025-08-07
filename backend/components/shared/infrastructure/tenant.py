import threading
from flask import Request

from components.shared.application.base import TenantResolverInterface

_tenant_local = threading.local()


def set_current_tenant(tenant):
    _tenant_local.tenant = tenant


def get_current_tenant():
    return getattr(_tenant_local, "tenant", None)


def get_tenant_from_http_request(request: Request):
    tenant = request.headers.get("X-Updraft-Tenant", None)
    return tenant


def get_tenant_from_path(request: Request):
    tenant = request.host
    return tenant


class TenantResolver(TenantResolverInterface):
    def get_current_tenant(self):
        return get_current_tenant()
