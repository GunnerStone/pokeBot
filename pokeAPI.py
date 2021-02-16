import win32gui
import pyautogui
import cv2
import time
import numpy
import ctypes
import pydirectinput
import pytesseract
import random
import pygetwindow
import re
# import only system from os 
from os import system, name 


class pokeAPI:

    #needed if running on Gunner's shitty latptop that cant play in 1920x1080
    x_offset, y_offset = 9,31
    w_offset, h_offset = 17,0
    def __init__(self, handle=None):
        self._handle = handle
        self._spell_memory = {}
        self._friends_area = (625, 65, 20, 240)
        self._spell_area = (245, 290, 370, 70)
        self._enemy_area = (68, 26, 650, 35)
        self._friendly_area = (136, 536, 650, 70)
        self._login_area = (307,553+36,187,44)

    def wait(self, s):
        """ Alias for time.sleep() that return self for function chaining """
        time.sleep(s)
        return self
    
    # define our clear function 
    def clear_console(self): 
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 
    
    def register_window(self, name="", nth=0):
        """ Assigns the instance to a pokemmo window (Required before using any other API functions) """
        def win_enum_callback(handle, param):
            #print(str(win32gui.GetWindowText(handle))[4:7]) #+'=='+'PokeMMO = '+str(name == str(win32gui.GetWindowText(handle))))
            window_name = str(str(win32gui.GetWindowText(handle))[0:7])
            if(len(window_name)>2):
                if (window_name[1]=='o' and window_name[2]=='k'):
                    print (window_name)
                if (name[1] == window_name[1] and name[2]== window_name[2]):
                    param.append(handle)

        handles = []
        # Get all windows with the name "Wizard101"
        win32gui.EnumWindows(win_enum_callback, handles)
        handles.sort()
        #print(handles)
        # Assigns the one at index nth
        self._handle = handles[nth]
        win32gui.MoveWindow(self._handle,0,0,1920,1080,True)
        rect = win32gui.GetWindowRect(self._handle)
        # x = rect[0]
        # y = rect[1]
        # w = rect[2] -x
        # h = rect[3] - y
        # x_offset = 1920 - w
        # y_offset = 1080 - h
        return self

    def read_text_from_img(self, img):
        #convert pyautogui/PIL to opencv format (numpy array)
        img = numpy.array(img,dtype=numpy.uint8) 

        #make image black/white
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY ) 
        #threshold to isolate black/white color & invert it so text is black
        _,img = cv2.threshold(img,190,255,cv2.THRESH_BINARY_INV)

        #run tesseract on preprocessed image
        return pytesseract.image_to_string(img)


    def is_active(self):
        """ Returns true if the window is focused """
        return self._handle == win32gui.GetForegroundWindow()

    def set_active(self):
        """ Sets the window to active if it isn't already """
        if not self.is_active():
            """ Press alt before and after to prevent a nasty bug """
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(self._handle)
            pyautogui.press('alt')
        return self

    
    def click_sidebar_pokemon(self,n=0):
        if (0 <= n <= 5):
            self.click(x=1875,y=385+69*n)
        return
    
    def use_HM_sidebar(self,n=0):
        #NOT YET IMPLEMENTED
        return
    def is_in_battle(self):
        #take screeenshot of enemy hp bar
        x,y = 300-self.x_offset, 256-self.y_offset
        large = self.screenshotRAM((x,y,104, 9))
        result = self.match_image(largeImg=large, smallImg='assets/battle_indicator.png',threshold=.05)
        if result is not False:
            return True
        else:
            return False
    def is_in_horde(self):
        x,y = 424-self.x_offset, 181-self.y_offset
        large = self.screenshotRAM((x,y,52, 9))
        if(self.x_offset == 0 or self.y_offset == 0):
            result = self.match_image(largeImg=large, smallImg='assets/horde_indicator.png',threshold=.05)
        else:
            result = self.match_image(largeImg=large, smallImg='assets/horde_indicator_laptop.png',threshold=.05)
        if result is not False:
            return True
        else:
            return False

    def use_first_attack(self,is_horde=False):
        time.sleep(.4)
        self.click(x=455-self.x_offset,y=690-self.y_offset)
        time.sleep(.4)
        self.click(x=455-self.x_offset,y=690-self.y_offset)
        if(is_horde==True):
            time.sleep(.4)
            self.click(x=455-self.x_offset,y=690-self.y_offset)
            time.sleep(.4)
    
    def flee_from_battle(self):
        time.sleep(.4)
        self.click(x=772-self.x_offset,y=772-self.y_offset)

    def stall_battle(self):
        time.sleep(random.uniform(.3,.5))
        self.click(x=715-self.x_offset,y=740-self.y_offset)
        time.sleep(random.uniform(.3,.5))
        self.click(x=715-self.x_offset,y=740-self.y_offset)
        time.sleep(random.uniform(.3,.5))
        self.click(x=715-self.x_offset,y=740-self.y_offset)

    def is_shiny_single(self):
        x, y, w, h = (365,226, 270, 26)
        x = x - self.x_offset
        y = y - self.y_offset
        w = w + self.w_offset
        h = h + self.h_offset
        img = self.screenshotRAM((x,y,w,h))
        name = (self.read_text_from_img(img)).upper()
        name = re.sub("[^0-9a-zA-Z.]+", "", name)
        indx = name.find("LV.")
        if (indx == -1):
            indx = name.find("LYV.")
        if indx < 0:
            indx = 5
        name = name[:indx]
        if(name[0:5]=="SHINY"):
            print("FOUND A SHINY "+name+"!")
            return True
        else:
            print("Found a "+name+"!")
        return False



    def is_shiny_horde(self):
        namePositions = [(441,210, 270, 26),(441,150, 270, 26),(830,150, 270, 26),(1220,150, 270, 26),(1220,210, 270, 26)]
        for i in range(len(namePositions)):
            x, y, w, h = namePositions[i]
            x = x - self.x_offset
            y = y - self.y_offset
            w = w + self.w_offset
            h = h + self.h_offset
            img = self.screenshotRAM((x,y,w,h))
            #self.screenshot("SHINYTEST"+str(i)+".png",(x,y,w,h))
            name = (self.read_text_from_img(img)).upper()
            name = re.sub("[^0-9a-zA-Z.]+", "", name)
            indx = name.find("LV.")
            if (indx == -1):
                indx = name.find("LYV.")
            if indx < 0:
                indx = 5
            #print (name) 
            name = name[:indx]
            if(name[0:5]=="SHINY"):
                print("FOUND A SHINY "+name+"!")
                return True
            else:
                print("Found a "+name+"!")
        return False

    def fish(self,hotkey='4'):
        time.sleep(.5)
        self.press_key(hotkey)
        time.sleep(4)
        img = self.screenshotRAM((560-self.x_offset,90-self.y_offset, 75, 40))
        s = self.read_text_from_img(img).upper()
        if(len(s)!=0):
            if(s[0]=='N' and s[1]=='O' and s[2]=='T'):
                #no fish on the line press z and return
                self.press_key('z')
                return self
        #fish on the line!
        self.press_key('z')
        time.sleep(12)
        print("done fishing")
        return self

    def fly_to(self,location="mistralton",hotkey='9'):
        #click on fly btn
        time.sleep(.5)
        self.press_key(hotkey)
        time.sleep(.5)
        fly_x, fly_y = 0,0
        if (location == "mistralton"):
            fly_x, fly_y = 565-self.x_offset , 540-self.y_offset
        elif (location == "lacunosa"):
            fly_x, fly_y = 1247-self.x_offset , 437-self.y_offset
        elif (location == "icirrus"):
            fly_x, fly_y = 725-self.x_offset , 440-self.y_offset
        elif (location == "opelucid"):
            fly_x, fly_y = 995-self.x_offset , 440-self.y_offset
        elif (location == "undella"):
            fly_x, fly_y = 1407-self.x_offset , 540-self.y_offset
        time.sleep(.2)
        self.click(fly_x,fly_y)
        time.sleep(.2)
        self.click(fly_x,fly_y)
        #wait for fly animation to finish
        time.sleep(4.5)
        return self

    def sweet_scent(self,hotkey='8'):
        time.sleep(.5)
        self.press_key(hotkey)
        time.sleep(13)
        #print('done casting')

    def surf(self):
        time.sleep(.5)
        self.press_key('z')
        time.sleep(1)
        self.press_key('z')
        time.sleep(1)
        self.press_key('z')
        time.sleep(3.5)

    def toggle_bike(self):
        self.press_key("3")

    def use_pokecenter(self,location="mistralton",hotkey='9'):
        self.fly_to(location,hotkey)
        #walk into pokecenter
        self.hold_key('up',5)
        #talk to nurse joy
        self.hold_key('z',7.5)
        self.hold_key('down',1.8)
        time.sleep(2.5)

    def look_for_battle(self):
        self.press_key('right')
        self.press_key('right')
        self.press_key('down')
        self.press_key('down')
        self.press_key('left')
        self.press_key('left')
        self.press_key('up')
        self.press_key('up')


    


    def get_window_rect(self):
        """Get the bounding rectangle of the window """
        rect = win32gui.GetWindowRect(self._handle)
        return [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]

    def match_image(self, largeImg, smallImg, threshold=0.1, debug=False):
        """ Finds smallImg in largeImg using template matching """
        """ Adjust threshold for the precision of the match (between 0 and 1, the lowest being more precise """
        """ Returns false if no match was found with the given threshold """
        method = cv2.TM_SQDIFF_NORMED

        # Read the images from the file
        # print(type(smallImg))
        # print(type(largeImg))
        if(type(smallImg) is str):
            small_image = cv2.imread(smallImg)
        else:
            small_image = cv2.cvtColor(numpy.array(smallImg), cv2.COLOR_RGB2BGR)
        if(type(largeImg) is str):
            large_image = cv2.imread(largeImg)
        else:
            large_image = cv2.cvtColor(numpy.array(largeImg), cv2.COLOR_RGB2BGR)
        
        w, h = small_image.shape[:-1]

        result = cv2.matchTemplate(small_image, large_image, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        if (mn >= threshold):
            return False

        # Extract the coordinates of our best match
        x, y = mnLoc

        if debug:
            # Draw the rectangle:
            # Get the size of the template. This is the same size as the match.
            trows, tcols = small_image.shape[:2]

            # Draw the rectangle on large_image
            cv2.rectangle(large_image, (x, y),
                          (x+tcols, y+trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv2.imshow('output', large_image)

            # The image is only displayed if we call this
            cv2.waitKey(0)

        # Return coordinates to center of match
        return (x + (w * 0.5), y + (h * 0.5))

    def pixel_matches_color(self, coords, rgb, threshold=0):
        """ Matches the color of a pixel relative to the window's position """
        wx, wy = self.get_window_rect()[:2]
        x, y = coords
        # self.move_mouse(x, y)
        return pyautogui.pixelMatchesColor(x + wx, y + wy, rgb, tolerance=threshold)

    def move_mouse(self, x, y, speed=.5):
        """ Moves to mouse to the position (x, y) relative to the window's position """
        wx, wy = self.get_window_rect()[:2]
        pydirectinput.moveTo(wx + x, wy + y, speed)
        return self

    def click(self, x, y, delay=.1, speed=.5, button='left'):
        """ Moves the mouse to (x, y) relative to the window and presses the mouse button """
        (self.set_active()
         .move_mouse(x, y, speed=speed)
         .wait(delay))

        pydirectinput.click(button=button,duration=0.1)
        return self

    def screenshot(self, name, region=False):
        """ 
        - Captures a screenshot of the window and saves it to 'name' 
        - Can also be used the capture specific parts of the window by passing in the region arg. (x, y, width, height) (Relative to the window position) 

        """
        #self.set_active()
        # region should be a tuple
        # Example: (x, y, width, height)
        window = self.get_window_rect()
        if not region:
            # Set the default region to the area of the window
            region = window
        else:
            # Adjust the region so that it is relative to the window
            wx, wy = window[:2]
            region = list(region)
            region[0] += wx
            region[1] += wy

        pyautogui.screenshot(name, region=region)
    
    def screenshotRAM(self, region=False):
        """ 
        - Captures a screenshot of the window and saves it to 'name' 
        - Can also be used the capture specific parts of the window by passing in the region arg. (x, y, width, height) (Relative to the window position) 

        """
        #self.set_active()
        # region should be a tuple
        # Example: (x, y, width, height)
        window = self.get_window_rect()
        if not region:
            # Set the default region to the area of the window
            region = window
        else:
            # Adjust the region so that it is relative to the window
            wx, wy = window[:2]
            region = list(region)
            region[0] += wx
            region[1] += wy

        return pyautogui.screenshot(region=region)

    

    def hold_key(self, key, holdtime=0.0):
        """ 
        Holds a key for a specific amount of time, usefull for moving with the W A S D keys 
        """
        self.set_active()
        start = time.time()
        pydirectinput.keyDown(key)
        """
        while time.time() - start < holdtime:
            pass
        """
        time.sleep(holdtime)
        pydirectinput.keyUp(key)

        return self
        # if(waittime > 0):
        #     self.accurate_delay(waittime)
        # pyautogui.keyDown(key)
        # self.accurate_delay(holdtime)
        # pyautogui.keyUp(key)

    def navigate_keys(self, keys, holdtimes, waittimes):
        #keys []
        #holdtimes []
        #waittimes []
        #assume they are in order
        curr_time = 0.0
            
        for i in range(len(keys)):
            #wait until key needs to be pressed
            delay_time = waittimes[i]-curr_time

            """start = time.time()
            while time.time() - start < delay_time:
                pass
            """
            time.sleep(delay_time)

            #hold key down for specified time
            pydirectinput.keyDown(keys[i])
            start = time.time()
            """
            while time.time() - start < holdtimes[i]:
                pass
            """
            time.sleep(holdtimes[i]-.15)
            pydirectinput.keyUp(keys[i])

            curr_time = waittimes[i]+holdtimes[i]
            

        return self
    def press_key(self, key):
        """
        Presses a key, useful for pressing 'x' to enter a dungeon
        """
        self.set_active()
        pydirectinput.press(key)
        return self