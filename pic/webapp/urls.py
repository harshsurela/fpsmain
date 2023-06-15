from django.urls import path
from . import views


urlpatterns = [
    path("",views.filldetails,name='filldetail'),
    path("userlogin/",views.loginPage,name="userlogin"),
    # path("detail/",views.filldetails,name="filldetail"),
    path("capture/<int:fno>/<int:retake>/<str:ftype>",views.index,name="capture"),
    path("cropimg/",views.cropimg,name="cropimg"),
    path("accesskey/",views.accesskey,name="accesskey"),
    path("deleteImg/",views.webDelete,name="webDelete"),
    path("logoutUser/",views.logoutUser,name="logoutuser"),
    path("concent/<str:uname>",views.concent,name="concent"),
    path('options/',views.options,name="options")
    

]