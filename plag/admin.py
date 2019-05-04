from django.contrib import admin

from .models import Course, Assignment

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')

admin.site.register(Course)
admin.site.register(Assignment, AssignmentAdmin)

