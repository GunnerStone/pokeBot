import win32gui
import pyautogui
import cv2
import time
import numpy
import ctypes
import pydirectinput

# import only system from os 
from os import system, name 


class pokeAPI:
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
            print (window_name)
            if name == window_name:
                param.append(handle)

        handles = []
        # Get all windows with the name "Wizard101"
        win32gui.EnumWindows(win_enum_callback, handles)
        handles.sort()
        #print(handles)
        # Assigns the one at index nth
        self._handle = handles[nth]
        return self

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
        x,y = 300, 256
        large = self.screenshotRAM((x,y,104, 9))
        result = self.match_image(largeImg=large, smallImg='assets/battle_indicator.png',threshold=.05)
        if result is not False:
            return True
        else:
            return False
    def is_in_horde(self):
        x,y = 424, 181
        large = self.screenshotRAM((x,y,52, 9))
        result = self.match_image(largeImg=large, smallImg='assets/horde_indicator.png',threshold=.05)
        if result is not False:
            return True
        else:
            return False

    def use_first_attack(self):
        time.sleep(.4)
        self.click(x=455,y=690)
        time.sleep(.4)
        self.click(x=455,y=690)
    
    def flee_from_battle(self):
        time.sleep(.4)
        self.click(x=772,y=772)

    def fly_to(self,location="mistralton",hm_slave=5):
        self.click_sidebar_pokemon(hm_slave)
        #click on fly btn
        time.sleep(.2)
        self.click(x=1738,y=880)
        fly_x, fly_y = 0,0
        if (location == "mistralton"):
            fly_x, fly_y = 565, 540
        elif (location == "lacunosa"):
            fly_x, fly_y = 1247, 437
        time.sleep(.2)
        self.click(fly_x,fly_y)
        time.sleep(.2)
        self.click(fly_x,fly_y)
        #wait for fly animation to finish
        time.sleep(4.5)

    def toggle_bike(self):
        self.press_key("3")

    def use_pokecenter(self,location="mistralton",hm_slave=5):
        self.fly_to(location,hm_slave)
        #walk into pokecenter
        self.hold_key('up',5)
        #talk to nurse joy
        self.hold_key('z',7)
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