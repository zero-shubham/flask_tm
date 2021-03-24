from dependency_injector import (
    containers,
    providers
)
from flask import (
    request,
    current_app
)
from tm.utils.core.jwt import (
    decode_access_token
)
from tm.users.models import (
    User
)
from flask_smorest import (
    abort
)
from tm.auth.models import (
    BlacklistedToken
)


class TokenUserService:
    def __init__(self) -> None:
        super().__init__()

    def get_token(self):
        return request.headers.get("authorization")

    def get_decoded_token(self) -> dict:
        decoded_token = None
        token = self.get_token()
        _, token = token.split(" ")

        try:
            decoded_token = decode_access_token(
                token
            )
        except Exception as e:
            abort(401, message="Invalid token.")

        already_blacklisted = BlacklistedToken.get_blacklisted_token_by_id(
            decoded_token["blacklist_id"]
        )
        if already_blacklisted:
            abort(
                401,
                message="Blacklisted token."
            )

        return decoded_token

    def get_token_user(self) -> User:
        decoded_token = self.get_decoded_token()
        user = User.get_by_id(
            decoded_token["id"]
        )
        if not user:
            abort(401, message="Invalid token.")
        return user


class TokenUserContainer(containers.DeclarativeContainer):

    token_user_service = providers.Factory(
        TokenUserService
    )
