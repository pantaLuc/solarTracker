from functools import partial
from django.db import connection

from rest_framework.views import APIView
from users.serializers import UserDetailsSerializer
from django.db.models import query
from django.shortcuts import redirect, render
from rest_framework import generics,permissions ,viewsets,status
from .models import Data, Network ,Node, Place
from .serializers import DataSerializer, NetworkSerializer, NodeSerializer, PlaceSerializer
from .permissions import IsUserOrReadOnly
from users.models import User
from rest_framework.response import Response
# Create your views here.


class NetworkDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_class=(IsUserOrReadOnly)
    queryset=Network.objects.all()
    serializer_class=NetworkSerializer

class NetworkCreateAPI(generics.CreateAPIView):
    query=Network.objects.all()
    serializer_class=NetworkSerializer

###operations on nodes
class NodeCreate(generics.CreateAPIView):
    queryset=Node.objects.all()
    serializer_class=NodeSerializer

class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Node.objects.all()
    serializer_class=NodeSerializer

class NodeList(generics.ListCreateAPIView):
    queryset=Node.objects.all()
    serializer_class=NodeSerializer

# operation sur le place 
class PlaceCreate(generics.CreateAPIView):
    queryset=Place.objects.all()
    serializer_class=PlaceSerializer
class PlaceDetail(generics.RetrieveUpdateAPIView):
    queryset=Place.objects.all()
    serializer_class=Place
class PlaceList(generics.ListCreateAPIView):
    queryset=Place.objects.all()
    serializer_class=PlaceSerializer
###operations sur les datas 

class DataCreate(generics.CreateAPIView):
    queryset=Data.objects.all()
    serializer_class=DataSerializer

class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Data.objects.all()
    serializer_class=DataSerializer


class AdminUserView(viewsets.ViewSet):

    def currentuser(self ,request):
        serializer=UserDetailsSerializer(request.user)
        return Response(serializer.data)
    def updateUser(self ,request ,pk=None):
        user=User.objects.get(id=pk)
        serializer=UserDetailsSerializer(instance=user ,data=request.data ,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
   
    def listUtilisateur(self,request):
            serializer = UserDetailsSerializer(request.user)
            if serializer.data['role']=='admin':
                queryset= User.objects.all()
                serializer = UserDetailsSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response({
                "message":"client can't view all user"
            })
    def listNeworks(self ,request):
            serializer = UserDetailsSerializer(request.user)
            if serializer.data['role']=='admin':
                queryset=Network.objects.all()
                serializer=NetworkSerializer(queryset ,many=True)
                return Response(serializer.data)
            return Response({
                "message":"client can't view all network"
            })
    def listData(self ,request):
        serializer = UserDetailsSerializer(request.user)
        if serializer.data['role']=='admin':
            queryset=Data.objects.all()
            serializer=DataSerializer(queryset ,many=True)
            return Response(serializer.data)
        return Response({
                "message":"client can't view all datas"
            }) 
    def  nodeNetwork(self ,request ,pk):
        serializer = UserDetailsSerializer(request.user)
        if serializer.data['role']=='admin':
            queryset=User.objects.get(id=pk)
            serializer=UserDetailsSerializer(queryset)
            netqueryset=Network.objects.get(user=pk)
            serializerNet=NetworkSerializer(netqueryset)
            nodequery=Node.objects.filter(network=serializerNet.data['id']).all()
            nodeserializer=NodeSerializer(nodequery,many=True)
            return Response(nodeserializer.data)
        return Response({
                "message":"client can't view all  Node of user "
            })
    def dataNode(self , request ,pk):
        serializer = UserDetailsSerializer(request.user)
        if serializer.data['role']=='admin':
            queryset=Data.objects.filter(id=pk).all()
            serializer=DataSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response({
            "message":"client can't view a this "
        })


class ClientUserView(viewsets.ViewSet):

    def userNetwork(self ,request ,pk):
        #userializer=UserDetailsSerializer(request.user)
       # if userializer.data['role']=='client':
        queryset=Network.objects.filter(user=pk).all()
        serializer=NetworkSerializer(queryset,many=True)
        return Response(serializer.data)
        

    def usernodeNetwork(self ,request ,pk):
        #userializer=UserDetailsSerializer(request.user)
        #if userializer.data['role']=="client":
        queryset=Network.objects.get(id=pk)
        netserializer=NetworkSerializer(queryset)
        nodequeryset=Node.objects.filter(network=netserializer.data['id']).all()
        nodeserializer=NodeSerializer(nodequeryset,many=True)
        return Response(nodeserializer.data)
        
    def userdatanodenetwork(self ,request ,pk):
        #userializer=UserDetailsSerializer(request.user)
        #if userializer.data['role']=='client':
        queryset=Data.objects.filter(node=pk).all()
        dataSerializer=DataSerializer(queryset,many=True)
        return Response(dataSerializer.data)
        

class ChartAPi(APIView):

    def get(self ,_):
        with connection.cursor() as cursor:
            cursor.execute( """
                SELECT strftime('%Y %m %d  %H %m',d.created_at) as date ,data
                FROM solarnet_data as d
                JOIN solarnet_node as n ON n.id =d.node_id 
                GROUP BY date
            """
            )
            row=cursor.fetchall()
        return Response(row)

        