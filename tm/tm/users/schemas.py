from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load
)
from tm.core.security import (
    get_password_hash
)
import pytz


class UserSchema(Schema):
    id = fields.UUID(required=True)
    user_name = fields.Str(
        required=True,
        validate=validate.Regexp(regex='^([A-Za-z0-9]+_*)+')
    )
    password = fields.Str(required=True)
    group = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=["super_admin", "teacher", "student"]
        )
    )
    created_at = fields.AwareDateTime(
        default_timezone=pytz.utc,
        required=True
    )
    updated_at = fields.AwareDateTime(
        default_timezone=pytz.utc,
        required=True
    )

    @pre_load
    def hash_password(self, in_data: dict, **kwargs):
        in_data["password"] = get_password_hash(in_data["password"])
        return in_data

    class Meta:
        load_only = ["password"]
        dump_only = ["created_at", "id"]
