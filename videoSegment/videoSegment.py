###
# this is to generate non-contiguous files 
###

# DEPENDENCIES #####
# this needs to be perfomed in the deeplabcut environement
import os
import matplotlib
import matplotlib.pyplot as plt
import os.path
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import cv2
import glob
from matplotlib.transforms import Bbox
from datetime import datetime
import shutil

text_params = {'ha': 'center', 'va': 'center', 'family': 'sans-serif',
               'fontweight': 'bold'}

# script input
    # path='C:/Users/Windows/Desktop/Media Files2'
    # timeShock = pd.read_csv('C:/Users/Windows/Desktop/Media Files2/time.txt', header=None, names=["shock"], infer_datetime_format=True)
    # rangeAroundShockBefore = 1 # range around the shock in seconds
    # rangeAroundShockAfter = 2
    # videoFormat = 'mpg'


# user input
print('\n##########################################################')
print('# VIDEO SEGMENTATION SOFTWARE                            #')
print('##########################################################')
print('\nThis software will output a video that is a segment of the original for a user \ndefined interval around time of interest stored in a txt file containing time of interest.')
print('The time of interest will be labeled by a red dot in the video.')
rangeAroundShockBefore= int(input('\ninterval of time in seconds to be extracted \nBEFORE the time point of interest (shock):'))
rangeAroundShockAfter= int(input('interval of time in seconds to be extracted \nAFTER the time point of interest (shock):'))

path= input('path to the behavior video of interest (eg. C:\\Users\\Windows\\Desktop\\Media Files):') 
path = os.path.normpath(path)
print(path)

print('\nname of the text file that contains all the times of interest')
print('the times should be as follow 01:30 (for 1 minute and 30 seconds)')
timeShock=input(' (located in the same path as the behavior video - eg: time.txt):') 
timeShock=path+'/'+timeShock
timeShock=pd.read_csv(timeShock, header=None, names=["shock"], infer_datetime_format=True)
print(timeShock)

videoFormat = input('extension of the video files (eg. mp4 or mpg, etc.):')

# DATA where the video are located 
outputVid=path+'/tmp'
os.makedirs(outputVid, exist_ok=True)
filesOri=glob.glob(path+'/*.'+videoFormat)
filesMp4=glob.glob(path+'/*.'+'mp4')

# DATA to record the time of interest
# timeShock.shock=[datetime.strptime(x,'%M:%S') for x in timeShock.shock]
timeShock = timeShock.shock.str.split(':', expand=True).astype(int)
s = pd.to_timedelta(timeShock[0], unit='m') + pd.to_timedelta(timeShock[1], unit='s')
timeShock = s.dt.total_seconds() # time shock in seconds

#Potential implementation of subprocess for conversion
# if filesMp4 == []:
#     for filesVididx, filesVid in enumerate(filesOri):
#         print(filesVid)
#         subprocess.call(['ffmpeg','-i',video[0],'-ss','00:00:00','-to','00:00:00.4','-c','copy',output1])


# create the images with the label plots those will be discarded afterwards
for i, j in enumerate(filesOri):
    print(i,j)
    outName=os.path.splitext(j)[0]
    outName=os.path.basename(outName)
    # video properties
    # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
    cap = cv2.VideoCapture(j)
    length = cap.get(7)# int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    # need to be careful with the frame rate not being always an integer this can create major delay
    # delt with below
    fps    = cap.get(5) #cap.get(cv2.CAP_PROP_FPS)
    timeShock1 = timeShock*fps # time shock converted to the number of frames
    timeShock1=timeShock1.round()
    timeShock1=timeShock1.astype(int)
    custdpi=72
    xdimIm=int(cap.get(3)) # 1280
    ydimIm=int(cap.get(4)) #720
    fps=round(fps)

    for ki, kk in enumerate(timeShock1):
        print('processing...')
        # print(ki, kk)
        
        for i in range(kk-(rangeAroundShockBefore*fps),kk+(rangeAroundShockAfter*fps), 1):
            figure= plt.figure(frameon=False, figsize=(xdimIm/custdpi, ydimIm/custdpi))
            ax=plt.Axes(figure, [0., 0., 1., 1.])
            ax.set_axis_off()
            Index=i
            cap = cv2.VideoCapture(j)
            cap.set(1, Index)
            ret, frame1= cap.read()
            plt.imshow(frame1)
            # plt.pause(0.1)
            # cap.release()

            if i >= kk and i <=kk+fps:
                plt.plot(xdimIm/2,ydimIm/2, color='red', marker='o', markersize=40)
                plt.text(xdimIm/2,ydimIm/2, str(ki), fontsize=34, **text_params, color='white')
                # print(i,'hello')
                # print(i)
            if i == (kk+(rangeAroundShockAfter*fps)-1):
                img = np.zeros((xdimIm,ydimIm,3), np.uint8)
                img = cv2.rectangle(img,(0,0),(xdimIm,ydimIm),(255,255,0),-1)
                plt.imshow(img)

            plt.axis('off')
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
            figure.savefig(outputVid+'/'+outName+'_'+f"{ki:02d}"+'_'+f"{i:08d}"+'.png', bbox_inches=Bbox([[0.0, 0.0], [xdimIm/custdpi, ydimIm/custdpi]]), pad_inches=0, dpi=custdpi) # xdimIm and ydimIm can be modified here for croping pupuse
            plt.close('all')

    # create the final video of interest
    img_array = []
    for filename in glob.glob(outputVid+'/'+outName+'*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(path+'/'+outName+'_'+str(rangeAroundShockBefore)+'-'+str(rangeAroundShockAfter)+'s'+'_segment.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    # remove all the images which are not necessary anymore
shutil.rmtree(outputVid)