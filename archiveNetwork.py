#### ----------------------------------
#### function 
#### ----------------------------------

import glob
import os
import concurrent.futures

def commonElement(list1, list2, option='dext'):
	'''
	function to identify common element in the list

	option: 'dext' enables to look at the basefilename without the extension useful to check if the files
	were in deed compressed

	'''
	if option == 'dext':
		list1 = [x.split(os.sep)[-1].split('.')[0] for x in list1]
		list2 = [x.split(os.sep)[-1].split('.')[0] for x in list1]

	commonElem = [x for x in list1 if x in list2]

	print('There are', len(commonElem), 'out of', max(len(list1), len(list2)), 'files which are common')

	notcommonElem = []
	if max(len(list1), len(list2)) != len(commonElem):
		notcommonElem = [x for x in list1 if x not in list2]
		# alternatively could use np.setdiff1d(list1, list2)
		print('None common element are:')
		print(notcommonElem)
	else:
		print('No none common element found')

	return notcommonElem

def archiveBinList(lastDate='2020-01-09'):
	'''
	this function is to archive all the folder that were in the acquired and for which the binaries
	have been converted
	this could also be baed on the presence of absence of the output folder in the parent directory
	lastDate: correspond to the string of character that are necessary to idenfy for when to archive
	'''
	path = '/run/user/1000/gvfs/smb-share:server=ishtar,share=millerrumbaughlab/Jessie/e3 - Data Analysis/e3 Data' 
	binaries = glob.glob(path+'/**/*.bin', recursive=True)
	binaries.sort()
	indexToStopArchived = [(i,j) for (i,j) in enumerate(binaries) if lastDate in j][-1][0]
	archBin = binaries[:indexToStopArchived]
	return archBin
def archiveDatFct(file):
	'''
	this function is to split a path into its useful components

	''' 
	customName = 'binArchive'
	os.makedirs(path+os.sep+customName, exist_ok=True)
	fileSplit = file.split(os.sep)
	os.makedirs(os.sep.join(fileSplit[:-2])+os.sep+customName+os.sep+fileSplit[-2], exist_ok=True)
	archName = os.sep.join(fileSplit[:-2])+os.sep+customName+os.sep+os.sep.join(fileSplit[-2:])
	
	os.rename(file, archName)


archBin = archiveBinList(lastDate='2020-01-09')

tmplist = glob.glob('/run/user/1000/gvfs/smb-share:server=ishtar,share=millerrumbaughlab/Jessie/e3 - Data Analysis/e3 Data/2019-03-25_15-07-07/*.txt') 


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(archiveDatFct, archBin)


#### ----------------------------------
#### to run common element 
#### ----------------------------------

# video for list comparison
list1 = '/run/user/1000/gvfs/smb-share:server=ishtar,share=millerrumbaughlab/Jessie/e3 - Data Analysis/e3 Data/allVideos/inDLCpipeline/'
list1 = glob.glob(list1+'*.mp4')

list2 = '/run/user/1000/gvfs/smb-share:server=ishtar,share=millerrumbaughlab/Jessie/e3 - Data Analysis/e3 Data/allVideos/avi_Process/done/'
list2 = glob.glob(list2+'*.avi')


commonElement(list1, list2, option='dext')