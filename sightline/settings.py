from django.conf import settings


DEFAULT_SETTINGS = {
    "visit": {
        "enabled": True,
        "interval_capturing": 5 # Seconds
    }
}


SIGHTLINE_SETTINGS = getattr(
    settings,
    "SIGHTLINE_SETTINGS",
    DEFAULT_SETTINGS
)


SIGHTLINE_VISIT_SETTINGS = getattr(
    SIGHTLINE_SETTINGS,
    "visit",
    DEFAULT_SETTINGS["visit"]
)

