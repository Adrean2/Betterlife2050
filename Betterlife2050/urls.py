from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from app import views
router = routers.DefaultRouter()

router.register("project",views.Project,basename="projects")
router.register("organization",views.Organization,basename="organizations")
router.register("user",views.User,basename="users")
router.register("comment",views.Comment,basename="comments")
router.register("project_member",views.ProjectMember,basename="project_member")
router.register("organization_member",views.OrganizationMember,basename="organization_members")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include(router.urls)),
]
