import random
import string
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from picfetcher.models import content
from django.http import HttpResponse
import os
import zipfile
from io import StringIO ,BytesIO
from picfetcher.models import content
from pic.settings import BASE_DIR
import datetime


def createsubadmin(request):
    adm = adminuser.objects.all()
    for a in adm:
        U = User.objects.create_user(a.user.username+"sub",a.email,a.email)
        sub=subadminuser()
        sub.admin=a
        sub.blocked=False
        sub.email=a.email
        sub.mobile =a.mobile
        sub.user=U
        sub.save()


    return redirect('adminpanel')


def assignsub(request):
    us = userprofile.objects.all()
    for u in us:
        u.subadmin=subadminuser.objects.get(admin=u.admin)
        u.save()

    return redirect('adminpanel')


def policy(request):

    return  render(request,"accounts/policy.html")


def index(request):
    """ The index fuction is used for the admin login """
    return  render(request,"accounts/login.html")

def admin(request):
    """
        This function is used when the admin submit's the form and then the form detail is processed
        so that only the authenticated users can use the app
    """
    try:
        if request.method == "POST":
            uname = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(username = uname,password=pwd)
            print("-----------------------11--")
            print(user)
            print("-------------------------")
            if user.is_superuser:
                print("superuser")
                login(request,user)
                return redirect("adminpanel")
            # admin = adminuser.objects.get(user=user)
            # if admin.blocked==True:
            #     return render(request,"accounts/adminLogin.html",{"message":"You have been blocked please contact the superAdmin"})
            # print(admin)
            # if admin is not None:
            #     login(request,user)
            #     return redirect("adminpanel")
            # else:
            #     return render(request,"accounts/adminLogin.html",{"message":"Please enter correct credentials"})
        else:
            return render(request,"accounts/adminLogin.html")
    except Exception as e:
        print(e)
        return render(request,"accounts/adminLogin.html",{"message":"Wrong Credentials "})


@login_required(login_url='admin')
def adminpage(request):
    """
    This function is called when the admin is authenticated
    """
    return render(request,"accounts/adminpage.html")

@login_required(login_url='admin')
def createToken(request):
    """
        Here the admin can create the 16 character alpha numeric access token.
        If the token is already used by other user then it will show wrong or used token.
    """
    # generate unique tokens from CF001 to CF500
    tokens=[]
    for i in range(1,501):
        tokens.append("CF"+str(i).zfill(3))
    print(tokens)
    # store them to acccessToken Database
    for i in tokens:
        token = AccessToken()
        token.token = i
        token.save()
    return redirect('adminpanel')
    # print(len(tokens))

    
       
@login_required(login_url='admin')
def logoutuser(request):
    """
    The funtion name define's its task(logout admin).
    """
    logout(request)
    return redirect('admin')

def logoutsuperuser(request):
    """
        To logout the super admin
    """
    logout(request)
    return redirect('superlogin')



def createadmin(request):
    """
        Here the super admin can create the admin
    """
    try:
        if request.method == "POST":
            uname = request.POST.get("username")
            pwd = request.POST.get("password")
            eml = request.POST.get("email")
            cuser = User.objects.create_user(username=uname,password=pwd)
            cuser.save()

            up = adminuser()
            up.user = cuser
            up.email = eml
            up.image = request.FILES.get("img1")
            print
            up.image2 = request.FILES.get("img2")
            print("-----------admi doe----------")
            print(request.FILES.get("img2"))
            up.save()
            subuser = User.objects.create_user(username=uname+"sub",password=eml)
            subuser.save()

            subad=subadminuser()
            subad.user=subuser
            subad.admin = up
            subad.email = eml
            subad.blocked = False
            subad.save()


            return render(request,"accounts/createadmin.html",{"message":"Admin created"})
        else:
            return render(request,"accounts/createadmin.html",)

    except Exception as e:
        return render(request,"accounts/createadmin.html",{"message":"something went wrong "+str(e)})

