class InfrastructureError(Exception):
    message = (
        "There was an unexpected infrastructure error,"
        " if this error persist contact support."
    )

    def __str__(self) -> str:
        return self.message


class EventPublisherError(InfrastructureError):
    def __init__(self, message: str):
        self.message = message


class FileStorageSaveError(InfrastructureError):
    def __init__(self, file_path: str, error: str):
        self.message = "Failed to upload {} with error {}".format(file_path, error)


class FileStorageGetError(InfrastructureError):
    def __init__(self, file_path: str, error: str):
        self.message = f"Failed to download {file_path} with error {error}"


class NoTopicFoundForGivenEvent(InfrastructureError):
    def __init__(self, event_name: str):
        self.message = "Could not find any topic registered for {}".format(event_name)


class NoTargetAsyncTaskForJobName(InfrastructureError):
    def __init__(self, job_name: str, available_tasks: dict, available_queues):
        self.message = (
            f"No target async task for job {job_name}. Available async tasks are"
            f" {available_tasks}. Available queues are {available_queues}"
        )


class NoConfigForTenant(InfrastructureError):
    def __init__(self, tenant_name):
        self.message = f"No config found for tenant {tenant_name}"


class UnknownChannelId(InfrastructureError):
    def __init__(self, channel_id):
        self.message = f"Unknown channel id {channel_id}"


class InvalidToken(InfrastructureError):
    def __init__(self, message: str = "Possible Header forgery attempt"):
        self.message = message
