import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "placepilot_test",
        "USER": "placepilot",
        "PASSWORD": "placepilot",
        "HOST": "localhost",
        "PORT": "5432",
    }
