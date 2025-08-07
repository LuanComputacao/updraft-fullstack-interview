from typing import Optional, Any
from environs import Env

class ParameterStore:
    def __init__(self):
        self._env = Env()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._env(key, default) if default is not None else self._env(key)

default_parameter_store = ParameterStore()
