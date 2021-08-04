from django.contrib.auth.models import User
from django.db import models


class Meeting(models.Model):
    baker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return f'{self.date}, Baker: {self.baker}. {", ".join([ma.__str__() for ma in self.meetingattendee_set.all()])}'


class MeetingAttendee(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.attendee.username


class CakeRatio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    baked_cakes = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    eaten_cakes = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    ratio = models.DecimalField(decimal_places=2, max_digits=5)

    def get_user_name(instance):
        return instance.user.first_name
    get_user_name.short_description = 'Name'

    def __str__(self):
        return f'{self.user.username}: {self.ratio}'