def superuserlogin(request):
    """
        Used for logging superadmin in
    """
    try:
        if request.method == "POST":
            uname = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(username = uname,password=pwd)
            print(user)
            print(user.is_superuser)
            if user.is_superuser:
                login(request,user)
                return redirect("superpanel")
            else:
                return  render(request,"accounts/login.html",{"message":"Something went wrong"})
        else:
            return  render(request,"accounts/login.html")
    except Exception as e:
        return  render(request,"accounts/login.html",{"message":"Something went wrong"})

@login_required(login_url="superlogin")
def superpanel(request):
    """
        Returns superadmin panel if the login details are right
    """
    return render(request,"accounts/superadminpage.html")


@login_required(login_url="admin")
def userlist(request):
    """
        Returns the list of user of the particular admin
    """
    # usre = adminuser.objects.get(user=request.user)
    userlist = userprofile.objects.all()
    return render(request,"accounts/userlist.html",{"users":userlist})


@login_required(login_url="admin")
def usercontent(request,cid):
    """
        Returns the contents of the user selected from the list of users
    """
    print(cid)
    user = userprofile.objects.get(contactno=cid)
    pic = content.objects.filter(added_by=user)
    print(pic)
    print(user)
    return render(request,"accounts/userContents.html",{"user":pic,"pro":user})

@login_required(login_url="superlogin")
def superusercontent(request,cid):
    """
        Super admin viewing the content of the selected user
    """
    u = User.objects.get(username=cid)
    user = userprofile.objects.get(user=u)
    pic = content.objects.filter(added_by=user)
    return render(request,"accounts/superusercontents.html",{"user":pic,"pro":user})


@login_required(login_url="superlogin")
def superadminlist(request):
    """
    Superadmin viewing admin list
    """
    userlist = adminuser.objects.all()
    return render(request,"accounts/superadminlist.html",{"users":userlist})

@login_required(login_url="superlogin")
def superuserlist(request):
    """
    Super admin viewing user list
    """
    userlist = userprofile.objects.all()

    return render(request,"accounts/superuserlist.html",{"users":userlist})


def notifyadminuser(request):
    try:
        if request.method == "POST":
            user = request.user
            admin = adminuser.objects.get(user=user)
            print(f" $admin is notified")
            notification = request.POST.get("notify")
            np=notify()
            np.title=notification
            np.admin = admin
            np.greetdate=request.POST.get('date')
            # np.time = request.POST.get("date")
            np.save()
            return render(request,"accounts/adminusernotify.html",{"message":"notified"})
        else:
            return render(request,"accounts/adminusernotify.html")
    except Exception as e:
        return render(request,"accounts/adminusernotify.html",{"message":"something went wrong"+str(e)})


@login_required(login_url="superlogin")
def notifycreate(request):
    """
        Over all notification sent by Super admin
    """
    try:
        if request.method == "POST":

            notification = request.POST.get("notify")
            np=notify()
            np.title=notification
            np.greetdate=request.POST.get('date')
            # np.time = request.POST.get("date")
            np.save()
            return render(request,"accounts/notify.html",{"message":"notified"})
        else:
            return render(request,"accounts/notify.html")
    except Exception as e:
        return render(request,"accounts/notify.html",{"message":"something went wrong"+str(e)})


