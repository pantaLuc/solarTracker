from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Data, Network, Node

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','user','nameNet','created_at' ,'updated_at','adress')
        model=Network
    
class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','name', 'description','created_at' ,'updated_at','network')
        model =Node

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','data','node' ,'created_at')
        model=Data