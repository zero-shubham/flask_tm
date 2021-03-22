from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load
)


class AuthLoginFormSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Regexp(regex='^([A-Za-z0-9]+_*)+')
    )
    password = fields.Str(required=True)
    grant_type = fields.Str(required=True)


class AuthLoginRespSchema(Schema):
    access_token = fields.Str(
        required=True
    )


class AuthLogoutRespSchema(Schema):
    logged_out = fields.Boolean(required=True)