def getfiles(request,un):
    """
        This function is used to get all the images of the selected user,
        and adds a file containing his/her details.
    """
    print(BASE_DIR)

    useracc = userprofile.objects.get(contactno=un)
    contentu = content.objects.filter(added_by =useracc )
    f = open(f"{useracc}details.txt","w")
    f.write(f"Username:{useracc.username}\nFather name:{useracc.father_name}\nDOB:{useracc.DOB}\nAddress:{useracc.address}\nContact No.:{useracc.contactno}\nE-mail:{useracc.email}\nSchool:{useracc.school}\nBlood Group:{useracc.bloodGroup}\nRemarks:{useracc.remarks}")
    f.close()

    fn = []
    processed = []
    for u in contentu:
        if ".jpg" or ".bmp" in u.thumbnail.path:

            fn.append(u.thumbnail.path)
        if ".jpg" or ".bmp" in u.processedimg.path:

            processed.append(u.processedimg.path)
    filenames = fn+processed
    print(filenames)
    # print(os.path.abspath(f"{useracc}details.txt"))
    filenames.append(os.path.abspath(f"{useracc}details.txt"))

    zip_subdir = "FPworld "+str(useracc.username)
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip

        fdir, fname = os.path.split(fpath)
        if fpath in fn:
            fname = f'RAW/{fname}'
        if fpath in processed:
            fname = f'PROCESSED/{fname}'
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


def test(request):
    """ Function always used for debugging """
    if request.method == "POST":
        m = request.POST.get("d")
        u=userprofile.objects.filter(datajoined=m)
        print(u)
        return render(request,"accounts/filtertest.html")
    else:
        return render(request,"accounts/filtertest.html")


def adelete(request,what,id):
    """
        The function is used to delete content of the particular users from the admin
    """
    if what=='user':
        print(id)
        u = userprofile.objects.get(contactno=id)
        u.delete()
    if what=='img':
        c = content.objects.get(id=id)
        a=c.added_by
        u=a.user
        c.delete()
        return redirect('usercontent',cid=u)
    return redirect('userlist')

def sdelete(request,what,id):
    """
        The function is used to delete content of the particular users from the super admin
    """
    if what=='user':
        print(id)
        u = User.objects.get(username=id)
        u.delete()
    if what=='img':
        c = content.objects.get(id=id)
        a=c.added_by
        u=a.user
        c.delete()
        return redirect('susercontent',cid=u)
    return redirect('superuserlist')

def sadelete(request,id):
    """
        Super admin can delete user
    """
    u = User.objects.get(username=id)
    a = adminuser.objects.get(user=u)
    user = userprofile.objects.filter(admin=a)
    print(user)
    for i in user:
        k = User.objects.get(username=i.user)
        k.delete()
    u.delete()
    return redirect('superadminlist')


