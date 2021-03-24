from flask.views import MethodView
from flask_smorest import (
    Blueprint,
    abort
)
from tm.users.models import (
    User
)
from tm.auth.schemas import (
    AuthLoginFormSchema,
    AuthLoginRespSchema,
    AuthLogoutRespSchema
)
from tm.core.security import (
    verify_password
)
from tm.core.jwt import (
    create_access_token
)
from uuid import (
    uuid4
)
from tm.containers.auth import (
    TokenUserContainer,
    TokenUserService
)
from dependency_injector.wiring import inject, Provide
from tm.auth.models import (
    BlacklistedToken
)
from datetime import datetime

auth_blp = Blueprint(
    'auth', 'auth', url_prefix='/auth',
    description='Operations related auth'
)


@auth_blp.route('/')
class Login(MethodView):

    @auth_blp.arguments(schema=AuthLoginFormSchema, location="form", as_kwargs=True)
    @auth_blp.response(status_code=200, schema=AuthLoginRespSchema)
    def post(self, **kwargs):
        """
        POST to login
        """
        user = User.get_by_user_name(
            user_name=kwargs["username"]
        )
        if not verify_password(
            kwargs["password"],
            user.password
        ):
            abort(401, message="User credentials don't match.")

        encoded_jwt, expire = create_access_token(
            data={
                "blacklist_id": str(uuid4()),
                "id": user.id,
                "group": user.group,
            }
        )

        return {
            "access_token": encoded_jwt.decode("utf-8")
        }

    @auth_blp.response(status_code=200, schema=AuthLogoutRespSchema)
    @auth_blp.doc(security=[{"OAuth2PasswordBearer": []}])
    @inject
    def delete(
        self,
        token_user_service: TokenUserService = Provide[TokenUserContainer.token_user_service]
    ):
        """
        DELETE to logout
        """
        # * check user exists
        token_user_service.get_token_user()

        decoded_token = token_user_service.get_decoded_token()

        new_blacklisted_token = BlacklistedToken(
            id=decoded_token["blacklist_id"],
            created_at=str(datetime.utcnow())
        )
        new_blacklisted_token.save()

        return {
            "logged_out": True
        }
