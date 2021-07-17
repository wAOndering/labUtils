import pandas as pd
import glob
import os
import subprocess
import concurrent.futures
import time

# could be worht a read for future improvements
# https://towardsdatascience.com/faster-video-processing-in-python-using-parallel-computing-25da1ad4a01

def checkFileSize(listoffiles):
    sizeAll = []
    for i in listoffiles:
        size = os.path.getsize(i)
        sizeAll.append(size)
    sizeAll = sum(sizeAll)*10**-9 # get the sum of all the files 
    # useful for file size
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    # print ('{:,.0f}'.format(os.path.getsize(sizeAll)/float(1<<30))+" GB")
    print('file size is ', sizeAll, 'GB')
    return sizeAll

def nameNew(fileName):
    fileName = fileName.split('.')[0]+'.mp4'
    # folderNameSplit = fileName.split(os.sep)
    # folderNameSplit = os.sep.join(folderNameSplit[1:-1])
    # fileName = fileName.split(os.sep)[-1].split('.')[0]+'.mp4'
    # folderName = r'C:\Users\Windows\Desktop\SpeedUPVID'+os.sep+folderNameSplit
    # fileName = folderName+os.sep+fileName
    # os.makedirs(folderName, exist_ok=True)
    return fileName

def tmpFct(file):
    newi = nameNew(file)

    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ''' Conversion note 
    -codec:v : mpeg4 necessary to be able to have good fps tbn tbr matching
    -r: enables to have the frame rate of intres
    -qscale:v: this is the quality of the video
    -codec:a: needed to have audio codec
    -video_track_timescale: force the tbn value
    '''
    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 500 -qscale:v 10 -codec:a copy -video_track_timescale 500 '+ newi , shell=True)
    print(file, newi)


mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.avi')

with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        executor.map(tmpFct, files)

finish = time.perf_counter()
print("Finished in time : ", finish)