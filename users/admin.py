from django.contrib import admin
from . import models

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'post_code', 
        'road_address', 
        'detail_address',
        )
    
    search_fields = (
        'post_code', 
        'road_address', 
        'detail_address'
        )
    
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'user_id',
        'name',
        'gender',
        'birth',
        'phone_number',
        'email',
    )

    list_display_links = (
        'user_id',
        'name',
    )



    
