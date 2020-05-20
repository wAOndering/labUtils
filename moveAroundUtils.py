path1=r'Y:\MLGroup\shock_test\Group 250 frames to label - C&Y\All 250 frames'
path2=r'Y:\MLGroup\shock_test\Group frames combined ~ 920'
filesList=glob.glob(path1+'/*.png')
allFiles=glob.glob(path2+'/*.png')

allFiles=[os.path.basename(s) for s in allFiles]
filesList=[os.path.basename(s) for s in filesList]

nonUsed=set(allFiles)-set(filesList)
nonUsedOld=[path2+'/'+s for s in nonUsed]
nonUsedNew=[newPath+'/'+s for s in nonUsed]

[os.rename(s) for s in filesList]

newPath='Y:/MLGroup/shock_test/Group 250 frames to label - C&Y/TooChoseFromForCris'

for i,j in enumerate(nonUsedOld):
	print(nonUsedOld[i], nonUsedNew[i])
	os.rename(nonUsedOld[i], nonUsedNew[i])


if str(aid) in s]

# manipulation for file names
import os
import time
import glob

path = input('path to csv files (eg. C:\\Users\\) :') #C:\Users\Windows\Desktop



path='D:\highspeed_vids\EMX1_for_Tom'
path = os.path.normpath(path)
os.chdir(path)


# rename all the pole video 
pole=glob.glob(path + '/**/*pole*.mp4', recursive=True)
for k in range(len(pole)):
		rena=os.path.dirname(pole[k])+'\\'
		os.rename(pole[k], rena+'00-00-00.000.mp4')

# rename all the files with their n+2 parent directory spltit[-3]
l_dir=[] 
files = glob.glob(path + '/**/*.mp4', recursive=True)
for i in range(len(files)):
	ldir=os.path.abspath(os.path.dirname(files[i]))
	split=files[i].split(os.sep)
	rename=ldir+'\\'+split[-3]+'_'+'_'+split[-1]
	#rename=ldir+'\\'+str(os.path.getctime(files[i]))+split[-3]+'_'+'_'+split[-1]
	os.rename(files[i], rename)

# move all the baseline files to baseline dir
os.makedirs('baseline')
baselinefiles=glob.glob(path + '/**/*baseline*.mp4', recursive=True)
for j in range(len(baselinefiles)):
	ren=os.path.join(path, 'baseline')+'\\'
	os.rename(baselinefiles[j], ren+os.path.basename(baselinefiles[j]))
	# need to modify this to go one more directory up

os.makedirs('outputs')
outputfiles=glob.glob(path + '/**/*output*.mp4', recursive=True)
for j in range(len(outputfiles)):
	ren=os.path.join(path, 'outputs')

	ldir=os.path.abspath(os.path.dirname(outputfiles[j]))
	split=outputfiles[j].split(os.sep)
	rename=ren+'\\'+split[-3]+'_'+split[-1]

	os.rename(outputfiles[j], rename)



# here have a line processing or calling sweep
#to test subprocess concate
#subprocess.call('ffmpeg -r 10 -i frame%03d.png -r ntsc '+str(out_movie), shell=True
# https://github.com/kkroening/ffmpeg-python

# correct potential error
# rename all the files with their n+2 parent directory spltit[-3]
l_dir=[] 
files = glob.glob(path + '/**/*.mp4', recursive=True)
for i in range(len(files)):
	ldir=os.path.abspath(os.path.dirname(files[i]))
	rename=ldir+'\\'+files[i].split('_')[-1]
	#rename=ldir+'\\'+str(os.path.getctime(files[i]))+split[-3]+'_'+'_'+split[-1]
	os.rename(files[i], rename)

# remove the files if needed
outputfiles=glob.glob(path + '/**/*output*.mp4', recursive=True)
for j in range(len(outputfiles)):
	os.remove(outputfiles[j])

outputfiles=glob.glob(path + '/**/mylist.txt', recursive=True)
for j in range(len(outputfiles)):
	os.remove(outputfiles[j])