from django.contrib import admin

from .models import TestModel



def run_script(modeladmin, request, queryset):
    for sf in queryset:
        sf.script.run_script(number=5)

@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):

    actions = [run_script]