def forgetpassword(request,who,by):
    """
        This function is used to reset password for all,
        'who' :- This variable is used to determine whose password is to be changed
        'by' :- This determines weather the request is from admin or the super admin
    """
    if who == "s":
        if request.method == "POST":
            user = request.POST.get('username')
            passw = request.POST.get('password')
            passw = request.POST.get('password2')
            eml = request.POST.get('email')

            try:
                u = User.objects.get(username=user)
                print(u.email == eml)
                if u.email != eml:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'message':"please enter valid email"})
                u.set_password(passw)
                u.save()
                return render(request,"accounts/login.html",{"message":"Password Updated"})
            except Exception as e:
                return render(request,"accounts/login.html",{"message":"Please enter valid details : "+str(e) })
        return render(request,"accounts/resetsuper.html",{'who':who,'by':by})
    elif who =="a":
        if request.method == "POST":
            user = request.POST.get('username')
            passw = request.POST.get('password')
            passw = request.POST.get('password2')
            eml = request.POST.get('email')
            try:
                u = User.objects.get(username=user)
                a=adminuser.objects.get(user=u)
                if a is None:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'messwage':"please enter valid credentials"})

                if a.email!=eml:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'message':"please enter valid email"})
                u.set_password(passw)
                u.save()
                return render(request,"accounts/adminLogin.html",{"message":"Password Updated"})
            except Exception as e:
                return render(request,"accounts/adminLogin.html",{"message":"Please enter valid details : "+str(e) })
        return render(request,"accounts/resetsuper.html",{'who':who,'by':by})

    elif who =="sub":
        if request.method == "POST":
            user = request.POST.get('username')
            passw = request.POST.get('password')
            passw = request.POST.get('password2')
            eml = request.POST.get('email')
            try:
                u = User.objects.get(username=user)
                a=subadminuser.objects.get(user=u)
                if a is None:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'messwage':"please enter valid credentials"})

                if a.email!=eml:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'message':"please enter valid email"})
                u.set_password(passw)
                u.save()
                return render(request,"accounts/subadminlogin.html",{"message":"Password Updated"})
            except Exception as e:
                return render(request,"accounts/adminLogin.html",{"message":"Please enter valid details : "+str(e) })
        return render(request,"accounts/resetsuper.html",{'who':who,'by':by})


    elif who =="u":
        if request.method == "POST":
            user = request.POST.get('username')
            passw = request.POST.get('password')
            passw = request.POST.get('password2')
            eml = request.POST.get('email')
            try:
                u = User.objects.get(username=user)
                userpro = userprofile.objects.get(user=u)

                if userpro.email!=eml:
                    print("---------------------------useml")
                    #return render(request,"accounts/resetsuper.html",{'who':who,'by':by,'message':"please enter valid email"})
                u.set_password(passw)
                u.save()

                if by == "a":
                    pic = content.objects.filter(added_by=userpro)
                    return render(request,"accounts/userContents.html",{"user":pic,"pro":userpro})
                elif by =="s":
                    pic = content.objects.filter(added_by=userpro)
                    return render(request,"accounts/superusercontents.html",{"user":pic,"pro":userpro})
                elif by == "sub":
                    pic = content.objects.filter(added_by=userpro)
                    return render(request,"accounts/subusercontent.html",{"user":pic,"pro":userpro})

            except Exception as e:
                try:
                    u = User.objects.get(username=user)
                    userpro = userprofile.objects.get(user=u)
                    if by == "a":
                        pic = content.objects.filter(added_by=userpro)
                        return render(request,"accounts/userContents.html",{"user":pic,"pro":userpro,"message":"password Updated"})
                    elif by =="s":
                        pic = content.objects.filter(added_by=userpro)
                        return render(request,"accounts/superuserContents.html",{"user":pic,"pro":userpro})

                except Exception as e:
                    return render(request,"accounts/resetsuper.html",{'who':who,'by':by})


        return render(request,"accounts/resetsuper.html",{'who':who,'by':by})
    return render(request,"accounts/resetsuper.html",{'who':who,'by':by})

def edituser(request,id,who):
    """
        This function is used to ewdit the selected user
        'who' :- This variable is used to determine whose password is to be changed
    """
    if request.method == "POST":
        try:
            u = User.objects.get(username=id)
            userpro = userprofile.objects.get(user=u)
            print(request.POST.get("username"))
            userpro.username = request.POST.get("username")
            userpro.father_name = request.POST.get("fn")
            userpro.mother_name = request.POST.get("mn")
            userpro.access_code = request.POST.get("access")
            userpro.contactno = request.POST.get("cono")
            userpro.DOB = request.POST.get("dob")
            userpro.address = request.POST.get("add")
            userpro.school = request.POST.get("school")
            userpro.email = request.POST.get("mail")
            userpro.idno = request.POST.get("idno")
            userpro.save()
        except Exception as e:
            getuser=User.objects.get(username=id)
            data = userprofile.objects.get(user=getuser)
            return render(request,"accounts/edituser.html",{'id':id,'data':data,'who':who,'message':"seems like you have entere3d something wrong please check all the fields :"+str(e)})
        if who == 'a':
            return redirect('usercontent',cid=id)
        if who == 's':
            return redirect('susercontent',cid=id)
        if who == 'sub':
            return redirect('subusercontent',cid=id)
   
    data = userprofile.objects.get(username=id)
    return render(request,"accounts/edituser.html",{'id':id,'data':data,'who':who})

def blockuser(request,id,ac):
    '''
        Super admin can block and unblock admin
        ac :- has the condition weather to block or unblock
    '''
    if ac=="bu":
        print(id)
        print("b")
        u = User.objects.get(username=id)
        a=adminuser.objects.get(user=u)
        a.blocked=True
        a.save()
        return redirect('superadminlist')
    if ac=="un":
        print(id)
        print("u")
        u = User.objects.get(username=id)
        a=adminuser.objects.get(user=u)
        a.blocked=False
        a.save()
        return redirect('superadminlist')


