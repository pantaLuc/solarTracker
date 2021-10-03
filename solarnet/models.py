from django.db import models
from users.models import User
#from django_mysql.models import DynamicField, Model
# Create your models here.

class Network(models.Model):
    nameNet=models.CharField(max_length=50)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    adress=models.CharField(max_length=50)

    def __str__(self) :
        return self.nameNet

class Node(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    network=models.ForeignKey(Network,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
        
class Data(models.Model):
    data=models.FloatField()
    node=models.ForeignKey(Node ,on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Place(models.Model):
    name=models.CharField(max_length=50)
    network=models.ForeignKey(Network,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    