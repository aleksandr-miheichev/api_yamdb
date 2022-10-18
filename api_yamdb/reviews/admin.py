from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import (Category, Comment, CustomUser, Genre, GenreTitle,
                            Review, Title)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {'slug': ('name',)}


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active'
            )
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class GenreAdmin(CategoryAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    list_filter = ('year', 'genre', 'category', 'name')
    search_fields = ('name',)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_id', 'title_id')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review)
admin.site.register(Title, TitleAdmin)
