from main import(
    celery,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USERNAME
)
from tm.auth.models import (
    BlacklistedToken
)
from datetime import (
    datetime,
    timedelta
)
from celery.schedules import crontab
from mongoengine import connect


@celery.task
def remove_outdated_blacklisted_token():

    now = datetime.utcnow()
    past_7_hrs = now-timedelta(hours=7)
    past_1_day = now-timedelta(days=1)

    tokens = BlacklistedToken.get_blacklisted_token_by_max_min_created_at(
        past_7_hrs,
        past_1_day
    )
    now = datetime.utcnow()

    for token in tokens:
        token_to_exp = token.created_at+timedelta(hours=6)
        if now >= token_to_exp:
            BlacklistedToken.delete_blacklisted_token_by_id(
                token.id
            )


celery.conf.beat_schedule = {
    "run-every-3-hours": {
        "task": f"{__name__}.remove_outdated_blacklisted_token",
        "schedule": crontab(minute=0, hour='*/3')
    },
}