def personalnotifications(request):
    '''
        Here we can send the personal notification to particular user
    '''
    if request.method == 'GET':
        try:
            admin = request.user
            adm=User.objects.get(username=admin)
            ad=adminuser.objects.get(user=adm)

            u=userprofile.objects.filter(admin=ad)

            return render(request,"accounts/personalnotifications.html",{'users':u})
        except Exception:

            u=userprofile.objects.all()

            return render(request,"accounts/personalnotifications.html",{'users':u})


    if request.method=="POST":
        try:
            notification = request.POST.get("notify")
            np=notify()
            np.title=notification
            np.greetdate=request.POST.get('date')
            user= request.POST.get('user')

            try:
                admin = request.user
                adm=User.objects.get(username=admin)
                try:
                    ad=adminuser.objects.get(user=adm)
                    use = User.objects.get(username=user)
                    np.user=userprofile.objects.get(user=use,admin=ad)
                    print(use.id)
                    np.save()
                    u=userprofile.objects.filter(admin=ad)
                    return render(request,"accounts/personalnotifications.html",{'users':u,'message':"notified"})
                except Exception as e:
                    ad=adminuser.objects.get(user=adm)
                    u=userprofile.objects.filter(admin=ad)
                    return render(request,"accounts/personalnotifications.html",{'users':u,'message':"Hey ! You have entered wrong values "+str(e)})

            except Exception as e:
                try:
                    use = User.objects.get(username=user)
                    np.user=userprofile.objects.get(user=use)
                    print(use.id)
                    np.save()
                    u=userprofile.objects.all()
                    return render(request,"accounts/personalnotifications.html",{'users':u,'message':"Notified"})
                except Exception as e:
                    u=userprofile.objects.all()
                    return render(request,"accounts/personalnotifications.html",{'users':u,'message':"Hey ! You have entered wrong values "+str(e)})


        except Exception as e:
            u=userprofile.objects.all()
            return render(request,"accounts/personalnotifications.html",{'users':u,'message':"You have entered wrong values "+str(e)})



def filteruser(request,who):
    '''
        We can filter user according to username and date
    '''
    if request.method =="POST":
        if who=='a':
            username = request.POST.get('username')
            date = request.POST.get('date')
            print(username,date)
            if username is "":
                if date is not "":
                    us=User.objects.get(username=request.user)
                    ad=adminuser.objects.get(user=us)
                    u = userprofile.objects.filter(datajoined=date,admin=ad)
                    return render(request,"accounts/userlist.html",{"users":u})
            elif date is "":
                if username is not "":
                    us=User.objects.get(username=request.user)
                    ad=adminuser.objects.get(user=us)
                    u = userprofile.objects.filter(admin=ad)
                    x=[]
                    for i in u :
                        if username in i.user.username:
                            print(i.user.username)
                            x.append(i)
                    return render(request,"accounts/userlist.html",{"users":x})

        if who=='s':
            username = request.POST.get('username')
            date = request.POST.get('date')
            print(username,date)
            if username is "":
                if date is not "":
                    u = userprofile.objects.filter(datajoined=date)
                    return render(request,"accounts/superuserlist.html",{"users":u})
            elif date is "":
                if username is not "":
                    u = userprofile.objects.all()
                    x=[]
                    for i in u :
                        if username in i.user.username:
                            print(i.user.username)
                            x.append(i)
                    return render(request,"accounts/superuserlist.html",{"users":x})

    if who=='a':
        return render(request,"accounts/filteruser.html",{"who":who})
    if who=='s':
        return render(request,"accounts/filteruser.html",{"who":who})


