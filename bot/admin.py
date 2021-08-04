from bot.models import CakeRatio, Meeting, MeetingAttendee
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingAttendee)
class MeetingAttendeeAdmin(admin.ModelAdmin):
    pass


@admin.register(CakeRatio)
class CakeRatioAdmin(admin.ModelAdmin):
    list_display = ("user", "get_user_name", "ratio")
    ordering = ["-ratio"]


class CakeRatioInline(admin.StackedInline):
    model = CakeRatio
    can_delete = False
    verbose_name_plural = 'cake ratio'


class UserAdmin(BaseUserAdmin):
    inlines = (CakeRatioInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
