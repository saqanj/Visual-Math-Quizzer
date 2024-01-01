# This is a test Last working with all caps variables, debuggin statements for arch path < 3 still in code
# Linear Motion Easy Graphical Asset
# Moves an image along a linear demarcated path against a background image
# Image files must be .png

# Visuals/Sounds

import os
import struct
import time
import tkinter as tk
from math import ceil, pi
from platform import system

# CONSTANTS

# movement type
# 0 is step movement (moves directly from one step to the next)
# 1 is continuous linear/sliding movement
# 2 is continuous arc movement

MOVE_STEP = 0
MOVE_LINEAR = 1
MOVE_ARC = 2

# VARIABLES

# images - files MUST be .png
background_imgfile = ""
moving_object_imgfile = ""
shrink_object_factor = 0  # moving object scale down factor, the larger the positive value, the smaller the object 

# sound
soundfile = ""   # the sound to play at each movement, initially default to no sound associated with movements

# coordinates (x,y) - start from upper left corner, positive y goes down
start_point = (0, 0) # start of the tick mark line
end_point = (0, 0)   # end of the tick mark line




class Image(tk.Canvas):
    def __init__(self, parent, backfile, movefile, scale_factor,start_x,start_y,end_x,end_y,max_steps,tick_len,move_type):
        
        """
        Args:
            parent (tk.Tk): parent tkinter object, meant to be the tkinter root
            backfile (str) : name of .png file containing the background image
            movefile(str) : name of .png file containing the moving object's image
            scale_factor (int) : amount by which to scale down moving object, larger number, the smaller the image becomes
            start_x (int): x coordinate of the beginning of path with (0,0) being the top left corner for all coordinates
            start_y (int): y coordinate of the beginning of path
            end_x (int): x coordinate of the end of path
            end_y (int): y coordinate of the end of path
            max_steps (int): number of steps on the linear path
            tick_len (int) : vertical length of the individual tick marks, positive values bove line, negative values below line 
            move_type (int): valid values : 0,1,2 indicating the type of movement between steps
            
        """

        global background_imgfile
        global moving_object_imgfile
        global shrink_object_factor
      
        global start_point
        global end_point
        global movement_type


        
        background_imgfile = backfile
        moving_object_imgfile = movefile
        shrink_object_factor = scale_factor
        start_point= (start_x,start_y)
        end_point = (end_x, end_y)
        movement_type= move_type    #must be 0, 1 or 2
          
        tick_mark_length =   tick_len #vertical length of the individual tick marks, positive values above line, negative values below line
        



        # canvas init
        
       
        self.background_file = tk.PhotoImage(file=background_imgfile)    # find background image
        tk.Canvas.__init__(self, parent, width=self.background_file.width(), height=self.background_file.height())

        # var initializations
        self.start = start_point
        self.end = end_point
        self.max_steps = max_steps
        self.current_object_index = 0   # current location (by steps taken)
        self.falling = False    # keeps track of if object is falling (to prevent errors)

        check_this_file_for_errors()

        # add background
        background_image = self.create_image(0,0,anchor=tk.NW,image=self.background_file)
        
        # define and create tick marks
        line = self.create_line(start_point[0],start_point[1],end_point[0],end_point[1])
        xdistance = end_point[0]-start_point[0]
        m = (end_point[1]-start_point[1])/(end_point[0]-start_point[0])
        b = start_point[1]-(m*start_point[0])
        f = lambda x: m*x+b # slope-intercept equation
        self.tick_marks = [(x, f(x)) for x in [xdistance/max_steps * i + start_point[0] for i in range(max_steps+1)]]
        for x, y in self.tick_marks:
            line = self.create_line(x, y, x, y+tick_mark_length)
        self.xmove = xdistance/max_steps
        self.ymove = (end_point[1]-start_point[1])/max_steps

        # add image for moving object at start
        self.file = tk.PhotoImage(file=moving_object_imgfile).subsample(shrink_object_factor,shrink_object_factor) # subsample scales image
        
        self.image = self.create_image(start_point[0], start_point[1], anchor=tk.S, image=self.file)

        

    def set_move_sound(self, path_to_soundfile):
        
        """ Associates a sound to automatically be played with each movement
        Args:
            path_to_soundfile (str): the path to the new sound
        """

        global soundfile
        
        if not os.path.exists(path_to_soundfile):
            raise FileNotFoundError(path_to_soundfile+" doesn't exist. Sound file must be in the same folder as program file")
        if path_to_soundfile[-4:] != '.wav' and path_to_soundfile[-4:] != '.mp3':
            raise Exception('Sound file must be .wav or .mp3')
        soundfile = path_to_soundfile
        
       
    def clear_move_sound(self):

        
        """ Disassociated any sound with each movement, causing movements to be silent
        Args:
            none
            
        """
        
        global soundfile
        soundfile = ''

        

    def play_sound(self,path_to_sound_file):

        """ Immediately plays the specified sound file
        Args:
            path_to_sound_file (str): the path to the .wav or .mpa sound file to play
            
        """
 
        if not os.path.exists(path_to_sound_file):
            raise FileNotFoundError(path_to_sound_file+" doesn't exist. Sound file must be in the same folder as program file")
        if path_to_sound_file[-4:] != '.wav' and path_to_sound_file[-4:] != '.mp3':
            raise Exception('Sound file must be .wav or .mp3')
        
        playsound(path_to_sound_file)


    def set_moving_element(self, path_to_image_file,image_scale):
        
        """ Changes the image for the moving object and its scale factor
        Args:
            path_to_image_file (str): the path to the new object image
            image_scale (int): the factor by which to shrink the image
        """
        
        global shrink_object_factor
        
        shrink_object_factor = image_scale
        if not os.path.exists(path_to_image_file):
            raise FileNotFoundError(path_to_image_file+ " doesn't exist. Image and Python files must be in the same folder as program file")
        if path_to_image_file[-4:] != '.png':
            raise Exception('Moving image file must be a .png')
        moving_object_imgfile = path_to_image_file
        self.file = tk.PhotoImage(file=path_to_image_file).subsample(shrink_object_factor,shrink_object_factor) # subsample scales image
        self.image = self.create_image(self.tick_marks[self.current_object_index][0], self.tick_marks[self.current_object_index][1], anchor=tk.S, image=self.file)

    def move_object(self, num_spaces=1):
        """ Moves object n spaces
        Args:
            num_spaces (int): the number of spaces to advance, with a defualt of 1 space forward
        """
      
        TIME_BETWEEN_MOVEMENTS = 0.1
       
        SUBSPACE_INTERVAL = 20 # subspaces to move between each space - controls the "smoothness"

        # arc settings
        ARC_HEIGHT_SCALE = 1    # 1 is a perfect semicircle, <1 is a short arc, >1 is a tall arc

        if (self.falling is True):    # if object already falling
            raise Exception("Object can not continue moving after starting to fall")

        # movement
        for i in range(abs(num_spaces)): # iterates each space
            if (self.current_object_index+num_spaces > self.max_steps) or (self.current_object_index+num_spaces < 0):  # if object goes too far forwards or backwards
                raise IndexError('Object Movement Out of Range')
        

            if movement_type == MOVE_STEP:  # step movement
                if num_spaces >= 0: # forwards movement
                    self.move(self.image, self.xmove, self.ymove)
                else:   # backwards movement
                    self.move(self.image, -self.xmove, -self.ymove)
                self.update()
                time.sleep(TIME_BETWEEN_MOVEMENTS)

            elif movement_type == MOVE_LINEAR:    # continuous linear movement
                for i in range(SUBSPACE_INTERVAL): # moves through 1 space in small intervals to appear continuous
                    if num_spaces >= 0: # forwards movement
                        self.move(self.image, self.xmove/SUBSPACE_INTERVAL, self.ymove/SUBSPACE_INTERVAL)
                    else:   # backwards movement
                        self.move(self.image, -self.xmove/SUBSPACE_INTERVAL, -self.ymove/SUBSPACE_INTERVAL)
                    self.update()
                    time.sleep(TIME_BETWEEN_MOVEMENTS/SUBSPACE_INTERVAL)

            elif movement_type == MOVE_ARC:    # continuous arc movement             
                
                if num_spaces >= 0: # forwards movement
                    arc_center = ((self.tick_marks[self.current_object_index][0]+self.tick_marks[self.current_object_index+1][0])/2, self.tick_marks[self.current_object_index+1][1])
                    
                else:   # backwards movement
                    arc_center = ((self.tick_marks[self.current_object_index][0]+self.tick_marks[self.current_object_index-1][0])/2, self.tick_marks[self.current_object_index-1][1])
                arc_radius = abs(self.xmove/2)

                if self.tick_marks[self.current_object_index][1] != arc_center[1]:  # if movement is not across a flat line
                    # find the approximate perimeter of the half elipse
                    elipse_h = (arc_radius-arc_radius*ARC_HEIGHT_SCALE)**2/(arc_radius+arc_radius*ARC_HEIGHT_SCALE)**2
                    elipse_perimeter = pi*(arc_radius+arc_radius*ARC_HEIGHT_SCALE)*(1+(3*elipse_h/(10+(4-3*elipse_h)**2)))/2
                    startend_jumpdrop_proportion = abs(self.tick_marks[self.current_object_index][1]-arc_center[1])/elipse_perimeter
                    jumpdrop_submovements = ceil(SUBSPACE_INTERVAL*startend_jumpdrop_proportion)
                else:   # if movement needs jumps/drops
                    jumpdrop_submovements = 0

                # if start is under arc center - jump up before the arc
                if self.tick_marks[self.current_object_index][1] > arc_center[1]:
                    start = self.tick_marks[self.current_object_index][1]
                    if num_spaces >= 0: # forwards movement
                        end = self.tick_marks[self.current_object_index+1][1]
                    else:   # backward movement
                        end = self.tick_marks[self.current_object_index-1][1]
                    movement_y_ticks = [start + y*(end-start)/jumpdrop_submovements for y in range(jumpdrop_submovements+1)]
                    for i in range(jumpdrop_submovements):
                        self.move(self.image, 0, movement_y_ticks[i+1]-movement_y_ticks[i])
                        self.update()
                        time.sleep(TIME_BETWEEN_MOVEMENTS/jumpdrop_submovements)

                # move as if start is at arc center        
                
                num_adjustments = SUBSPACE_INTERVAL - jumpdrop_submovements # how many submovements
                start = self.tick_marks[self.current_object_index][0]
                 
                if num_spaces >= 0: # forward movement
                    end = self.tick_marks[self.current_object_index+1][0]
                else:   # backward movement
                    end = self.tick_marks[self.current_object_index-1][0]

               
                      
                movement_x_ticks = [start + x*(end-start)/num_adjustments for x in range(num_adjustments+1)]
                movement_y_ticks = [-ARC_HEIGHT_SCALE*(arc_radius**2-(x-arc_center[0])**2)**.5+arc_center[1] for x in movement_x_ticks]   # equation is negative because -y is up
                for i in range(num_adjustments):
                    
                    
                    self.move(self.image, movement_x_ticks[i+1]-movement_x_ticks[i], movement_y_ticks[i+1]-movement_y_ticks[i])
  
                    self.update()
                 
                    time.sleep(TIME_BETWEEN_MOVEMENTS/num_adjustments)
                  


                # if start is over arc center - drop down after the arc
                if self.tick_marks[self.current_object_index][1] < arc_center[1]:

                     
                    start = self.tick_marks[self.current_object_index][1]
                    if num_spaces >= 0: # forward movement
                        end = self.tick_marks[self.current_object_index+1][1]
                    else:   # backward movement
                        end = self.tick_marks[self.current_object_index-1][1]
                    movement_y_ticks = [start + y*(end-start)/jumpdrop_submovements for y in range(jumpdrop_submovements+1)]
                    for i in range(jumpdrop_submovements):
      
                        
                        self.move(self.image, 0, movement_y_ticks[i+1]-movement_y_ticks[i])
                        self.update()
                        time.sleep(TIME_BETWEEN_MOVEMENTS/jumpdrop_submovements)
           
            playsound(soundfile)
        self.current_object_index += num_spaces
            
    def move_object_backwards(self, num_spaces=None):
        """ Moves object backwards n spaces
        Args:
            num_spaces (int): the number of spaces to advance backwards
        """
        if num_spaces is None:  # use default value
            self.move_object(-1)
        else:   # move backwards n spaces
            self.move_object(-num_spaces)


    def fall_object(self, fall_forwards,x_distance,y_distance):
        """ Causes moving object to fall in a given direction
        Args:
            fall_forwards (bool): True to fall with the direction of travel, False to fall against it (i.e., False while moving right will make the object fall backwards (left))
            x_distance (int) : distance to fall left/right, negative to left, positive to right
            y_distance (int) : distance to fall up/down, negative up, positive down
        """
        FALL_DISTANCE_X = x_distance # distance to fall left/right 
        FALL_DISTANCE_Y = y_distance   # distance to fall up/down

        TELEPORT_TO_END = False # True to instantly teleport the object to the end upon falling

        # continuous movement settings
        
        SUBSPACE_INTERVAL = 20 # subspaces to move between each space - controls the "smoothness"
        TIME_BETWEEN_MOVEMENTS = 0.005  # time between subspace movement to look like continuous movement (0.005 recommended)
   

        if TELEPORT_TO_END is True:
            if fall_forwards is True:   # fall forwards
                self.coords(self.image, self.end[0], self.end[1])   # teleport to end
            else:   # fall backwards
                self.coords(self.image, self.start[0], self.start[1])   # teleport to start
        else:
            if fall_forwards is True:   # fall forwards
                self.move_object(self.max_steps-self.current_object_index)
            else:   # fall backwards
                self.move_object(-self.current_object_index)
        
        self.falling = True


        if fall_forwards is True and start_point[0]>end_point[0]:   # if falling forwards and traveling in -x direction
            FALL_DISTANCE_X = -FALL_DISTANCE_X  # fall in the negative x direction
        elif fall_forwards is False and start_point[0]<end_point[0]:    # if falling backwards and traveling in +x direction
            FALL_DISTANCE_X = -FALL_DISTANCE_X  # fall in the negative x direction
        
        if movement_type == 0:  # step (iterative) fall
            self.move(self.image, FALL_DISTANCE_X, FALL_DISTANCE_Y)    # fall down
            self.update()

        elif movement_type in [1,2]:    # continuous fall
            for i in range(SUBSPACE_INTERVAL): # moves through 1 space in small intervals to appear continuous
                self.move(self.image, FALL_DISTANCE_X/SUBSPACE_INTERVAL, FALL_DISTANCE_Y/SUBSPACE_INTERVAL)
                time.sleep(TIME_BETWEEN_MOVEMENTS)
                self.update()

    def fall_forwards(self,x_distance,y_distance):
        
        """ Causes the moving object to fall forwards off path end
            x_distance (int) : distance to fall left/right, negative to left, positive to right
            y_distance (int) : distance to fall up/down, negative up, positive down
        """
        
        global movement_type
        if (movement_type == 0):
            movement_type = 1
        self.fall_object(True,x_distance,y_distance)

    def fall_backwards(self,x_distance,y_distance):
        
        """ Causes the moving object to fall backward off path end
            x_distance (int) : distance to fall left/right, negative to left, positive to right
            y_distance (int) : distance to fall up/down, negative up, positive down
        """
        global movement_type
        if (movement_type == 0):
            movement_type = 1
        
        self.fall_object(False, x_distance,y_distance)

    

