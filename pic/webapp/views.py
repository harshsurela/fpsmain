from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from accounts.models import userprofile,adminuser,notify,AccessToken
from django.views.decorators.csrf import csrf_exempt
from picfetcher.models import content
from django.http import JsonResponse
from rest_framework.response import Response
import datetime
from django.contrib.auth.decorators import login_required

import os
from api.serializers import contentSerializer
from rest_framework import status

from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.
def loginPage(request):
    if request.method == "POST":
        print(request.POST["username"])
        try:
            uname = request.POST["username"]
            password = request.POST["password"]
            print(uname,password)
            user = authenticate(request,username = uname,password=password)
            userp = userprofile.objects.get(user=user)
            consent = userp.consent
            if user is not None:
                login(request,user)
                userp =  userprofile.objects.get(user=user)
                if userp.admin.allowedUsage ==2 or userp.admin.allowedUsage==3:
                    print(userp)
                    img = userp.admin.image
                    return render(request, "webapp/splashscreen.html",{"imgsrc":img})
                else:
                    print(userp.admin.allowedUsage)
                    return render(request, "webapp/login.html",{"message":"The admin is not allowed to use app"})        
                # return redirect("filldetail")
        except Exception as e:
            print(e)
            return render(request, "webapp/login.html",{"message":"Incorrect username or password"})

    return render(request,"webapp/login.html")



def filldetails(request):
    if request.method == "POST":
        try:
            idno = ""
            idno = request.POST["idno"]
            token=AccessToken.objects.get(token=idno)
            if token.is_used == False:
                token.is_used = True
                token.save()
            else:
                return render(request,"webapp/filldetail.html",{"message":"Token already used Or Wrong"})
        except:
            pass
        username = request.POST["username"]
        fathername = request.POST["fathername"]
        mothername = request.POST["mothername"]
        dob = request.POST["dob"]
        email = request.POST["email"]
        school = request.POST["school"]
        
        contact = request.POST["contact"]
        address = request.POST["address"]
        blood= request.POST["blood"]
        standard= request.POST["standard"]
        remarks= request.POST["remarks"]
        concent = False
        # try:
        #     con = request.POST["concent"]
        #     if con == "on":
        #         concent =True
        # except:
        #     pass
        print(username,mothername,concent)
        # idi = request.POST["idi"]

        # up = User.objects.get(id = idi)
        userpro = userprofile()
        userpro.father_name = fathername
        userpro.mother_name = mothername
        userpro.DOB = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        userpro.email = email
        userpro.address = address
        userpro.contactno = contact
        userpro.username = username
        token=AccessToken.objects.get(token=idno)
        userpro.token=AccessToken(token).id
        userpro.school = school
        userpro.consent = concent
        userpro.bloodGroup = blood
        userpro.standard = standard
        userpro.remarks = remarks
        userpro.save()
        
        if userpro.consent == True:
            return redirect("options")
        else:
            return render(request,"webapp/consent.html",{'token':token.id})
    # user =request.user
    # userpro = userprofile.objects.get(user = user)
    
    return render(request,"webapp/filldetail.html")

def concent(request,token):
    userpro = userprofile.objects.get(token = token)
    userpro.consent = True
    userpro.save()
    # make a session variable for token
    request.session['token'] = token

    return render(request,"options.html")

def options(request):
    print(request.POST)
    if request.method == "POST":
        try:
            if request.POST["option"] == "10":
                print("10")
                return redirect("capture",1,0,"10")
            elif request.POST["option"] == "2":
                print("2")
                return redirect("capture",1,0,"2")
        except:
            pass
    # return redirect("capture",1,0)
    return redirect("concent")

def index(request,fno,retake,ftype):
    if(ftype=="10"):
        request.session['ftype'] = ftype
        if fno>30:
            return redirect("filldetail")
        names = [ 
            "LEFT THUMB Tilted towards little finger",
        "LEFT THUMB Center",
        "LEFT THUMB Tilted towards thumb",
        "LEFT INDEX Tilted towards little finger",
        "LEFT INDEX Center",
        "LEFT INDEX Tilted towards thumb",
        "LEFT MIDDLE Tilted towards little finger",
        "LEFT MIDDLE Center",
        "LEFT MIDDLE Tilted towards thumb",
        "LEFT RING Tilted towards little finger",
        "LEFT RING Center",
        "LEFT RING Tilted towards thumb",
        "LEFT LITTLE Tilted towards little finger",
        "LEFT LITTLE Center",
        "LEFT LITTLE Tilted towards thumb",
        "Right Thumb Tilted towards little finger",
        "Right Thumb Center",
        "Right Thumb Tilted towards thumb",
        "Right Index Tilted towards little finger",
        "Right Index Center",
        "Right Index Tilted towards thumb",
        "RIGHT MIDDLE Tilted towards little finger",
        "RIGHT MIDDLE Center",
        "RIGHT MIDDLE Tilted towards thumb",
        "RIGHT RING Tilted towards little finger",
        "RIGHT RING Center",
        "RIGHT RING Tilted towards thumb",
        "RIGHT LITTLE Tilted towards little finger",
        "RIGHT LITTLE Center",
        "RIGHT LITTLE Tilted towards thumb"]


        print(f"the fno -> {fno}")
    elif ftype=="2":
        request.session['ftype'] = ftype
        if fno>6:
            return redirect("filldetail")
        names = ["LEFT THUMB LEFT ANGLE ","LEFT THUMB CENTER ANGLE","LEFT THUMB RIGHT ANGLE","RIGHT THUMB LEFT ANGLE","RIGHT THUMB CENTER ANGLE","RIGHT THUMB RIGHT ANGLE"]

    return render(request,'webapp/base.html',{'fno':fno,'fname':names[fno-1],"retake":retake})

@csrf_exempt
def webDelete(request):
  
  idi = request.POST.get("idi")
  print(idi)
  ck = content.objects.get(id=idi)
  path = ck.thumbnail

  ck.delete()
  return JsonResponse({"message":"done"},status=201)


@csrf_exempt
def cropimg(request):
    print(request.POST.get('iname'))
    iname =request.POST.get('iname')
    # user = request.user
    # userpro = userprofile.objects.get(user=user)
    con = content()
    # # print(request.is_ajax)
    # print(request.FILES)
    if request.method == "POST":
        img = request.FILES['file']
        i = Image.open(img)
        i = i.convert('RGB')
        thumb_io = BytesIO()
        i.save(thumb_io, format='JPEG', quality=80)
        inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, 'foo.jpeg','image/jpeg', thumb_io.tell(), None)
        print(img)
        token = request.session['token']
        userpro = userprofile.objects.get(token = token)
        con.name = iname
        con.thumbnail = inmemory_uploaded_file
        con.processedimg = inmemory_uploaded_file
        con.added_by = userprofile(userpro.id)
        con.camera_selected = "True"
        con.save()
        return JsonResponse({'data': con.processedimg.__str__(),"id":con.id})

def accesskey(request):
    if request.method == "POST":
        accessCode = request.POST["accesskey"]
        user =request.user
        userpro = userprofile.objects.get(user = user)
        print(userpro.access_code)
        if userpro.access_code == accessCode:
            img = userpro.admin.image2
            logout(request)
            return render(request, "webapp/splashscreen.html",{"imgsrc":img})
            # return redirect("userlogin")
            
        else:
            return render(request,"webapp/accesscode.html",{"message":"Please enter the valid access key"})        
    return render(request,"webapp/accesscode.html")

def logoutUser(request):
    logout(request)
    return redirect("userlogin")
