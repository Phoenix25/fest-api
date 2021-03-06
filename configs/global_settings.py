import os, sys, django, random
gettext = lambda s: s


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hz3@sbz0q+wb&irbyn0h)cu9+9t7ofh@1tn3s!^)xia8_u$2+4' # Good practice to have one more in local settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DAJAXICE_DEBUG = DEBUG

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
PYTHON_VERSION = '%s.%s' % sys.version_info[:2]
DJANGO_VERSION = django.get_version()

ALLOWED_HOSTS = ['*']


#Absolute URL where the site has been hosted. Don't forget the trailing slash.
SITE_URL = 'http://localhost:8000/'

LOGIN_URL = 'login'

# -------------------------------------------------------------------
# Apps
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)
THIRD_PARTY_APPS = (
    # For development ease of use
    'south',
    'debug_toolbar',
    'django_extensions',
    
    # ajax functionality
    'dajaxice',
    'dajax',
    
    # For programming ease
    'post_office',
    'annoying',

    # Notification
    'notifications',

    # Social Auth Login
    'social.apps.django_app.default',

    # Markdown for text area candy
    'markdown_deux',

    # Search Indexer
    # 'haystack',
)
API_APPS =(
    'misc',
    'apps.home', 
    'apps.users',
    'apps.walls',
    'apps.events',
    'apps.docs',
    'apps.portals.applications.core',
    'apps.portals.applications.coord',
    'apps.portals.applications.account',
    'apps.portals.applications.application_portal',
)
INSTALLED_APPS =  DJANGO_APPS + THIRD_PARTY_APPS + API_APPS

# -------------------------------------------------------------------
# Various configs
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)
MIDDLEWARE_CLASSES = (
    'annoying.middlewares.StaticServe',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'apps.users.backends.RootBackend', # custom default password
)

ROOT_URLCONF = 'configs.urls'
WSGI_APPLICATION = 'configs.wsgi.application'

# Explicit settings patch for debug_toolbar for Django 1.6
# http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
# DEBUG_TOOLBAR_PATCH_SETTINGS = False

#AUTH_PROFILE_MODULE = 'apps.portals.applications.account.UserProfile'
# Database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(PROJECT_PATH, 'db.sqlite3'),
#    }
#}

# -------------------------------------------------------------------
# Internationalization
LANGUAGE_CODE = 'en-IN'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'N j, Y'
DATETIME_FORMAT = 'P, N j, Y'
TIME_FORMAT = '%H:%M'
DATE_INPUT_FORMATS = (
    # '%b %d %Y',       # 'Oct 25 2006'
    # '%b %d, %Y',      # 'Oct 25, 2006'
    # '%d %b %Y',       # '25 Oct 2006'
    '%d %b, %Y',      # '25 Oct, 2006'
    # '%B %d %Y',       # 'October 25 2006'
    '%B %d, %Y',      # 'October 25, 2006'
    # '%d %B %Y',       # '25 October 2006'
    # '%d %B, %Y',      # '25 October, 2006'
    # '%Y-%m-%d',       # '2006-10-25'
    '%d-%m-%Y',       # '10-25-2006'
    # '%m/%d/%Y',       # '10/25/2006'
    '%d/%m/%Y',       # '25/10/2006'
)

# -------------------------------------------------------------------
# Paths for static, media and templates
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, "files", "static-collected")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, "files", "media")
EMAIL_ROOT = os.path.join(PROJECT_PATH, "files", "emails") # Contains email files for Post Office
DATA_ROOT = os.path.join(PROJECT_PATH, "files", "data") # Contains gen data files (used by some manage commands)
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "files", "static"), # Remember first element should be the user defined one.
    # used in management commands
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "files", "templates"),
)

# -------------------------------------------------------------------
# To disable suspicious operation error messages
def skip_suspicious_operations(record):
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        # Define filter for suspicious operations
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Settings for specific Apps
# ---------------------------------------------------
# Post Office
EMAIL_BACKEND = 'post_office.EmailBackend'

