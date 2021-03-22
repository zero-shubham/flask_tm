import mongoengine as me
from datetime import datetime
from uuid import (
    uuid4
)


class BlacklistedToken(me.Document):
    id = me.StringField(default=lambda: str(uuid4()), primary_key=True)
    created_at = me.DateTimeField(default=datetime.utcnow)

    @classmethod
    def get_blacklisted_token_by_id(
        cls,
        id: str
    ):
        result = cls.objects(
            id=id
        )
        if result:
            return result[0]
