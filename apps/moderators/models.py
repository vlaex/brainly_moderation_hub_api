from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import URLValidator
from core import make_db_choices_from_enum, Market, Gender


class Moderator(AbstractBaseUser):
    """
    Represents a Brainly moderator.

    Each moderator is identified by a global ID in the format `{market}:{numeric_id}`.
    The user ID is a numeric ID on a specific market (e.g., `123456789`).

    Moderators can be mentors to other moderators or mentees themselves.
    Moderators can have friends and achievements.

    The `points` field indicates the number of points the moderator has.
    The point system is used for rankings, leaderboards, achievements.
    """

    global_id = models.CharField(db_column="id", verbose_name="global_id", primary_key=True)
    user_id = models.BigIntegerField(verbose_name="id")
    market = models.CharField(max_length=5, choices=make_db_choices_from_enum(Market))
    is_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    nick = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=100, blank=True)
    ranks = ArrayField(models.IntegerField(), blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    points = models.IntegerField()

    created_at = models.DateTimeField(null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=["https"])])
    gender = models.CharField(max_length=50, choices=make_db_choices_from_enum(Gender))
    date_of_birth = models.DateField(null=True)
    helped_users_count = models.IntegerField(default=0)
    thanks_from_users = models.IntegerField(default=0)
    country = models.CharField(max_length=5, blank=True, null=True)

    friends = models.ManyToManyField("self", blank=True)
    mentor = models.ForeignKey("self", models.SET_NULL, null=True, related_name="mentees")

    privileges = ArrayField(models.IntegerField())

    USERNAME_FIELD = "global_id"
    REQUIRED_FIELDS = ["user_id", "market", "nick"]

    @property
    def is_active(self):
        return not self.is_deactivated

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = "moderators"


class ModeratorPreferences(models.Model):
    """
    Represents personalized settings for a moderator.

    Moderators can specify their preferences such as hiding their date of birth and friends.
    If a moderator is a mentor, they can choose to receive a notification about a new mentee
    and decide whether to send invites to mentees automatically, with an expiration date for such invites.
    """

    moderator = models.OneToOneField(
        Moderator,
        on_delete=models.CASCADE,
        related_name="preferences",
        primary_key=True
    )

    hide_date_of_birth = models.BooleanField(default=False)
    hide_friends = models.BooleanField(default=False)
    send_invite_to_mentees_automatically = models.BooleanField(default=False)
    invite_to_mentees_expiration_days = models.PositiveIntegerField(default=0)
    receive_mentee_notification = models.BooleanField(default=False)

    class Meta:
        db_table = "moderator_preferences"
