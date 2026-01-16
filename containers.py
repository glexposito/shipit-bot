from dependency_injector import containers, providers

from services.dev_ops_service import DevOpsService


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the application.
    """

    # This allows you to inject configuration from files or environment variables.
    config = providers.Configuration()

    # Define how to create the DevOpsService.
    # It's a Singleton, so the same instance is used everywhere.
    dev_ops_service = providers.Singleton(DevOpsService)
