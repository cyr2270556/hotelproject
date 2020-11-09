from django.urls import path
from . import views
urlpatterns = [
    #http://127.0.0.1:8000/uploadtest/upload_test
    path('upload_test',views.upload),

]