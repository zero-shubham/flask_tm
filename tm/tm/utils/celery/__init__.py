import os
from main import (
    celery,
    create_app
)
from tm.auth.models import (
    BlacklistedToken
)
from datetime import (
    datetime,
    timedelta
)
from tm.utils.celery.tasks import (
    auth
)


app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.app_context().push()
