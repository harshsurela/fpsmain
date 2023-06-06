from django.urls import path
from . import views
from django.contrib.auth import views as ve


urlpatterns = [
    path('policy',views.policy,name="policy"),
    #superadmin urls...
    path('',views.admin,name="admin"),
    # path('superlogin',views.superuserlogin,name="superlogin"),
    # path('logoutSuperuser',views.logoutsuperuser,name="logoutsuper"),
    # path('createadmin',views.createadmin,name="createadmin"),
    # path('superadminpanel',views.superpanel,name="superpanel"),
    # path("suoeruserlist",views.superuserlist,name="superuserlist"),
    # path("superadminlist",views.superadminlist,name="superadminlist"),
    # path("susercontent/<str:cid>",views.superusercontent,name="susercontent"),
    # path("delete/<str:what>,<str:id>",views.sdelete,name="sdelete"),
    # path("sadelete/<str:id>",views.sadelete,name="sadelete"),
    # path("blockuser/<str:id>,<str:ac>",views.blockuser,name="blockuser"),
    # path("editadmin/<str:id>",views.editadmin,name="editadmin"),
    path("deleteoldimg",views.deleteoldimg,name="deleteoldimg"),
    path("download/<str:un>",views.getfiles,name="download"),
    # path("adminnotify",views.adminotify,name="adminnotify"),
    # path('adminview/<str:cid>',views.adminview,name="adminview"),
    # path('users/<str:cid>',views.subuserview,name="subuserview"),
    

    #Admin urls....
    # path('admin',views.admin,name="admin"),
    path('adminPanel',views.adminpage,name="adminpanel"),
    path('createToken',views.createToken,name="createToken"),
    path('logout',views.logoutuser,name="logout"),
    path("userlist",views.userlist,name="userlist"),
    path("usercontent/<str:cid>",views.usercontent,name="usercontent"),
    path("notify",views.notifycreate,name="notify"),
    path("test",views.test,name="test"),
    path("deleteuser/<str:what>,<str:id>",views.adelete,name="adelete"),
    path("getmynotificaton",views.getnotify,name="getnotify"),
    # path('createsubadmin',views.createsubadmin,name='createsubadmin'),
    # path('viewsubadmin',views.adminsublist,name='sublist'),
    # path('subuserslist/<str:cid>',views.adminsubuserlist,name="subuserlistview"),
    path('adminusernotify/',views.notifyadminuser,name="notifyadminuser"),

    #Common url's
    path("resetsuper/<str:who>,<str:by>",views.forgetpassword,name="resetsuper"),
    path("edituser/<str:id>,<str:who>",views.edituser,name="edituser"),
    path("personalnotifiactions",views.personalnotifications,name="personalnotification"),
    path("filteruser/<str:who>",views.filteruser,name="filteruser"),
    path('cs/',views.createsubadmin,name='csub'),
    path('as/',views.assignsub,name='asub'),
    path("subdelete/<str:cid>",views.deletesubadmin,name="subdelete"),
    path("superdelete/<str:cid>",views.superdeletesubadmin,name="subuserdelete"),
    path("tokens",views.viewTokens,name="tokens"),
    path("deletetoken/<str:cid>",views.deletetoken,name="deletetoken"),

    #suadmin url's
    # path("subadmin/",views.subadminlogin,name='subadminlogin'),
    # path("subadminpanel/",views.subadminpage,name='subadminpanel'),
    # path('subcreateuser',views.subcreateuser,name="subcreateuser"),
    # path("subuserlist",views.subadminuserlist,name="subuserlist"),
    # path("subusercontent/<str:cid>",views.subusercontent,name="subusercontent"),
    # path('sublogout',views.sublogoutuser,name="sublogout"),


]