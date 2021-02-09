from pokeAPI import *
import time
from threading import Thread
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import sys
import os

try:
    driver = pokeAPI().register_window()
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

    def navigate_to_grass():
        driver.hold_key('left',0.6)
        driver.hold_key('up',1.3)
        driver.hold_key('right',1.7)
        driver.hold_key('up',0.50)
        driver.hold_key('right',.5)
        driver.hold_key('up',2.4)

    def farm_money_until_low():
        #Start bot underneath poke-center exit facing down
        print("Going to pokecenter")
        driver.use_pokecenter()
        currentPP = 10
        print("Navigating to Grass Patches")
        navigate_to_grass()
        driver.press_key('up')
        driver.press_key('up')
        print("Starting farm loop")
        while(currentPP>0):
            print("Looking for battle")
            while((not driver.is_in_battle()) and (not driver.is_in_horde())):
                driver.look_for_battle()
            print("Battle")
            #wait for battle options to pop up
            print("waiting for intro animations")
            time.sleep(7)
            if (driver.is_in_horde()):
                print("Fleeing from battle")
                driver.flee_from_battle()
            else:
                print("using attack")
                driver.use_first_attack()
            print("waiting for attack animations & battle close")
            time.sleep(11)
            print("holding z through any prompts")
            driver.hold_key('z',3)
            currentPP -= 1



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