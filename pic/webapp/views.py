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
        username = request.POST["username"]
        fathername = request.POST["fathername"]
        dob = request.POST["dob"]
        email = request.POST["email"]
        school = request.POST["school"]
        
        contact = request.POST["contact"]
        address = request.POST["address"]
        blood= request.POST["blood"]
        remarks= request.POST["remarks"]
        concent = False
        # try:
        #     con = request.POST["concent"]
        #     if con == "on":
        #         concent =True
        # except:
        #     pass
        # idi = request.POST["idi"]

        # up = User.objects.get(id = idi)
        user=userprofile.objects.filter(contactno = contact)
        if user:
            return render(request,"webapp/filldetail.html",{"message":"Contact Number  already exists"})
        else:
            userpro = userprofile()
            userpro.father_name = fathername
            if dob != "":
                userpro.DOB = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
            else:
                userpro.DOB = datetime.datetime.strptime("1812-01-01", "%Y-%m-%d").date()
            userpro.email = email
            userpro.address = address
            userpro.contactno = contact
            userpro.username = username
            userpro.school = school
            userpro.consent = concent
            userpro.bloodGroup = blood
            userpro.remarks = remarks
            userpro.save()
            
            if userpro.consent == True:
                return redirect("options")
            else:
                return render(request,"webapp/consent.html",{'contact':userpro.contactno})
    # user =request.user
    # userpro = userprofile.objects.get(user = user)
    return render(request,"webapp/filldetail.html")

def concent(request,contact):
    try:
        userpro = userprofile.objects.get(contactno  =contact)
        userpro.consent = True
        userpro.save()
        request.session['contact'] = contact
        return render(request,"options.html")
    except Exception as e:
        print(e)
        return render(request,"webapp/filldetail.html",{"message":"Something went wrong"})

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
            return redirect("accesskey")
        names = [ 
            "LEFT THUMB",
        "LEFT THUMB",
        "LEFT THUMB",
        "LEFT INDEX",
        "LEFT INDEX",
        "LEFT INDEX",
        "LEFT MIDDLE",
        "LEFT MIDDLE",
        "LEFT MIDDLE",
        "LEFT RING ",
        "LEFT RING ",
        "LEFT RING ",
        "LEFT LITTLE",
        "LEFT LITTLE",
        "LEFT LITTLE",
        "Right Thumb",
        "Right Thumb",
        "Right Thumb",
        "Right Index",
        "Right Index",
        "Right Index",
        "RIGHT MIDDLE",
        "RIGHT MIDDLE",
        "RIGHT MIDDLE",
        "RIGHT RING",
        "RIGHT RING",
        "RIGHT RING",
        "RIGHT LITTLE",
        "RIGHT LITTLE",
        "RIGHT LITTLE"]
        #first alphabet capitalize each word in the string
        names = [x.title() for x in names]
        print(names)
        
        sentenses=["Please keep your thumb tilted toward Left.",
                   "Please keep your thumb centre.",
                   "Please keep your thumb tilted toward Right.",
                   "Please keep your index finger tilted toward Left.",
                   "Please keep your index finger centre.",
                   "Please keep your index finger tilted toward Right.",
                   "Please keep your middle finger tilted toward Left.",
                   "Please keep your middle finger centre.",
                   "Please keep your middle finger tilted toward Right.",
                   "Please keep your ring finger tilted toward Left.",
                   "Please keep your ring finger centre.",
                   "Please keep your ring finger tilted toward Right.",
                   "Please keep your little finger tilted toward Left.",
                   "Please keep your little finger centre.",
                   "Please keep your little finger tilted toward Right.",
                   "Please keep your thumb tilted toward Right.",
                   "Please keep your thumb centre.",
                   "Please keep your thumb tilted toward Left.",
                   "Please keep your index finger tilted toward Right.",
                   "Please keep your index finger centre.",
                   "Please keep your index finger tilted toward Left.",
                   "Please keep your middle finger tilted toward Right.",
                   "Please keep your middle finger centre.",
                   "Please keep your middle finger tilted toward Left.",
                   "Please keep your ring finger tilted toward Right.",
                   "Please keep your ring finger centre.",
                   "Please keep your ring finger tilted toward Left.",
                   "Please keep your little finger tilted toward Right.",
                   "Please keep your little finger centre.",
                   "Please keep your little finger tilted toward Left."]
#  save files with names like  
# L1 - Left , L1 - Centre ,L1 - Right
# L2 - Left , L2 - Centre ,L2 - Right
# L3 - Left , L3 - Centre ,L3 - Right
# L4 - Left , L4 - Centre ,L4 - Right
# L5 - Left , L5 - Centre ,L5 - Right	
# R1 - Reft , R1 - Centre ,R1 - Right
# R2 - Reft , R2 - Centre ,R2 - Right
# R3 - Reft , R3 - Centre ,R3 - Right
# R4 - Reft , R4 - Centre ,R4 - Right
# R5 - Reft , R5 - Centre ,R5 - Right
        fileSaveList=["L1-Left","L1-Centre","L1-Right","L2-Left","L2-Centre","L2-Right","L3-Left","L3-Centre","L3-Right","L4-Left","L4-Centre","L4-Right","L5-Left","L5-Centre","L5-Right","R1-Left","R1-Centre","R1-Right","R2-Left","R2-Centre","R2-Right","R3-Left","R3-Centre","R3-Right","R4-Left","R4-Centre","R4-Right","R5-Left","R5-Centre","R5-Right"]      
        print(f"the fno -> {fno}")
    elif ftype=="2":
        request.session['ftype'] = ftype
        if fno>6:
            return redirect("thankyou")
        names = ["LEFT THUMB","LEFT THUMB","LEFT THUMB","RIGHT THUMB","RIGHT THUMB ","RIGHT THUMB"]
        #first alphabet capitalize each word in the string
        names = [x.title() for x in names]
        sentenses=["Please keep your thumb tilted toward Left.",
                     "Please keep your thumb in centre.",
                     "Please keep your thumb tilted toward Right.",
                     "Please keep your thumb tilted toward Right.",
                     "Please keep your thumb in centre.",
                     "Please keep your thumb tilted toward Left."]
        
        fileSaveList=["L1-Left","L1-Centre","L1-Right","R1-Right","R1-Centre","R1-Left"]
    return render(request,'webapp/base.html',{'fno':fno,'fname':names[fno-1],"retake":retake,"sentense":sentenses[fno-1],"fileSaveList":fileSaveList[fno-1]})

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
        contact = request.session['contact']
        userpro = userprofile.objects.get(contactno =contact)
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
        print(accessCode)
        try:        
            token = AccessToken.objects.get(token = accessCode)
            print(token)
            if token:
                user = userprofile.objects.get(contactno = request.session['contact'])
                user.reference_code = accessCode
                user.save()
                return render(request,"webapp/thankyou.html")
                # return redirect("userlogin")
        except Exception as e:
            print(e)
            return render(request,"webapp/accesscode.html",{"message":"Please enter the Correct Reference Code"})        
    return render(request,"webapp/accesscode.html")

def logoutUser(request):
    logout(request)
    return redirect("userlogin")

def thankyou(request):
    print("In Thank You")
    return render(request,"webapp/thankyou.html")