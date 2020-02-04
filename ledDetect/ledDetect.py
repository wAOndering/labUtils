# script to extract the ligth pulse from 2p laser on video 
# the idea being that the laser will drastically change the mean
# intensity of the image and this can be identied using convolution
# OpenCV is used here to read the video files

# to access file over the server Samba look into pysmb
# https://pypi.org/project/pysmb/

# useful site for manipulating video file and add a scroll bar
# https://stackoverflow.com/questions/21983062/in-python-opencv-is-there-a-way-to-quickly-scroll-through-frames-of-a-video-all

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# path the the working folder
# list of all the mp4 files
path=r'C:\Users\Windows\Desktop\cut_pole1'
path='/home/rum/Desktop/cut_pole2'
files=glob.glob(path + '/*.mp4', recursive=True)

# define parameter of interest for the video
startTime=1 #start time of the video to be detected at in minutes

# initalize the video
allStepIdx=[]
depth=[]
aidF=[]

# loop over the files to extract the information
for i in files:

	# print the file being processed
	print(i)
	
	# extract the animal id from the file path
	aid=os.path.splitext(i)[0]

	## add condtion for character conversion / \\
	aid=aid.split('/')
	aid=aid[-1]

	# load the video file to be working with
	vcap = cv2.VideoCapture(i)
	fps=int(vcap.get(5)) # frame rate of video acquisition 
	# initialize variable to store the mean intensity of each frame
	
	# start=time.time() to time the process
	vcap.set(1,fps*startTime*60) # set the starting point of the frame 6 min at 500 fps 6*500*60
	# the execution speed on while loop (faster than for loop 10000frames/14sec)
	meanFrame=[]
	while True:
		ret, frame = vcap.read()
		# height, width, layers = frame.shape
		frame=frame[280:480, 340:640]
		# cv2.imshow('Frame',frame)
		# if cv2.waitKey(25) & 0xFF == ord('q'):
  #         break
		meanFrame.append(np.mean(frame))
		if len(meanFrame) > 400000: # 10000 limit the analysis on the first 300 frames of video
			break
			vcap.release()
	# etime=(time.time()-start)

	# perform convolution to identify the step in the time series
	meanFrame -= np.mean(meanFrame)
	step = np.hstack((np.ones(len(meanFrame)), -1*np.ones(len(meanFrame))))
	step = np.flip(step) # comment out this line if the switch
	meanFrame_step = np.convolve(meanFrame, step, mode='valid')
	step_idx = np.argmax(meanFrame_step)

	# plot overview of the detection
	figure=plt.figure()
	plt.plot(meanFrame)
	plt.axvline(step_idx, color='r')
	# plt.show()
	figure.savefig(path+'/detection_'+aid+'.png', bbox_inches='tight', transparent=False, dpi=300)

	step_idx = fps*startTime*60+step_idx # correct the start time according



	# extract all the major information for one files
	allStepIdx.append(step_idx)
	aidF.append(aid)



# summary of the data for animal depth and laserOn
distMeas=pd.DataFrame({'animalID': aidF,
					   'Transition': allStepIdx})

# sort the data by animal id and depth
distMeas=distMeas.sort_values(by=['animalID','Transition'])
distMeas=distMeas.reset_index(drop=True)

pd.DataFrame.to_csv(distMeas, path+'/LaserTriggerDetect.csv')
