import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

path=r'C:\Users\Windows\Desktop\cut_pole1'
outputVid=path+'/videoQC'
os.makedirs(outputVid, exist_ok=True)

files=glob.glob(path + '\\*.csv', recursive=True)
dt=pd.read_csv(files[0])

files=glob.glob(path + '\\*.mp4', recursive=True)

# loop over the files to extract the information
for i in files:
    # print the file being processed
    print(i)
    
    # extract the animal id from the file path
    aid=os.path.splitext(i)[0]
    aid=aid.split('\\')
    aid=aid[-1]

    transVal=dt.loc[dt.animalID == aid, 'Transition'].iloc[0]
    sample=range(transVal-2,transVal+3)
    vcap = cv2.VideoCapture(i)

    for jj in sample:
        figure= plt.figure()
        vcap.set(1,jj)
        ret, frame= vcap.read()
        plt.imshow(frame)
        figure.savefig(outputVid+'/'+aid+'_'+f"{jj:08d}"+'.png') # xdimIm and ydimIm can be modified here for croping pupuse
        plt.close('all')

