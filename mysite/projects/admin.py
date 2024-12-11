from django.contrib import admin

# Register your models here.

from projects.models import Project, Comment, Category, Requirement, Status

admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Requirement)
admin.site.register(Status)