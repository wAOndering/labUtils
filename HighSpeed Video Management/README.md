# Highspeed video compression

## Introduction

This is a set of scripts to facilitate the management of acquisition video and ensuring there proper encoding with software like [whisk](https://github.com/nclack/whisk)

The main objective is to obtain readable video that can be compressed while retaining software compatibility. As some of the highspeed video aquired are 

## Process 
1. Acquire highspeed video with StreamPix (Norpix software) as `*.seq` file
2. Use batch conversion utilities from StreamPix (Norpix software) to convert `*.seq` to `*.avi`
3. Convert/encode the `*.avi` to `*.mp4`
- windows open `cmd`
- go to the folder (with `cd`) where the script `avi2mp4.py` is located
- run the script `python avi2mp4.py`
- this enables the conversion of 14Tb --> 0.14Tb overnight

## Downstream analysis

### Analysis with whisk
**important consideration:**
- we encountered memory issues when running long highspeed video with whisk thus the video can be sliced 
- encoding is critical to have tbc, tbn and tbr consistent (see whisk issues [here](https://github.com/nclack/whisk/issues/35))  

**key points for ffmpeg usage:**
`-codec:v`: mpeg4 necessary to be able to have good fps tbn tbr matching
`-r`: enables to have the frame rate of intres
`-qscale:v`: this is the quality of the video
`-codec:a`: needed to have audio codec
`-video_track_timescale`: force the tbn value



