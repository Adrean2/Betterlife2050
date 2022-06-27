from ast import Or
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProjectMember, OrganizationMember, Project,Comment,User,Organization


admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(User,UserAdmin)
admin.site.register(Organization)
admin.site.register(ProjectMember)
admin.site.register(OrganizationMember)
 