def playsound(sound_file):
    
    """ Determines the user's OS and plays a soundfile
        sound_file (str) : name of .wav or .mp3 sound file
    """
   
    sys_os = system()   # get user's OS

    if sys_os == 'Windows':
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

    elif sys_os == 'Darwin':    #OSX
        import os
        os.system('afplay '+sound_file)

    else:
        pass    # audio on Unix not yet supported
        
        raise Exception("Audio on Unix not yet supported")


def check_this_file_for_errors():
    """ Checks user inputs in this file
    """

 
    # check that files exist
    if not os.path.exists(background_imgfile) :
       
        raise FileNotFoundError("***** Background image file doesn't exist. Image and Python files must be in the same folder.")
    if not os.path.exists(moving_object_imgfile):
       
        raise FileNotFoundError("*****Moving image file doesn't exist. Image and Python files must be in the same folder.")
    if soundfile!= '':
        if not os.path.exists(soundfile):
            raise FileNotFoundError("Sound file doesn't exist. Sound file must be in the same folder,")

    # check that images are PNGs
    if background_imgfile[-4:] != '.png' or moving_object_imgfile[-4:] != '.png':
        raise Exception('Image files must be PNGs')

    # check that start and end points are within the frame
    with open(background_imgfile, 'rb') as imgf:
        img_data = imgf.read(25)
    img_width, img_height = struct.unpack('>LL', img_data[16:24])
    if not 0 <= start_point[0] <= img_width:
        raise Exception("Start 'x' coord out of bounds. Must be 0 <= x <= " + str(img_width))
    elif not 0 <= start_point[1] <= img_height:
        raise Exception("Start 'y' coord out of bounds. Must be 0 <= y <="+str(img_height))
    elif not 0 <= end_point[0] <= img_width:
        raise Exception("End 'x' coord out of bounds. Must be 0 <= x <= "+str(img_width))
    elif not 0 <= end_point[1] <= img_height:
        raise Exception("End 'y' coord out of bounds. Must be 0 <= y <="+str(img_height))


    if movement_type not in [MOVE_STEP,MOVE_LINEAR,MOVE_ARC]:
        raise Exception("Movement type must be "+str(MOVE_STEP)+", "+str(MOVE_LINEAR)+" or "+ str(MOVE_ARC)) 

#check_this_file_for_errors()
