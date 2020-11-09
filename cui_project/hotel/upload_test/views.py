import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from upload_test.models import Content
from django.conf import settings
# Create your views here.

@csrf_exempt
def upload(request):
    if request.method=="GET":
        return render(request,'upload_test/uploadtest.html')
    elif request.method=="POST":

        title=request.POST['title']
        #title=request.POST['title']
        a_file=request.FILES['myfile']
        # filename = os.path.join(settings.MEDIA_ROOT,a_file.name)
        Content.objects.create(desc=title,myfile=a_file)
        return HttpResponse('ok')