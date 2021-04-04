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

    @classmethod
    def get_blacklisted_token_by_max_min_created_at(
        cls,
        min_created_at,
        max_created_at
    ):
        result = cls.objects(
            created_at__lte=min_created_at,
            created_at__gte=max_created_at
        )
        return result

    @classmethod
    def delete_blacklisted_token_by_id(
        cls,
        id: str
    ):
        blacklisted_token = cls.get_blacklisted_token_by_id(
            id
        )
        deleted = blacklisted_token.delete()
        blacklisted_token_exists = cls.get_blacklisted_token_by_id(
            id
        )

        return True if not blacklisted_token_exists else False
