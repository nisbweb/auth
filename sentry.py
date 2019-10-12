import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(
    dsn="https://d0687bae23d146239969f217d2b37d15@sentry.io/1777649",
    integrations=[FlaskIntegration()]
)