# ---------------------------------------------------
# Python Social Auth
AUTHENTICATION_BACKENDS = (
    # 'social.backends.amazon.AmazonOAuth2',
    # 'social.backends.angel.AngelOAuth2',
    # 'social.backends.aol.AOLOpenId',
    # 'social.backends.appsfuel.AppsfuelOAuth2',
    # 'social.backends.behance.BehanceOAuth2',
    # 'social.backends.belgiumeid.BelgiumEIDOpenId',
    # 'social.backends.bitbucket.BitbucketOAuth',
    # 'social.backends.box.BoxOAuth2',
    # 'social.backends.clef.ClefOAuth2',
    # 'social.backends.coinbase.CoinbaseOAuth2',
    # 'social.backends.dailymotion.DailymotionOAuth2',
    # 'social.backends.disqus.DisqusOAuth2',
    # 'social.backends.douban.DoubanOAuth2',
    # 'social.backends.dropbox.DropboxOAuth',
    # 'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.fedora.FedoraOpenId',
    # 'social.backends.fitbit.FitbitOAuth',
    # 'social.backends.flickr.FlickrOAuth',
    # 'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    # 'social.backends.google.GooglePlusAuth',
    # 'social.backends.instagram.InstagramOAuth2',
    # 'social.backends.jawbone.JawboneOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    # 'social.backends.live.LiveOAuth2',
    # 'social.backends.livejournal.LiveJournalOpenId',
    # 'social.backends.mailru.MailruOAuth2',
    # 'social.backends.mendeley.MendeleyOAuth',
    # 'social.backends.mendeley.MendeleyOAuth2',
    # 'social.backends.mixcloud.MixcloudOAuth2',
    # 'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    # 'social.backends.open_id.OpenIdAuth',
    # 'social.backends.openstreetmap.OpenStreetMapOAuth',
    # 'social.backends.orkut.OrkutOAuth',
    # 'social.backends.persona.PersonaAuth',
    # 'social.backends.podio.PodioOAuth2',
    # 'social.backends.rdio.RdioOAuth1',
    # 'social.backends.rdio.RdioOAuth2',
    # 'social.backends.readability.ReadabilityOAuth',
    # 'social.backends.reddit.RedditOAuth2',
    # 'social.backends.runkeeper.RunKeeperOAuth2',
    # 'social.backends.skyrock.SkyrockOAuth',
    # 'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    # 'social.backends.steam.SteamOpenId',
    # 'social.backends.stocktwits.StocktwitsOAuth2',
    # 'social.backends.stripe.StripeOAuth2',
    # 'social.backends.suse.OpenSUSEOpenId',
    # 'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    # 'social.backends.trello.TrelloOAuth',
    # 'social.backends.tripit.TripItOAuth',
    # 'social.backends.tumblr.TumblrOAuth',
    # 'social.backends.twilio.TwilioAuth',
    'social.backends.twitter.TwitterOAuth',
    # 'social.backends.vk.VKOAuth2',
    # 'social.backends.weibo.WeiboOAuth2',
    # 'social.backends.xing.XingOAuth',
    # 'social.backends.yahoo.YahooOAuth',
    # 'social.backends.yahoo.YahooOpenId',
    # 'social.backends.yammer.YammerOAuth2',
    # 'social.backends.yandex.YandexOAuth2',
    # 'social.backends.vimeo.VimeoOAuth1',
    # 'social.backends.lastfm.LastFmAuth',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_STRATEGY            = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE             = 'social.apps.django_app.default.models.DjangoStorage'

# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/new'
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-assoc/'
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected/'
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False
# SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
# SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
# SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    # I added these.
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    # Social Auth
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)
# SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth-Vader', 'Obi-Wan-Kenobi', 'R2-D2', 'C-3PO', 'Yoda', 'Tony-Stark', 'Bruce-Wayne', 'Black-Widow', 'Eric-Lensher', 'Charles-Xavier', 'Logan'])
# SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    # 'example.app.pipeline.require_email',
    # 'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
# Social auth - backend specific
    # Google
SOCIAL_AUTH_GOOGLE_CONSUMER_KEY          = ''
SOCIAL_AUTH_GOOGLE_CONSUMER_SECRET       = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY            = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET         = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE           = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
    # 'https://www.googleapis.com/auth/plus.login',    
]

    # Facebook
SOCIAL_AUTH_FACEBOOK_KEY                = ''
SOCIAL_AUTH_FACEBOOK_SECRET             = ''
SOCIAL_AUTH_FACEBOOK_SCOPE              = ['basic_info', 'email']
SOCIAL_AUTH_FACEBOOK_EXTENDED_PERMISSIONS = ['email','publish_actions']
    # Twitter
SOCIAL_AUTH_TWITTER_KEY                 = ''
SOCIAL_AUTH_TWITTER_SECRET              = ''
    # Linkedin
SOCIAL_AUTH_LINKEDIN_CONSUMER_KEY        = ''
SOCIAL_AUTH_LINKEDIN_CONSUMER_SECRET     = ''
    # Facebook
SOCIAL_AUTH_YAHOO_CONSUMER_KEY           = ''
SOCIAL_AUTH_YAHOO_CONSUMER_SECRET        = ''

# ---------------------------------------------------
# Django markdown deux
MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            "cuddled-lists": True,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
            "cuddled-lists": True,
        },
        "safe_mode": False,
    },
}
MARKDOWN_DEUX_HELP_URL = "http://daringfireball.net/projects/markdown/syntax"


GOOGLE_API_USER_EMAIL = ''
GOOGLE_API_CLIENT_SECRETS = os.path.join(os.path.dirname(__file__),  'docs_client_secrets.json')
GOOGLE_API_REDIRECT_URI = SITE_URL + 'docs/oauth2callback'
GOOGLE_API_CREDENTIALS = ""
GOOGLE_DRIVE_ROOT_FOLDER_ID = ""

RECAPTCHA_PUBLIC_KEY = '6Lf1ktUSAAAAALOtemzm08LVwHmfku6yXXCdrMJn'
RECAPTCHA_PRIVATE_KEY = '6Lf1ktUSAAAAANLvSSLPiSpgocDrjyK9ApPUvcaF'