from dependency_injector import (
    containers,
    providers
)
from flask import (
    request,
    current_app
)


class TokenUserService:
    def __init__(self) -> None:
        super().__init__()

    def get_token(self):
        return request.headers.get("authorization")


class TokenUserContainer(containers.DeclarativeContainer):

    token_user_service = providers.Factory(
        TokenUserService
    )
