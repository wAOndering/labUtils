import subprocess
import os 
import glob 
import pandas as pd 
from tqdm import tqdm # used to measure remaining time progress

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

# read the shocktimes
path='/home/rum/Desktop/MakeVid'
videolist=glob.glob(path+'/*.mp4')
os.makedirs(path+'/output/', exist_ok=True)

files=path+'/'+'shocktime.csv'
files=pd.read_csv(files)
for i,j in tqdm(enumerate(files.ID)):
	print(i,j)
	tmplst=files.iloc[i,2:].tolist()
	for ii in tmplst:
		print(ii)
		tti=ii.split(':')
		tti=[int(x) for x in tti]
		tti=tti[0]*60+tti[1]
		jStart=convert((tti-4*30)/30)
		jStop=convert((tti+4*60)/30)
		tmp=[s for s in videolist if str(j) in s][0]
		subprocess.call('ffmpeg -i '+tmp+' -ss '+jStart+ ' -to '+ jStop + ' ' + tmp+'_cut_'+str(tti)+'.mp4', shell=True)
		

croppedVid=glob.glob(path+'/*_cut_.mp4')
outfile = open(path+"/listconcat.txt", "w")
print >> outfile, "\n".join(str(i) for i in your_list)
outfile.close()



path=r'C:\Users\Windows\Desktop\output'
filesList=glob.glob(path+'/*cut*.mp4')


filesList=['file ' + x for x in filesList]
filesList=pd.DataFrame({'frame':filesList})


import json

# open output file for writing
with open('listfile.txt', 'w') as filehandle:
    json.dump(filesList, filehandle)

import os
cwd = os.getcwd()
os.chdir('C:/Users/Windows/Desktop/output/')


	subprocess.call('ffmpeg -f concat -safe 0 -i ttest.txt -c copy output21.mp4', shell=True)