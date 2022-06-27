from rest_framework.permissions import BasePermission, SAFE_METHODS
from . import models

EDIT_METHODS = ["PUT","PATCH"]


def find_org_member(user,obj):
    org_member = None
    if type(obj) == models.Organization:
        org_member = models.OrganizationMember.objects.filter(user__id=user.id).filter(organization__id=obj.id)
    elif type(obj) in [models.OrganizationMember,models.Project]:
        org_member = models.OrganizationMember.objects.filter(user__id=user.id).filter(organization__id=obj.organization.id)
    elif type(obj) in [models.ProjectMember,models.Comment]:
        org_member = models.OrganizationMember.objects.filter(user__id=user.id).filter(organization__id=obj.project.organization.id)
    if bool(org_member) is True:
        return org_member[0]
    return None


# correct queries depending on obj
def find_project_member(user,obj):
    project_member = None
    if type(obj) == models.Project:
        project_member = models.ProjectMember.objects.filter(user__id=user.id).filter(project__id=obj.id)
    else:
        project_member = models.ProjectMember.objects.filter(user__id=user.id).filter(project__id=obj.project.id)
    if bool(project_member) is True:
        return project_member[0]
    return None


# function that determines if a user is a member of a project and/or organization.
def is_project_member_or_org_member(user,obj):
    project_member = find_project_member(user,obj)
    org_member = find_org_member(user,obj)
    if project_member:
        return project_member
    if org_member:
        return org_member
    return None
    

class is_admin_authenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False


class is_project_member(BasePermission):
    def has_permission(self, request, view):
        return not view.action == "create"

    def has_object_permission(self, request, view, obj):
        user = find_project_member(request.user,obj)
        # Checks if project_member exists then checks his role.
        if user:
            if user.role == "M":
                # handles project permissions
                if type(obj) == models.Project:
                    if request.method in SAFE_METHODS:
                        return False
                    elif request.method in EDIT_METHODS:
                        return True
        # Members can't use DELETE/POST methods
        return False


class is_project_owner(BasePermission):    
    def has_object_permission(self, request, view, obj):
        user = find_project_member(request.user,obj)
        # Checks if project_member exists then checks his role.
        if not user:
            return False
        if user.role == "O":
            # handles project permissions
            if type(obj) == models.Project:
                if request.method in SAFE_METHODS:
                    return True
                elif request.method in EDIT_METHODS:
                    return True
                elif request.method == "DELETE":
                    return True
            # handles comment permissions
            elif type(obj) == models.Comment:
                if request.method == "POST":
                    return True

        return False


class is_org_admin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = find_org_member(request.user,obj)
        if not user:
            return False
        if user.role == "A":
            # handles project permissions
            if type(obj) == models.Project:
                return True
            # handles organization permissions
            elif type(obj) == models.Organization:
                if request.method in SAFE_METHODS:
                    return True
                elif request.method in EDIT_METHODS:
                    return True
            # org admins have every other objects accesses.
            else:
                return True
        return False


class is_org_member(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = find_org_member(request.user,obj)
        if not user:
            return False
        if user.role == "M":
            # handles project permissions
            if type(obj) == models.Project:
                if request.method in [SAFE_METHODS,"POST"]:
                    return True
            # handles organization permissions
            elif type(obj) == models.Organization:
                if request.method in SAFE_METHODS:
                    return True
            # handles comment permissions
            elif type(obj) == models.Comment:
                if request.method in [SAFE_METHODS]:
                    return True
        return False


class managing_members(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = is_project_member_or_org_member(request.user,obj)
        if not user:
            return False
        if request.method in SAFE_METHODS:
            return True
        elif user.role == "A" or request.user.is_superuser:
            return True
        return False


class comment_deletion(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in [EDIT_METHODS, "DELETE"]:
            return obj.author == request.user
        return False


class is_admin_or_not_create(BasePermission):
    def has_permission(self, request, view):
        if not view.action == "create":
            return True
        else:
            return request.user.is_superuser