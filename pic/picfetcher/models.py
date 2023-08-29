from django.db import models
import cv2
from accounts.models import userprofile
import os
from uuid import uuid4
from pic.settings import BASE_DIR
from django.utils.deconstruct import deconstructible
import numpy as np
from PIL import Image
import re
from . import imgpro
# import fingerprint_enhancer

# Create your models here.
@deconstructible
class PathAndRename(object):
    path=""
    def __init__(self, sub_path):
        print("======= sub path =======")
        print(sub_path)
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.name:
            filename = '{}.{}'.format(instance.name, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("pics")



class content(models.Model):


    thumbnail = models.ImageField(upload_to=path_and_rename)
    name = models.CharField(max_length=70,default="")
    camera_selected = models.CharField(max_length=6,default="False")
    publishedDate = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(userprofile,null=False,on_delete=models.CASCADE)
    processedimg = models.ImageField(upload_to=path_and_rename,null=False)


    def __str__(self):
        return  self.name



    def save(self, *args, **kwargs):
        super(content,self).save(*args, **kwargs)
        if self.camera_selected == "True":
            # w = 718
            # h =1276
            # d =(w,h)
            # img = cv2.imread(self.processedimg.path,0)
            # img = cv2.medianBlur(img,3)

            # th1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,0)

            # # th1 = cv2.medianBlur(th1,3)

            # cv2.imwrite(self.processedimg.path,th1)
            print("about to call imgpro...")

            imgpro.main(self.thumbnail.path,self.processedimg.path)

            # pa = re.search('/pics/(.+?).png',self.thumbnail.path).group(1)
            # print(pa)
            # # rgb  = th1.convert('RGB')
            # # rgb.save(os.path.join(str(BASE_DIR)+"/processedimg/"+"self.name"+"processed.jpg"))
            # cv2.imwrite(os.path.join(str(BASE_DIR)+"/media/processedimg/"+pa+"processed.png"),th1)
            # self.processedimg ="/processedimg/"+pa+"processed.png"

            #laplacien
            #s = cv2.Laplacian(img,cv2.CV_64F,ksize=11)

            #canny
            #img2 = cv2.GaussianBlur(img,(3,3),0)
            #s=cv2.Canny(img2, 15, 20)
            #s=cv2.Laplacian(img,cv2.CV_64F,ksize=11)

            #if(self.camera_selected == "True"):
                #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                #img =cv2.resize(img,d,interpolation = cv2.INTER_AREA)
                #img = img[590:1500,580:1300]
                #img = img[520:1750,750:1300]



            #s = cv2.Sobel(img, cv2.CV_64F, 0, 1,ksize=7)

            # Sharpening_kernal = np.array([
            #                              [9,-9,9],
            #                              [-9,0,-9],
            #                              [9,-9,9]
            #                              ])


           # s1 = cv2.Sobel(img, cv2.CV_64F, 0, 1,ksize=3)
            #s = cv2.Sobel(img, cv2.CV_64F, 1, 0,ksize=15)

            #sx = cv2.bitwise_or(s,s1)
            #cv2.imwrite(self.thumbnail.path,s)

            # i = cv2.imread(self.thumbnail.path)
            # #imgsharp = cv2.filter2D(i,-1,Sharpening_kernal)
            # out = fingerprint_enhancer.enhance_Fingerprint(i)

            #out=cv2.medianBlur(np.float32(i),3)



            # cv2.imwrite(self.thumbnail.path,out)

            # picture = Image.open(self.thumbnail.path)
            # picture.save(self.thumbnail.path,
            #         "JPEG",
            #         optimize = True,
            #         quality = 80)
