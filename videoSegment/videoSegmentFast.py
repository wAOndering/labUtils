import subprocess
import os 
import glob 


os.getcwd() # get the current directory
path= '/home/rum/Desktop/videoTolook'
os.chdir(path) # change the directory
files=glob.glob(path+'/*.mp4')

for i,j in enumerate(files):
	print(i,j)
	tmp=os.path.basename(j)
	if os.path.getsize(j) >= 0.5e+9:
		subprocess.call('ffmpeg -i '+tmp+' -ss 00:19:10 -to 00:35:00 cut_'+tmp, shell=True)			
	else:
		continue

		





# ## OPTIMAL CONFIG
# # this script below works fine run from the terminal
# 'ffmpeg -i 19-28-00.169.mp4 -ss 00:22:10 -to 00:22:20 outputtest.mp4'
# config_path='/home/rum/Desktop/DLC/NETWORKS/e3HighspeedWhisker-tom-2019-11-03/config.yaml'


# ## SUBOPTIMAL TOOLS
# # should be added in the following format if the string format is directly apply it does not work
# # works only producing good video when 
# start_time=1
# end_time=6
# from moviepy.video.io.VideoFileClip import VideoFileClip
# input_video_path = '/home/rum/Desktop/2019-04-04_Thy1_e3_HS-opto.mp4'
# output_video_path = '/home/rum/Desktop/test2.mp4'
# with VideoFileClip(input_video_path) as video:
#     new = video.subclip(start_time, end_time)
#     new.write_videofile(output_video_path)

# # this produce a low quality video for the video of interest could be due to encoding
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("/home/rum/Desktop/2019-04-04_Thy1_e3_HS-opto.mp4", start_time, end_time, targetname="/home/rum/Desktop/test.mp4")


