from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Organization(models.Model):
    LANGUAGE_CHOICES = [("FR","French"),("EN","English"),("ES","Spanish"),("DE","German"),("OT","Other")]
    name = models.CharField(max_length=200,blank=True,default="EN")
    description = models.TextField(blank=True)
    language = models.CharField(max_length=2,choices=LANGUAGE_CHOICES,blank=True)
    members = models.ManyToManyField(to=User,through="OrganizationMember")

    def __str__(self):
        return f"{self.name}, {self.description[0:80]}..."


class OrganizationMember(models.Model):
    ROLE_CHOICES = [("A","Admin"),("M","Member")]
    role = models.CharField(max_length=1,choices=ROLE_CHOICES,default=2)
    user = models.ForeignKey(to=User,on_delete=CASCADE,blank=True)
    organization = models.ForeignKey(to=Organization,on_delete=CASCADE)
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=(["user","organization"]),name="Unique User/Organization"),
        ]
    def __str__(self):
        return f"{self.user.username}, {self.role},{self.organization.name}"


class Project(models.Model):
    APPENDIX_GOALS = [
        (1,"No poverty"),
        (2,"Zero hunger"),
        (3,"Good health and well-being"),
        (4,"Quality education"),
        (5,"Gender equality"),
        (6,"Clean water and sanitation"),
        (7,"Affordable and clean energy"),
        (8,"Decent work and economic growth"),
        (9,"Industry, innovation, and infrastructure"),
        (10,"Reduces inequalities"),
        (11,"Sustainable cities and communities"),
        (12,"Responsible consumption & production"),
        (13,"Climate action"),
        (14,"Life below water"),
        (15,"Life on land"),
        (16,"Peace, justice, and strong institutions"),
        ]

    title = models.CharField(max_length=200,blank=True)
    goal = models.IntegerField(choices=APPENDIX_GOALS,blank=True)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(to=Organization,related_name="project_organization",on_delete=CASCADE,blank=True)
    members = models.ManyToManyField(to=User, related_name="project_member",through="ProjectMember")

    def __str__(self):
        return f"{self.title}, {self.organization.name}"


class ProjectMember(models.Model):
    ROLE_CHOICES = [("O","Owner"),("M","Member")]
    role = models.CharField(max_length=1,choices=ROLE_CHOICES,default="M")
    user = models.ForeignKey(to=User,on_delete=CASCADE,blank=True)
    project = models.ForeignKey(to="Project",on_delete=CASCADE,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(["user","project"]),name="Unique User/Project"),
            ]
    def __str__(self):
        return f"{self.user.username}, {self.role}, {self.project.title}"


class Comment(models.Model):

    content = models.TextField(blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project,on_delete=CASCADE)
    author = models.ForeignKey(User,on_delete=CASCADE,blank=True,null=True)
    answer = models.ForeignKey(to='self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')
    isParent = models.BooleanField(default=False)

    def __str__(self):
        return f"comment {self.id}, created at {self.date_published} by {self.author.username}"
