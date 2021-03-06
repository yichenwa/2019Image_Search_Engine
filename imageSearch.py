import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import cv2
import time
# author Yichen Wang
sift=cv2.xfeatures2d.SIFT_create()
l=[]
count1=0
starttime=time.time()
"""
1. import sample image
This part is import the sample image,get its SIFT
"""
img1 = cv2.imread("/Users/saber/Desktop/01.jpg",0)
h1,w1=img1.shape
img1=cv2.resize(img1,(int(w1/2),int(h1/2)),interpolation=cv2.INTER_CUBIC)
kp1, des1 = sift.detectAndCompute(img1, None)

"""
2. go through all images in the folder
We need to go through all images in the folder once. 
I set DATADIR to be the path to the folder "paris"
And then convert the RGB images into GRAY as the GRAY has smaller size
"""
DATADIR="/Users/saber/Desktop/534A2/paris"
CATEGORIES=["defense","eiffel","general","invalides","louvre","moulinrouge","museedorsay","notredame","pantheon","pompidou","sacrecoeur","triomphe"]
#CATEGORIES=["invalides","louvre"]

for i in range(0,len(CATEGORIES)):
    count2=count1
    category=CATEGORIES[i]#......
    path = os.path.join(DATADIR,category)
    folder_size=len(os.listdir(path))
    #for imgindex in os.listdir(path):
    #print("Let's check "+CATEGORIES[i]+" folder, it has "+str(len(os.listdir(path)))+" images")
    #for imgindex in os.listdir(path):
    for j in range(0,len(os.listdir(path))):
        imgindex=(os.listdir(path))[j]
        img2=cv2.imread(os.path.join(path,imgindex),0)

        if img2 is not None:
            #print(img1.dtype, img2.dtype)
            h2, w2 = img2.shape
            img2 = cv2.resize(img2, (int(w2 / 2), int(h2 / 2)), interpolation=cv2.INTER_CUBIC)
            """
            3. image representation
            I decide to use local features, SIFT
            """
            kp2, des2 = sift.detectAndCompute(img2, None)

            """
            4. matching
            Then use Brute-Force Matching to get k best matches, I set k=2.
            """
            bf = cv2.BFMatcher()
            if des2 is not None and len(des2)!=0:
                matches = bf.knnMatch(des1, des2, k=2)
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])

                """
                5.draw rectangle
                "good" is a list, and it contains the matched key points in img2.
                use list p to save the (x,y), get the largest and smallest x-coordinate, 
                the largest and smallest y-coordinate, then we can get the four points of rectangle.    
                """
                #print(category,len(good))
                if (len(good) >= 15):
                    p = []
                    for n in good:
                        idx = n[0].trainIdx
                        (x, y) = kp2[idx].pt
                        p.append((x, y))

                    max_x = max(p, key=lambda x: x[0])[0]
                    min_x = min(p, key=lambda x: x[0])[0]
                    max_y = max(p, key=lambda x: x[1])[1]
                    min_y = min(p, key=lambda x: x[1])[1]

                    # cv2.rectangle(img2, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (255, 0, 0), 5)
                    # cv2.imshow(str(c),img2)
                    count1+=1

                    """
                    6. ranking
                    j is the image's index in the folder
                        """
                    l.append((len(good), j, [(int(min_x), int(min_y)), (int(max_x), int(max_y))], i))


    print 'In %d th class it has %d images, gets %d images contains sample images' % (i, folder_size, count1-count2)

    #break


"""
5. ranking
    5-1 sort the list l
    5-2 select first 10 elements in l
"""

l.sort()
l=l[::-1]
if len(l) > 10:
    l = l[0:10]
a=1
for m in l:
    #print(m)
    img_idx=m[1]
    folder_idx=m[3]

    category = CATEGORIES[folder_idx]
    path = os.path.join(DATADIR, category)

    imgindex = (os.listdir(path))[img_idx]
    img = cv2.imread(os.path.join(path, imgindex))
    h, w,g = img.shape
    img = cv2.resize(img, (int(w / 2), int(h / 2)), interpolation=cv2.INTER_CUBIC)

    left_top=m[2][0]
    right_bottom=m[2][1]

    cv2.rectangle(img,left_top,right_bottom,(255,0,0),5)
    cv2.imshow(str(a), img)
    a+=1
    #cv2.waitKey(1200)

endtime=time.time()
print 'Finish in %d seconds' %(endtime-starttime)
cv2.waitKey()
cv2.destroyAllWindows()


