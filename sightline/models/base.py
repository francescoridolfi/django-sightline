from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import hashlib, datetime, user_agents


class LogMixin(models.Model):
    """
    LogMixin provides common logging fields and properties for SightLine models.
    Attributes:
        timestamp (DateTimeField): The date and time when the log entry was created.
        raw_user_agent (TextField): The raw user agent string from the client request.
        ip_address (GenericIPAddressField): The IP address from which the request originated.
    Properties:
        insertion_date (datetime.date): Returns the date part of the timestamp.
        insertion_time (datetime.time): Returns the time part of the timestamp.
        user_agent (user_agents.parsers.UserAgent): Returns a parsed user agent object from the raw user agent string.
    """

    class Meta:
        abstract = True

    timestamp = models.DateTimeField(
        verbose_name=_("Insertion Date"),
    )

    raw_user_agent = models.TextField(
        verbose_name=_("User Agent")
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address")
    )

    @property
    def insertion_date(self) -> datetime.date:
        return self.timestamp.date()
    
    @property
    def insertion_time(self) -> datetime.time:
        return self.timestamp.time()

    @property
    def user_agent(self) -> user_agents.parsers.UserAgent:
        if self.raw_user_agent is None or self.raw_user_agent == "":
            return None
        return user_agents.parsers.parse(self.raw_user_agent)


class SessionMixin(LogMixin):
    """
    SessionMixin provides user session tracking fields and logic for SightLine models.
    Attributes:
        user_instance (ForeignKey): Reference to the user associated with the session. 
            Uses the model specified by AUTH_USER_MODEL. Allows null and blank values.
        user_username (CharField): Stores the username of the associated user. 
            Allows null and blank values.
    Properties:
        is_logged (bool): Returns True if a username is associated with the session, 
            indicating that a user is logged in; otherwise, returns False.
    """

    class Meta:
        abstract = True

    user_instance = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_user_log",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    user_username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    @property
    def is_logged(self):
        return self.user_username is not None


class BaseLog(SessionMixin):
    """
    Abstract base model for logging user session activities with a unique MD5 hash identifier.
    Attributes:
        identifier (CharField): MD5 auto-generated hash from log details.
    Methods:
        md5() -> hashlib._Hash:
            Generates and returns an MD5 hash object based on insertion date, IP address, user agent, and user name (or "None" if not logged in).
    """
    class Meta:
        abstract = True

    identifier = models.CharField(
        verbose_name=_("Hash Code"),
        max_length=32,
        help_text=_("MD5 auto generated hash from log details")
    )

    def save(
        self,
        *args,
        **kwargs
    ):
        self.identifier = self.md5().hexdigest()

        return super().save(
            *args,
            **kwargs
        )
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.pk} identifier={self.identifier} date={self.insertion_date}>"

    # Rules: date + ip_address + user_agent | "None" + user_name | "None"
    def md5(self):
        """
        Generates an MD5 hash based on the object's insertion date, IP address, user agent, and username (if logged in else 'None').
        Returns:
            hashlib._Hash: An MD5 hash object representing a unique log identifier for the instance.
        """
        hashcode = hashlib.md5(self.insertion_date.isoformat().encode())
        hashcode.update(self.ip_address.encode())
        hashcode.update(self.raw_user_agent.encode())
        hashcode.update(self.user_username.encode() if self.is_logged else "None".encode())

        return hashcode
