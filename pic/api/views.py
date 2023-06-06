from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from .serializers import contentSerializer,notifyserializer
from picfetcher.models import content
from accounts.models import userprofile,adminuser,notify
from rest_framework import mixins
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from rest_framework.parsers import MultiPartParser,FormParser




from django.conf import settings
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework import status

import datetime

'''
  This module is used to link this backend to the flutter apk developed
'''


@api_view(['GET'])
def api(request):
    articles = content.objects.all().order_by('id').reverse()
    serial = contentSerializer(articles,many=True)

    return Response(serial.data,status=201)


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = contentSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete(request):
  print(request.data)
  idi = request.data["idi"]
  print(idi)
  ck = content.objects.get(id=idi)
  path = ck.thumbnail

  ck.delete()
  return Response({"message":"done"},status=201)

@api_view(['POST'])
def consent(request):
    idi = request.data["idi"]
    consent = request.data["consent"]
    try:
        if consent =="true":
            ck = userprofile.objects.get(user=idi)
            ck.consent = True
            ck.save()
            return Response({"message":"done"},status=201)
    except Exception as e:
        return Response({"message":"error"+str(e)},status=401)


@api_view(['POST'])
def access(request):
    idi = request.data["idi"]
    access = request.data["access"]
    try:

            ck = userprofile.objects.get(user=idi)
            access_code = ck.access_code
            if(access == access_code):
                return Response({"message":"done"},status=201)
            else:
                return Response({"message":"error"},status=401)
    except Exception as e:
        return Response({"message":"error"+str(e)},status=401)



@api_view(['POST'])
def apilogin(request):
    get = request.body
    try:
        uname = request.data["username"]
        password = request.data["password"]
        user = authenticate(request,username = uname,password=password)
        userp = userprofile.objects.get(user=user)
        consent = userp.consent
        if user is not None:
          if userp.admin.allowedUsage ==1 or userp.admin.allowedUsage ==3:
            return Response({"message":"Login sucessful","id":user.id,"consent":consent},status=201)
          else:
            return Response({"Error":"The admin is not allowed to use app"},status=401)
    except Exception as e:

        return Response({"Error":"Incorrect username or password"+str(e),},status=401)


@api_view(['POST'])
def fillform(request):
  print(request.data)
  username = request.data["username"]
  fathername = request.data["fathername"]
  mothername = request.data["mothername"]
  dob = request.data["dob"]
  email = request.data["email"]
  school = request.data["school"]
  idno = request.data["idno"]
  contact = request.data["contact"]
  address = request.data["address"]
  print(username,mothername)
  idi = request.data["idi"]

  up = User.objects.get(id = idi)
  articles = userprofile.objects.get(user = idi)
  articles.father_name = fathername
  articles.mother_name = mothername
  articles.DOB = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
  articles.email = email
  articles.address = address
  articles.contactno = contact
  articles.username = username
  articles.idno = idno
  articles.school = school
  articles.save()
  print(up)
  return Response({"article":articles.consent},status=201)


@api_view(['POST'])
def getSplash(request):
  try:
    idi = request.data["idi"]
    user = User.objects.get(id=idi)
    up = userprofile.objects.get(user=user)
    ad = adminuser.objects.get(user=up.admin)
    img1 = ad.image
    print(str(img1))
    img2 = ad.image2
    print(user)
    return Response({"img1":str(img1),"img2":str(img2)},status=201)
  except Exception as e:
    return Response({"message":"something went wrong"},status=401)


@api_view(['GET'])
def notifyapi(request):
    np = notify.objects.filter(user=None,greetdate=datetime.date.today())
    serial = notifyserializer(np,many=True)
    return Response({"notify":serial.data},status=201)

def email(request):
  subject = 'welcome to GFG world'
  message = f'Hi {request.user.username}, thank you for registering in geeksforgeeks.'
  email_from = settings.EMAIL_HOST_USER
  recipient_list = ["eswaritsme@gmail.com", ]
  send_mail( subject, message, email_from, recipient_list )
  return Response({"notify":serial.data},status=201)


@api_view(['POST'])
def personalnotifyapi(request):

    try:
        idi = request.data['idi']
        user = use = User.objects.get(id=idi)
        userpro = userprofile.objects.get(user=user)
        np = notify.objects.filter(user=userpro,greetdate=datetime.date.today())
        pn = notify.objects.filter(greetdate=datetime.datetime.today(),user=userpro)
        print(pn)
        alldata = list(np)+list(pn)
        serial = notifyserializer(alldata,many=True)
        return Response({"notify":serial.data},status=201)
    except Exception as e:
        print(str(e))
        return Response({"message":"something went wrong "+str(e)},status=401)

@api_view(['POST'])
def loginCheck(request):

  try:
        idi = request.data['idi']
        user = use = User.objects.get(id=idi)
        userpro = userprofile.objects.get(user=user)
        if userpro:
          return Response({"notify":userpro.username},status=201)
        else:
          return Response({"message":"something went wrong "+str(e)},status=401)
  except Exception as e:
      return Response({"message":"something went wrong "+str(e)},status=401)

