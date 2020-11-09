from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from info import views as info_views
from roomlist import views as roomlist_views
from order import views as order_views
from payment import views as payment_views
urlpatterns = [
    path('admin/', admin.site.urls),

    #分页模板
    # path('pagetest',views.paging,name='test'),

    #文件下载模板
    # path('downloadtest',views.download),

    # path('uploadtest/',include('upload_test.urls')),

    #子应用模板
    # path('sonapp/',include('sonapp.urls')),

    #127.0.0.1:8000/v1/users
    path('v1/users', user_views.UsersView.as_view()),

    path('v1/users/', include('user.urls')),

    path('v1/infos',info_views.InfosView.as_view()),

    path('v1/roomlist/<str:hotelname>',roomlist_views.RoomView.as_view()),

    path('v1/order',order_views.OrderViews.as_view()),

    path('payment/jump/', payment_views.JumpView.as_view()),

    path('payment/result/', payment_views.ResultView.as_view()),

]
#用户可以根据地址栏输入访问上传的文件
urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)
# print(settings.MEDIA_URL)
# print(settings.MEDIA_ROOT)