from users.serializers import UserDetailsSerializer
from django.db.models import query
from django.shortcuts import redirect, render
from rest_framework import generics,permissions ,viewsets
from .models import Data, Network ,Node
from .serializers import DataSerializer, NetworkSerializer, NodeSerializer
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


###operations sur les datas 

class DataCreate(generics.CreateAPIView):
    queryset=Data.objects.all()
    serializer_class=DataSerializer

class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Data.objects.all()
    serializer_class=DataSerializer


class AdminUserView(viewsets.ViewSet):
   
    def listUtilisateur(self,request):
            serializer = UserDetailsSerializer(request.user)
            if serializer.data['role']=='admin':
                queryset= User.objects.all()
                serializer = UserDetailsSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response({
                "message":"client can view all user"
            })
    def listNeworks(self ,request):
            serializer = UserDetailsSerializer(request.user)
            if serializer.data['role']=='admin':
                queryset=Network.objects.all()
                serializer=NetworkSerializer(queryset ,many=True)
                return Response(serializer.data)
            return Response({
                "message":"client can view all network"
            })
    def listofData(self ,request):
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
            "message":"client can view a this "
        })

#class Client