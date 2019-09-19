# script to extract the first frame after LED 
# dependencies 
import glob
import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
#
path='/home/rum/Desktop/pupilDLC/2019-08-28-EMXRUM2-wheel/'
# path='Y:\\Sheldon\\awake_gcamp_vids\\2plight'
files=glob.glob(path + '*shockFrameTime.csv', recursive=True)
filesVideo=glob.glob(path + '*.mp4', recursive=True)

# To extract the first frame of the video when the LED appear
firstFrame=[]
for i, j in enumerate(files):
	print(i,j)
	aid=j.split(os.sep)[-1]
	aid=aid.split('_')[0]
	dt=pd.read_csv(j)
	firstFrameTmp=pd.DataFrame({'id': [aid],
				  'frame': [dt.shockFrame[0]],
				  'secFromStart':[dt.shockFrame[0]/30]})
	firstFrame.append(firstFrameTmp)

firstFrame=pd.concat(firstFrame)
pd.DataFrame.to_csv(firstFrame, path+'firstFrame.txt')





# To plot some video
# this enables to plot few frames of the video to control if 
# the convolution was done properly
custdpi=300
xdimIm=1280
ydimIm=720

filesVideo=glob.glob(path + '*.mp4', recursive=True)
for i, j in enumerate(filesVideo):
	aid=j.split(os.sep)[-1]
	aid=aid.split('.')[0]
	fFtmp=firstFrame[firstFrame.id == aid]['frame'][0]

	for i in range(fFtmp-2,fFtmp+2, 1):
	    print(i)
	    figure= plt.figure(frameon=False, figsize=(xdimIm/custdpi, ydimIm/custdpi))
	    # ax=plt.Axes(figure, [0., 0., 1., 1.])
	    # ax.set_axis_off()
	    Index=i
	    cap = cv2.VideoCapture(j)
	    cap.set(1, Index)
	    ret, frame1= cap.read()
	    cv2.imshow('Frame',frame1)
	    plt.pause(0.1)
	    cap.release()

	plt.close('all')