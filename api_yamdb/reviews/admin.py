from django.contrib import admin

from .models import Category, Genre, Title, User


class TitleInlineAdmin(admin.TabularInline):
    model = Title.genre.through
    min_num = 1
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class TitleAdmin(admin.ModelAdmin):
    inlines = [TitleInlineAdmin]


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
