from django.urls import path
from . import views
urlpatterns = [

    path('index',views.index),

    path('ajax',views.ajaxtest),

    path('ajaxdata',views.ajaxdata),

    path('json', views.jsontest),

    path('jsondata', views.jsondata),

    path('jsonpost', views.jsontestpost),

    path('jsondatapost', views.jsondatapost),

    path('crosstest', views.crosstest),

    path('crosstestdata',views.crosstestdata),


]