from solarnet.models import Node
from django.urls import path
from .views import DataCreate, NetworkCreateAPI, NetworkDetail , NodeCreate, NodeDetail,AdminUserView,ClientUserView
from rest_framework.schemas import get_schema_view # new
from rest_framework import permissions
from drf_yasg import openapi # new




urlpatterns = [
path('network/<int:pk>/', NetworkDetail.as_view()),
path('network/',NetworkCreateAPI.as_view()),
path('node/<int:pk>/', NodeDetail.as_view()),
path('node/' ,NodeCreate.as_view()),
path('data/' , DataCreate.as_view()),
path('currentuser/' ,AdminUserView.as_view({
            'get': 'currentuser',
        })),
###adminView
path('listuser/' ,AdminUserView.as_view({
            'get': 'listUtilisateur',
        })),

path('listneworks/' ,AdminUserView.as_view({
    'get':'listNeworks',
})),
path('listData/' ,AdminUserView.as_view({
    'get':'listofData',
})),

path('nodeNetwork/<int:pk>/' ,AdminUserView.as_view({
    'get':'nodeNetwork',
})),

path('dataNode/<int:pk>/' ,AdminUserView.as_view({
    'get':'dataNode',
})),

##ClientAdmin
path('userNetwork/<int:pk>/' ,ClientUserView.as_view({
    'get':'userNetwork',
})),
path('usernodeNetwork/<int:pk>/' ,ClientUserView.as_view({
    'get':'usernodeNetwork',
})),
path('userdatanodenetwork/<int:pk>/',ClientUserView.as_view({
    'get':'userdatanodenetwork',
})),

path('openapi', get_schema_view( # new
title="Solarnet API",
description="An  API ressource for my  end  Year Project",
version="1.0.0"
), name='openapi-schema'),
]