def editadmin(request,id):
    '''
        Super admin can edit details
    '''

    use=User.objects.get(username=id)
    ad = adminuser.objects.get(user=use)

    try:
        if request.method == "POST":
            try:
                uname = request.POST.get("username")
                use=User.objects.get(username=uname)
                up = adminuser.objects.get(user=use)
                if request.FILES.get("img1") is not None:
                    up.image = request.FILES.get("img1")
                if request.FILES.get("img2") is not None:
                    up.image2 = request.FILES.get("img2")

                up.allowedUsage = int(request.POST.get("allow"))
                up.email = request.POST.get("email")
                up.mobile = request.POST.get("mobile")
                up.save()
                return render(request,"accounts/editadmin.html",{'ad':ad,'id':id,"message":"Admin edited"})
            except Exception as e:
                return render(request,"accounts/editadmin.html",{'ad':ad,'id':id,'message':"It seems that you have entered something wrong please refill is properly  "+str(e)})
        else:
            return render(request,"accounts/editadmin.html",{'ad':ad,'id':id})

    except Exception as e:
        return render(request,"accounts/editadmin.html",{'ad':ad,'id':id,"message":"something went wrong "+str(e)})


def adminotify(request):
    '''
    Super admin can send notification to admin
    '''
    u = adminuser.objects.all()
    if request.method=="POST":
        try:
            notification = request.POST.get("notify")
            np=adminnotify()
            np.title=notification
            np.greetdate=request.POST.get('date')
            user= request.POST.get('user')
            use = User.objects.get(username=user)
            np.user=adminuser.objects.get(user=use)
            print(use.id)
            np.save()
        except Exception as e:
            return render(request,"accounts/adminnotify.html",{'users':u,'message':"You have entered wrong values "+str(e)})
    return render(request,"accounts/adminnotify.html",{'users':u})


def deleteoldimg(request):
    '''
        This function is used to delete old function
    '''
    img=content.objects.all()
    print(datetime.date.today()-datetime.timedelta(days=3))
    for i in img:
        if i.publishedDate < (datetime.date.today()-datetime.timedelta(days=3)):

            # print(i)
            i.delete()

        # i.delete()
    return redirect('superpanel')

def getnotify(request):
    '''
        This function is used by admin to get his daily notification
    '''
    u=request.user
    ad= adminuser.objects.get(user=u)
    getnotify = adminnotify.objects.filter(user=ad,greetdate=datetime.date.today())
    if len(getnotify)>0:
        return render(request,"accounts/adminpage.html",{"notify":getnotify})
    else:
        return render(request,"accounts/adminpage.html")

@login_required(login_url='subadminlogin')
def subadminpage(request):
    return render(request,'accounts/subadminpanel.html')

def subadminlogin(request):
    if request.method == 'POST':
        try:
            if request.method == "POST":
                uname = request.POST.get("username")
                pwd = request.POST.get("password")
                user = authenticate(username = uname,password=pwd)
                print(user)
                admin = subadminuser.objects.get(user=user)
                if admin.blocked==True:
                    return render(request,"accounts/subadminlogin.html",{"message":"You have been blocked please contact the superAdmin"})
                print(admin)
                if admin is not None:
                    login(request,user)
                    return redirect('subadminpanel')
                else:
                    return render(request,"accounts/subadminlogin.html",{"message":"Please enter correct credentials"})
            else:
                return render(request,"accounts/subadminlogin.html")
        except Exception as e:
            return render(request,"accounts/subadminlogin.html",{"message":"something went wrong please inform the SuperAdmin about this."})



    return render(request,'accounts/subadminlogin.html')


@login_required(login_url='subadminlogin')
def subcreateuser(request):
    """
        Here the admin can create the users by adding their details.
        If the username is already taken by other admin then the current admin can't use the same username for their users.
    """
    # try:
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        idi =  request.POST.get("id")
        cuser = User.objects.create_user(username=uname,password=pwd)
        cuser.save()
        adm = subadminuser.objects.get(user=request.user)
        up = userprofile()
        up.access_code = idi
        up.user = cuser
        up.subadmin = adm
        up.admin = adminuser.objects.get(user=adm.admin.user)
        up.username = uname
        up.save()
        return render(request,"accounts/subcreateuser.html",{"message":"User Created"})
    else:
        return render(request,"accounts/subcreateuser.html")

    # except Exception as e:
    #     return render(request,"accounts/subcreateuser.html",{"message":"Something went wrong "+str(e)})


