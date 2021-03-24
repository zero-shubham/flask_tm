import click
from flask.cli import (
    with_appcontext
)
from tm.users.models import (
    add_new_user
)
from tm.users.schemas import (
    UserSchema
)
from tm.utils.core.security import (
    get_password_hash
)
from uuid import (
    uuid4
)
from datetime import datetime
import pytz


@click.command("create_super_admin")
@click.argument("user_name")
@click.argument("password")
@with_appcontext
def create_super_admin(user_name, password):
    user_schema = UserSchema()
    user_details = user_schema.load(
        {
            "user_name": user_name,
            "password": password,
            "group": "super_admin",
            "updated_at": str(datetime.utcnow())
        }
    )
    added_user = add_new_user(
        user_details
    )
    print(
        f"Added super_admin with id: {added_user.id}"
    )
