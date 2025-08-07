class ResourceNotFound(RuntimeError):
    resource = None

    def __init__(self, resource: dict):
        self.message = "Could not find resource {}".format(resource)

    def __str__(self) -> str:
        return self.message
