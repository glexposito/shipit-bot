from dependency_injector import containers, providers

from services.release_service import ReleaseService


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the application.
    """

    # This allows you to inject configuration from files or environment variables.
    config = providers.Configuration()

    # Define how to create the ReleaseService.
    # It's a Singleton, so the same instance is used everywhere.
    release_service = providers.Singleton(ReleaseService)
