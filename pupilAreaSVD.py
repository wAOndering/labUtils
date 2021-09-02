import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
import os

def distfrom0(x,y):
    ''' this calculate distance assuming that the pupil has been centered on 0 see pupilArea function'''
    length = (x**2 + y**2)**0.5
    return length

def readHdf(file):
    ''' function to flatten the hdf files 
    '''
    vname = file.split(os.sep)[-1].split('DLC')[0]
    scorer = file.split(os.sep)[-1].split('.h5')[0].split(vname)[-1]

    if '_filtered' in scorer:
        scorer = scorer.split('_filtered')[0]

    df = pd.read_hdf(file, "df_with_missing")
    df = df[scorer]
    # drop the multi index and change the column names
    df.columns = [''.join(col) for col in df.columns]
    # reset row index
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'frame'}, inplace=True)

    return df

def pupilArea(xArray, yArray, plotOption = False):
    '''
    this function enables the determination of the pupil area based on components of the SVD
    
    Args:
    xlist: corresponde to the x-coordinates of the points
    ylist: corresond  to the y-coordinates of the points
    '''
    if type(xArray) != np.ndarray:
        xArray = np.array(xArray)
    if type(yArray) != np.ndarray:
        yArray = np.array(xArray)

    xOri = copy.copy(xArray)
    yOri = copy.copy(yArray)
    # center the peripheral points to 0
    xmean, ymean = xArray.mean(), yArray.mean()
    xArray -= xmean
    yArray -= ymean

    # use SVD to fit the elipse on the points
    U, S, V = np.linalg.svd(np.stack((xArray, yArray))) 

    # get a and b from ellipse equation correpsonding to the major axis of the elipse
    transform = np.sqrt(2/len(xArray)) * U.dot(np.diag(S))  
    a = distfrom0(transform[0][0], transform[0][1])
    b = distfrom0(transform[1][0], transform[1][1])

    eArea = np.pi*a*b


    if plotOption == True:
        plt.figure()
        plt.plot(xOri, yOri, '.', label='original pupil detect') 
        plt.plot(xArray, yArray, '.', label='0-ctr pupil detect')
        tt = np.linspace(0, 2*np.pi, 1000)
        circle = np.stack((np.cos(tt), np.sin(tt)))    # unit circle    
        fit = transform.dot(circle) + np.array([[xmean], [ymean]])
        ctrfit = transform.dot(circle)
        plt.plot(fit[0, :], fit[1, :], label='ori_fit')
        plt.plot(ctrfit[0, :], ctrfit[1, :], 'r', label='norm_fit')



        plt.plot([0,transform[0][0]], [0,transform[0][1]], 'k', label='norm_fit')
        plt.plot([0,transform[1][0]], [0,transform[1][1]], 'k', label='norm_fit')

        plt.xlabel('pixel in x')
        plt.ylabel('pixel in y')
        plt.text(transform[0][0]/2, transform[0][1]/2+5, r"a", size=12)
        plt.text(transform[1][0]/2+10, transform[1][1]/2, r"b", size=12)

        plt.suptitle('a: '+ "{0:.2f}".format(a) + 'px // b: ' + "{0:.2f}".format(b) + 'px // area: ' r"{0:.2f}".format(eArea)+'px'+r'$^2$')
        plt.legend()
        plt.show()

    return a, b, eArea


xArray= np.array([215.5597229 , 245.46385193, 298.2673645 , 351.57635498,
       374.80493164, 351.94219971, 290.47238159, 244.37632751])
yArray= np.array([252.43092346, 195.86381531, 172.02670288, 195.4186554 ,
       240.27752686, 290.78457642, 319.05545044, 297.3888855 ])

pupilArea(xArray, yArray, True)

file = r"Y:\Sheldon\human pupil\ZooTomDLC-tom-2021-01-04\videos\SDM_lightsDLC_resnet50_ZooTomDLCJan4shuffle1_650000_filtered.h5"
df = readHdf(file)
colx = [x for x in df.columns if 'x' in x]
coly = [x for x in df.columns if 'y' in x]
givenFrame = 600
x = np.array(df.loc[givenFrame,colx])
y = np.array(df.loc[givenFrame,coly])
pupilArea(x, y, True)
