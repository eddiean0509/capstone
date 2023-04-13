import os

BASE_DIR = os.path.dirname(__file__)


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'eblog.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask wtf
SECRET_KEY = "dev"

# api session sharing
# SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

# auth0
AUTH0_DOMAIN = "dev-hpy3w0iqgvxjbq0p.us.auth0.com"
AUTH0_ALGORITHMS = ["RS256"]
API_AUDIENCE = "eblog"
