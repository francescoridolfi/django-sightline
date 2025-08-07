from django.conf import settings


DEFAULT_SETTINGS = {
    "visit": {
        "enabled": True,
        "interval_capturing": 5 # Seconds
    },
    "geoip": {
        "enabled": False,
        "marker_interval": 10 # days
    }
}


SIGHTLINE_SETTINGS = getattr(
    settings,
    "SIGHTLINE_SETTINGS",
    DEFAULT_SETTINGS
)

SIGHTLINE_VISIT_SETTINGS = SIGHTLINE_SETTINGS.get(
    "visit",
    DEFAULT_SETTINGS["visit"]
)

SIGHTLINE_GEOIP_SETTINGS = SIGHTLINE_SETTINGS.get(
    "geoip",
    DEFAULT_SETTINGS["geoip"]
)