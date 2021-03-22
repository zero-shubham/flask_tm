import mongoengine as me
from datetime import datetime
from enum import Enum
from uuid import (
    uuid4
)
from tm.users.schemas import (
    UserSchema
)


class UserGroupEnum(str, Enum):
    super_admin = 'super_admin'
    teacher = 'teacher'
    student = 'student'


class User(me.Document):
    id = me.StringField(default=lambda: str(uuid4()), primary_key=True)
    user_name = me.StringField(regex='^([A-Za-z0-9]+_*)+', required=True)
    password = me.StringField(required=True)
    group = me.EnumField(UserGroupEnum, required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    @classmethod
    def get_by_id(
        cls,
        id: str
    ):
        result = cls.objects(
            id=id
        )
        if result:
            return result[0]

    @classmethod
    def get_by_user_name(
        cls,
        user_name: str
    ):
        result = cls.objects(
            user_name=user_name
        )
        if result:
            return result[0]


def add_new_user(
    details: UserSchema
) -> User:
    new_user = User(**dict(details))
    new_user.save()
    return new_user
