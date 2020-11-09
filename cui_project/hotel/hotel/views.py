#from django.core.cache import caches
#不同的子应用使用不同的缓存地址
import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.


#分页模板
# def paging(request):
#     list1 = ['a', 'b', 'c', 'd', 'e']  # 分页对象
#     paginator = Paginator(list1, 2)  # 每页记录条数
#     cur_page = request.GET.get('page', 1)  # 没有默认值1
#     page = paginator.page(cur_page)
#     return render(request,'index.html', locals())

# def download(request):
#     #text/csv文件格式可查表改
#     response = HttpResponse(content_type='text/csv')
#     #mybook文件名可改
#     response['Content-Disposition'] = 'attachment; filename="mybook.csv"'
#     #写入对象
#     all_data = Test.objects.all()
#     writer = csv.writer(response)
#     writer.writerow(['id', 'title'])
#     for b in all_data:
#         writer.writerow([b.id, b.title])
#
#     return response

