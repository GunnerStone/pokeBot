from pokeAPI import *
import time
from threading import Thread
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import sys
import os
import random

try:
    driver = pokeAPI().register_window(name="РokеММO")
    wx, wy = driver.get_window_rect()[:2]

    ROUND_COUNT = 0
    print = print_formatted_text
    style = Style.from_dict({
            'msg': '#71f076 bold',
            'sub-msg': '#616161 italic'
        })

    def display_metrics():
            while(True):
                global ROUND_COUNT
                driver.clear_console()
                #Current dungeon run number
                str_buffer = str(ROUND_COUNT)
                print(HTML(
                    u'<b>></b> <ansicyan><u>Current Dungeon Run</u></ansicyan>'+"<b> : </b>"+'<i><ansigrey>'+str_buffer+'</ansigrey></i>'
                ), style=style)

                time.sleep(1)

    def navigate_to_low_level_grass():
        driver.hold_key('left',0.6)
        driver.hold_key('up',1.3)
        driver.hold_key('right',1.7)
        driver.hold_key('up',0.50)
        driver.hold_key('right',.5)
        driver.hold_key('up',2.4)
        
    def navigate_to_high_level_grass():
        #get on bike
        driver.toggle_bike()
        driver.hold_key('left',random.uniform(3, 3.3))
        driver.toggle_bike()
        driver.press_key('up')
        driver.press_key('up')

    def navigate_to_druddigon():
        #get on bike
        driver.toggle_bike()
        driver.hold_key('left',0.3)
        driver.hold_key('up',3.2)
        driver.hold_key('right',0.3)
        driver.hold_key('up',1.5)
        driver.hold_key('left',0.15)
        driver.hold_key('up',3.6)
        time.sleep(2)
        driver.press_key('up')


    def farm_money_until_low():
        #Start bot underneath poke-center exit facing down
        print("Going to pokecenter")
        driver.use_pokecenter(location="icirrus")
        # driver.fly_to(location="lacunosa")
        
        # driver.press_key("up")
        # driver.press_key("up")
        
        #sweet scent can be used 6 times before needing to go to pokecenter
        currentPP = 6
        print("Navigating to Grass Patches")
        navigate_to_druddigon()
        print("Starting farm loop")
        while(currentPP>0):
            print("Looking for battle")
            while((not driver.is_in_battle()) and (not driver.is_in_horde())):
                driver.sweet_scent()
            print("Battle Found")
            in_battle = True
            #wait for battle options to pop up
            if (driver.is_in_horde()):
                print("Scanning for Horde Shinies")
                if(driver.is_shiny_horde() == False):
                    print("Shiny not found")
                    print("Using AOE attack")
                    driver.use_first_attack(is_horde=True)
                    print("Attack animations & battle close")
                    time.sleep(12)
                    in_battle = False
                else:
                    print("Shiny found!!!")
                    print("Stalling until human services game")
                    while True:
                        time.sleep(60)
            else:
                while(in_battle):
                    print("Scanning for Single-Battle Shinies")
                    if(driver.is_shiny_single()==False):
                        print("Shiny not found")
                        print("Using AOE attack")
                        driver.use_first_attack()
                        print("Attack animations & battle close")
                        time.sleep(12)
                        #if battle is over set loop flag to false
                        if(not driver.is_in_battle()):
                            print("Enemy pokemon was defeated")
                            in_battle = False
                    else:
                        print("Shiny found!!!")
                        print("Stalling until human services game")
                        while True:
                            time.sleep(60)
            
            print("Holding z through any prompts")
            driver.hold_key('z',3)
            currentPP -= 1
        driver.hold_key('down',1)
        



    metric_thread = Thread(target=display_metrics,args=())

    try:
        #metric_thread.start()
        while True:
            farm_money_until_low()
            ROUND_COUNT += 1
    except KeyboardInterrupt:
            print ('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
except Exception as e:
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)