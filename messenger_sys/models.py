from django.db import models

# Create your models here.
class MatrixRoom(models.Model):
    room_matrix_id = models.CharField(max_length=255, blank=True, null=True)
    room_title = models.CharField(max_length=255)
    room_topic = models.CharField(max_length=255, blank=True, null=True)
    room_visibility = models.CharField(max_length=255, blank=True, null=True)
    room_alias = models.CharField(max_length=255, blank=True, null=True)
    room_version = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=255, blank=True, null=True)
    room_federate = models.BooleanField(default=False)
    room_is_direct = models.BooleanField(default=False)
    room_preset = models.CharField(max_length=255, blank=True, null=True)
    room_predessor = models.CharField(max_length=255, blank=True, null=True)
    room_space = models.CharField(max_length=255, blank=True, null=True)
    room_power_level_override = models.IntegerField(default=0)
    room_invite = models.TextField(null=True, blank=True)
    room_initial_state = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.room_title