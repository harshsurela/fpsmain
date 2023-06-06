from django.urls import path
from . import views


urlpatterns = [
    path("",views.api,name='api'),
    path('apicreate/',views.FileView.as_view(),name='apicreate'),
    path('apilogin/',views.apilogin,name='apilogin'),
    path('apidelete/',views.delete,name='apidelete'),
    path('apifillform/',views.fillform,name='apifillform'),
    path('apiconsent/',views.consent,name='apiconsent'),
    path('splash/',views.getSplash,name='splash'),
    path('access/',views.access,name='access'),
    path('notify/',views.notifyapi,name='apinotify'),
    path('sendmail/',views.email,name="email"),
    path('personalnotify/',views.personalnotifyapi,name="personalnotifyapi"),
    path('checkuser/',views.loginCheck,name="getuser")

]