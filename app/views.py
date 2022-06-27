from rest_framework import viewsets,status
from rest_framework.response import Response
from app.permissions import comment_deletion, is_admin_or_not_create,is_project_member, is_project_owner,is_org_member,is_admin_authenticated,is_org_admin,managing_members
from . import serializers
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

role_based_permissions = [is_admin_authenticated|is_org_admin|is_org_member|is_project_owner|is_project_member]


class User(viewsets.ModelViewSet):
    permission_classes = [is_admin_authenticated|managing_members]
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class Project(viewsets.ModelViewSet):
    permission_classes = role_based_permissions
    serializer_class = serializers.ProjectSerializer
    queryset= models.Project.objects.all()


    def perform_create(self,serializer):
        project = serializer.save()
        models.ProjectMember.objects.create(user=self.request.user,project=project,role="O")


    def list(self,request):
        queryset = self.get_queryset()
        serializer = serializers.ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        try:
            instance = models.Project.objects.get(pk=pk)
            serializer = serializers.ProjectListSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("This project doesn't exist.", status=status.HTTP_404_NOT_FOUND)


class Comment(viewsets.ModelViewSet):

    permission_classes = role_based_permissions + [comment_deletion]
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def perform_create(self,serializer):
        comment = serializer.save()
        # update parent comment
        if comment.answer is not None:
            comment.answer.isParent = True
            comment.answer.save()
        serializer.save(author=self.request.user)

    def destroy(self,request, *args,**kwargs ):
        instance = self.get_object()
        if instance.isParent is True:
            instance.content = "<deleted comment>"
            instance.save()
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def list(self,request):
        queryset = self.get_queryset()
        serializer = serializers.CommentListSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def retrieve(self,request,pk=None):
        try:
            instance = models.Comment.objects.get(pk=pk)
            serializer = serializers.CommentListSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("This comment doesn't exist.", status=status.HTTP_404_NOT_FOUND)


class Organization(viewsets.ModelViewSet):
    permission_classes = [is_admin_or_not_create,is_org_member]
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()


    def list(self,request):
        queryset = self.get_queryset()
        serializer = serializers.OrganizationListSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        try:
            instance = models.Organization.objects.get(pk=pk)
            serializer = serializers.OrganizationListSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("This organization doesn't exist.", status=status.HTTP_404_NOT_FOUND)


class ProjectMember(viewsets.ModelViewSet):
    permission_classes = [is_admin_authenticated|managing_members]
    serializer_class = serializers.ProjectMemberSerializer
    queryset = models.ProjectMember.objects.all()

    def list(self,request):
        queryset = self.get_queryset()
        serializer = serializers.ProjectMemberListSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        try:
            instance = models.ProjectMember.objects.get(pk=pk)
            serializer = serializers.ProjectMemberListSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("This member doesn't exist.", status=status.HTTP_404_NOT_FOUND)
        

    
class OrganizationMember(viewsets.ModelViewSet):
    permission_classes = [is_admin_authenticated|managing_members]
    serializer_class = serializers.OrganizationMemberSerializer
    queryset = models.OrganizationMember.objects.all()

    def list(self,request):
        queryset = self.get_queryset()
        serializer = serializers.OrganizationMemberListSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        try:
            instance = models.OrganizationMember.objects.get(pk=pk)
            serializer = serializers.OrganizationMemberListSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("This member doesn't exist.", status=status.HTTP_404_NOT_FOUND)