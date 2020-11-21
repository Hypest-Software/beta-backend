from django.contrib import admin
from beta_apis.models import User
# Register your models here.
@admin.register(User)
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