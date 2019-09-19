# DEPENDENCIES #####
# this needs to be perfomed in the deeplabcut environement
import os, pickle, yaml
import ruamel.yaml
from pathlib import Path
from deeplabcut.utils import auxiliaryfunctions
import matplotlib.pyplot as plt
import os.path
from pathlib import Path
import argparse
from deeplabcut.utils import auxiliaryfunctions
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2
import glob
from matplotlib.transforms import Bbox

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

# DATA
config_path='/home/rum/Desktop/pupilDLC/SheldonPolePupil20190402-tom-2019-04-02/config.yaml'
path='/home/rum/Desktop/pupilDLC/2019-05-22_EMX1 2nd cohort pupil'
outputVid=path+'/videoQC'
os.makedirs(outputVid, exist_ok=True)
pathDir=glob.glob(path+'**/') # list all the directory
# pathDir=[s for s in pathDir if fileDesc.Record_folder[9] in s][0]
files=glob.glob(pathDir[0]+'*.csv', recursive=True)
filehd=glob.glob(pathDir[0]+'*.h5')
filesMp4=glob.glob(pathDir[0]+'*.mp4')


for k, filel in enumerate(filehd):
    print(k, filel)

    Dataframe = pd.read_hdf(filel)
    aid=os.path.basename(os.path.splitext(filel)[0])[0:5]
    fileV=[s for s in filesMp4 if aid in s][0]

    # see line 40 https://github.com/AlexEMG/DeepLabCut/blob/2a2ad95a1ec35ad7f98d0155b4aa0d3ecedaefac/deeplabcut/utils/plotting.py
    config_file = config_path
    cfg = auxiliaryfunctions.read_config(config_file)
    scorer='DeepCut_resnet50_SheldonPolePupil20190402Apr2shuffle1_700000' # scorer = cfg['scorer']
    bodyparts = cfg['bodyparts']
    videos = cfg['video_sets'].keys()
    markerSize = cfg['dotsize']
    alpha = cfg['alphavalue']
    colormap = plt.get_cmap(cfg['colormap'])
    colormap = colormap.reversed()
    project_path=cfg['project_path']
    pcutoff=cfg['pcutoff']
    bodyparts2plot = cfg['bodyparts']
    bodyparts2plot = bodyparts2plot[4:8]
    pcutoff = cfg['pcutoff']
    colors = get_cmap(len(bodyparts2plot),name = cfg['colormap'])
    alphavalue = cfg['alphavalue']

    # plot the video
    custdpi=300
    xdimIm=1280
    ydimIm=720

    cap = cv2.VideoCapture(fileV)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    randSampleQC=np.random.randint(length, size=10)
    # Index=Dataframe[scorer][bp]['likelihood'].values > pcutoff
    for i in randSampleQC:
        print(i)
        figure= plt.figure(frameon=False, figsize=(xdimIm/custdpi, ydimIm/custdpi))
        # ax=plt.Axes(figure, [0., 0., 1., 1.])
        # ax.set_axis_off()
        Index=i
        cap = cv2.VideoCapture(fileV)
        cap.set(1, Index)
        ret, frame1= cap.read()
        plt.imshow(frame1)
        # plt.pause(0.01)
        # cap.release()

    # plot the bodyparts
        for bpindex, bp in enumerate(bodyparts2plot):
                # Index=Dataframe[scorer][bp]['likelihood'].values > pcutoff
                Index=Index
                plt.plot(Dataframe[scorer][bp]['x'].values[Index],Dataframe[scorer][bp]['y'].values[Index],'.',color=colors(bpindex),alpha=alphavalue)

        plt.axis('off')
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        # plt.show()
        # for ploting wth full screen without 
        figure.savefig(outputVid+'/'+aid+'_'+f"{i:08d}"+'.png', bbox_inches=Bbox([[0.0, 0.0], [1280/custdpi, 720/custdpi]]), pad_inches=0, dpi=custdpi) # xdimIm and ydimIm can be modified here for croping pupuse
        
        ## for ploting with just the eye 
        # this can also be custom
        # figure.savefig('/home/rum/Desktop/opencv/makeOpencvVideo/'+str(i)+'plo3.png', bbox_inches=Bbox([[300/custdpi, 500/custdpi], [450/custdpi, 650/custdpi]]), pad_inches=0, dpi=custdpi) # xdimIm and ydimIm can be modified here for croping pupuse
        plt.close('all')
    #plt.gca().invert_yaxis()
    # plt.show()






























img_array = []
for filename in glob.glob('/home/rum/Desktop/opencv/makeOpencvVideo/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

fps=2
out = cv2.VideoWriter('/home/rum/Desktop/opencv/makeOpencvVideo/project1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()




# To plot some video
# this enables to plot few frames of the video to control if 
# the convolution was done properly
custdpi=300
xdimIm=1280
ydimIm=720

for i, j in enumerate(fileV):
    # aid=j.split(os.sep)[-1]
    # aid=aid.split('.')[0]
    # fFtmp=firstFrame[firstFrame.id == aid]['frame'][0]

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




## VIDEO PLAYING ##
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(fileV)
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
      # Break the loop
      else: 
        break
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()