@login_required(login_url='subadminlogin')
def subadminuserlist(request):
    usre = subadminuser.objects.get(user=request.user)
    userlist = userprofile.objects.filter(subadmin=usre)
    return render(request,"accounts/subuserlist.html",{"users":userlist})


@login_required(login_url="subadmin")
def subusercontent(request,cid):
    """
        Returns the contents of the user selected from the list of users
    """
    u = User.objects.get(username=cid)
    user = userprofile.objects.get(user=u)
    pic = content.objects.filter(added_by=user)
    return render(request,"accounts/subusercontent.html",{"user":pic,"pro":user})

@login_required(login_url="subadminlogin")
def sublogoutuser(request):
    """
    The funtion name define's its task(logout admin).
    """
    logout(request)
    return redirect('subadminlogin')

def adminview(request,cid):
    usr = User.objects.get(username=cid)
    adm = adminuser.objects.get(user=usr)
    users=subadminuser.objects.filter(admin=adm)
    return render(request,'accounts/adminsubadmin.html',{'users':users})

def subuserview(request,cid):
    usr = User.objects.get(username=cid)
    sub = subadminuser.objects.get(user=usr)
    usr = userprofile.objects.filter(subadmin=sub)
    return render(request,"accounts/superuserlist.html",{"users":usr})

def createsubadmin(request):
    try:
        if request.method == "POST":
            uname = request.POST.get("username")
            pwd = request.POST.get("password")

            cuser = User.objects.create_user(username=uname,password=pwd)
            cuser.save()
            adm = adminuser.objects.get(user=request.user)

            up = subadminuser()


            up.user = cuser
            up.admin = adm
            up.username = uname
            up.email = request.POST.get('email')
            up.save()
            return render(request,"accounts/createsubadmin.html",{"message":"subadmin Created"})
        else:
            return render(request,"accounts/createsubadmin.html")

    except Exception as e:
        return render(request,"accounts/createsubadmin.html",{"message":"Something went wrong"+str(e)})

def adminsublist(request):

    adm = adminuser.objects.get(user=request.user)
    users=subadminuser.objects.filter(admin=adm)
    return render(request,'accounts/adminsublist.html',{'users':users})

def adminsubuserlist(request,cid):
    usr = User.objects.get(username=cid)
    sub = subadminuser.objects.get(user=usr)
    usr = userprofile.objects.filter(subadmin=sub)
    return render(request,"accounts/userlist.html",{"users":usr})

def deletesubadmin(request,cid):
    print(cid)
    u = User.objects.get(username=cid)
    a = subadminuser.objects.filter(user = u)
    print(a)
    # user = subadminuser.objects.filter(admin=a)
    # print(user)
    # for i in user:
    #     k = User.objects.get(username=i.user)
    #     k.delete()
    a.delete()
    return redirect('sublist')

def superdeletesubadmin(request,cid):
    print(cid)
    u = User.objects.get(username=cid)
    a = subadminuser.objects.filter(user = u)
    print(a)
    k = a[0].admin
    # user = subadminuser.objects.filter(admin=a)
    # print(user)
    # for i in user:
    #     k = User.objects.get(username=i.user)
    #     k.delete()
    a.delete()
    return redirect('adminview',k.user)

def viewTokens(request):
    tokens = AccessToken.objects.all()
    return render(request,'accounts/viewtokens.html',{'tokens':tokens})

def deletetoken(request,cid):
    print(cid)
    token = AccessToken.objects.get(token=cid)
    token.delete()
    return redirect('tokens')
