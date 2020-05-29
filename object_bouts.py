# -*- coding: utf-8 -*-
"""
Created on Sun May 24 21:43:23 2020

@author: Kadjita Asumbisa and Jia-Ru Chang
"""

from scipy.spatial import distance
import pandas as pd
import matplotlib.pyplot as plt


def object_bouts(filename, bout_distance, framerate):
    """
    Args: filename: Path to an excel file with animal pos X and Y in cols 1 and 2 
        and fixed object XY position in remaining columns i.e X1,Y1,X2,Y2,X3,Y3 
        corresponing to each object point. ALternatively, excel output from DeepLabcut
        can simply be used as input. i.e 'C:/Users/kasum/Downloads/Trenholm_lab-master/data.xlsx'
        
        bout_distance: an int or float corresponding to the threshold(distance) 
        for counting bouts. i.e 50
        framerate: an int or float of the capture frame rate of the camera in Hz. i.e 30 
    
    Returns: 
        fig: a figure showing trajectory plot, object points and detected bouts
        bouts: dictionary of bout counts and total duration of bouts in seconds
        
    """    
    position_data=pd.read_excel(filename) #read_excel file with position data
    
    animal_pos=position_data.iloc[:,:2] #Extract animal XY cordinates for all frames
    obj_pos=position_data.iloc[0,2:] #Extracts all the XY fixed object coordinates from frame 1
    
    #Extracting object pos for X and Y. Object pos are arranges in a series of X and Y
    obj_x=[obj_pos[i] for i in range(0,len(obj_pos),2)] #Even i corresponds to X
    obj_y=[obj_pos[i+1] for i in range(0,len(obj_pos),2)] #Odd i corresponds to Y
    
    #Initializing counts for bouts and corresponding animal XY pos for each bout
    obj_bouts=0
    bouts_xpos=[]
    bouts_ypos=[]
    
    #Computing object approach bouts using euclidean distance
    for i in range(len(obj_x)): #iterate through number of object xy pair counts
        for j in range(len(animal_pos)): 
            dist=distance.euclidean([obj_x[i],obj_y[i]], [animal_pos.iloc[j,0],animal_pos.iloc[j,1]])
            if dist <= bout_distance: #Threshold for counting bouts
                obj_bouts+=1
                bouts_xpos.append(animal_pos.iloc[j,0])
                bouts_ypos.append(animal_pos.iloc[j,1])
    
    #Dividing the bout count by frame rate gives the totol duration of bouts in secs        
    bout_duration=obj_bouts/framerate
        
    bouts={'tot_bouts':obj_bouts,'bout_duration': bout_duration } #dict of data to be returned
    
    ######## PLOTS #################################
    #Trajectory plot
    fig=plt.figure()
    path, =plt.plot(animal_pos.iloc[:,0].values,animal_pos.iloc[:,1].values,c='grey') # ',' in var defnition allows us to store only 1st item(1d).This makes the handle 1d for easy grp legend calls 
    
    #Object points plot
    for i in range(0,len(obj_pos),2):
        obj=plt.scatter(obj_pos[i],obj_pos[i+1],c='black')
    
    #Bouts plot                                       
    bout=plt.scatter(bouts_xpos,bouts_ypos,c='r', alpha=0.5)
    plt.legend([path,obj,bout],['path','object','bout'],loc='best')
    plt.gca().set_yticks([])
    plt.gca().set_xticks([])
    plt.show()  
    
    return fig, bouts


filename=r'C:\Users\kasum\Downloads\Trenholm_lab-master\data.xlsx' #filepath
    
fig,bouts_data=object_bouts(filename,100,30)
