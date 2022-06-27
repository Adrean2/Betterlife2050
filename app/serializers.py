from re import M
from xml.etree.ElementTree import Comment
from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id","username"]


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["id","name"]

        
class OrganizationListSerializer(ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["id","name","language"]


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id","title","goal","description","organization","members"]


class ProjectListSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    organization.Meta.fields = ["id","name"]
    class Meta:
        model = models.Project
        fields = ["id","title","goal","description","organization","members"]


class ProjectMemberSerializer(ModelSerializer):
    class Meta:
        model = models.ProjectMember
        fields = ["id","user","role","project"]


class ProjectMemberListSerializer(ModelSerializer):
    user = UserSerializer()
    project = ProjectListSerializer()
    class Meta:
        model = models.ProjectMember
        fields = ["id","user","role","project"]

    
class OrganizationMemberSerializer(ModelSerializer):
    class Meta:
        model = models.OrganizationMember
        fields = ["user","role","organization"]


class OrganizationMemberListSerializer(ModelSerializer):
    organization = OrganizationListSerializer()
    user = UserSerializer()
    class Meta:
        model = models.OrganizationMember
        fields = ["user","role","organization"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
    

class CommentAnswerSerializer(ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = models.Comment
        fields = ["id","author"]

class CommentListSerializer(ModelSerializer):
    author = UserSerializer()
    answer = CommentAnswerSerializer()
    class Meta:
        model = models.Comment
        fields = ["id","author","content","answer"]

