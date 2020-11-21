from django.contrib import admin
from beta_apis.models import Users, Report, ReportPhoto
# Register your models here.
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'full_name',
        'photo',
    )
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('username', 'email', 'full_name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'latitude',
        'longitude',
        'describe',
        'is_public',
        'created_at',
        'updated_at'
    )


@admin.register(ReportPhoto)
class ReportPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'report_id',
        'user_id',
        'public_url',
        'created_at',
        'updated_at'
    )



